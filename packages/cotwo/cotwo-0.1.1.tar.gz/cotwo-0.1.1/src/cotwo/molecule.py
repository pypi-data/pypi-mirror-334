"""
Module for molecular structure representation and manipulation.
Provides classes and utilities for working with atoms, molecules, and coordinate systems.
"""

from pathlib import Path
from typing import Self

import numpy as np
import polars as pl
from numpy.typing import NDArray
from rdkit import Chem
from rdkit.Chem import AllChem

PERIODIC_TABLE = pl.read_json(Path(__file__).parent / "periodic_table.json")


class Atom:
    """
    Represents an atom with its element type and 3D coordinates.

    Attributes:
    -----------
    element : dict
        Chemical element symbol (e.g., 'H', 'C', 'O') for properties
    coords : NDArray[np.float64]
        3D coordinates of the atom in Angstroms
    """

    def __init__(self, symbol: str, coords: NDArray[np.float64]):
        self.element: dict = PERIODIC_TABLE.filter(pl.col("symbol") == symbol).to_dict()
        self.coords = coords

    def to_str(self) -> str:
        """
        Convert atom to string representation in XYZ format.

        Returns:
        --------
        str
            Formatted string with element and coordinates (e.g., "H 0.0000 0.0000 0.0000")
        """
        return f"{self.element['symbol'].item()} {self.coords[0]:.4f} {self.coords[1]:.4f} {self.coords[2]:.4f}"

    @classmethod
    def from_str(cls, line: str) -> "Atom":
        """
        Create an Atom instance from a string representation.

        Parameters:
        -----------
        line : str
            String containing element and coordinates (e.g., "H 0.0 0.0 0.0")

        Returns:
        --------
        Atom
            New Atom instance with parsed element and coordinates
        """
        element, *coords = line.split()
        return cls(element, coords=np.array([float(coord) for coord in coords]))


def convert_smiles_to_xyz(smiles: str) -> str:
    """
    Convert a SMILES string to XYZ format using RDKit.

    Parameters:
    -----------
    smiles : str
        SMILES representation of molecule

    Returns:
    --------
    str
        XYZ format string containing atomic coordinates
    """
    # Convert SMILES string to a molecule object
    mol = Chem.MolFromSmiles(smiles)

    # Generate 3D conformer
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, useRandomCoords=False)  # type: ignore

    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    conf = mol.GetConformer()
    coords = [conf.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]

    xyz_str = f"{len(atoms)}\nGenerated from SMILES: {smiles}\n"
    xyz_str += "\n".join(
        f"{atoms[i]} {coords[i].x:.4f} {coords[i].y:.4f} {coords[i].z:.4f}"
        for i in range(len(atoms))
    )

    return xyz_str


class Xyz:
    """
    Represents a molecular structure with atoms and properties.

    Instanciate with .from_smiles, .from_file, or .from_str

    Attributes:
    -----------
    atoms : list[Atom]
        List of atoms in the molecule
    charge : int
        Total molecular charge
    mult : int
        Spin multiplicity
    spin: float
        Total spin
    """

    def __init__(self, atoms: list[Atom], charge: int = 0, mult: int = 1) -> None:
        """
        Initialize a Xyz instance.

        Parameters:
        -----------
        atoms : list[Atom]
            List of atoms comprising the molecule
        charge : int, optional
            Molecular charge. Defaults to 0
        mult : int, optional
            Spin multiplicity. Defaults to 1 (singlet)
        """
        self.atoms = atoms
        self.charge = charge
        self.mult = mult

    def __str__(self) -> str:
        """
        String representation of molecule in XYZ format.

        Returns:
        --------
        str
            XYZ format string of the molecule
        """
        xyz_str = f"{len(self.atoms)}\n\n"
        xyz_str += "\n".join((atom.to_str() for atom in self.atoms))
        return xyz_str

    @property
    def spin(self) -> float:
        """
        Calculate the spin of the molecule.

        Returns:
        --------
        float
            Spin multiplicity
        """
        return (self.mult - 1) / 2

    @classmethod
    def from_str(cls, xyz: str) -> "Xyz":
        """
        Create a Xyz instance from XYZ format string.

        Parameters:
        -----------
        xyz : str
            XYZ format string containing molecular structure

        Returns:
        --------
        Xyz
            New Xyz instance with parsed atoms
        """
        atoms = []
        for line in xyz.strip().split("\n")[2:]:
            element, *coords = line.split()
            coords = np.array([float(coord) for coord in coords])
            atoms.append(Atom(element, coords))
        return cls(atoms)

    @classmethod
    def from_file(cls, path: str | Path) -> "Xyz":
        path = Path(path)
        if path.suffix == ".xyz":
            return cls.from_xyz_file(path)
        elif path.suffix == ".out":
            return cls.from_output_file(path)
        else:
            raise ValueError("Unsupported file type")

    @classmethod
    def from_xyz_file(cls, path: str | Path) -> "Xyz":
        return cls.from_str(Path(path).read_text())

    @classmethod
    def from_output_file(cls, path: str | Path) -> "Xyz":
        lines = Path(path).read_text().splitlines()
        for i, line in enumerate(lines):
            if "CARTESIAN COORDINATES (ANGSTROEM)" in line.strip():
                break
        else:
            raise ValueError("Failed to find cartesian coordinates in file")

        rows = []
        for line in lines[i + 2 :]:
            if not line.strip():
                break
            rows.append(line)

        xyz_string = "\n".join(rows)
        return cls.from_str(f"{len(rows)}\n\n" + xyz_string)

    @classmethod
    def from_smiles(cls, smiles: str) -> "Xyz":
        """
        Create a Xyz instance from SMILES string.

        Parameters:
        -----------
        smiles : str
            SMILES representation of molecule

        Returns:
        --------
        Xyz
            New Xyz instance with 3D structure
        """
        xyz = convert_smiles_to_xyz(smiles)
        return cls.from_str(xyz)

    # def to_df(self) -> pl.DataFrame:
    #     """The first line is the number of atoms, the second is a comment, and then
    #     each subsequent line has: Symbol X Y Z.
    #     """
    #     lines = str(self).splitlines()
    #     num_atoms = int(lines[0].strip())
    #     atoms = []
    #     for line in lines[2 : 2 + num_atoms]:
    #         parts = line.split()
    #         symbol = parts[0]
    #         x, y, z = map(float, parts[1:4])
    #         atoms.append({"Symbol": symbol, "X": x, "Y": y, "Z": z})
    #     return pl.DataFrame(atoms)

    def get_distance(self, i: int, j: int) -> float:
        """
        Calculate distance between two atoms in the molecule.

        Parameters:
        -----------
        i : int
            Index of first atom
        j : int
            Index of second atom

        Returns:
        --------
        float
            Distance between atoms in Angstroms
        """
        return float(np.linalg.norm(self.atoms[i].coords - self.atoms[j].coords))

    def set_distance(self, i: int, j: int, distance: float) -> Self:
        """
        Set the distance between two atoms in the molecule.

        Parameters:
        -----------
        i : int
            Index of first atom
        j : int
            Index of second atom
        distance : float
            Desired distance in Angstroms

        Notes:
        ------
        The second atom (j) is moved while keeping the first atom (i) fixed.
        The direction vector between the atoms is preserved.
        """
        direction = self.atoms[j].coords - self.atoms[i].coords
        direction /= np.linalg.norm(direction)
        self.atoms[j].coords = self.atoms[i].coords + direction * distance
        return self
