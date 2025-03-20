from collections import namedtuple
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.ndimage import zoom
from skimage import measure

from cotwo.molecule import Atom


class IsosurfaceRenderer:
    def __init__(
        self,
        file: str | Path,
        isovalue: float = 0.005,
        smoothness: float = 1.0,
    ):
        density_data: dict = self._parse_cube_file(file)

        # Calculate spacing for the grid
        smoothed_values = zoom(input=density_data["values"], zoom=smoothness, order=3)
        # smoothed_values = density_data["values"]

        basis_x = density_data["basis_vectors"]["x"].x
        basis_y = density_data["basis_vectors"]["y"].y
        basis_z = density_data["basis_vectors"]["z"].z

        spacing = (
            basis_x / smoothness,
            basis_y / smoothness,
            basis_z / smoothness,
        )

        # Extract vertices and faces using marching cubes
        vertices_pos, faces_pos, _, _ = measure.marching_cubes(
            smoothed_values, level=isovalue, spacing=spacing
        )
        vertices_neg, faces_neg, _, _ = measure.marching_cubes(
            smoothed_values, level=-isovalue, spacing=spacing
        )

        # Adjust vertices positions by origin offset
        vertices_pos += density_data["origin"]
        vertices_neg += density_data["origin"]

        self.data = (vertices_pos, faces_pos, vertices_neg, faces_neg)

    def spawn_isosurfaces(
        self, fig: go.Figure, colors: list[str] = ["#1E88E5", "#004D40"]
    ) -> None:
        fig.add_traces(self.get_traces(colors))

    def get_traces(
        self, colors: list[str] = ["#1E88E5", "#004D40"]
    ) -> tuple[go.Mesh3d, go.Mesh3d]:
        return (self._positive_trace(colors[0]), self._negative_trace(colors[1]))

    def _positive_trace(self, color: str = "red") -> go.Mesh3d:
        trace = go.Mesh3d(
            x=self.data[0][:, 0],
            y=self.data[0][:, 1],
            z=self.data[0][:, 2],
            i=self.data[1][:, 0],
            j=self.data[1][:, 1],
            k=self.data[1][:, 2],
            color=color,
            opacity=1,
            name="Positive",
            showlegend=True,
            hoverinfo="skip",
            lighting=dict(
                ambient=0.5,
                diffuse=0.7,
                specular=0.2,
                roughness=0.2,
                fresnel=0.1,
            ),
        )
        return trace

    def _negative_trace(self, color: str = "yellow") -> go.Mesh3d:
        trace = go.Mesh3d(
            x=self.data[2][:, 0],
            y=self.data[2][:, 1],
            z=self.data[2][:, 2],
            i=self.data[3][:, 0],
            j=self.data[3][:, 1],
            k=self.data[3][:, 2],
            color=color,
            opacity=1,
            name="Negative",
            showlegend=True,
            hoverinfo="skip",
            lighting=dict(
                ambient=0.5,
                diffuse=0.7,
                specular=0.2,
                roughness=0.2,
                fresnel=0.1,
            ),
        )
        return trace

    @staticmethod
    def _parse_cube_file(file: str | Path) -> dict:
        lines = Path(file).read_text().splitlines()

        _comments = lines[:2]
        n_atoms, *origin = lines[2].strip().split()
        n_atoms = int(n_atoms)

        # Cube files encode the unit (Bohrs or Angstroms) in the sign
        # of the number of atoms...
        # If n_atoms is negative, the units are in Angstroms
        unit = "bohr"
        if n_atoms < 0:
            n_atoms = -n_atoms
            unit = "angstrom"
        scale = 0.529177 if unit == "bohr" else 1.0

        origin = np.array([float(coord) * scale for coord in origin])

        BasisVector = namedtuple("BasisVector", ["n_voxels", "x", "y", "z"])
        basis_vectors = {
            "x": BasisVector(
                int(lines[3].split()[0]),
                *[float(coord) * scale for coord in lines[3].split()[1:]],
            ),
            "y": BasisVector(
                int(lines[4].split()[0]),
                *[float(coord) * scale for coord in lines[4].split()[1:]],
            ),
            "z": BasisVector(
                int(lines[5].split()[0]),
                *[float(coord) * scale for coord in lines[5].split()[1:]],
            ),
        }

        if (
            not basis_vectors["x"].n_voxels
            == basis_vectors["y"].n_voxels
            == basis_vectors["z"].n_voxels
        ):
            raise ValueError("Number of voxels in each direction must be equal")

        grid_resolution = basis_vectors["x"].n_voxels

        atoms = []
        for line in lines[6 : 6 + n_atoms]:
            element, _charge, *coords = line.split()
            coords = np.array([float(coord) for coord in coords])
            atoms.append(Atom(element, coords))

        grid_values = []
        for line in lines[6 + n_atoms :]:
            grid_values.extend(map(float, line.split()))

        grid_values = np.array(grid_values).reshape(
            basis_vectors["x"].n_voxels,
            basis_vectors["y"].n_voxels,
            basis_vectors["z"].n_voxels,
        )

        return {
            "origin": origin,
            "basis_vectors": basis_vectors,
            "grid": grid_resolution,
            "values": grid_values,
        }
