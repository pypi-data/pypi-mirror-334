"""
Module: Top.py
Author: Miłosz Wieczór <milosz.wieczor@irbbarcelona.org>
License: GPL 3.0

Description:
    This module implements the high-level Top object, representing a GROMACS topology.

Contents:
    Classes:
        Top:
            Represents the topology (parameters, molecule definitions, and system components) of a molecular system.

Usage:
    This module is intended to be imported as part of the library. It is not
    meant to be run as a standalone script. Example:

        import gromologist as gml
        topology = gml.Top("topol.top")

Notes:
    The "Top" class is also capable of reading and processing .itp files, as long as they contain
    valid subsections.
"""


import os
import platform
import datetime
from copy import deepcopy
from typing import Optional, Iterable, TextIO, Union

import gromologist as gml
from collections import OrderedDict


class Top:
    def __init__(self, filename='', gmx_dir=None, gmx_exe=None, pdb=None, ignore_ifdef=False, define=None, ifdef=None,
                 ignore_missing_defines=False, keep_all=True, suppress=False, amber=False, charmm=False):
        """
        A class to represent and contain the Gromacs topology file and provide
        tools for editing topology elements
        :param filename: str, path to the .top file
        :param gmx_dir: str, Gromacs FF directory
        :param pdb: str, path to a matching PDB file
        :param ignore_ifdef: bool, whether to ignore #include statements within #ifdef blocks (e.g. posre.itp)
        :param define: dict, key:value pairs with variables that will be defined in .mdp
        """
        # TODO maybe allow for construction of a blank top with a possibility to read data later?
        self.suppress = suppress
        self.gromacs_dir, self.gmx_exe = gml.find_gmx_dir(suppress)
        self.gromacs_dir = gmx_dir if not self.gromacs_dir else self.gromacs_dir
        self.gmx_exe = gmx_exe if not self.gmx_exe else self.gmx_exe
        self.pdb = None
        self.rtp = {}
        self.pdb = None if pdb is None else gml.Pdb(pdb, top=self)
        self.fname = filename
        self.top = self.fname.split(os.sep)[-1]
        if self.fname.startswith(os.sep):
            self.dir = os.sep.join(self.fname.split(os.sep)[:-1])
        else:
            self.dir = os.getcwd() + os.sep + os.sep.join(self.fname.split(os.sep)[:-1])
        if not (self.fname == '' and (amber or charmm)):
            with open(self.fname) as top_file:
                self._contents = top_file.readlines()
        else:
            if amber and not charmm:
                self.print("Creating an empty amber topology file")
                self._contents = ['#define _FF_AMBER\n', '[ defaults ]\n', '1 2 yes 0.5 0.8333\n', '[ atomtypes ]\n']
            elif charmm and not amber:
                self.print("Creating an empty charmm topology file")
                self._contents = ['#define _FF_CHARMM\n', '[ defaults ]\n', '1 2 yes 1.0 1.0\n', '[ atomtypes ]\n']
            else:
                raise RuntimeError("To make an empty topology, select either 'amber=True' or 'charmm=True'")
        self.defines = {}
        self.ignore_missing_defines = ignore_missing_defines
        if define is not None:
            self.defines.update(define)
        self._preprocess_conditional_includes(ifdef)
        self._include_all(ignore_ifdef)
        if not keep_all:
            self._resolve_ifdefs([] if ifdef is None else ifdef)
        else:
            self.print("Keeping all conditional (#ifdef/#endif) sections, this might lead to issues if sections "
                       "are being merged or moved around - look out for messages & check your topology afterwards!")
        self.sections = []
        self.header = []
        self._parse_sections()

    def from_selection(self, selection: str) -> "gml.Top":
        """
        Returns a new .top file corresponding to the specified selection
        :param selection: str, a Gromologist-compatible selection
        :return: gml.Top, the new topology
        """
        new_top = deepcopy(self)
        chosen_atoms = self.get_atoms(selection)
        mols_to_remove = []
        for mol in new_top.molecules:
            atoms_to_remove = []
            for at in mol.atoms:
                if at not in chosen_atoms:
                    atoms_to_remove.append(at.num)
            atoms_to_remove = atoms_to_remove[::-1]
            for atomnum in atoms_to_remove:
                mol.del_atom(atomnum)
            if mol.natoms == 0:
                mols_to_remove.append(mol.mol_name)
        for mol_to_remove in mols_to_remove:
            new_top.remove_molecule(mol_to_remove)
        new_top.parameters.sort_dihedrals()
        return new_top

    def save_from_selection(self, selection: str, filename: str = 'subsystem.top') -> None:
        """
        Generates and saves a new .top file corresponding to the specified selection
        :param selection: str, a Gromologist-compatible selection
        :param filename: str, name of the resulting topology file
        :return: None
        """
        new_top = self.from_selection(selection)
        new_top.save_top(filename)

    def clone(self) -> "gml.Top":
        return deepcopy(self)

    @property
    def system(self) -> list:
        """
        Returns a list of tuples with the contents of the system,
        following the [ molecules ] section of a topology
        """
        if not self.top.endswith('top'):
            return []
        else:
            return self.read_system_properties()

    def __repr__(self) -> str:
        return (f"Topology with {self.natoms} atoms, total charge {self.charge:.3f}, "
                f"and {len(self.molecules)} molecules defined")

    def print(self, *args) -> None:
        """
        A custom Print function that can be turned out with suppress=True
        """
        if not self.suppress:
            print(*args)

    @classmethod
    def _from_text(cls, text: str, gmx_dir: Optional[str] = None, pdb: Optional[str] = None,
                   ignore_ifdef: bool = False) -> "gml.Top":
        """
        A simple wrapper to generate a topology from an in-memory string object
        :param text: str, the text to be parsed
        :param gmx_dir: str, optional path to the gromacs directory
        :param pdb: str, optional path to the corresponding structure
        :param ignore_ifdef: bool, optional to ignore missing #ifdefs
        :return: a Top instance
        """
        with open('tmp_topfile.gromo', 'w') as tmp:
            tmp.write(text)
        instance = cls('tmp_topfile.gromo', gmx_dir, pdb, ignore_ifdef)
        os.remove('tmp_topfile.gromo')
        return instance

    @property
    def molecules(self) -> list:
        """
        A property attribute returning the list of all SectionMols corresponding to molecules
        :return: list of SectionMol objects
        """
        return [s for s in self.sections if isinstance(s, gml.SectionMol)]

    @property
    def alchemical_molecules(self) -> list:
        """
        As Top.molecules but only returns alchemical molecules (ones that have state B defined)
        :return: list of SectionMol objects
        """
        return [s for s in self.sections if isinstance(s, gml.SectionMol) and s.is_alchemical]

    @property
    def parameters(self) -> "gml.SectionParam":
        """
        A property attribute that returns the SectionParams section containing all parameter sets
        :return: list
        """
        return [s for s in self.sections if isinstance(s, gml.SectionParam)][0]

    @property
    def has_partner(self) -> bool:
        return True if self.pdb is not None else False

    @property
    def atoms(self) -> list:
        """
        A property attribute that returns a list of all atoms in the system
        :return: list of EntryAtom entries
        """
        atomlist = []
        for mol_count in self.system:
            molecule = self.get_molecule(mol_count[0])
            for q in range(mol_count[1]):
                for a in molecule.atoms:
                    atomlist.append(a)
        return atomlist

    @property
    def defaults(self) -> dict:
        """
        Returns a dictionary with the values set in the [ defaults ] section
        :return: dict with named 'defaults' values
        """
        def_values = [lin for lin in self.parameters.get_subsection('defaults').entries_param][0].modifiers
        try:
            return {'nbfunc': int(def_values[0]), 'comb-rule': int(def_values[1]), 'gen-pairs': def_values[2],
                    'fudgeLJ': float(def_values[3]), 'fudgeQQ': float(def_values[4])}
        except IndexError:
            return {'nbfunc': int(def_values[0]), 'comb-rule': int(def_values[1]), 'gen-pairs': def_values[2],
                    'fudgeLJ': 1.0, 'fudgeQQ': 1.0}

    def remove_molecule(self, molname: str) -> None:
        """
        Removes a molecule definition and the corresponding entry from the system
        definition (e.g. SOL to remove the solvent)
        :param molname: str, name of the molecule to remove
        :return: None
        """
        section = [s for s in self.sections if isinstance(s, gml.SectionMol) and s.mol_name == molname][0]
        self.sections.remove(section)
        system_subsection = [s.get_subsection('molecules') for s in self.sections if
                             'molecules' in [ss.header for ss in s.subsections]][0]
        entries_to_del = [e for e in system_subsection.entries if str(e).split()[0] == molname]
        for entry in entries_to_del:
            system_subsection.entries.remove(entry)

    def merge_molecules(self, molname1: Union[str, int], molname2: Union[str, int]) -> None:
        """
        Combines two molecules into a single [ moleculetype ]
        :param molname1: str or int, name of molecule 1 or index of molecule 1
        :param molname2: str or int, name of molecule 2 or index of molecule 2
        :return: None
        """
        mol1 = self.molecules[molname1] if isinstance(molname1, int) else self.get_molecule(molname1)
        mol2 = self.molecules[molname2] if isinstance(molname2, int) else self.get_molecule(molname2)
        mol1.merge_two(mol2, -1, -1)

    def explicit_multiple_molecules(self, molname: Union[str, int], renumber_residues: bool = True) -> None:
        """
        If a molecule has multiple copies, this transforms it to an explicit
        representation where each copy has its individual residue ID and can
        be specifically modified
        :param molname: the molecule to "unpack"
        :param renumber_residues: whether to renumber residues e.g. to enable individual selections
        :return: None
        """
        mol = self.molecules[molname] if isinstance(molname, int) else self.get_molecule(molname)
        target_num = [x for x in self.system if x[0] == mol.mol_name][0][1]
        other = deepcopy(mol)
        for i in range(target_num - 1):
            mol.merge_two(other, -1, -1, renumber_residues)
        system_setup = self.sections[-1].get_subsection('molecules')
        for e in system_setup.entries:
            if mol.mol_name in e.content:
                e.content = [mol.mol_name, '1']

    def select_atoms(self, selection_string: str) -> list:
        """
        Returns atoms' indices according to the specified selection string
        :param selection_string: str, a VMD-compatible selection
        :return: list, 0-based indices of atoms compatible with the selection
        """
        sel = gml.SelectionParser(self)
        return sel(selection_string)

    def select_atom(self, selection_string: str) -> int:
        """
        Returns atoms' indices according to the specified selection string
        :param selection_string: str, a VMD-compatible selection
        :return: int, 0-based index of atom compatible with the selection
        """
        sel = gml.SelectionParser(self)
        result = sel(selection_string)
        if len(result) > 1:
            raise RuntimeError("Selection {} returned more than one atom: {}".format(selection_string, result))
        elif len(result) < 1:
            raise RuntimeError("Selection {} returned no atoms".format(selection_string, result))
        return result[0]

    def get_atoms(self, selection_string: str) -> list:
        """
        Returns a list of atoms compatible with a selection
        :param selection_string: str, selection compatible with gromologist syntax
        :return: list of gml.Entry entries
        """
        atomlist = self.atoms
        return [atomlist[i] for i in self.select_atoms(selection_string)]

    def get_atom(self, selection_string: str) -> "gml.EntryAtom":
        """
        Returns a single atom compatible with a selection
        :param selection_string: str, selection compatible with gromologist syntax
        :return: a single gml.Entry entry
        """
        return self.atoms[self.select_atom(selection_string)]

    @property
    def defined_atomtypes(self) -> set:
        """
        Returns a set of all atomtypes defined in this topology (in [ atomtypes ])
        :return: set, all atomtypes defined in the parameters' section
        """
        return {ent.types[0] for ent in self.parameters.atomtypes.entries_param}

    def find_undefined_types(self) -> None:
        """
        Checks if any atom types required by some bonded or nonbonded parameters are missing in [ atomtypes ] definition
        :return: None
        """
        deftyp = self.defined_atomtypes.union({"X"})
        for ssect in self.parameters.subsections:
            types = {t for e in ssect.entries_param for t in e.types}
            if types.difference(deftyp):
                for atype in list(types.difference(deftyp)):
                    if ssect.header == 'cmaptypes' and '-' in atype and atype.split('-')[0] in deftyp:
                        continue
                    print(f"WARNING: atomtype {atype} required in {ssect.header} not found "
                          f"in [ atomtypes ]")

    def list_molecules(self) -> None:
        """
        Prints out a list of molecules contained in the System
        :return: None
        """
        for mol_count in self.system:
            print("{:20s}{:>10d}".format(mol_count[0], mol_count[1]))

    def remove_all_comments(self) -> None:
        """
        Removes comments from all topology lines (useful e.g. for comparing with diff)
        :return: None
        """
        for sect in self.sections:
            for ssub in sect.subsections:
                for entry in ssub.entries:
                    entry.comment = ''

    def clear_ff_params(self, section: str = 'all') -> None:
        """
        Removes all FF parameters included in the topology that are not used by the defined molecules
        :param section: str, 'all' if applied to all parameters, else as specified
        :return: None
        """
        used_params = []
        for mol in self.molecules:
            used_params.extend(mol.find_used_ff_params(section=section))
        for pairsect in ['nonbond_params', 'pairtypes']:  # TODO mod the part below to work with section = ...
            try:
                ssect = self.parameters.get_subsection(pairsect)
                for ent in ssect.entries_param:
                    if not (ent.types[0] in self.defined_atomtypes and ent[1] in self.defined_atomtypes):
                        used_params.append(ent.identifier)
            except KeyError:
                continue
        used_params.extend(self.parameters.find_used_ff_params(section=section))
        self.parameters.clean_unused(used_params, section=section)

    def add_pdb(self, pdbfile: Union[str, "gml.Pdb"]) -> None:
        """
        Allows to pair a PDB file with the topology after the instance was initialized
        :param pdbfile: str, path to PDB file, or gml.Pdb object
        :return: None
        """
        if isinstance(pdbfile, str):
            self.pdb = gml.Pdb(pdbfile, top=self)
        else:
            self.pdb = pdbfile
            self.pdb.add_top(self)

    def add_ff_params(self, section: str = 'all', external_paramsB: Optional["gml.SectionParam"] = None) -> None:
        """
        Explicitly puts FF parameters in sections 'bonds', 'angles',
        'dihedrals' so that the resulting topology is independent of
        FF sections
        :param section: str, 'all' or name of the section, e.g. 'bonds'
        :param external_paramsB: gml.SectionParam, an external section to look for parameters for state B
        :return: None
        """
        # TODO make sure params are not duplicated
        for mol in self.molecules:
            mol.add_ff_params(add_section=section, external_paramsB=external_paramsB)

    def load_frcmod(self, frcmod: str) -> None:
        """
        Loads an Amber frcmod file, adding parameters to an existing Gromacs topology
        (note that type names will not always match!)
        :param frcmod: str, path to the frcmod file
        :return: None
        """
        gml.load_frcmod(self, frcmod)

    def add_molecule_from_file(self, filename: str, molnames: Optional[list] = None, molcount: Optional[list] = None,
                               prefix_type: Optional[str] = None) -> None:
        """
        Adds a molecule from an external file (can be .itp or .top) to the current topology
        :param filename: name of the file containing the molecule to be added
        :param molnames: list, enumerates molecules to be added (can be just 1-element list), None means add all
        :param molcount: list, enumerates numbers of molecules that will be added, by default 1 per moleculetype
        :param prefix_type: str, if specified, all atomtypes will be prefixed with this str to disambiguate
        :return: None
        """
        contents = [line for line in open(filename)]
        special_sections = {'defaults', 'moleculetype', 'system'}
        special_lines = [n for n, l in enumerate(contents)
                         if l.strip() and l.strip().strip('[]').strip().split()[0] in special_sections]
        special_lines.append(len(contents))
        inserted_mols = []
        existing_mols = [molsect.mol_name for molsect in self.molecules]
        for beg, end in zip(special_lines[:-1], special_lines[1:]):
            if 'moleculetype' in contents[beg]:
                molsections = [n for n, i in enumerate(self.sections) if isinstance(i, gml.SectionMol)][-1]
                section = self._yield_sec(contents[beg:end])
                if molnames is None or section.mol_name in molnames:
                    if section.mol_name in existing_mols:
                        print(f"Skipping molecule {section.mol_name} as its name is already taken. If needed, rename it "
                              f"in [ moleculetypes ]")
                        continue
                    self.sections.insert(molsections+1, section)
                    inserted_mols.append(section.mol_name)
        self.print("Molecules inserted. Try running Top.find_missing_ff_params() to see if the topology contains"
                   "all necessary parameters.\n\n")
        if prefix_type is not None:
            for newmol in inserted_mols:
                mol = self.get_molecule(newmol)
                types = list(set([a.type for a in mol.atoms]))
                for atype in types:
                    mol.set_type(atomtype=atype, prefix=prefix_type)
        if molcount is None:
            self.print("To add the newly defined molecule to the system, use Top.add_molecules_to_system() or "
                       "manually edit the [ molecules ] section in the topology. You can also specify `molcount` in "
                       "this function to automatically add the desired number of molecules to the system.")
        else:
            try:
                _ = len(molcount)
            except TypeError:
                molcount = [molcount] * len(inserted_mols)
            else:
                assert len(molcount) == len(inserted_mols)
            for mc, mname in zip(molcount, inserted_mols):
                self.add_molecules_to_system(mname, mc)
                self.print(f"Added {mc} instances of molecule {mname}")

    def add_parameters_from_file(self, filename: str, sections: Optional[list] = None, overwrite: bool = False,
                                 prefix_type: Optional[str] = None) -> None:
        """
        Adds parameters from an external file
        :param filename: name of the file containing the parameters to be added
        :param sections: list, enumerates sections to be added (can be just 1-element list), None means add all
        :param overwrite: bool, whether to overwrite existing parameters in case of conflict (default is not)
        :param prefix_type: str, if specified, will add
        :return: None
        """
        other = gml.Top(filename, ignore_ifdef=True)
        if prefix_type is not None:
            other.prefix_types(prefix_type)
        try:
            defs_self = self.parameters.get_subsection('defaults').entries_param[0].content
            defs_other = other.parameters.get_subsection('defaults').entries_param[0].content
        except KeyError:
            inp = 'q'
            while inp.lower() not in 'nfty':
                inp = input("\n\nAt least one of the files does not define a [ defaults ] section with key \n"
                            "interaction modifiers. Do you trust that the parameter sets are compatible? (y/n)\n\n")
            if inp.lower() in 'nf':
                return
        else:
            if not all([int(defs_self[0]) == int(defs_other[0]), int(defs_self[1]) == int(defs_other[1]),
                        defs_self[2] == defs_other[2], float(defs_self[3]) == float(defs_other[3]),
                        float(defs_self[4]) == float(defs_other[4])]):
                raise RuntimeError(f"Can't merge parameters with different [ defaults ] sections, "
                                   f"make sure they are identical: {defs_self} and {defs_other}")
        other_subs = other.parameters.subsections if sections is None else [sc for sc in other.parameters.subsections
                                                                            if sc.header in sections]
        for subsection in other_subs:
            if subsection.header != 'defaults':
                try:
                    # let's check if we already have this subsection in our topo
                    own_subs = self.parameters.get_subsection(subsection.header)
                except KeyError:
                    # if not, let's add it as it is assuming it's non-empty
                    if len(subsection.entries_param) > 0:
                        self.parameters.subsections.append(self.parameters._yield_sub([f'[ {subsection.header} ]']))
                        own_subs = self.parameters.get_subsection(subsection.header)
                own_subs._combine_entries(subsection, overwrite)

    def add_molecules_to_system(self, molname: str, nmol: int) -> None:
        """
        Adds a specified number of molecules to the system (specified
        in the [ molecules ] section at the end of the .top file)
        :param molname: str, name of the molecule (has to be already defined in the topology)
        :param nmol: int, number of molecules to be repeated
        :return: None
        """
        mollist = [mol.mol_name for mol in self.molecules]
        if molname not in mollist:
            raise RuntimeError(f"Molecule {molname} not found among defined molecules ({mollist}), please add it"
                               f"manually or via Top.add_molecule_from_itp()")
        system_subsection = [s.get_subsection('molecules') for s in self.sections
                             if 'molecules' in [ss.header for ss in s.subsections]]
        if len(system_subsection) > 1:
            raise RuntimeError("Multiple 'molecules' subsection found in the topology, this is not allowed")
        elif len(system_subsection) == 0:
            self.print("Section 'molecules' not present in the topology, will be created now")
            system_subsection = self._yield_sec(["[ molecules ]"])
            self.sections.append(system_subsection)
        else:
            system_subsection = system_subsection[0]
        system_subsection.add_entry(gml.Entry(f"{molname} {nmol}", system_subsection))

    def extract_explicit_parameters(self, molname: Optional[str] = None) -> None:
        """
        Takes the parameters explicitly defined in sections [ bonds ], [ angles ], [ dihedrals ]
        and puts them in [ bondtypes ], ...
        :param molname: list or str, optionally only apply to a subset of molecules
        :return: None
        """
        if molname is None:
            molecules = self.molecules
        elif isinstance(molname, str):
            molecules = [self.get_molecule(molname)]
        else:
            molecules = [self.get_molecule(mname) for mname in molname]
        to_add = set()
        for mol in molecules:
            for ssect in mol.subsections:
                if not isinstance(ssect, gml.SubsectionBonded):
                    continue
                for e in ssect.entries_bonded:
                    if len(e.params_state_a) > 0:
                        e.read_types()
                        to_add.add((tuple(sorted(e.types_state_a)), tuple(e.params_state_a), int(e.interaction_type)))
        to_add = sorted(list(to_add), key=lambda x: x[0])
        for entry in to_add:
            self.parameters.add_bonded_param(entry[0], list(entry[1]), entry[2])
        self.parameters.fix_zero_periodicity()

    def prefix_types(self, prefix: str, types_list: Optional[list] = None) -> None:
        """
        Add a prefix to all types in the topology, to make it compatible with any other topology
        :param prefix: str, will be added in front of the atomtype to modify it
        :param types_list: list of str, will modify all types except for when an explicit list of types is provided here
        :return: None
        """
        types = list(self.defined_atomtypes) if types_list is None else types_list
        if any([prefix + tp in types for tp in types]):
            raise RuntimeError(f"The combination of prefix {prefix} and one of the types {types} is already defined")
        for atype in types:
            for mol in self.molecules:
                mol.set_type(prefix=prefix, atomtype=atype)
            self.parameters.rename_type(atype, prefix=prefix)

    def find_missing_ff_params(self, section: str = 'all', fix_by_analogy: bool = False, fix_B_from_A: bool = False,
                               fix_A_from_B: bool = False, fix_dummy: bool = False, once: bool = False) -> None:
        """
        Identifies FF parameters that are not defined in sections
        'bondtypes', angletypes', ...; if required, will attempt to
        match parameters by analogy
        :param section: str, 'all' or name of the section, e.g. 'bonds'
        :param fix_by_analogy: dict, if set, will attempt to use params by analogy, matching key types to value types
        :param fix_B_from_A: bool, will assign params for state B from state A
        :param fix_A_from_B: bool, will assign params for state A from state B
        :param fix_dummy: bool, will assign zeros as parameters
        :param once: bool, will only print a given missing term once per molecule
        :return: None
        """
        # TODO check if all types are defined
        # TODO double-wildcards not recognized?
        for mol in self.molecules:
            mol.find_missing_ff_params(section, fix_by_analogy, fix_B_from_A, fix_A_from_B, fix_dummy, once=once)

    def hydrogen_mass_repartitioning(self, hmass: float = 3.024, methionine=False) -> None:
        """
        Repartitions the masses from heavy atoms to hydrogens in the entire system to ensure that each
        hydrogen has the desired mass; this enables the use of a 4-fs time step in
        standard MD simulations. Skips molecules up to 5 atoms (e.g. water).
        :param hmass: float, desired mass of the hydrogen atom; default is 3.024 (as set by -heavyh in pdb2gmx)
        :param methionine: bool, whether to add repartitioning for methionine (might crash in CHARMM otherwise)
        :return: None
        """
        for mol in self.molecules:
            if len(mol.atoms) > 5:
                mol.hydrogen_mass_repartitioning(hmass, methionine)

    def add_posres(self, keyword: Union[str, None] = 'POSRES', value: int = 1000, selection=None) -> None:
        """
        Adds a (conditional) position restraint entry for each molecule in the system
        (only heavy atoms); optionally, POSRES can be set for a subset defined by a selection
        (for custom POSRES, use the analogous molecule function, e.g. Top.molecules[0].add_posres();
        by default, only molecules larger than 5 atoms are considered
        :param keyword: str, will be used for the #IFDEF preprocessor command; default is POSRES, if None the section
        will not be conditional
        :param value: force constant for the restraint
        :param selection: str or None, can be used to set the restraint for a subset of the system
        :return: None
        """
        for mol in self.molecules:
            if len(mol.atoms) > 5:
                mol.add_posres(keyword, value, selection)

    def add_params_file(self, paramfile: str) -> None:
        prmtop = Top._from_text('#include {}\n'.format(paramfile))
        own_defentry = [e for e in self.sections[0].subsections[0].entries if isinstance(e, gml.EntryParam)][0]
        other_defentry = [e for e in prmtop.sections[0].subsections[0].entries if isinstance(e, gml.EntryParam)][0]
        if all([x == y for x, y in zip(own_defentry, other_defentry)]):
            _ = prmtop.sections[0].subsections.pop(0)
        else:
            raise RuntimeError('The two topologies have different [ defaults ] entries: \n\n{} \n\n'
                               'and \n\n{}\n\n'.format(' '.join(own_defentry), ' '.join(other_defentry)))
        paramsect_own = self.parameters
        paramsect_other = prmtop.parameters
        paramsect_own.subsections.extend(paramsect_other.subsections)
        paramsect_own._merge()

    def _include_all(self, ign_ifdef: bool) -> None:
        """
        includes all .itp files in the .top file to facilitate processing
        :return: None
        """
        ignore_lines = self._find_ifdef_lines() if ign_ifdef else set()
        lines = [i for i in range(len(self._contents)) if self._contents[i].strip().startswith("#include")
                 and i not in ignore_lines]
        while len(lines) > 0:
            lnum = lines[0]
            to_include, extra_prefix = self._find_in_path(self._contents.pop(lnum).split()[1].strip('"\''))
            with open(to_include) as includable:
                contents = self._add_prefix_to_include(includable.readlines(), extra_prefix)
            self._contents[lnum:lnum] = contents
            ignore_lines = self._find_ifdef_lines() if ign_ifdef else set()
            lines = [i for i in range(len(self._contents)) if self._contents[i].startswith("#include")
                     and i not in ignore_lines]

    def _preprocess_conditional_includes(self, ifdef: list) -> None:
        """
        Because of the implementation of CHARMM36m/CHARMM36 in gmx,
        the two variants are chosen depending on a preprocessing conditional
        so we need to pre-treat the topology to account for that
        -- I know it's extremely ugly but all other options require too much from the user --
        :param ifdef: list of str, defined keywords
        :return:
        """
        start_final = []
        flag = False
        for n, line in enumerate(self._contents):
            if len(line.split()) > 2 and line.split()[0] == '#ifdef' and line.split()[1] == "USE_OLD_C36":
                start_final.append(n)
            elif len(start_final) == 1 and line.strip().startswith('#include'):
                flag = True
            elif len(start_final) == 1 and len(line.split()) > 1 and line.split()[0] == '#endif' and flag:
                start_final.append(n)
        if len(start_final) == 2:
            if "USE_OLD_C36" in ifdef:
                incl = '#include "old_c36_cmap.itp"\n'
            else:
                self.top.print('Will use (newer) CMAP parameters for CHARMM36m. To use CHARMM36, '
                               'specify ifdef=["USE_OLD_C36"] (if your FF version supports that)')
                incl = '#include "cmap.itp"\n'
            for lnum in range(start_final[0], start_final[1]+1):
                self._contents.pop(lnum)
            self._contents.insert(start_final[0], incl)

    def _find_ifdef_lines(self) -> set:
        """
        Finds #ifdef/#endif blocks in the topology if user
        explicitly asks to ignore them
        :return: set, int numbers of all lines that fall within an #ifdef/#endif block
        """
        ignore_set = set()
        counter = 0
        for n, line in enumerate(self._contents):
            if line.strip().startswith("#ifdef") or line.strip().startswith("#ifndef"):
                counter += 1
            elif line.strip().startswith("#endif"):
                counter -= 1
            if counter > 0:
                ignore_set.add(n)
        return ignore_set

    def compare_two_ffparamsets(self, other_top, ffparams_only=False) -> None:
        self_copy = deepcopy(self)
        other = gml.obj_or_str(top=other_top)
        self_copy.clear_ff_params()
        other.clear_ff_params()
        self_copy.clear_sections()
        other.clear_sections()
        self.print("Comparing ff parameters:")
        own_entries = set([str(x) for param_subs in self_copy.parameters.subsections for x in param_subs if
                           isinstance(x, gml.EntryParam)])
        other_entries = set([str(x) for param_subs in other.parameters.subsections for x in param_subs if
                             isinstance(x, gml.EntryParam)])
        odd_a = own_entries.difference(other_entries)
        odd_b = other_entries.difference(own_entries)
        self.print(f"Unmatched parameters in topology {self.fname}:")
        for i in sorted(list(odd_a)):
            self.print(i)
        self.print(f"Unmatched parameters in topology {other.fname}:")
        for i in sorted(list(odd_b)):
            self.print(i)

    def _resolve_ifdefs(self, ifdefs: list) -> None:
        continuing = True
        while continuing:
            remove_lines = []
            counter = 0
            keeping = True
            keyword = None
            header_in_ifdef = False
            for n, line in enumerate(self._contents):
                if line.strip().startswith('[') and counter > 0 and keyword != 'USE_OLD_C36':
                    header = line.strip().strip('[]').strip()
                    raise RuntimeError(f"Found a [ {header} ] section header within a conditional block, this can lead"
                                       f"to issues if sections are rearranged. Please fix this first.")
                if line.startswith('#define') and len(line.strip().split()) == 2:
                    ifdefs.append(line.strip().split()[1])
                if line.strip().startswith("#ifdef") or line.strip().startswith("#ifndef"):
                    keyword = line.strip().split()[1] if keyword is None else keyword
                    counter += 1
                    if keyword in ifdefs:
                        keeping = True if line.strip().startswith("#ifdef") else False
                    else:
                        keeping = False if line.strip().startswith("#ifdef") else True
                    if counter == 1:
                        remove_lines.append(n)
                elif line.strip().startswith("#else"):
                    if counter == 0:
                        raise RuntimeError("Found an #else statement not linked to an #ifdef or #ifndef")
                    if counter == 1:
                        keeping = not keeping
                        remove_lines.append(n)
                if counter > 0:
                    if not keeping:
                        remove_lines.append(n)
                    if line.strip().startswith("["):
                        header_in_ifdef = True
                if line.strip().startswith("#endif"):
                    if counter == 1:
                        remove_lines.append(n)
                        counter -= 1
                        if header_in_ifdef:
                            if remove_lines and keyword not in ifdefs:
                                self.print("Part of the #ifdef {} section ({} lines) will be dropped as specified "
                                           "because the keyword was not defined. To prevent it, add 'ifdef=['{}']' "
                                           "as an argument when loading the topology to (unconditionally) keep "
                                           "specific sections, or set 'keep_all=True' to preserve the original (might "
                                           "occasionally produce issues).".format(keyword, len(remove_lines), keyword))
                            elif remove_lines and keyword in ifdefs:
                                self.print("Part of the #ifdef {} section ({} lines) will be dropped "
                                           "as specified.".format(keyword, len(remove_lines), keyword))
                            remove_lines = sorted(list(set(remove_lines)))
                            for i in remove_lines[::-1]:
                                _ = self._contents.pop(i)
                            break
                        else:
                            remove_lines = []
                            keyword = None
                            keeping = True
                    else:
                        counter -= 1
            else:
                continuing = False

    def clear_sections(self) -> None:
        """
        Removes all SectionMol instances that are not part
        of the system definition in [ system ]
        :return: None
        """
        if self.system is None:
            raise AttributeError("System properties have not been read, this is likely not a complete .top file")
        sections_to_delete = []
        for section_num, section in enumerate(self.sections):
            if isinstance(section, gml.SectionMol) and section.mol_name not in {x[0] for x in self.system}:
                sections_to_delete.append(section_num)
        self.sections = [s for n, s in enumerate(self.sections) if n not in sections_to_delete]

    def _find_in_path(self, filename: str) -> (str, str):
        """
        looks for a file to be included in either the current directory
        or in Gromacs directories (as given by user), in order to
        include all .itp files in a single .top file
        :param filename: str, name of the file to be searched for
        :return: str, full path to the file, path to the file directory
        """
        if filename.strip().startswith('./'):
            filename = filename.strip()[2:]
        pref = '/'.join(filename.split('/')[:-1])
        suff = filename.split('/')[-1]
        if filename.startswith('/') and os.path.isfile(filename):
            return filename, pref
        elif os.path.isfile(self.dir.rstrip(os.sep) + os.sep + pref + os.sep + suff):
            return self.dir.rstrip(os.sep) + os.sep + pref + os.sep + suff, pref
        elif self.gromacs_dir is not None and os.path.isfile(self.gromacs_dir.rstrip(os.sep) + os.sep + pref +
                                                             os.sep + suff):
            return self.gromacs_dir.rstrip(os.sep) + os.sep + pref + os.sep + suff, pref
        else:
            raise FileNotFoundError('file {} not found in neither local nor Gromacs directory.\n'
                                    'If the file is included in an #ifdef/#ifndef block, please try setting'
                                    ' ignore_ifdef=True'.format(filename))

    @staticmethod
    def _add_prefix_to_include(content: list, prefix: str) -> list:
        """
        Modifies #include statements if nested #includes
        point to different directories
        :param content: list of str, content of the included file
        :param prefix: str, directory name to add in the nested include
        :return: list of str, modified content
        """
        if prefix:
            for nline, line in enumerate(content):
                if line.strip().startswith("#include"):
                    try:
                        index = line.index('"')
                    except ValueError:
                        index = line.index("'")
                    newline = line[:index+1] + prefix + '/' + line[index+1:]
                    content[nline] = newline
        return content

    def _parse_sections(self) -> None:
        """
        Cuts the content in sections as defined by the position
        of special headers, and builds the self.sections list
        :return: None
        """
        section_lines = [l.strip().strip('[]').strip().split()[0] for n, l in enumerate(self._contents)
                         if len(l.strip().split()) == 3 and l.strip()[0] == '[' and l.strip()[-1] == ']']
        if section_lines[0] != 'defaults':
            print("The topology file lacks the [ defaults ] section, it will work but won't be fully functional")
            first = 'defaults' if section_lines[0] == 'moleculetype' else section_lines[0]
        else:
            first = 'defaults'
        special_sections = {first, 'moleculetype', 'system'}
        special_lines = [n for n, l in enumerate(self._contents)
                         if l.strip() and l.strip().strip('[]').strip().split()[0] in special_sections]
        special_lines.append(len(self._contents))
        for beg, end in zip(special_lines[:-1], special_lines[1:]):
            self.sections.append(self._yield_sec(self._contents[beg:end]))
            excess_if = self.count_ifs(beg) - self.count_ifs(beg, endif=True)
            self.sections[-1].conditional = excess_if
        # in case there are #defines at the very beginning (e.g. CHARMM36):
        for lnum in range(0, special_lines[0]):
            if not self._contents[lnum].lstrip().startswith(';') and self._contents[lnum].strip():
                if not self._contents[lnum].strip().startswith('*'):
                    entry = gml.Entry(self._contents[lnum].strip(), self.sections[0].subsections[0])
                    self.header.append(entry)

    def _yield_sec(self, content: list) -> "gml.Section":
        """
        Chooses which class (Section or derived classes)
        should be used for the particular set of entries
        :param content: list of str, slice of self.content
        :return: Section (or its subclass) instance
        """
        if 'defaults' in content[0] or 'atomtypes' in content[0]:
            return gml.SectionParam(content, self)
        elif 'moleculetype' in content[0]:
            return gml.SectionMol(content, self)
        else:
            return gml.Section(content, self)

    def count_ifs(self, linenum: int, endif: bool = False) -> int:
        """
        Counts #if or #endif directives up to line linenum
        :param linenum: int, line number
        :param endif: bool, if True we're looking for #endif instead of #if
        :return: int, number of directives found
        """
        if not endif:
            return len([ln for ln in self._contents[:linenum] if
                        ln.strip().startswith("#ifdef") or ln.strip().startswith("#ifndef")])
        else:
            return len([ln for ln in self._contents[:linenum] if ln.strip().startswith("#endif")])

    def read_system_properties(self) -> list:
        """
        Reads in system composition based on the [ molecules ] section
        :return: list of tuples (Mol_name, number_of_molecules)
        """
        system_subsection = [s.get_subsection('molecules') for s in self.sections
                             if 'molecules' in [ss.header for ss in s.subsections]]
        molecules = []  # we want to preserve the order of molecules in the system for e.g. PDB checking
        if len(system_subsection) > 1:
            raise RuntimeError("Multiple 'molecules' subsection found in the topology, this is not allowed")
        elif len(system_subsection) == 0:
            self.print("Section 'molecules' not present in the topology, assuming this is an isolated .itp")
            return []
        for e in system_subsection[0]:
            if e.content:
                molecules.append((e.content[0], int(e.content[1])))
        return molecules

    @property
    def charge(self) -> float:
        return sum([mol_count[1] * self.get_molecule(mol_count[0]).charge for mol_count in self.system])

    @property
    def natoms(self) -> int:
        return sum([mol_count[1] * self.get_molecule(mol_count[0]).natoms for mol_count in self.system])

    def nmol(self, name: Optional[str] = None) -> int:
        return sum([x[1] for x in self.system if name is None or x[0] == name])

    def explicit_defines(self) -> None:
        """
        Changes pre-defined keywords in parameter sets
        according to #define entries in FF params
        :return: None
        """
        self.parameters._get_defines()
        for m in self.molecules:
            for s in m.subsections:
                if isinstance(s, gml.SubsectionBonded):
                    s.explicit_defines()

    def get_molecule(self, mol_name: str) -> "gml.SectionMol":
        """
        Finds a molecule (SectionMol instance) whose mol_name
        matches the query name
        :param mol_name: name of the molecule
        :return: SectionMol instance
        """
        mol = [s for s in self.sections if isinstance(s, gml.SectionMol) and s.mol_name == mol_name]
        if len(mol) == 0:
            raise KeyError("Molecule {} is not defined in topology".format(mol_name))
        elif len(mol) > 1:
            raise RuntimeError("Molecule {} is duplicated in topology".format(mol_name))
        return mol[0]

    def check_pdb(self, maxwarn: Optional[int] = None, fix_pdb: bool = False, fix_top: bool = False) -> None:
        """c2r.gro
        Compares the topology with a PDB object to check
        for consistency, just as gmx grompp does;
        if inconsistencies are found, prints a report
        :param maxwarn: int, maximum number of warnings to print, default is 20
        :param fix_pdb: bool, whether to set names in Pdb using names from the Top
        :param fix_top: bool, whether to set names in Top using names from the Pdb
        :return: None
        """
        if self.pdb:
            mw = 20 if maxwarn is None else maxwarn
            self.pdb.check_top(mw, fix_pdb=fix_pdb, fix_top=fix_top)
        else:
            raise AttributeError("No PDB file has been bound to this topology")

    def map_property_on_structure(self, property: str = 'charge', field: str = 'beta') -> None:
        """
        Creates an atom-by-atom list of a chosen property and puts it in
        the beta column of the associated structure to be visualized
        :param property: str, name of the property (typically: charge, epsilon, mass, num, resid, sigma)
        :param field: str, 'beta' or 'occupancy' (both can be used to hold a property)
        :return: None
        """
        a = self.atoms[0]
        avail_prop = [x for x in dir(a) if isinstance(getattr(a, x), (int, float)) and not isinstance(getattr(a, x), bool)]
        if field not in ['beta', 'occupancy']:
            raise ValueError(f'"field" has to be "beta" or "occupancy", but is {field}')
        if self.pdb:
            if property not in avail_prop:
                raise AttributeError(
                    f"Atoms don't have the numerical property {property}, available ones are {avail_prop}")
            self.pdb.set_beta([getattr(a, property) for a in self.atoms], set_occupancy=(field == 'occupancy'))
            self.print(f'{property}s are now assigned to the {field}-column in the associated structure, '
                       f'save it as a PDB file in order to visualize')
        else:
            raise AttributeError("No PDB file has been bound to this topology")

    def save_top(self, outname: str = 'merged.top', split: bool = False) -> None:
        """
        Saves the combined topology to the specified file
        :param outname: str, file name for output
        :param split: bool, whether to split into individual .top files
        :return: None
        """
        outfile = open(outname, 'w')
        self._write_header(outfile)
        if not split:
            for section in self.sections:
                self._write_section(outfile, section)
        else:
            for section in self.sections:
                if isinstance(section, gml.SectionParam):
                    with open('ffparams.itp', 'w') as out_itp:
                        self._write_section(out_itp, section)
                    outfile.write('\n; Include ff parameters\n#include "ffparams.itp"\n')
                elif isinstance(section, gml.SectionMol):
                    with open('{}.itp'.format(section.mol_name), 'w') as out_itp:
                        self._write_section(out_itp, section)
                    outfile.write('\n; Include {mn} topology\n#include "{mn}.itp"\n'.format(mn=section.mol_name))
                else:
                    self._write_section(outfile, section)
        outfile.close()

    def patch_alchemical(self) -> None:
        for mol in self.molecules:
            if mol.is_alchemical:
                mol._patch_alch()

    def swap_states(self, **kwargs) -> None:
        for mol in self.alchemical_molecules:
            mol.swap_states(**kwargs)

    def drop_state_a(self, remove_dummies: bool = False) -> None:
        """
        Collapses alchemical A states in the whole topology, making state B
        the new non-alchemical default state A
        :param remove_dummies: remove_dummies: bool, whether to remove A-state dummies
        :return:
        """
        for mol in self.alchemical_molecules:
            mol.drop_state_a(remove_dummies)

    def drop_state_b(self, remove_dummies: bool = False) -> None:
        """
        Collapses alchemical B states in the whole topology, making state A
        the (only) non-alchemical state
        :param remove_dummies: remove_dummies: bool, whether to remove B-state dummies
        :return:
        """
        for mol in self.alchemical_molecules:
            mol.drop_state_b(remove_dummies)

    def rename_dummies(self) -> None:
        """
        If dummies are converted to atoms in topology manipulations, this allows to
        give them reasonable names so that they can be visualized without issues
        :return: None
        """
        for mol in self.molecules:
            for a in mol.atoms:
                if a.atomname.startswith('D'):
                    a.atomname = a.atomname.replace('DH', 'Hx').replace('DO', 'Ox').replace('DN', 'Nx').\
                        replace('DC', 'Cx').replace('DS', 'Sx')

    def recalculate_qtot(self) -> None:
        """
        Inserts the "qtot" cumulative-charge counter in atoms' comments
        :return: None
        """
        for mol in self.molecules:
            mol.recalc_qtot()

    def solute_tempering(self, temperatures: list, molecules: list) -> None:
        """
        Prepares .top files for REST2
        :param temperatures: list of float, set of "fake" temperatures for REST2 (lowest should be first)
        :param molecules: list of int, indices of molecules that will have their parameters modified
        :return: None
        """
        self.explicit_defines()
        for n, t in enumerate(temperatures):
            self.print(f'generating topology for effective temperature of {t} K...')
            mod = deepcopy(self)
            mod.molecules[0].scale_rest2_bonded(temperatures[0] / t)
            for i in molecules:
                mod.molecules[i].scale_rest2_charges(temperatures[0]/t)
            mod.save_top(self.fname.replace('.top', f'-rest{temperatures[0]/t:.3f}.top'))

    @staticmethod
    def _write_section(outfile: TextIO, section) -> None:
        """
        Writes a single section to the output file
        :param outfile: an open file in/out object, links to the output file
        :param section: a Section object to be written
        :return:
        """
        # TODO if there are 2 interaction types, split into two separate sections just for safety
        for subsection in section.subsections:
            outfile.write('\n[ {} ]\n'.format(subsection.header))
            for entry in subsection:
                if not entry.comment and not entry.content:
                    continue
                else:
                    if subsection.header == 'cmaptypes':
                        str_entry = str(entry).rstrip() + '\n\n'
                    else:
                        str_entry = str(entry).rstrip() + '\n'
                    outfile.write(str_entry)

    def _write_header(self, outfile: TextIO) -> None:
        """
        Writes the header to a newly generated file
        :param outfile: an open file in/out object, links to the output file
        :return: None
        """
        outname = outfile.name.split('/')[-1]
        outfile.write(";\n;  File {} was generated with the gromologist library\n"
                      ";  by user: {}\n;  on host: {}\n;  at date: {} \n;\n".format(outname,
                                                                                    platform.os.getenv("USER"),
                                                                                    platform.uname()[1],
                                                                                    datetime.datetime.now()))
        for entry in self.header:
            str_entry = str(entry).rstrip() + '\n'
            outfile.write(str_entry)
