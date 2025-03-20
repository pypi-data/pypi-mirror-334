from pathlib import Path

import plotly.graph_objects as go

from cotwo.isosurface_renderer import IsosurfaceRenderer
from cotwo.molecule import Xyz
from cotwo.molecule_renderer import MoleculeRenderer


class StructureRenderer:
    def __init__(self, file: str):
        xyz = Xyz.from_file(file)
        molecule = MoleculeRenderer(xyz)

        self.fig = go.Figure()
        molecule.spawn(self.fig)

        self._set_layout()

    def add_isosurface(self, file: str, isovalue: float = 0.005):
        colors = ["#1E88E5", "#004D40"]
        if "spindens" in Path(file).name:
            colors = ["#24FF51", "#FA7496"]
        isosurface = IsosurfaceRenderer(file, isovalue, smoothness=2)
        isosurface.spawn_isosurfaces(self.fig, colors)

    def _set_layout(self):
        self.fig.update_layout(
            # width=self.width,
            # height=self.height,
            # title=self.title,
            scene=dict(
                aspectmode="data",
                xaxis_visible=False,
                yaxis_visible=False,
                zaxis_visible=False,
                bgcolor="whitesmoke",
                dragmode="orbit",  # Ensures orbital rotation mode is active
            ),
            scene_camera=dict(
                up=dict(x=0, y=0, z=2),
                eye=dict(x=0, y=2.5, z=0),
                center=dict(x=0, y=0, z=0),
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(dict(yanchor="top", y=0.99, xanchor="left", x=0.01)),
        )

    def show(self, width: int = 640, height: int = 640):
        self.fig.update_layout(width=width, height=height)
        self.fig.show()
