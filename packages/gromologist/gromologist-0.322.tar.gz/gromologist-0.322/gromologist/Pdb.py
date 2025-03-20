"""
Module: Pdb.py
Author: Miłosz Wieczór <milosz.wieczor@irbbarcelona.org>
License: GPL 3.0

Description:
    This module includes classes describing structure file formats
    compatible with Gromacs, and hierarchical objects related to molecular structure

Contents:
    Classes:
        Pdb:
            Represents a molecular structure containing multiple atoms.
        Residue:
            Represents a structural unit within a larger molecular geometry.
        Atom:
            Describes a single atom with its position in space and properties.
        Traj:
            Contains multiple structures with identical composition but different geometry.

Usage:
    This module is intended to be imported as part of the library. It is not
    meant to be run as a standalone script. Example:

        import gromologist as gml
        protein = gml.Pdb("protein.pdb")

Notes:
    The "Pdb" class is capable of reading .gro and .cif files as well, and provides
    methods to read from the .xyz format.
"""

import gromologist as gml
from collections import defaultdict
from copy import deepcopy
from typing import Optional, Union, Iterable, Sized, Sequence
import math
import numpy as np


class Pdb:
    prot_map = {'ALA': 'A', 'CYS': 'C', 'CYX': 'C', 'CYM': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F', 'GLY': 'G',
                'HIS': 'H', 'HIE': 'H', 'HID': 'H', 'HSD': 'H', 'HSE': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
                'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', 'SER': 'S', 'THR': 'T', 'VAL': 'V',
                'TRP': 'W', 'TYR': 'Y', "GLUP": "E", "GLH": "E", "ASPP": "D", "ASH": "D", 'LYN': 'K'}

    nucl_map = {'DA': "A", 'DG': "G", 'DC': "C", 'DT': "T", 'DA5': "A", 'DG5': "G", 'DC5': "C", 'DT5': "T",
                'DA3': "A", 'DG3': "G", 'DC3': "C", 'DT3': "T", 'RA': "A", 'RG': "G", 'RC': "C", 'RU': "U",
                'RA5': "A", 'RG5': "G", 'RC5': "C", 'RU5': "U", 'RA3': "A", 'RG3': "G", 'RC3': "C", 'RU3': "U",
                'A': "A", 'G': "G", 'C': "C", 'U': "U", 'A5': "A", 'G5': "G", 'C5': "C", 'U5': "U",
                'A3': "A", 'G3': "G", 'C3': "C", 'U3': "U", "AN": "A", "GN": "G", "UN": "U", "CN": "C", "TN": "T"}

    def __init__(self, filename: str = None, top: Union[str, "gml.Top"] = None, altloc: str = 'A', qt: bool = False,
                 keep_altlocs = False, **kwargs):
        """
        Initializes a Pdb instnace
        :param filename: str, name of the file (.gro or .pdb)
        :param top: str or Top, a topology matching the structure
        :param altloc: str ('A' or 'B'), which altloc to keep if relevant
        :param qt: bool, whether to try to read the PDBQT format (with charges and types)
        :param kwargs: will be passed to Top constructor if top is a string/path
        """
        self.fname = filename
        if self.fname:
            if self.fname.endswith('gro'):
                self.atoms, self.box, self.remarks = self._parse_contents_gro([line.rstrip()
                                                                               for line in open(self.fname)])
            elif self.fname.endswith('cif'):
                self.atoms, self.box, self.remarks = self._parse_contents_cif([line.rstrip()
                                                                               for line in open(self.fname)])
            else:
                self.atoms, self.box, self.remarks = self._parse_contents([line.strip() for line in open(self.fname)],
                                                                          qt)
        else:
            self.atoms, self.box, self.remarks = [], 3 * [100] + 3 * [90], []
        if self.fname is None:
            self.fname = 'NewGmlStructure'
        self.top = top if not isinstance(top, str) else gml.Top(top, **kwargs)
        if self.top and not self.top.pdb:
            self.top.pdb = self
        if not self.atoms and self.top:
            ind = 0
            for mol in self.top.molecules:
                for entry in mol.atoms:
                    self.atoms.append(Atom.from_top_entry(entry, ind))
        self.gbox = self._calc_gro_box()
        self.altloc = altloc
        self.conect = {}
        self.qt = qt
        self._ter_format = "TER   {:>5d}      {:3s} {:1s}{:>4d}   \n"
        self._atom_format_gro = "{:>5d}{:5s}{:>5s}{:>5d}{:8.3f}{:8.3f}{:8.3f}\n"
        self._cryst_format = "CRYST1{:9.3f}{:9.3f}{:9.3f}{:7.2f}{:7.2f}{:7.2f} P 1           1\n"
        # clear altloc if all are identical
        if self.atoms and self.atoms[0].altloc.strip():
            if all([a.altloc == self.atoms[0].altloc for a in self.atoms]):
                for a in self.atoms:
                    a.altloc = ' '
        if self.altlocs.strip() and not keep_altlocs:
            print(f"Keeping atoms with altloc {self.altloc} only. If this is not what you want, set keep_altloc=True, "
                  f"but be warned that atom indexing might work incorrectly")
            self.keep_altloc(self.altloc)
        self.reindex()

    def __repr__(self) -> str:
        return "PDB file {} with {} atoms".format(self.fname, len(self.atoms))

    def __len__(self) -> int:
        if self.altlocs == ' ':
            return len(self.atoms)
        else:
            return len([a for a in self.atoms if a.altloc == self.altloc or not a.altloc.strip()])

    def __getitem__(self, item: int) -> "gml.Atom":
        return self.atoms[item]

    @property
    def altlocs(self) -> str:
        return ''.join(sorted(list(set(a.altloc for a in self.atoms))))

    @property
    def _atom_format(self) -> str:
        if self.qt:
            return "ATOM  {:>5d} {:4s}{:1s}{:4s}{:1s}{:>4d}{:1s}   " \
                   "{:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}{:9.3f} {:>2s}\n"
        else:
            return "ATOM  {:>5d} {:4s}{:1s}{:4s}{:1s}{:>4d}{:1s}   " \
                   "{:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:>2s}\n"

    def keep_altloc(self, chosen_altloc: str) -> None:
        """
        Keeps atoms with a selected altloc indicator
        :param chosen_altloc: str, the altloc that will be kept
        :return: None
        """
        assert len(str(chosen_altloc)) == 1
        all_altlocs = self.altlocs
        if chosen_altloc not in all_altlocs:
            raise RuntimeError(f"Altloc indicator {chosen_altloc} not found, there are: {self.altlocs}.")
        new_list = [a for a in self.atoms if a.altloc == self.altloc or not a.altloc.strip()]
        self.atoms = new_list

    def add_top(self, top: Union[str, "gml.Top"], **kwargs) -> None:
        """
        Adds a Top object to the current Pdb object, enabling some
        operations that couple the two
        :param top: str, path to the .top file
        :param kwargs: dict, extra parameters to pass to Top constructor
        :return: None
        """
        if isinstance(top, str):
            self.top = gml.Top(top, **kwargs)
        else:
            self.top = top
        if self.top and not self.top.pdb:
            self.top.pdb = self

    @property
    def natoms(self) -> int:
        """
        Returns the number of atoms
        :return: int, number of atoms
        """
        return len(self.atoms)

    @property
    def chains(self) -> list:
        """
        Returns a list of all chains defined in the structure
        :return: list of str, chain names
        """
        chns = []
        for a in self.atoms:
            if a.chain not in chns:
                chns.append(a.chain)
        return chns

    @property
    def residues(self) -> list:
        """
        Returns a list of all residues in the structure
        :return: list of gml.Residue objects
        """
        residues = []
        for a in self.atoms:
            id = f'{a.resname}{a.resnum}{a.chain.strip()}'
            if not residues or id != str(residues[-1]):
                residues.append(Residue(self, id=a.resnum, name=a.resname, chain=a.chain.strip()))
        return residues

    @property
    def has_partner(self) -> bool:
        """
        Indicates whether the Pdb is paired with a .top object
        :return: bool
        """
        return True if self.top is not None else False

    def add_remark(self, note: str) -> None:
        """
        Adds REMARK entries to Pdb objects e.g. to keep axtra information
        :param note: str, any text to be kept in the structure file
        :return: None
        """
        self.remarks.append(f"REMARK   0 {note}") # TODO make sure it works as intended

    def from_selection(self, selection: str, atom_indices: Optional[list] = None) -> "gml.Pdb":
        """
        Creates a new Pdb instance as a subset of an existing one,
        given a selection that defines a subset of atoms
        :param pdb: Pdb instance, source structure
        :param selection: str, a syntactically correct selection
        :return: Pdb, a subset of the original structure
        """
        # TODO what to do in case of a bound Top object? implement Top.slice()?
        if atom_indices is None:
            selected_indices = self.get_atom_indices(selection)
        else:
            selected_indices = atom_indices
        new_pdb = Pdb()
        new_pdb.atoms = [deepcopy(atom) for n, atom in enumerate(self.atoms) if n in selected_indices]
        new_pdb.box = self.box
        new_pdb.remarks = self.remarks
        new_pdb.altloc = self.altloc
        new_pdb.reindex()
        return new_pdb

    @classmethod
    def from_text(cls, text: str, ftype: str = 'pdb') -> "gml.Pdb":
        """
        Reads coordinates from text, useful for reading trajectories
        :param text: str, contents of the pdb/gro
        :param ftype: str, type of file (pdb, gro, bqt)
        :return: a new Pdb instance
        """
        new_pdb = Pdb()
        if ftype == 'pdb':
            new_pdb.atoms, new_pdb.box, new_pdb.remarks = cls._parse_contents(
                [line.strip() for line in text.split('\n')], False)
        elif ftype == 'bqt':
            new_pdb.atoms, new_pdb.box, new_pdb.remarks = cls._parse_contents(
                [line.strip() for line in text.split('\n')], True)
        elif ftype == 'gro':
            new_pdb.atoms, new_pdb.box, new_pdb.remarks = cls._parse_contents_gro(
                [line.strip() for line in text.split('\n')])
        new_pdb.reindex()
        return new_pdb

    def insert_from(self, pdb: Union[str, "gml.Pdb"], selection: str = 'all', after: str = 'all') -> None:
        """
        Inserts selected atoms from another structure file in a selected position
        :param pdb: str or gml.Pdb, the other structure
        :param selection: str, the selection of atoms that will be inserted
        :param after: str, selection after which the atoms will be inserted (e.g. 'chain A')
        :return: None
        """
        pdb = gml.obj_or_str(pdb)
        last_index = self.get_atom_indices(after)[-1]
        for at in pdb.get_atoms(selection)[::-1]:
            self.atoms.insert(last_index + 1, deepcopy(at))
        self.reindex()

    def _match_top_to_pdb(self, serial: int) -> "gml.Entry":
        if not self.top:
            raise RuntimeError("Add a topology to the structure in order to match ")
        selected = self.get_atom_index(f'serial {serial}')
        assert self.natoms == self.top.natoms
        assert serial <= self.natoms
        system = self.top.system
        for mol_n in system:
            molname, molnum = mol_n
            mol = self.top.get_molecule(molname)
            for i in range(molnum):
                if selected <= mol.natoms:
                    return mol.atoms[selected - 1]
                else:
                    selected -= mol.atoms
        raise RuntimeError("Something went wrong, not found the atom in question")

    def _match_top_molecule(self, serial: int) -> "gml.SectionMol":
        if not self.top:
            raise RuntimeError("Add a topology to the structure in order to match ")
        selected = self.get_atom_index(f'serial {serial}')
        assert self.natoms == self.top.natoms
        assert serial <= self.natoms
        system = self.top.system
        for mol_n in system:
            molname, molnum = mol_n
            mol = self.top.get_molecule(molname)
            for i in range(molnum):
                if selected <= mol.natoms:
                    return mol
                else:
                    selected -= mol.atoms
        raise RuntimeError("Something went wrong, not found the atom in question")

    def print_protein_sequence(self, gaps: bool = False) -> list:
        """
        Prints protein sequence chain by chain, recognizing amino acids
        as residues that contain a CA atom; unrecognized residues are written as X
        :param gaps: bool, whether to pad gaps (non-continuous numbering) with dashes '-'
        :return: str, the protein sequence
        """
        chains = list({a.chain.strip() for a in self.atoms if a.atomname == 'CA'})
        sequences = []
        if not chains:
            print("No protein chains in the molecule, run Pdb.add_chains() first")
            return []
        for ch in sorted(chains):
            cas = set(self.get_atom_indices(f'name CA and chain {ch}'))
            atoms = [a for n, a in enumerate(self.atoms) if n in cas and a.altloc in [' ', self.altloc]]
            if not gaps:
                sequences.append(''.join([Pdb.prot_map[i.resname] if i.resname in Pdb.prot_map.keys() else 'X'
                                          for i in atoms]))
            else:
                res = [a.resnum for n, a in enumerate(self.atoms) if n in cas and a.altloc in [' ', self.altloc]]
                seq = []
                counter = 0
                for r in range(res[0], res[-1] + 1):
                    if r in res:
                        rname = atoms[counter].resname
                        counter += 1
                        seq.append(Pdb.prot_map[rname] if rname in Pdb.prot_map.keys() else 'X')
                    else:
                        seq.append('-')
                sequences.append(''.join(seq))
        return sequences

    def print_nucleic_sequence(self, as_modeller=False) -> list:
        """
        Prints nucleic acid sequences chain by chain, recognizing nucleotides
        as residues that contain an O4' atom; unrecognized residues are written as X
        :return: str, the nucleic acid sequence
        """
        mapping = defaultdict(lambda: 'X')
        sequences = []
        mapping.update(Pdb.nucl_map)
        chains = list({a.chain.strip() for a in self.atoms if a.atomname == "O4'"})
        chaintypes = []
        if not chains:
            print("No nucleic acid chains in the molecule, run Pdb.add_chains() first")
            return []
        for ch in sorted(chains):
            cas = set(self.get_atom_indices(f"name O4' and chain {ch}"))
            atoms = [a for n, a in enumerate(self.atoms) if n in cas]
            sequences.append(''.join([mapping[i.resname] if i.resname in mapping.keys() else 'X' for i in atoms]))
            if atoms[0].resname.startswith('D'):
                chaintypes.append('D')
            else:
                chaintypes.append('R')
        if as_modeller:
            codes_d = {"A": 'e', "T": 't', "C": 'j', "G": 'l'}
            codes_r = {"A": 'a', "U": 'u', "C": 'c', "G": 'g'}
            sequences = [''.join([codes_d[i] for i in seq]) if stype == "D" else ''.join([codes_r[i] for i in seq]) for seq, stype in zip(sequences, chaintypes)]
        return sequences

    def find_missing(self) -> None:
        """
        Assuming standard naming conventions, finds atoms that are missing
        in protein structures and prints them (heavy atoms only!)
        :return: None
        """
        pro_bb = ['N', 'O', 'C', 'CA']
        pro_sc = {'A': ['CB'], 'C': ['CB', 'SG'], 'D': ['CB', 'CG', 'OD1', 'OD2'], 'E': ['CB', 'CG', 'CD', 'OE1',
                                                                                         'OE2'],
                  'F': ['CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'], 'G': [], 'H': ['CB', 'CG', 'ND1', 'CE1',
                                                                                      'CD2', 'NE2'],
                  'I': ['CB', 'CG1', 'CG2', 'CD'], 'K': ['CB', 'CG', 'CD', 'CE', 'NZ'], 'L': ['CB', 'CG',
                                                                                              'CD1', 'CD2'],
                  'M': ['CB', 'CG', 'SD', 'CE'], 'N': ['CB', 'CG', 'OD1', 'ND2'], 'P': ['CB', 'CG',
                                                                                        'CD'],
                  'Q': ['CB', 'CG', 'CD', 'OE1', 'NE2'], 'R': ['CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'],
                  'S': ['CB', 'OG'], 'T': ['CB', 'CG2', 'OG1'], 'V': ['CB', 'CG1', 'CG2'], 'W': ['CB', 'CG', 'CD1',
                                                                                                 'CD2', 'NE1', 'CE2',
                                                                                                 'CE3', 'CH2', 'CZ2',
                                                                                                 'CZ3'],
                  'Y': ['CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ',
                        'OH']}
        alt = {'I': ['CD', 'CD1']}  # pretty temporary and non-extensible, need to rethink
        curr_res = ('X', 0)
        atomlist = []
        for at in self.atoms:
            if (at.resname, at.resnum) != curr_res:
                if 'CA' in atomlist:
                    full = set(pro_bb + pro_sc[Pdb.prot_map[curr_res[0]]])
                    if not full.issubset(set(atomlist)):
                        if Pdb.prot_map[curr_res[0]] in alt.keys():
                            modfull = set([alt[Pdb.prot_map[curr_res[0]]][1] if x == alt[Pdb.prot_map[curr_res[0]]][0]
                                           else x for x in full])
                            if not modfull.issubset(set(atomlist)):
                                print(f"atoms {modfull.difference(set(atomlist))} missing from residue {curr_res}")
                        else:
                            print(f"atoms {full.difference(set(atomlist))} missing from residue {curr_res}")
                # TODO implement for nucleic
                curr_res = (at.resname, at.resnum)
                atomlist = []
            atomlist.append(at.atomname)

    def names_from_top(self) -> None:
        """
        Sets names from the associated topology file
        :return: None
        """
        if self.top is None:
            raise RuntimeError("No .top is bound to this structure, add 'top=...' when loading molecule")
        if self.top.natoms != self.natoms:
            raise RuntimeError("Different numbers of atoms between .pdb and .top")
        for at, ap in zip(self.top.atoms, self.atoms):
            ap.atomname = at.atomname

    def add_chains(self, selection: str = None, chain: str = None, offset: int = 0, maxwarn: int = 100,
                   cutoff: float = 10, protein_only: bool = False, nopbc: bool = False) -> None:
        """
        Given a matching Top instance, adds chain identifiers to atoms
        based on the (previously verified) matching between invididual
        molecules defined in Top and consecutive atoms in this Pdb instance.
        Solvent molecules are ommited, and only characters from A to Z
        are supported as valid chain identifiers.
        Optionally, given `serials` and `chain`, one can set all atoms
        with atom numbers in `serials` as belonging to chain `chain`.
        :param selection: str, select only a subset of atoms whose chain ID will be set to the value of 'chain'
        :param chain: str, chain to set for the specified selection
        :param offset: int, start chain ordering from letter other than A
        :param maxwarn: int, max number of warnings before an error shows up
        :param cutoff: float, distance threshold (in A) for chain separation if using geometric criteria
        :param protein_only: bool, whether to only add chains to protein residues
        :param nopbc: bool, whether to ignore PBC distances (assumes molecule is whole)
        :return: None
        """
        base_char = 65 + offset  # 65 is ASCII for "A"
        curr_resid = None
        prev_atom = None
        if (selection is None and chain is not None) or (selection is not None and chain is None):
            raise ValueError("Both serials and chain have to be specified simultaneously")
        if selection is not None and chain is not None:
            for atom in self.get_atoms(selection):
                atom.chain = chain
            return
        if not self.top:
            for atom in self.atoms:
                if protein_only and atom.resname not in Pdb.prot_map.keys():
                    continue
                if not prev_atom:
                    prev_atom = atom
                    curr_resid = atom.resnum
                if atom.resnum != curr_resid:
                    if nopbc:
                        dist = self._atoms_dist(atom, prev_atom)
                    else:
                        dist = self._atoms_dist_pbc(atom, prev_atom)
                    prev_atom = atom
                    curr_resid = atom.resnum
                    if dist > cutoff:
                        base_char += 1
                if base_char == 91:
                    base_char += 6
                if base_char > 122:
                    break
                atom.chain = chr(base_char)
        else:
            self.check_top(maxwarn=maxwarn)
            excluded = {'SOL', 'HOH', 'TIP3', 'WAT', 'OPC', 'K', 'NA', 'CL', 'POT', 'SOD', 'NA+', 'K+', 'CLA'}
            index = 0
            for mol_count in self.top.system:
                if mol_count[0].upper() not in excluded:
                    n_mols = mol_count[1]
                    mol = self.top.get_molecule(mol_count[0])
                    n_atoms = mol.natoms
                    for m in range(n_mols):
                        for a in range(n_atoms):
                            self.atoms[index].chain = chr(base_char)
                            index += 1
                        if (protein_only and self.atoms[index].resname in Pdb.prot_map.keys()) or not protein_only:
                            base_char += 1
                        if base_char > 90:
                            return

    def list_atoms(self, selection: str = None) -> None:
        """
        Prints atoms in the structure, optionally
        only the subset corresponding to the selection
        :param selection: str, selection to be printed, default is None
        :return: None
        """
        atoms = self.atoms if selection is None else self.get_atoms(selection)
        for a in atoms:
            print(self._write_atom(a).strip())

    def check_top(self, maxwarn: int = 20, fix_pdb: bool = False, fix_top: bool = False) -> None:
        """
        Checks the structure against the associated topology to identify
        and list potential mismatches in atom names
        :param maxwarn: int, maximum number of warnings to print, default is 20
        :param fix_pdb: bool, whether to set names in Pdb using names from the Top
        :param fix_top: bool, whether to set names in Top using names from the Pdb
        :return: None
        """
        if fix_pdb and fix_top:
            raise ValueError("You either want to fix topology or pdb naming")
        if self.top is None:
            raise ValueError("a Top object has not been assigned; molecule info missing")
        index, err = 0, 0
        self._remove_altloc()
        for atom_top, atom_pdb in zip(self.top.atoms, self.atoms):
            try:
                rtrn = self._check_mismatch(atom_top, atom_pdb, atom_top.molname)
            except IndexError:
                raise RuntimeError("Mismatch encountered: PDB has {} atoms while topology "
                                   "has {}".format(len(self.atoms), len(self.top.atoms)))
            if rtrn:
                if fix_pdb:
                    self.atoms[index].atomname = atom_top.atomname
                elif fix_top:
                    atom_top.atomname = self.atoms[index].atomname
            err += rtrn
            index += 1
            if err > maxwarn > -1:
                raise RuntimeError("Error: too many warnings; use maxwarn=N to allow for up to N exceptions,"
                                   "or maxwarn=-1 to allow for any number of them")
        if self.natoms == self.top.natoms:
            print("Check passed, all names match")
        elif self.natoms > self.top.natoms:
            raise RuntimeError(f"All atom names match, but there are {self.natoms - self.top.natoms} extra atoms at "
                               f"the end of your structure file")
        else:
            raise RuntimeError(f"All atom names match, but there are {self.top.natoms - self.natoms} extra atoms at "
                               f"the end of your topology file")

    @staticmethod
    def _check_mismatch(atom_entry: "gml.EntryAtom", atom_instance: "gml.Atom", mol_name: str) -> int:
        """
        Checks a Pdb entry against a Top entry to make sure the atom names match
        :param atom_entry: EntryAtom instance from the Top
        :param atom_instance: Atom instance from the Pdb
        :param mol_name: str, name of the molecule to print in the message
        :return: int, 0 if names match or 1 otherwise
        """
        if atom_entry.atomname != atom_instance.atomname or atom_entry.resname != atom_instance.resname:
            print("Atoms {} ({}/{}) in molecule {} topology and {} ({}/{}) in .pdb have "
                  "non-matching names".format(atom_entry.num, atom_entry.atomname, atom_entry.resname, mol_name,
                                              atom_instance.serial, atom_instance.atomname, atom_instance.resname))
            return 1
        return 0

    def cap_protein_chain(self, chain: str = "A", nterm: bool = True, cterm: bool = True) -> None:
        """
        Adds an N- or C-terminal cap to the protein structure (without the hydrogen; you need to
        pass it through gmx pdb2gmx still)
        :param chain: str, name of the chain to cap
        :param nterm: bool, whether to cap the N-term
        :param cterm: bool, whether to cap the C-term
        :return: None
        """
        if nterm:
            refatom_n = self.get_atoms(f"name N and chain {chain}")[0]
            firstatom_n = self.get_atoms(f"resid {refatom_n.resnum} and chain {chain}")[0]
            self.insert_atom(firstatom_n.serial, name="CC", hooksel=f"serial {refatom_n.serial}",
                             bondlength=1.35, p1_sel=f"resid {refatom_n.resnum} and name C and chain {chain}",
                             p2_sel=f"resid {refatom_n.resnum} and name CA and chain {chain}", resname='ACE')
            self.insert_atom(firstatom_n.serial - 1, name="CH3", hooksel=f"resname ACE and name CC and chain {chain}",
                             bondlength=1.5, p1_sel=f"resid {refatom_n.resnum} and name CA and chain {chain}",
                             p2_sel=f"resid {refatom_n.resnum} and name N and chain {chain}", resname='ACE')
            self.insert_atom(firstatom_n.serial, name="O", hooksel=f"resname ACE and name CC and chain {chain}",
                             bondlength=1.25, vector=self._vector(['CC', 'CH3', 'N', 'CC'], refatom_n.resnum, chain),
                             resname='ACE')
            for at in self.get_atoms(f'resname ACE and chain {chain}'):
                if at.atomname == 'CC':
                    at.atomname = 'C'
                at.resnum = refatom_n.resnum - 1
        if cterm:
            refatom_c = self.get_atoms(f"name C and chain {chain}")[-1]
            try:
                oxt = self.get_atom(f'name OXT and resid {refatom_c.resnum} and chain {chain}')
            except:
                pass
            else:
                self.delete_atom(oxt.serial)
            lastatom_c = self.get_atoms(f"resid {refatom_c.resnum} and chain {chain}")[-1]
            self.insert_atom(lastatom_c.serial + 1, name="NN", hooksel=f"serial {refatom_c.serial}",
                             bondlength=1.35, vector=self._vector(['C', 'CA', 'O', 'C'], refatom_c.resnum, chain),
                             resname='NME')
            self.insert_atom(lastatom_c.serial + 2, name="CH3", hooksel=f"resname NME and name NN and chain {chain}",
                             bondlength=1.5, p1_sel=f"resid {refatom_c.resnum} and name CA and chain {chain}",
                             p2_sel=f"resid {refatom_c.resnum} and name C and chain {chain}", resname='NME')
            for at in self.get_atoms(f'resname NME and chain {chain}'):
                if at.atomname == 'NN':
                    at.atomname = 'N'
                at.resnum = refatom_c.resnum + 1
        self.reindex()

    def permute_chains(self, permute: list, rename: bool = True) -> None:
        """
        Permutes the atoms in a molecule so that the order of chain is altered
        :param permute: list, target permutation (0-based)
        :param rename: bool, whether to adjust chain names after the permutation
        :return: None
        """
        assert sorted(permute) == list(range(len(permute)))
        assert len(self.chains) == len(permute)
        new_atoms = []
        for chnr in permute:
            chname = self.chains[chnr]
            new_atoms.extend(self.get_atoms(f'chain {chname}'))
        new_atoms.extend(self.get_atoms(f'not chain {" ".join(self.chains)}'))
        self.atoms = new_atoms
        if rename:
            self.renumber_atoms()
            ordchains = {k: v for k, v in zip(self.chains, sorted(self.chains))}
            for atom in self.atoms:
                if atom.chain in ordchains.keys():
                    atom.chain = ordchains[atom.chain]
        self.reindex()

    def print_mols(self) -> None:
        """
        Identifies and lists molecules contained in the structure, chain by chain
        :return: None
        """
        # TODO fix
        chains = list({a.chain.strip() for a in self.atoms})
        if not chains:
            print("No chains in the molecule, run Pdb.add_chains() first")

        def identify(atom):
            first = atom.resname
            if first in Pdb.prot_map.keys() or (
                    first[1:] in Pdb.prot_map.keys() and first[0] in 'NC') or first == 'ACE':
                return 'Protein'
            elif first in Pdb.nucl_map.keys():
                return 'Nucleic'
            else:
                return atom.resname

        mol_list = []
        mol = identify(self.atoms[0])
        chain = self.atoms[0].chain
        res = self.atoms[0].resnum
        for a in self.atoms:
            if mol in ['Protein', 'Nucleic']:
                if a.chain != chain:
                    mol_list.append([mol + f'_chain_{chain}', 1])
                    chain = a.chain
                    mol = identify(a)
            else:
                if a.resnum != res:
                    if len(mol) >= 1 and mol_list and mol == mol_list[-1][0]:
                        mol_list[-1][1] += 1
                    else:
                        mol_list.append([mol, 1])
                    mol = identify(a)
                    chain = a.chain
            res = a.resnum
        if len(mol) >= 1 and mol_list and mol == mol_list[-1][0]:
            mol_list[-1][1] += 1
        else:
            mol_list.append([mol, 1])
        for i in mol_list:
            print(f'{i[0]} {i[1]}')

    def _remove_altloc(self) -> None:
        """
        Only keeps one of the alternative locations in case
        there is more (by default, A is kept)
        :return: None
        """
        self.atoms = [a for a in self.atoms if a.altloc in [' ', self.altloc]]

    def _write_atom(self, atom: "gml.Atom", pdb: bool = True) -> str:
        """
        Fn to convert an Atom instance to a line compatible with .pdb or .gro formatting
        :param atom: an Atom instance to be written
        :param pdb: bool, whether to write as .pdb (otherwise .gro)
        :return: str, formatted line
        """
        atom.serial %= 100000
        atom.resnum %= 10000
        if atom.occ > 1000:
            atom.occ %= 1000
        if atom.beta > 1000:
            atom.beta %= 1000
        if pdb:
            if len(atom.atomname) < 4:
                atname = ' ' + atom.atomname
            else:
                atname = atom.atomname
            if self.qt:
                return self._atom_format.format(atom.serial, atname, atom.altloc, atom.resname, atom.chain,
                                                atom.resnum, atom.insert, atom.x, atom.y, atom.z, atom.occ, atom.beta,
                                                atom.q, atom.type)
            else:
                return self._atom_format.format(atom.serial, atname, atom.altloc, atom.resname, atom.chain,
                                                atom.resnum, atom.insert, atom.x, atom.y, atom.z, atom.occ, atom.beta,
                                                atom.element)
        else:
            return self._atom_format_gro.format(atom.resnum, atom.resname, atom.atomname, atom.serial, atom.x / 10,
                                                atom.y / 10, atom.z / 10)

    @staticmethod
    def _write_conect(atom: int, bonded: list) -> str:
        return 'CONECT' + ('{:>5}' * (len(bonded) + 1)).format(atom, *bonded) + '\n'

    def shift_periodic_image(self, vec: list, selection: Optional[str] = 'all') -> None:
        """
        Move a part of the system by a box vector in X, Y and/or Z dimension
        :param vec: list of 3 int (i, j, k), the selection will be translated by [i*a, j*b, k*c]
        :param selection: str, if chosen, the translation will only be applied to this part of the system
        :return: None
        """
        deg2rad = 57.29577951308232
        alpha, beta, gamma = self.box[3]/deg2rad, self.box[4]/deg2rad, self.box[5]/deg2rad
        box_vec_a = [self.box[0], 0, 0]
        box_vec_b = [self.box[1] * math.cos(gamma), self.box[1] * math.sin(gamma), 0]
        v3_x = self.box[2] * (math.cos(alpha) - math.cos(beta) * math.cos(gamma)) / math.sin(gamma)
        v3_y = self.box[2] * (math.sin(beta) * math.cos(alpha) - math.cos(beta) * math.sin(alpha) * math.cos(gamma))
        v3_z = self.box[2] * (math.sin(beta) * math.sin(alpha) + math.cos(beta) * math.cos(gamma))
        box_vec_c = [v3_x, v3_y, v3_z]
        vec_to_move = [box_vec_a[j] * vec[0] + box_vec_b[j] * vec[1] + box_vec_c[j] * vec[2] for j in range(3)]
        print(box_vec_a, box_vec_b, box_vec_c, vec_to_move)
        self.translate(vec_to_move, selection)

    def translate(self, vec: list, selection: Optional[str] = 'all') -> None:
        """
        Moves a selection in space by the provided vector
        :param vec: list, 3 components
        :param selection: str, selection (all by default)
        :return: None
        """
        atoms_to_move = self.get_atoms(selection)
        for atom in atoms_to_move:
            atom.x += vec[0]
            atom.y += vec[1]
            atom.z += vec[2]

    def tip3_to_opc(self, offset: float = 0.147722363) -> None:
        """
        Converts a 3-point water model in a structure to a 4-point
        by adding a virtual site to each water molecule
        :param offset: a fractional value used to define the position of the virtual site, for OPC equal to 0.147722363
        :return: None
        """
        names = {"TIP3", "WAT", "SOL", "HOH", "TIP"}
        o_names = {"O", "OW"}
        h_names = {"H", "HW"}
        new_atoms = []
        water_mol = {}
        for n, a in enumerate(self.atoms):
            if a.resname in names:
                if a.atomname in o_names:
                    water_mol["O"] = a
                if a.atomname[:-1] in h_names:
                    try:
                        _ = water_mol["H1"]
                    except KeyError:
                        water_mol["H1"] = a
                    else:
                        water_mol["H2"] = a
                if len(water_mol) == 3:
                    new_atoms.append(a)
                    new_atom = Atom(self._write_atom(water_mol["O"]), 0)
                    new_atom.atomname = "MW"
                    new_atom.set_coords([a + offset * (b + c - 2 * a) for a, b, c
                                         in zip(new_atom.coords, water_mol["H1"].coords, water_mol["H2"].coords)])
                    new_atoms.append(new_atom)
                    water_mol = {}
                else:
                    new_atoms.append(a)
            else:
                new_atoms.append(a)
        self.atoms = new_atoms
        self.reindex()

    def renumber_atoms(self, offset: int = 1, selection: Optional[str] = None) -> None:
        """
        Consecutively renumbers all atoms in the structure
        :param offset: int, number of the first atom to be set
        :param selection: str, will only renumber atoms matching the selection
        :return: None
        """
        # TODO add hex as optional?
        ats = self.atoms if selection is None else self.get_atoms(selection)
        for n, atom in enumerate(ats, offset):
            atom.serial = 1 + (n - 1) % 99999

    def renumber_residues(self, offset: Union[int, list] = 1, selection: Optional[str] = None,
                          per_chain: bool = False, force_positive: bool = False) -> None:
        """
        Consecutively renumbers all residues in the structure
        :param offset: int or list, number of the first residue to be set (can be per-chain)
        :param selection: str, will only renumber residues matching the selection
        :param per_chain: bool, whether numbering of each chain should start from `offset`
        :param force_positive: bool, makes sure no residue has ID 0 or negative
        :return: None
        """
        if per_chain:
            if isinstance(offset, int):
                offset = [offset] * len(self.chains)
            else:
                assert len(offset) == len(self.chains)
            count = offset[0]
        else:
            count = offset
        if force_positive:
            count = 1 + (count - 1) % 9999
        ats = range(len(self.atoms)) if selection is None else self.get_atom_indices(selection)
        for n in ats:
            if per_chain and n > 1 and self.atoms[n].chain != self.atoms[n - 1].chain:
                try:
                    count = offset[self.chains.index(self.atoms[n].chain)]
                except:
                    count = 1
            temp = count
            try:
                if self.atoms[n].resnum != self.atoms[n + 1].resnum or self.atoms[n].chain != self.atoms[n + 1].chain:
                    if not force_positive:
                        temp = count + 1
                    else:
                        # avoid resnum==10000 as it gets written as 0 and causes problems:
                        temp = 1 + count % 9999
            except IndexError:
                pass
            self.atoms[n].resnum = count
            count = temp

    def reposition_atom_from_hook(self, atomsel: str, hooksel: str, bondlength: float, p1_sel: Optional[str] = None,
                                  p2_sel: Optional[str] = None, vector: Optional[Iterable] = None) -> None:
        """
        Sets coordinates of an atom based on a "hook" atom (one it's bound to), bond length, and a vector defining
        the direction of the bond
        :param atomsel: str, unique selection for the atom being moved
        :param hooksel: str, unique selection for the hook atom
        :param bondlength: float, length of the bond (in A)
        :param p1_sel: str, selection for the 1st atom defining the vector to position the new atom
        :param p2_sel: str, selection for the 2nd atom defining the vector to position the new atom
        :param vector: iterable, defines the vector direction to position the new atom
        :return: None
        """
        coords = self.get_coords()
        if p1_sel is not None and p2_sel is not None:
            p1_xyz = coords[self.get_atom_index(p1_sel)]
            p2_xyz = coords[self.get_atom_index(p2_sel)]
            vec = p2_xyz - p1_xyz
        elif vector is not None:
            vec = vector
        else:
            raise RuntimeError("In repositioning, please use either p1/p2 selections or specify the vector")
        movable = self.get_atom(atomsel)
        hook_xyz = coords[self.get_atom_index(hooksel)]
        vec_len = np.linalg.norm(vec)
        scale = bondlength / vec_len
        movable.set_coords([h + scale * v for h, v in zip(hook_xyz, vec)])

    def match_order_by_top_names(self, arange: Optional[tuple] = None, equivalents: Optional[dict] = None) -> None:
        """
        Whenever PDB atoms have different ordering than .top ones
        but naming is consistent, we can use the ordering from .top
        to reorder PDB atoms.
        This can be done for the entire system if molecules are unique;
        otherwise, range has to be specified (using the Pythonic convention)
        to avoid ambiguities. In that case, matching molecules will only be
        looked for in the specified range.
        :param arange: tuple, start and end point of the modification (end is excluded)
        :param equivalents: dict, matching PDB names to topology names
        :return:
        """
        if self.top is None:
            raise ValueError("a Top object has not been assigned; molecule info missing")
        new_atoms = []
        index = 0
        # TODO is arange here working at all?
        for mol_count in self.top.system:
            mol = self.top.get_molecule(mol_count[0])
            n_mols = mol_count[1]
            atom_subsection = mol.get_subsection('atoms')
            atom_entries = [e for e in atom_subsection if isinstance(e, gml.EntryAtom)]
            for _ in range(n_mols):
                for a in atom_entries:
                    if arange is None or arange[0] <= index < arange[1]:
                        if equivalents is not None and a.atomname in equivalents.keys():
                            pdb_loc = self.get_atom_indices(
                                f"resname {a.resname} and resid {a.resid} "
                                f"and name {a.atomname} {equivalents[a.atomname]}")
                        else:
                            pdb_loc = self.get_atom_indices(
                                f"resname {a.resname} and resid {a.resid} and name {a.atomname}")
                        pdb_loc = [loc for loc in pdb_loc if not arange or arange[0] <= index < arange[1]]
                        if len(pdb_loc) != 1:
                            raise ValueError("Could not proceed; for match-based renumbering, residue numberings "
                                             "have to be consistent between PDB and .top, atom names need to match, "
                                             "and molecules cannot be repeated.\nError encountered when processing "
                                             "residue {} with resid {}, atom name {}".format(a.resname, a.resid,
                                                                                             a.atomname))
                        new_atoms.append(self.atoms[list(pdb_loc)[0]])
                    index += 1
        self.atoms = new_atoms

    def insert_atom(self, serial: int, name: str = "HX", hooksel: Optional[str] = None,
                    bondlength: Optional[float] = None, p1_sel: Optional[str] = None, p2_sel: Optional[str] = None,
                    vector: Optional[Iterable] = None, renumber: Optional[bool] = True, **kwargs) -> None:
        """
        Inserts an atom into the atomlist. The atom is defined by
        providing a base Atom instance and a number of keyworded modifiers,
        e.g. atomname="CA", serial=15, ...
        :param serial: int, the new serial (1-based) of the inserted Atom in the Atoms list
        :param name: str, name of the new atom
        :param hooksel: str, unique selection for the atom the new atom will be bound to
        :param bondlength: float, length of the bond extending from the "hook" atom (in A)
        :param p1_sel: str, selection for the 1st atom defining the vector to position the new atom
        :param p2_sel: str, selection for the 2nd atom defining the vector to position the new atom
        :param vector: iterable, defines the vector direction to position the new atom
        :param renumber: bool, whether to renumber atoms after inserting
        :param kwargs: Atom attributes to be held by the new atom
        :return: None
        """
        base_atom = self.get_atom(hooksel)
        new_atom = Atom(self._write_atom(base_atom), 0)
        kwargs.update({"atomname": name})
        for kw in kwargs.keys():
            if kw not in {"serial", "atomname", "resname", "chain", "resnum", "x", "y", "z", "occ", "beta", "element"}:
                raise ValueError("{} is not a valid Atom attribute")
            new_atom.__setattr__(kw, kwargs[kw])
        self.atoms.insert(serial - 1, new_atom)
        if renumber:
            self.renumber_atoms()
        self.reindex()
        rname = base_atom.resname if "resname" not in kwargs.keys() else kwargs["resname"]
        chsel = f'chain {base_atom.chain} and ' if base_atom.chain.strip() else ''
        atomsel = f'{chsel}name {name} and resid {base_atom.resnum} and resname {rname}'
        if (atomsel is not None and hooksel is not None and bondlength is not None and
                ((p1_sel is not None and p2_sel is not None) or vector is not None)):
            if bondlength > 0:
                self.reposition_atom_from_hook(atomsel, hooksel, bondlength, p1_sel, p2_sel, vector)

    def delete_atom(self, serial: int, renumber: bool = False) -> None:
        """
        Removes an atom from the Pdb object
        :param serial: int, serial number of the atom to be removed (usually 1-based)
        :param renumber: bool, whether to renumber atoms after removal
        :return: None
        """
        num = [n for n, a in enumerate(self.atoms) if a.serial == serial]
        if len(num) == 0:
            raise ValueError('No atoms with serial number {}'.format(serial))
        elif len(num) > 1:
            raise ValueError('Multiple atoms with serial number {}; consider renumbering'.format(serial))
        atom = self.atoms.pop(num[0])
        print('Entry {} deleted from PDB'.format(str(atom)))
        if renumber:
            self.renumber_atoms()
        self.reindex()

    def add_elements(self, force: bool = False) -> None:
        """
        Guesses the element (last element in the .pdb file) based on the atom name,
        useful for e.g. element-based coloring in VMD
        :param force: bool, assign even if present already
        :return: None
        """
        for a in self.atoms:
            if (not a.element) or force:
                a.element = [x for x in a.atomname if not x.isdigit()][0]

    def add_qt(self) -> None:
        """
        Adds charge (q) and type from an associated topology
        :return: None
        """
        if self.top is None:
            raise RuntimeError("Add .top to this structure to read charges/types, e.g. using the .add_top() method")
        for ap, at in zip(self.atoms, self.top.atoms):
            ap.q = at.charge
            ap.type = at.type
        self.qt = True

    def get_atom_indices(self, selection_string: str = 'all', as_plumed: bool = False, as_ndx: bool = False,
                         from_pdb: Optional[Union[str, "gml.Pdb"]] = None) -> [list, str]:
        """
        Applies a selection to the structure and returns the 0-based indices of selected atoms
        :param selection_string: str, consistent with the selection language syntax (see README)
        :param as_plumed: bool, whether to format as a PLUMED-compatible atom selection
        :param as_ndx: bool, whether to format as an .ndx-compatible atom selection
        :param from_pdb: get these from an external gml.Pdb object
        :return: list of int, 0-based (!!!) indices of atoms, or a formatted string
        """
        if from_pdb is None:
            sel = gml.SelectionParser(self)
            indices = sel(selection_string)
        else:
            pdb = gml.obj_or_str(from_pdb)
            indices = []
            for atom in pdb.atoms:
                chsel = f" and chain {atom.chain}" if atom.chain.strip() else ""
                fullsel = (f'{selection_string} and resid {atom.resnum} and resname {atom.resname} '
                           f'and name {atom.atomname}{chsel}')
                inds = self.get_atom_indices(fullsel)
                if len(inds) == 1:
                    indices.append(inds[0])
                elif len(inds) == 0:
                    print(f"Skipping selection '{fullsel}' as it returned no atoms")
                else:
                    raise RuntimeError(f"Selection {fullsel} returned multiple atoms ({inds}), make sure a combination "
                                       f"of resid + resname + atomname + chain is unique within the structure")
        if not as_plumed and not as_ndx:
            return indices
        elif as_plumed:
            return f"ATOMS={','.join([str(ind + 1) for ind in indices])}"
        elif as_ndx:
            outstr = '[ groupname ]\n'
            for n, ind in enumerate(indices, 1):
                outstr += f'{ind + 1:7d}'
                if n % 10 == 0:
                    outstr += '\n'
            return outstr

    def get_atom_index(self, selection_string) -> int:
        """
        Applies a selection to the structure and returns the 0-based index of the selected atom,
        assuming the selection corresponds to a single unique atom (will throw an error otherwise)
        :param selection_string: str, consistent with the selection language syntax (see README)
        :return: int, 0-based (!!!) index of the selected atom
        """
        sel = gml.SelectionParser(self)
        result = sel(selection_string)
        if len(result) > 1:
            raise RuntimeError("Selection {} returned more than one atom: {}".format(selection_string, result))
        elif len(result) < 1:
            raise RuntimeError("Selection {} returned no atoms".format(selection_string, result))
        return result[0]

    def get_atom(self, selection_string) -> "gml.Atom":
        """
        Works as get_atom_index, but returns an atom instead of a list of indices
        :param selection_string: str, consistent with the selection language syntax (see README)
        :return: an Atom instance, the selected atom
        """
        return self.atoms[self.get_atom_index(selection_string)]

    def get_atoms(self, selection_string) -> list:
        """
        Works as get_atom_indices, but returns a list of atoms instead of a list of indices
        :param selection_string: str, consistent with the selection language syntax (see README)
        :return: a list of Atom instances, the selected atoms
        """
        return [self.atoms[i] for i in self.get_atom_indices(selection_string)]

    def same_residue_as(self, query_iter) -> set:
        """
        Broadens the query to all atoms contained in residues from which atoms were selected
        :param query_iter: iterable of int, indices of the atoms in the query
        :return: set, a broadened list of atom indices
        """
        new_list = []
        for atom in query_iter:
            residue, resid = self.atoms[atom].resname, self.atoms[atom].resnum
            matching = [n for n, a in enumerate(self.atoms) if a.resname == residue and a.resnum == resid]
            new_list.extend(matching)
        return set(new_list)

    def within(self, query_iter: Iterable[int], threshold: float, nopbc: bool = False) -> set:
        """
        Returns a set of all atoms contained within the specified radius of a selection
        :param query_iter: iterable of int, indices of the atoms in the query
        :param threshold: float, a distance within which atoms will be included
        :param nopbc: bool, whether to include PBC in the distance calculation (much faster)
        :return: set, a broadened list of atom indices
        """
        new_list = []
        dist_array = np.array(self.get_coords())
        if nopbc:
            for n in query_iter:
                vecs = np.linalg.norm(dist_array - dist_array[n, :], axis=1)
                new_list.extend(list(np.where(vecs <= threshold)[0]))
        else:
            for n, atom in enumerate(self.atoms):
                if any([self._atoms_dist_pbc(atom, self.atoms[query]) <= threshold for query in query_iter]):
                    new_list.append(n)
        return set(new_list)

    @staticmethod
    def _atoms_dist(at1: "gml.Atom", at2: "gml.Atom") -> float:
        """
        Calculates the (non-PBC-corrected) distance between atoms at1 and at2
        :param at1: Atom, 1st atom defining the distance
        :param at2: Atom, 2nd atom defining the distance
        :return: float, distance
        """
        return np.linalg.norm(at2.coords - at1.coords)

    def _calc_minv(self) -> np.ndarray:
        a = [self.gbox[0] * 10, self.gbox[3] * 10, self.gbox[4] * 10]
        b = [self.gbox[5] * 10, self.gbox[1] * 10, self.gbox[6] * 10]
        c = [self.gbox[7] * 10, self.gbox[8] * 10, self.gbox[2] * 10]
        M = np.column_stack((a, b, c))
        return np.linalg.inv(M)

    def _atoms_dist_pbc(self, at1, at2, ext_box = None) -> float:
        if not self.box[3] == self.box[4] == self.box[5] == 90.0:
            d = self._atoms_vec(at1, at2)
            if ext_box is None:
                a = [self.gbox[0] * 10, self.gbox[3] * 10, self.gbox[4] * 10]
                b = [self.gbox[5] * 10, self.gbox[1] * 10, self.gbox[6] * 10]
                c = [self.gbox[7] * 10, self.gbox[8] * 10, self.gbox[2] * 10]
                M = np.column_stack((a, b, c))
                M_inv = np.linalg.inv(M)
            else:
                M_inv = ext_box
            frac_coords = np.dot(M_inv, d)
            frac_coords_wrapped = frac_coords - np.round(frac_coords)
            d_wrapped = np.dot(M, frac_coords_wrapped) # TODO fix this
            distance = np.linalg.norm(d_wrapped)
            return distance
            # mindist = []
            # for i in [-1, 0, 1]:
            #     for j in [-1, 0, 1]:
            #         for k in [-1, 0, 1]:
            #             mindist.append(sum([(d[x] + a[x] * i + b[x] * j + c[x] * k) ** 2 for x in range(3)]) ** 0.5)
            # return min(mindist)
        else:
            # pos1 = np.array([at1.x, at1.y, at1.z])
            # pos2 = np.array([at2.x, at2.y, at2.z])
            # box_lengths = np.array([self.box[0], self.box[1], self.box[2]])
            # delta = pos2 - pos1
            # delta -= box_lengths * np.round(delta / box_lengths)
            # distance = np.linalg.norm(delta)
            # return distance
            return (min([abs(at2.x - at1.x), self.box[0] - abs(at2.x - at1.x)]) ** 2 +
                    min([abs(at2.y - at1.y), self.box[1] - abs(at2.y - at1.y)]) ** 2 +
                    min([abs(at2.z - at1.z), self.box[2] - abs(at2.z - at1.z)]) ** 2) ** 0.5

    @staticmethod
    def _atoms_vec(at1: "gml.Atom", at2: "gml.Atom") -> np.array:
        """
        Calculates the vector between two vectors (ignoring PBC)
        :param at1: gml.Atom, first atom
        :param at2: gml.Atom, second atom
        :return: np.array, array with 3 components (X Y Z)
        """
        return np.array([at2.x - at1.x, at2.y - at1.y, at2.z - at1.z])

    def _atoms_vec_pbc(self, at1: "gml.Atom", at2: "gml.Atom") -> np.array:
        """
        Calculates the vector between two vectors (including PBC)
        :param at1: gml.Atom, first atom
        :param at2: gml.Atom, second atom
        :return: np.array, array with 3 components (X Y Z)
        """
        a = [self.gbox[0] * 10, self.gbox[3] * 10, self.gbox[4] * 10]
        b = [self.gbox[5] * 10, self.gbox[1] * 10, self.gbox[6] * 10]
        c = [self.gbox[7] * 10, self.gbox[8] * 10, self.gbox[2] * 10]
        d = self._atoms_vec(at1, at2)
        vecs = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    vecs.append([(d[x] + a[x] * i + b[x] * j + c[x] * k) for x in range(3)])
        return np.array([min([v[0] for v in vecs], key=lambda x: abs(x)),
                         min([v[1] for v in vecs], key=lambda x: abs(x)),
                         min([v[2] for v in vecs], key=lambda x: abs(x))])

    @staticmethod
    def _parse_contents(contents: list, qt: bool) -> tuple:
        """
        A parser to extract data from .pdb files
        and convert them to internal parameters
        :param contents: list of str, contents of the .pdb file
        :param qt: bool, whether the .pdb contains extra charge/type columns
        :return: (list of Atom instances, tuple of floats of len 6, list of str)
        """
        atoms, remarks, conect = [], [], {}
        box = [75, 75, 75, 90, 90, 90]  # generic default, will be overwritten if present
        for line in contents:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                atoms.append(Atom(line, qt))
            elif line.startswith("CRYST1"):
                try:
                    box = [float(line[6 + 9 * a:6 + 9 * (a + 1)]) for a in range(3)] + \
                          [float(line[33 + 7 * a:33 + 7 * (a + 1)]) for a in range(3)]
                except ValueError:
                    print(f"Couldn't read box size correctly from line: {line}, setting dummy box size")
            elif not line.startswith('TER') and not line.startswith('END') and line.strip():
                remarks.append(line)
            elif line.startswith('CONECT'):
                conect[int(line[6:11].strip())] = []
                for i in [11, 16, 21, 26]:
                    if line[i:i + 5].strip():
                        conect[int(line[6:11].strip())].append(int(line[i:i + 5].strip()))
            if line.startswith('END') or line.startswith('ENDMDL'):
                break
        return atoms, tuple(box), remarks

    def remove_hydrogens(self) -> None:
        """
        Uses the standard naming convention (see Pdb.add_elements()
        to identify and remove hydrogen atoms
        :return: None
        """
        self.add_elements()
        new_list = [a for a in self.atoms if a.element != 'H']
        self.atoms = new_list
        self.reindex()

    def mutate_protein_residue(self, resid: int, target: str, chain: Optional[str] = '') -> None:
        """
        Mutates a chosen residue to a different one (in a standard rotameric state)
        :param resid: int, number of the residue to be mutated
        :param target: str, single-letter code of the residue to be mutated
        :param chain: str, optional name of the chain
        :return: None
        """
        self.renumber_atoms()
        chstr = 'chain {} and '.format(chain) if chain else ''
        orig = self.get_atom('{}resid {} and name CA'.format(chstr, resid))
        mutant = gml.ProteinMutant(orig.resname, target)
        mutant.check_chiral(self, orig)
        atoms_add, hooks, geo_refs, bond_lengths, _, afters = mutant.atoms_to_add()
        atoms_remove = mutant.atoms_to_remove()
        for at in atoms_remove:
            equivalents = {'OG': 'OG1', 'HG': 'HG1', 'HG1': 'HG11', 'HG2': 'HG12', 'HG3': 'HG13', 'CG': 'CG1',
                           'CD': 'CD1', 'HD': 'HD1', 'HD1': ['HD11', 'HE2'], 'HD2': 'HD12', 'HD3': 'HD13', 'H': 'HN'}
            print("Removing atom {} from resid {} in structure".format(at, resid))
            atnum = None
            try:
                atnum = self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, at))
            except RuntimeError:
                equivs = equivalents[at] if isinstance(equivalents[at], list) else [equivalents[at]]
                for equiv in equivs:
                    try:
                        atnum = self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, equiv))
                    except RuntimeError:
                        continue
                    else:
                        break
                else:
                    if atnum is None:
                        raise RuntimeError(f"Couldn't find any of the following: {at}, {', '.join(equivs)}")
            _ = self.atoms.pop(atnum)
        for atom_add, hook, geo_ref, bond_length, aft in zip(atoms_add, hooks, geo_refs, bond_lengths, afters):
            print("Adding atom {} to resid {} in structure".format(atom_add, resid))
            for n in range(len(geo_ref)):
                if isinstance(geo_ref[n], tuple):
                    for i in geo_ref[n]:
                        try:
                            self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, i))
                        except RuntimeError:
                            continue
                        else:
                            geo_ref[n] = i
                            break
            if isinstance(hook, tuple):
                for hk in hook:
                    try:
                        _ = self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, hk))
                    except RuntimeError:
                        continue
                    else:
                        hook = hk
                        break
            hooksel = '{}resid {} and name {}'.format(chstr, resid, hook)
            aftnr = None
            # TODO add unittest to check we're inserting correctly
            if isinstance(aft, tuple):
                for n, af in enumerate(aft):
                    try:
                        _ = self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, af))
                    except RuntimeError:
                        continue
                    else:
                        aftnr = self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, af))
                        break
                else:
                    if aftnr is None:
                        raise RuntimeError(f"Didn't find any of the atoms: {aft} in residue {resid}")
            else:
                aftnr = self.get_atom_index('{}resid {} and name {}'.format(chstr, resid, aft))
            if len(geo_ref) == 2:
                p1sel = '{}resid {} and name {}'.format(chstr, resid, geo_ref[0])
                p2sel = '{}resid {} and name {}'.format(chstr, resid, geo_ref[1])
                self.insert_atom(aftnr + 2, name=atom_add, hooksel=hooksel,
                                 bondlength=bond_length,
                                 p1_sel=p1sel, p2_sel=p2sel, atomname=atom_add, resname=mutant.target_3l)
            else:
                vec = self._vector(geo_ref, resid, chain)
                self.insert_atom(aftnr + 2, name=atom_add, hooksel=hooksel,
                                 bondlength=bond_length,
                                 vector=vec, atomname=atom_add, resname=mutant.target_3l)
        self.renumber_atoms()
        prot_resids = list(self.prot_map.keys())
        processed_residue = self.get_atoms(f'{chstr}resid {resid} and resname {" ".join(prot_resids)}')
        for atom in processed_residue:
            atom.resname = mutant.target_3l
        self.reindex()

    def _vector(self, atnames: list, resid: int, chain: Optional[str], nopbc: bool = False) -> np.array:
        """
        Defines a vector based on a number of atoms within a residue. There are 2 cases:
        (a) if 3 atoms are passed, the vector will be defining a missing 4th atom in an sp2 arrangement,
            assuming the 1st atom passed is the center of the triangle
        (b) if 2 or 4+ atoms are passed, the 1st atom is assumed to be the reference, and vectors to all
            the other atoms will be simply added
        :param atnames: list of str, names of the atoms
        :param resid: int, number of the residue
        :param chain: str, can be used to narrow down the selection to a particular chain
        :param nopbc: bool, whether to ignore PBC in calculating vectors
        :return:
        """
        chstr = 'chain {} and '.format(chain) if chain else ''
        atoms = [self.get_atom('{}resid {} and name {}'.format(chstr, resid, at)) for at in atnames]
        if nopbc:
            vecs = [self._atoms_vec(atoms[0], at2) for at2 in atoms[1:]]
        else:
            vecs = [self._atoms_vec_pbc(atoms[0], at2) for at2 in atoms[1:]]
        nv = len(vecs)
        f = -1 if nv == 3 else 1
        return np.array([f * sum(v[0] for v in vecs) / nv, f * sum(v[1] for v in vecs) / nv, f * sum(v[2] for v in vecs) / nv])

    def add_vsn(self, resid: int, name: str, vsname: str = 'Vn', serial: Optional[int] = None,
                chain: Optional[str] = None) -> None:
        """
        Adds a virtual site (VS) on top of another atom, useful for Go-models
        :param resid: int, number of the residue that will contain the VS
        :param name: str, atom to use for the construction of the VS
        :param vsname: str, name of the new virtual site
        :param serial: int, where to locate the new VS in the atomlist
        :param chain: str, additional specification to identify the atoms
        :return: None
        """
        chsel = f' and chain {chain}' if chain is not None else ''
        serial = self.get_atoms(f"resid {resid}{chsel}")[-1].serial + 2 if serial is None else serial
        self.insert_atom(serial, name=vsname, hooksel=f"resid {resid} and name {name}{chsel}",
                         bondlength=0, vector=[0, 0, 0], atomname=vsname)
        self.reindex()

    def add_vs2(self, resid: int, name1: str, name2: str, vsname: str = 'V1', fraction: float = 0.5,
                serial: Optional[int] = None, chain: Optional[str] = None) -> None:
        """
        Adds a virtual site (VS) defined by two atoms, interpolating between
        their coordinates
        :param resid: int, number of the residue that will contain the VS
        :param name1: str, 1st atom to use for the construction of the VS
        :param name2: str, 2nd atom to use for the construction of the VS
        :param vsname: str, name of the new virtual site
        :param fraction: float, where to put the VS (0 = on atom 1, 1 = on atom 2, can be interpolated or extrapolated)
        :param serial: int, where to locate the new VS in the atomlist
        :param chain: str, additional specification to identify the atoms
        :return: None
        """
        # TODO also add in topology?
        chsel = f' and chain {chain}' if chain is not None else ''
        serial = self.get_atoms(f"resid {resid}{chsel}")[-1].serial + 2 if serial is None else serial
        a1 = self.get_atom(f"resid {resid} and name {name1}{chsel}")
        a2 = self.get_atom(f"resid {resid} and name {name2}{chsel}")
        dist = self._atoms_dist_pbc(a1, a2)
        self.insert_atom(serial, name=vsname, hooksel=f"resid {resid} and name {name1}{chsel}",
                         bondlength=dist * fraction, p1_sel=f"resid {resid} and name {name1}{chsel}",
                         p2_sel=f"resid {resid} and name {name2}{chsel}", atomname=vsname)
        self.reindex()

    def add_vs3out(self, resid: int, name1: str, name2: str, name3: str, vsname: str = 'V3', a: float = 0.0,
                   b: float = 0.0, c: float = 1.5, serial: Optional[int] = None, chain: Optional[str] = None,
                   resid2: Optional[int] = None, resid3: Optional[int] = None, add_in_top: bool = True) -> None:
        """
        Adds an out-of-plane virtual site (VS) defined by three atoms, using a cross-product between
        two vectors defined by three atoms (i,j) and (i,k)
        :param resid: int, number of the residue that will contain the VS
        :param name1: str, 1st atom to use for the construction of the VS
        :param name2: str, 2nd atom to use for the construction of the VS
        :param name3: str, 3rd atom to use for the construction of the VS
        :param vsname: str, name of the new virtual site
        :param a: float, first parameter used to construct the site
        :param b: float, second parameter used to construct the site
        :param c: float, third parameter used to construct the site, or out-of-plane distance (in nm)
        :param serial: int, where to locate the new VS in the atomlist
        :param chain: str, additional specification to identify the atoms
        :param resid2: int, if atom 2 is from a different residue, specify here
        :param resid3: int, if atom 3 is from a different residue, specify here
        :param add_in_top: bool, whether to add the VS in the associated topology
        :return: None
        """
        chsel = f' and chain {chain}' if chain is not None else ''
        a1 = self.get_atom(f"resid {resid} and name {name1}{chsel}")
        serial = a1.serial + 1 if serial is None else serial
        a2 = self.get_atom(f"resid {resid if resid2 is None else resid2} and name {name2}{chsel}")
        a3 = self.get_atom(f"resid {resid if resid3 is None else resid3} and name {name3}{chsel}")
        v1 = self._atoms_vec(a1, a2)
        v2 = self._atoms_vec(a1, a3)
        v3 = self._cross_product(v1, v2)
        n1 = self._normalize(v3)
        vec = [a * vv1 + b * vv2 + 10*c * nn1 for vv1, vv2, nn1 in zip(v1, v2, n1)]
        if self.top and add_in_top:
            self.top.parameters.add_dummy_def('MW')
            mol = self._match_top_molecule(serial)
            mol.add_vs3out(serial, a1.serial, a2.serial, a3.serial, a, b, c, vsname, 'MW')
        self.insert_atom(serial, name=vsname, hooksel=f"resid {resid} and name {name1}{chsel}",
                         vector=vec, atomname=vsname, bondlength=float(np.linalg.norm(vec)))
        self.reindex()

    def interatomic_dist(self, resid1: int = 1, resid2: int = 2) -> list:
        """
        Calculates all distances between atoms in two selected residues
        :param resid1: int, 1st residue to consider
        :param resid2: int, 2nd residue to consider
        :return: list of float, all calculated interatomic distances
        """
        dists = []
        for atom1 in self.get_atoms(f"resid {resid1}"):
            for atom2 in self.get_atoms(f"resid {resid2}"):
                dists.append(self._atoms_dist_pbc(atom1, atom2))
        return dists

    def check_chiral_aa(self, nopbc: bool = False, fix: bool = False) -> None:
        """
        Checks for correct chirality in amino acids, first in the backbone
        and then for chiral side chains; to work with "fix", the last one has to be
        a hydrogen
        :param nopbc: bool, whether to ignore PBC information
        :param fix: bool, whether to try fixing chirality by switching the position of the hydrogen
        :return: None
        """
        # TODO check for GLY (consistent between HA1 and HA2)?
        prot_atoms = self.get_atoms('name CA and not resname GLY')
        self.check_chiral(prot_atoms, 'N', 'C', 'HA HA1', nopbc=nopbc, fix=fix)
        ile_atoms = self.get_atoms('name CB and resname ILE')
        self.check_chiral(ile_atoms, 'CG2', 'CA', 'HB', 'side chain chirality', nopbc=nopbc, fix=fix)
        thr_atoms = self.get_atoms('name CB and resname THR')
        self.check_chiral(thr_atoms, 'CG1 CG2', 'CA', 'HB', 'side chain chirality', nopbc=nopbc, fix=fix)

    def check_chiral(self, cent_atoms_list: list, at1: str, at2: str, at3: str,
                     label: str = 'backbone chirality', printing: bool = True, nopbc: bool = False, fix: bool = False,
                     values_only: bool = False) -> bool:
        """
        Decides on correct or wrong chirality of selected chiral
        centers by calculating selected dihedrals
        :param cent_atoms_list: list of Atom instances, central atoms around which to check chirality
        :param at1: str, name of the 1st surrounding atom
        :param at2: str, name of the 2nd surrounding atom
        :param at3: str, name of the 3rd surrounding atom
        :param label: str, type of chirality (only to display in the warning)
        :param printing: bool, whether to print warnings (default) or return True if all checks are passed
        :param nopbc: bool, whether to ignore PBC when calculating vectors
        :param fix: bool, whether to try fixing chirality by switching the position of the hydrogen
        :param values_only: prints the values of the arbitrarily defined dihedral to spot outliers
        :return: None (if printing), bool (if not printing)
        """
        for at in cent_atoms_list:
            resnum, resname, chain = at.resnum, at.resname, at.chain
            chn = ' and chain ' + chain if chain.strip() else ''
            n = self.get_atom(f'name {at1} and resnum {resnum} and resname {resname} {chn}')
            c = self.get_atom(f'name {at2} and resnum {resnum} and resname {resname} {chn}')
            h = self.get_atom(f'name {at3} and resnum {resnum} and resname {resname} {chn}')
            chi = self._get_chirality([n, c, h, at], nopbc)
            if chi < -0.9 or 0 > chi > -0.35:
                if values_only:
                    print(chi)
                    continue
                if printing:
                    print(f"Check {label} for residue {resname} num {resnum}, looks a bit off")
                else:
                    return False
            elif chi > 0:
                if values_only:
                    print(chi)
                    continue
                if fix:
                    self.fix_chirality(h_sel=f'name {at3} and resnum {resnum} and resname {resname} {chn}',
                                       c_sel=f'name {at.atomname} and resnum {resnum} and resname {resname} {chn}')
                    print(f"Trying to fix chirality for residue {resname} num {resnum} by moving {at3} to the opposite "
                          f"side of {at.atomname}, run a minimization and check again")
                if printing and not fix:
                    print(f"Check {label} for residue {resname} num {resnum}, looks like a D-form")
                if not printing:
                    return False
            if not printing:
                return True

    def fix_chirality(self, h_sel: str, c_sel: str) -> None:
        """
        A quick-and-dirty chirality fix that moves the hydrogen to the
        opposite side of the carbon atom (needs minimization afterwards)
        :param h_sel: str, selection that returns the hydrogen atom to be moved
        :param c_sel: str, selection that returns the carbon atom bound to that hydrogen
        :return: None
        """
        self.reposition_atom_from_hook(h_sel, c_sel, 1.09, h_sel, c_sel)

    def _get_chirality(self, atomlist: list, nopbc: bool = False) -> float:
        """
        Calculates a dihedral defined by 4 atoms that
        constitute a chiral center
        :param atomlist: list of len 4, atoms defining the chiral center
        :param nopbc: bool, whether to ignore PBC when calculating vectors
        :return: float, the dihedral's value
        """
        if nopbc:
            v1 = self._atoms_vec(atomlist[0], atomlist[1])
            v2 = self._atoms_vec(atomlist[1], atomlist[2])
            v3 = self._atoms_vec(atomlist[2], atomlist[3])
        else:
            v1 = self._atoms_vec_pbc(atomlist[0], atomlist[1])
            v2 = self._atoms_vec_pbc(atomlist[1], atomlist[2])
            v3 = self._atoms_vec_pbc(atomlist[2], atomlist[3])
        n1 = self._normalize(self._cross_product(v1, v2))
        n2 = self._normalize(self._cross_product(v2, v3))
        m1 = self._normalize(self._cross_product(n1, self._normalize(v2)))
        x = self._scalar_product(n1, n2)
        y = self._scalar_product(m1, n2)
        return math.atan2(y, x)

    def dihedral(self, dihname: str) -> list:
        """
        Returns indices corresponding to a dihedral when prompted with a query
        in a format @dihname-resid, e.g. @chi-1 (following Plumed's convention)
        :param dihname: str, query
        :return: list of 4 ints, atom indices corresponding to the dihedral
        """
        name, resid = dihname.strip('@').split('-')
        dihs = {'phi': (), 'psi': (), 'alpha': ("O3'-", "P", "O5'", "C5'"), 'beta': (("P", "H5T"), "O5'", "C5'", "C4'"),
                'gamma': ("O5'", "C5'", "C4'", "C3'"), 'delta': ("C5'", "C4'", "C3'", "O3'"),
                'epsilon': ("C4'", "C3'", "O3'", ("H3T", "P+")), 'zeta': ("C3'", "O3'", "P+", "O5'+"),
                'chi': ("O4'", "C1'", "NX", "CX"), 'nu0': ("C4'", "O4'", "C1'", "C2'"),
                'nu1': ("O4'", "C1'", "C2'", "C3'"), 'nu2': ("C1'", "C2'", "C3'", "C4'"),
                'nu3': ("C2'", "C3'", "C4'", "O4'"), 'nu4': ("C3'", "C4'", "O4'", "C1'"),
                'kappa': ("C3'", "C2'", "O2'", "HO'2")}
        namelist = dihs[name]
        indices = []
        for atomname in namelist:
            selection = ''
            if isinstance(atomname, tuple):
                for option in atomname:
                    modname = option.strip('-+')
                    resmod = 1 if option.endswith('+') else -1 if option.endswith('-') else 0
                    selection += f'(resid {int(resid)+resmod} and name {modname}) or '
                selection = selection[:-4]  # trim the last "or"
            else:
                resmod = 1 if atomname.endswith('+') else -1 if atomname.endswith('-') else 0
                if name == 'chi' and atomname.endswith('X'):
                    resname = self.atoms[indices[0]].resname
                    if any([i in resname for i in 'UTC']):
                        if atomname.startswith('C'):
                            modname = 'C2'
                        elif atomname.startswith('N'):
                            modname = 'N1'
                    else:
                        if atomname.startswith('C'):
                            modname = 'C4'
                        elif atomname.startswith('N'):
                            modname = 'N9'
                else:
                    modname = atomname
                modname = modname.strip('-+')
                selection = f'resid {int(resid)+resmod} and name {modname}'
            indices.append(self.get_atom_index(selection))
        return indices

    @staticmethod
    def _cross_product(v1: Sequence[float], v2: Sequence[float]) -> np.array:
        """
        Calculates a cross product between two vectors
        :param v1: iterable of floats, len 3
        :param v2: iterable of floats, len 3
        :return: list, vector of length 3
        """
        return np.cross(v1, v2)

    @staticmethod
    def _scalar_product(v1: Sequence[float], v2: Sequence[float]) -> float:
        """
        Calculates a dot product between two vectors
        :param v1: iterable of floats, len 3
        :param v2: iterable of floats, len 3
        :return: float
        """
        return np.dot(v1, v2)

    @staticmethod
    def _normalize(v: np.array) -> np.array:
        """
        Normalizes a vector
        :param v: iterable of floats, len 3
        :return: list, vector of length 3
        """
        return v / np.linalg.norm(v)

    @staticmethod
    def _parse_contents_gro(contents: list) -> tuple:
        """
        A parser to extract data from .gro files
        and convert them to internal parameters
        :param contents: list of str, contents of the .gro file
        :return: (list of Atom instances, tuple of floats of len 6, list of str)
        """
        contents = [x for x in contents if x.strip()]
        atoms, remarks = [], []
        header = contents[0]
        remarks.append("TITLE     {}".format(header))
        natoms = int(contents[1])
        for line in contents[2:2 + natoms]:
            atoms.append(Atom.from_gro(line, index=len(atoms)))
        if len(contents[-1].split()) == 3:
            box = [10 * float(x) for x in contents[-1].split()] + [90., 90., 90.]
        elif len(contents[-1].split()) == 9:
            boxline = [float(x) for x in contents[-1].split()]
            assert boxline[3] == boxline[4] == boxline[6] == 0
            box = [0.0] * 6
            box[0] = boxline[0]
            box[-1] = math.atan(boxline[1] / boxline[5]) if boxline[5] != 0 else 90
            box[1] = boxline[1] / math.sin(box[-1] * math.pi / 180)
            box[2] = math.sqrt(boxline[7] ** 2 + boxline[8] ** 2 + boxline[2] ** 2)
            box[-2] = math.acos(boxline[7] / box[2])
            box[-3] = math.acos((boxline[8] * math.sin(box[-1] * math.pi / 180)) / box[2]
                                + math.cos(box[-2]) * math.cos(box[-1] * math.pi / 180))
            box[0], box[1], box[2] = box[0] * 10, box[1] * 10, box[2] * 10
            box[3], box[4], box[5] = round(box[3] * 180 / math.pi, 4), round(box[4] * 180 / math.pi, 4), round(box[5],
                                                                                                               4)
        else:
            raise RuntimeError('Can\'t read box properties')
        return atoms, tuple(box), remarks

    @staticmethod
    def _parse_contents_cif(contents: list) -> tuple:
        """
        A parser to extract data from .cif files
        and convert them to internal parameters
        :param contents: list of str, contents of the .gro file
        :return: (list of Atom instances, tuple of floats of len 6, list of str)
        """
        contents = [x for x in contents if x.strip() if x.startswith('ATOM') or x.startswith('HETATM')]
        atoms, remarks = [], []
        for line in contents:
            atoms.append(Atom.from_cif(line, index=len(atoms)))
        # TODO look into reading box?
        box = [75, 75, 75] + [90., 90., 90.]
        return atoms, tuple(box), remarks

    def make_term(self, term_type: str, atom_serial: int) -> None:
        """
        For introducing protein chain breaks, this adds terminal atoms to N- and C-terminal residues
        :param term_type: str, "C" or "N" for the type of the terminus
        :param atom_serial: int, the atom that defines the split
        :return: None
        """
        if term_type not in ["C", "N"]:
            raise RuntimeError(f"term_type has to be either 'C' or 'N', '{term_type}' was passed")
        atom = self.get_atom(f'serial {atom_serial}')
        if term_type == "C":
            self.insert_atom(atom.serial + 2, name='OX', hooksel=f'serial {atom_serial}', bondlength=1.25,
                             vector=self._vector(['C', 'O', 'CA', 'C'], atom.resnum, atom.chain))
        else:
            hname = self.get_atom(f'serial {atom_serial + 1}').atomname
            self.insert_atom(atom.serial + 2, name='H2', hooksel=f'serial {atom_serial}', bondlength=0.95,
                             vector=self._vector(['N', hname, 'CB', 'N'], atom.resnum, atom.chain))
            self.insert_atom(atom.serial + 3, name='H3', hooksel=f'serial {atom_serial}', bondlength=0.95,
                             vector=self._vector(['N', hname, 'HA', 'N'], atom.resnum, atom.chain))
        self.reindex()

    def add_conect(self, cutoff: float = 2.05, cutoff_h: float = 1.3, pbc: bool = False) -> None:
        """
        Adds CONECT entries to the PDB, using the value of
        cutoff to determine molecule connectivity
        :param cutoff: float, cut-off to determine atom bonding patterns
        :param cutoff_h: float, cut-off to determine atom bonding patterns with hydrogens
        :param pbc: bool, whether to account for periodic boundary conditions when calculating distances
        :return: None
        """
        # TODO if top present, take bonds from there
        self.add_elements()
        if pbc:
            self._conect_simple(cutoff, cutoff_h, pbc)
            return
        hs = self.get_atom_indices('element H')
        coords = np.array(self.get_coords())
        for n, atom in enumerate(self.atoms):
            dists = np.linalg.norm(coords - np.array(atom.coords), axis=1)
            if n not in hs:
                selected = [self.atoms[i].serial for i in
                            list(np.where(np.logical_and(dists < cutoff, dists > 0.1))[0]) if i not in hs]
                selected_h = [self.atoms[i].serial for i in
                              list(np.where(np.logical_and(dists < cutoff_h, dists > 0.1))[0])
                              if i in hs]
                self.conect[atom.serial] = selected + selected_h
            else:
                selected_h = [self.atoms[i].serial for i in
                              list(np.where(np.logical_and(dists < cutoff_h, dists > 0.1))[0])]
                self.conect[atom.serial] = selected_h

    def _conect_simple(self, cf1: float, cf2: float, pbc: bool) -> None:
        hs = self.get_atom_indices('element H')
        for n, atom in enumerate(self.atoms):
            if pbc:
                dists = [self._atoms_dist(atom, at) for at in self.atoms]
            else:
                dists = [self._atoms_dist_pbc(atom, at) for at in self.atoms]
            if n not in hs:
                selected = [self.atoms[m].serial for m, a in enumerate(dists) if 0.1 < a < cf1 and m not in hs]
                selected_h = [self.atoms[m].serial for m, a in enumerate(dists) if 0.1 < a < cf2 and m in hs]
                self.conect[atom.serial] = selected + selected_h
            else:
                selected = [self.atoms[m].serial for m, a in enumerate(dists) if 0.1 < a < cf2]
                self.conect[atom.serial] = selected

    def set_beta(self, values: Sequence, selection: str = None, smooth: Optional[float] = None,
                 ignore_mem: bool = False, set_occupancy: bool = False) -> None:
        """
        Enables user to write arbitrary values to the beta field
        of the PDB entry
        :param values: iterable; values to fill
        :param selection: str, optional; can be used to specify a subset of atoms
        :param smooth: if float, defines sigma (in Angstrom) for beta-value smoothing
        :param ignore_mem: bool, allows to ignore memory warnings
        :param set_occupancy: bool, instead write to the "Occupancy" column (allows to hold two different datasets)
        :return: None
        """
        if any([v > 999 for v in values]):
            print("At least one value is too large to fit into the `beta` field, consider division "
                  "to make values smaller")
        atoms = self.atoms if selection is None else self.get_atoms(selection)
        if len(values) != len(atoms):
            raise ValueError("Lists 'value' and 'serials' have inconsistent sizes: {} and {}".format(len(values),
                                                                                                     len(atoms)))
        index = 0
        if smooth is None:
            for atom in atoms:
                if not set_occupancy:
                    atom.beta = values[index]
                else:
                    atom.occ = values[index]
                index += 1
        else:
            if len(atoms) > 10000 and not ignore_mem:
                raise RuntimeError("Try to restrict the number of atoms (e.g. selecting CA only), or you're risking "
                                   "running out of memory. To proceed anyway, run again with ignore_mem=True")
            values = np.array(values)
            atomnums = [n for n, atom in enumerate(self.atoms) if atom in atoms]
            coords = np.array(self.get_coords())[atomnums]
            for atom in self.atoms:
                dists = np.linalg.norm(coords - np.array(atom.coords), axis=1)
                weights = np.exp(-(dists ** 2 / (2 * smooth)))
                weights /= np.sum(weights)
                if not set_occupancy:
                    atom.beta = np.sum(values * weights)
                else:
                    atom.occ = values[index]

    def get_beta(self, selection: str = None, get_occupancy: bool = False) -> np.array:
        """
        Returns an array of beta factors (or occupancies) corresponding to a selection
        :param selection: str, selection for which to return values
        :param get_occupancy: bool, if true then returns occupancies rather than betas
        :return: np.array, an array of corresponding values of size len_selection
        """
        if selection is None:
            if not get_occupancy:
                return np.array([a.beta for a in self.atoms])
            else:
                return np.array([a.occ for a in self.atoms])
        else:
            if not get_occupancy:
                return np.array([a.beta for a in self.get_atoms(selection)])
            else:
                return np.array([a.occ for a in self.get_atoms(selection)])

    def translate_selection(self, selection: str = 'all', vector: Sequence = (0, 0, 0)) -> None:
        """
        Translates a subset of atoms defined by the selection by a specified vector in 3D space
        :param selection: str, selection that will be moved
        :param vector: iterable of 3 floats, vector specifying the translation
        :return: None
        """
        if len(vector) != 3:
            raise RuntimeError("Please specify a 3-component vector")
        for atom in self.get_atoms(selection):
            atom.x += vector[0]
            atom.y += vector[1]
            atom.z += vector[2]

    def interpolate_struct(self, other: "gml.Pdb", num_inter: int, write: bool = False) -> Union[None, "gml.Traj"]:
        """
        Generates linearly & equally spaced intermediates between two structures,
        the current (self) and another PDB with the same number of atoms
        :param other: Pdb instance, other endpoint to interpolate between
        :param num_inter: int, number of intermediate structures
        :param write: bool, whether to save the intermediates as separate .pdb files (True) or just return them (False)
        :return: None (if write=True) or list of Pdb instances (if write=False)
        """
        inter = []
        self_atoms = np.array(self.get_coords())
        other_atoms = np.array(other.get_coords())
        for i in range(1, num_inter + 1):
            incr = (other_atoms - self_atoms) / (num_inter + 1)
            pdb = deepcopy(self)
            pdb.set_coords(self_atoms + i * incr)
            inter.append(pdb)
        if write:
            for n, struct in enumerate([self] + inter + [other]):
                struct.save_pdb(f'interpolated_structure_{n}.pdb')
            return
        else:
            return gml.Traj([self] + inter + [other])

    def save_pdb(self, outname: str = 'out.pdb', add_ter: bool = False) -> None:
        """
        Saves the structure in the PDB format
        :param outname: str, name of the file being produced
        :param add_ter: bool, whether to add TER entries (required by some downstream protocols)
        :return: None
        """
        with open(outname, 'w') as outfile:
            outfile.write(self._cryst_format.format(*self.box))
            for line in self.remarks:
                outfile.write(line.strip() + '\n')
            for n, atom in enumerate(self.atoms):
                outfile.write(self._write_atom(atom))
                if add_ter and n < self.natoms - 1 and atom.chain != self.atoms[n + 1].chain:
                    outfile.write(self._ter_format.format(atom.serial, atom.resname, atom.chain, atom.resnum))
            for conect in self.conect.keys():
                outfile.write(self._write_conect(conect, self.conect[conect]))
            outfile.write('END\n')

    def reindex(self):
        for n, a in enumerate(self.atoms):
            a.index = n

    def save_xyz(self, outname: str = 'out.xyz') -> None:
        """
        Saves the structure in the PDB format
        :param outname: str, name of the file being produced
        :return: None
        """
        self.add_elements()
        with open(outname, 'w') as outfile:
            outfile.write(str(len(self.atoms)) + '\n')
            outfile.write('written by gromologist\n')
            for atom in self.atoms:
                outfile.write(f' {atom.element} {atom.x} {atom.y} {atom.z}\n')

    def save_from_selection(self, selection: str, outname: str = 'out.pdb', renum: bool = False,
                            atom_indices: Optional[list] = None) -> None:
        """
        Saves a .pdb of a subset corresponding to a selection
        :param selection: str, a selection compatible with the gromologist selection language
        :param outname: str, name of the output file
        :param renum: bool, whether to renumber atoms in the new structure
        :return: None
        """
        pdb = self.from_selection(selection, atom_indices)
        if renum:
            pdb.renumber_atoms()
        pdb.save_pdb(outname)

    def save_gro(self, outname: str = 'out.gro') -> None:
        """
        Saves the structure in the GRO format
        :param outname: str, name of the file being produced
        :return: None
        """
        with open(outname, 'w') as outfile:
            outfile.write("written by gromologist\n{}\n".format(len(self.atoms)))
            for atom in self.atoms:
                outfile.write(self._write_atom(atom, pdb=False))
            gbox = self._calc_gro_box()
            if sum([x ** 2 for x in gbox[3:]]) > 0:
                outfile.write((9 * "{:10.5f}" + "\n").format(*gbox))
            else:
                outfile.write((3 * "{:10.5f}" + "\n").format(*gbox[:3]))

    def _calc_gro_box(self) -> list:
        """
        Converter function to the matrix-based .gro box definition
        :return: list of float, matrix entries
        """
        if self.box[3] == self.box[4] == self.box[5] == 90.0:
            return [x / 10 for x in self.box[:3]] + 6 * [0.0]
        else:
            gbox = 9 * [0.0]
            conv = math.pi / 180
            gbox[0] = self.box[0] / 10
            gbox[1] = self.box[1] / 10 * math.sin(self.box[5] * conv)
            gbox[7] = self.box[2] / 10 * math.cos(self.box[4] * conv)
            gbox[8] = self.box[2] / 10 * (math.cos(self.box[3] * conv) - math.cos(self.box[4] * conv) * math.cos(
                self.box[5] * conv)) / math.sin(self.box[5] * conv)
            gbox[2] = math.sqrt(self.box[2] * self.box[2] / 100 - gbox[7] * gbox[7] - gbox[8] * gbox[8])
            gbox[5] = self.box[1] / 10 * math.cos(self.box[5] * conv)
            return gbox

    def get_coords(self, selection: Optional[str] = None) -> np.array:
        """
        Returns all atomic coordinates
        :param selection: str, selection for the coordinates to be retreived
        :return: list of list of float, coordinates of all atoms
        """
        if selection is not None:
            subset = self.get_atom_indices(selection)
            return np.array([[a.x, a.y, a.z] for a in [self.atoms[q] for q in subset]])
        else:
            return np.array([[a.x, a.y, a.z] for a in self.atoms])

    def set_coords(self, new_coords: Iterable, selection: Optional[str] = None) -> None:
        """
        Sets all atomic coordinates
        :param new_coords: list of list of int, new coordinates to be set
        :param selection: str, selection for the coordinates to be retreived
        :return: None
        """
        atoms = self.atoms if selection is None else self.get_atoms(selection)
        assert len(new_coords) == len(atoms)
        for atom, coords in zip(atoms, new_coords):
            assert len(coords) == 3
            atom.x, atom.y, atom.z = coords


class Residue:
    def __init__(self, pdb: "gml.Pdb", id: int, name: str, chain: str = ''):
        self.pdb = pdb
        self.id = id
        self.name = name
        self.chain = chain

    @property
    def selection(self) -> str:
        """
        Returns a selection that selects this residue
        :return: str, text of the selection
        """
        chainsel = f'and chain {self.chain}' if self.chain.strip() else ''
        return f'resid {self.id} and resname {self.name} {chainsel}'

    @property
    def atoms(self) -> list:
        """
        Returns a list of gml.Atom objects that are part of this residue
        :return: list of gml.Atom objects
        """
        return self.pdb.get_atoms(self.selection)

    @property
    def structure(self) -> "gml.Pdb":
        """
        Returns the whole PDB to which the residue is bound
        :return: gml.Pdb
        """
        return self.pdb

    def gen_pdb(self) -> "gml.Pdb":
        """
        Generates a PDB that only contains this residue
        :return: gml.Pdb with the isolated residue
        """
        return Pdb.from_selection(self.pdb, self.selection)

    def __repr__(self) -> str:
        return f'{self.name}{self.id}{self.chain.strip()}'

    def __str__(self) -> str:
        return f'{self.name}{self.id}{self.chain.strip()}'


class Atom:
    def __init__(self, line: str, index: int, qt: bool = False):
        """
        Represents a single atom contained in the structure file
        :param line: str, line from the structure file
        :param qt: bool, whether there are extra charge (q) and type (t) fields at the end
        """
        self.label = line[:6].strip()
        self.index = index
        try:
            self.serial = int(line[6:11].strip())
        except ValueError:
            try:
                self.serial = int(line[6:11].strip(), 16)
            except ValueError:
                raise RuntimeError(f"Cannot interpret atom number {line[6:11].strip()} as decimal or hexadecimal")
        self.atomname = line[12:16].strip()
        self.altloc = line[16:17]
        self.resname = line[17:21].strip()
        self.chain = line[21:22]
        try:
            self.resnum = int(line[22:26].strip())
        except ValueError:
            try:
                self.resnum = int(line[22:26].strip(), 16)
            except ValueError:
                raise RuntimeError(f"Cannot interpret residue number {line[22:26].strip()} as decimal or hexadecimal")
        self.insert = line[26:27]
        self.x, self.y, self.z = [float(line[30 + 8 * a:30 + 8 * (a + 1)]) for a in range(3)]
        if not qt:
            self.occ = float(line[54:60].strip()) if line[54:60].strip() else 1.0
            self.beta = float(line[60:66].strip()) if line[60:66].strip() else 0.0
            self.q = 0.0
            self.type = 'X'
        else:
            self.occ = 1.0
            self.beta = 0.0
            self.q = float(line[54:62].strip())
            self.type = str(line[62:].strip())
        try:
            self.element = line[76:78].strip()
        except IndexError:
            name = self.atomname.strip('1234567890')
            if name in 'CHONSP':
                self.element = name[:1]
            else:
                self.element = name[:2]


    @classmethod
    def from_gro(cls, line: str, index: int) -> "gml.Atom":
        """
        Reads fields from a line formatted according
        to the .gro format specification
        :param line: str, line from a .gro file
        :return: an Atom instance
        """
        data = "ATOM  {:>5d} {:4s} {:4s} {:>4d}    {:>8.3f}{:>8.3f}{:>8.3f}  1.00  0.00"
        resnum = int(line[:5].strip()) % 10000
        resname = line[5:10].strip()
        atomname = line[10:15].strip()
        atomnum = int(line[15:20].strip())
        x, y, z = [float(line[20 + 8 * i:20 + 8 * (i + 1)].strip()) * 10 for i in range(3)]
        return cls(data.format(atomnum, atomname[:4], resname[:4], resnum, x, y, z), index)

    @classmethod
    def from_cif(cls, line: str, index: int) -> "gml.Atom":
        """
        Reads fields from a line formatted according
        to the .gro format specification
        :param line: str, line from a .gro file
        :return: an Atom instance
        """
        data = "ATOM  {:>5d} {:4s} {:4s}{:1s}{:>4d}    {:>8.3f}{:>8.3f}{:>8.3f}  1.00{:6.2f}"
        resnum = int(line.split()[8]) % 10000
        resname = line.split()[5]
        atomname = line.split()[3]
        atomnum = int(line.split()[1])
        chain = line.split()[6]
        beta = float(line.split()[14])
        x, y, z = [float(line.split()[i]) for i in range(10, 13)]
        return cls(data.format(atomnum, atomname[:4], resname[:4], chain, resnum, x, y, z, beta), index)

    @classmethod
    def from_top_entry(cls, entry: "gml.EntryAtom", index: int) -> "gml.Atom":
        """
        Creates a dummy Atom instance (no coordinates)
        based on atom information provided by the .top file
        :param entry: a gromologist.EntryAtom instance
        :return: an Atom instance
        """
        data = "ATOM  {:>5d} {:4s} {:4s} {:>4d}    {:>8.3f}{:>8.3f}{:>8.3f}  1.00  0.00"
        resnum = entry.resid
        resname = entry.resname
        atomname = entry.atomname
        atomnum = entry.num
        x, y, z = [0, 0, 0]
        return cls(data.format(atomnum, atomname, resname, resnum, x, y, z), index)

    @property
    def coords(self) -> np.array:
        """
        The coordinates of a given atom
        :return: list of float
        """
        return np.array([self.x, self.y, self.z])

    def set_coords(self, coords: Iterable) -> None:
        """
        A setter for Atom coordinates
        :param coords: iterable of len-3 elements
        :return: None
        """
        self.x, self.y, self.z = coords

    def __repr__(self) -> str:
        chain = self.chain if self.chain != " " else "unspecified"
        return "Atom {} in residue {}{} of chain {}".format(self.atomname, self.resname, self.resnum, chain)


class Traj:
    """
    A provisional implementation that stores a trajectory as a list of Pdb objects
    """

    def __init__(self, structures: Union[str, list] = None, top: Optional["gml.Top"]=None, altloc: str = 'A', **kwargs):
        self.fname = 'gmltraj.pdb' if 'name' not in kwargs.keys() else kwargs['name']
        if isinstance(structures, str):
            self.structures = self.get_coords_from_file(structures)
        elif isinstance(structures[0], str):
            self.structures = [gml.Pdb(struct) for struct in structures]
        elif isinstance(structures[0], gml.Pdb) and isinstance(structures, list):
            self.structures = structures
        else:
            raise RuntimeError("Cannot understand the format of input")
        self.check_consistency()
        self.top = top if not isinstance(top, str) else gml.Top(top, **kwargs)
        if self.top and not self.top.pdb:
            self.top.pdb = self
        self.altloc = altloc
        self._atom_format = "ATOM  {:>5d} {:4s}{:1s}{:4s}{:1s}{:>4d}{:1s}   " \
                            "{:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:>2s}\n"
        self._cryst_format = "CRYST1{:9.3f}{:9.3f}{:9.3f}{:7.2f}{:7.2f}{:7.2f} P 1           1\n"
        self.atoms = self.structures[0].atoms

    def __repr__(self) -> str:
        return "trajectory file {} with {} frames and {} atoms".format(self.fname, self.nframes,
                                                                       len(self.structures[0].atoms))

    @property
    def nframes(self) -> int:
        """
        Simply the number of frames in the trajectory
        :return: int, no of frames
        """
        return len(self.structures)

    def from_selection_inplace(self, selection: str) -> None:
        """
        Retains a subset of atoms in each frame, in-place (modifies the object instead of returning the modified one)
        :param selection: str, the selection to restrict the system
        :return: None
        """
        new_pdbs = [p.from_selection(selection) for p in self.structures]
        self.structures = new_pdbs
        self.atoms = self.structures[0].atoms
        if self.top is not None:
            self.top = self.top.from_selection(selection)

    @classmethod
    def from_xyz(cls, xyz: str, struct: Union[str, "gml.Pdb"]) -> "gml.Traj":
        """
        Reads coordinates from text, useful for reading trajectories
        :param text: str, contents of the pdb/gro
        :param ftype: str, type of file (pdb, gro, bqt)
        :return: a new Pdb instance
        """
        pdb = gml.obj_or_str(struct)
        coords = gml.process_xyz(xyz)
        assert len(pdb.atoms) == coords.shape[1]
        traj = []
        for nframe in range(coords.shape[0]):
            traj.append(deepcopy(pdb))
            traj[-1].set_coords(coords[nframe])
        return cls(traj)


    def get_coords_from_file(self, infile: str) -> list:
        """
        Reads the full trajectory from a multi-frame .pdb or .gro file
        :param infile: str, name of the file
        :return: list of gml.Pdb objects
        """
        ftype = infile[-3:]
        structs = []
        content = [line for line in open(infile)]
        if ftype == 'pdb':
            term_lines = [0] + [n + 1 for n, line in enumerate(content)
                                if line.startswith('END') or line.startswith('ENDMDL')]
        elif ftype == 'gro':
            natoms = int(content[1].strip())
            per_frame = natoms + 3
            term_lines = range(0, len(content) + 1, per_frame)
        else:
            raise RuntimeError(f'file type should be pdb or gro, {ftype} was given')
        for i, j in zip(term_lines[:-1], term_lines[1:]):
            frame = '\n'.join(content[i:j])
            new_pdb = Pdb.from_text(frame, ftype)
            if len(new_pdb.atoms) > 0:
                structs.append(new_pdb)
        return structs

    def add_frame(self, pdb: Union[str, "gml.Pdb"], position: Optional[int] = None) -> None:
        """
        Adds a frame to the trajectory
        :param pdb: string or gml.Pdb, structure to be added to the trajectory
        :param position: int, at which position to place the new frame
        :return:
        """
        if isinstance(pdb, str):
            newstr = Pdb(pdb)
        else:
            newstr = pdb
        if position is None:
            self.structures.append(newstr)
        else:
            self.structures.insert(position, newstr)
        self.check_consistency()

    def add_frames(self, pdb: Union[str, "gml.Traj"]) -> None:
        """
        Adds a frame to the trajectory
        :param pdb: either str or gml.Traj, frames to add to the current traj
        :return: None
        """
        if isinstance(pdb, str):
            self.structures.extend(self.get_coords_from_file(pdb))
        else:
            self.structures.extend(pdb.structures)
        self.check_consistency()

    def check_consistency(self) -> None:
        """
        Checks whether all frames have the same number of atoms (and only this)
        :return: None
        """
        if not all([len(pdb.atoms) == len(self.structures[0].atoms) for pdb in self.structures]):
            raise RuntimeError(f"Not all structures have the same number of atoms, "
                               f"with {[len(pdb.atoms) for pdb in self.structures]}")

    def as_string(self, end: str = "ENDMDL") -> str:
        """
        A printer function to facilitate writing to PDBs
        :param end: how to end each MODEL entry, some softwares can be sensitive to this
        :return: str, text-based content of the trajectory in multi-PDB format
        """
        text = ''
        for nframe, frame in enumerate(self.structures, 1):
            text = text + 'MODEL     {:>4d}\n'.format(nframe)
            text = text + self._cryst_format.format(*frame.box)
            for atom in frame.atoms:
                text = text + frame._write_atom(atom)
            text = text + end + '\n'
        return text

    def __getitem__(self, item: int) -> "gml.Pdb":
        return self.structures[item]

    def __len__(self) -> int:
        return len(self.structures)

    def atom_properties_from(self, pdb: Union[str, "gml.Pdb"], names=True, indices=True, chains=True, resid=True) -> None:
        """
        Sets the properties of all atoms from a given trajectory based on a specified PDB;
        by default, atom names, atom indices, chains, and residue IDs will be copied
        :param pdb: str or gml.Pdb, the source PDB from which data should be copied
        :param names: bool, whether to copy atom names
        :param indices: bool, whether to copy atom indices
        :param chains: bool, whether to copy chains
        :param resid: bool, whether to copy residue numbers
        :return:
        """
        if isinstance(pdb, str):
            pdb = gml.Pdb(pdb)
        assert len(pdb.atoms) == len(self.atoms)
        for fr in self.structures:
            for af, ar in zip(fr.atoms, pdb.atoms):
                if names:
                    af.atomname = ar.atomname
                if indices:
                    af.serial = ar.serial
                if chains:
                    af.chain = ar.chain
                if resid:
                    af.resnum = ar.resnum

    def extrapolate(self) -> None:
        """
        Adds one structure before and after the trajectory (assuming the sequence represents a pathway)
        through linear extrapolation (in-place)
        :return: None
        """
        from copy import deepcopy
        initdiff = np.array(self.structures[0].get_coords()) - np.array(self.structures[1].get_coords())
        enddiff = np.array(self.structures[-1].get_coords()) - np.array(self.structures[-2].get_coords())
        self.add_frame(deepcopy(self.structures[0]), position=0)
        self.add_frame(deepcopy(self.structures[-1]))
        self.structures[0].set_coords(np.array(self.structures[1].get_coords()) + initdiff)
        self.structures[-1].set_coords(np.array(self.structures[-2].get_coords()) + enddiff)

    def scale_box(self, scaling_factor: Union[list, float]) -> None:
        """
        Scales the box for all frames in the trajectory (useful for reruns when cutoff issues arise)
        :param scaling_factor: float (scaling factor) or list of 3 floats for box vectors a, b, c
        :return: None
        """
        try:
            _ = scaling_factor[2]
        except:
            scaling_factor = 3 * [scaling_factor]
        assert len(scaling_factor) == 3
        for struct in self.structures:
            struct.box = [struct.box[0] * scaling_factor[0], struct.box[1] * scaling_factor[1],
                          struct.box[2] * scaling_factor[2], struct.box[3], struct.box[4], struct.box[5]]

    def equal_spacing(self) -> None:
        """
        A special function that converts a trajectory defining a conformational transition
        into a similar trajectory but (roughly) equally spaced in RMSD space; used for
        the string method with "structural" intermediates
        :return: None
        """

        def compute_cumulative_distance(points):
            """Compute the cumulative distance along a path defined by 'points'."""
            deltas = np.diff(points, axis=0)
            segment_lengths = np.sqrt(np.sum(deltas ** 2, axis=1))
            return np.insert(np.cumsum(segment_lengths), 0, 0)

        def interpolate_between_points(point1, point2, fraction):
            """Interpolate between two points given a fraction."""
            return point1 + fraction * (point2 - point1)

        def resample_by_distance(points, distance):
            """Resample a path defined by 'points' such that the new points are approximately 'distance' apart."""
            cumulative_distances = compute_cumulative_distance(points)
            max_distance = cumulative_distances[-1]
            # Start with the first point
            new_points = [points[0]]
            current_distance = distance
            while current_distance < max_distance:
                # Find two points which are before and after the current distance
                idx = np.searchsorted(cumulative_distances, current_distance) - 1
                point_before, point_after = points[idx], points[idx + 1]
                distance_before, distance_after = cumulative_distances[idx], cumulative_distances[idx + 1]
                # Interpolate between the two points for the resampled point
                fraction = (current_distance - distance_before) / (distance_after - distance_before)
                new_point = interpolate_between_points(point_before, point_after, fraction)
                new_points.append(new_point)
                current_distance += distance
            return np.array(new_points)

        def find_optimal_distance(points, num_points, tolerance=1e-3, max_iterations=100):
            total_length = compute_cumulative_distance(points)[-1]
            guessed_distance = total_length / (num_points - 1)
            for iteration in range(max_iterations):
                resampled = resample_by_distance(points, guessed_distance)
                if len(resampled) == num_points:
                    return guessed_distance
                elif len(resampled) < num_points:
                    guessed_distance *= 0.99
                else:
                    guessed_distance *= 1.01
            raise ValueError("Couldn't converge to a solution in given max_iterations.")

        for natom in range(len(self.atoms)):
            atom_path = np.array([struct.atoms[natom].coords for struct in self.structures])
            resampled_path = resample_by_distance(atom_path, find_optimal_distance(atom_path, len(self)))
            for struct, coords in zip(self.structures[1:-1], resampled_path[1:-1]):
                struct.atoms[natom].set_coords(coords)

    def save_traj_as_pdb(self, filename: Optional[str] = None, end: str = "ENDMDL") -> None:
        """
        Saves all frames to a single PDB file
        :param filename: str, name of the file; if not specified, will overwrite the source file
        :param end: how to end each MODEL entry, some softwares can be sensitive to this
        :return: None
        """
        filename = self.fname if filename is None else filename
        with open(filename, 'w') as outfile:
            outfile.write(self.as_string(end))

    def save_traj_as_many_pdbs(self, core_filename: Optional[str] = None) -> None:
        """
        Saves all frames to individual PDB files
        :param core_filename: str, all filenames will be based on this name
        :return: None
        """
        if core_filename is None:
            core_filename = '.'.join(self.fname.split('.')[:-1])
        for num, frame in enumerate(self.structures):
            frame.save_pdb(f'{core_filename}{num}.pdb')

    def save_traj_as_many_xyzs(self, core_filename: Optional[str] = None) -> None:
        """
        Saves all frames to individual PDB files
        :param core_filename: str, all filenames will be based on this name
        :return: None
        """
        if core_filename is None:
            core_filename = '.'.join(self.fname.split('.')[:-1])
        for num, frame in enumerate(self.structures):
            frame.save_xyz(f'{core_filename}{num}.xyz')
