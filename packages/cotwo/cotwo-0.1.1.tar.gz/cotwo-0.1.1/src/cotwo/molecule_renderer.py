import numpy as np
import plotly.graph_objects as go

from cotwo.molecule import Atom, Xyz

ATOM_SCALE = 0.25
BOND_SCALE = 0.1
BOND_DETECTION_SCALE = 0.7
ATOM_RESOLUTION = 32
BOND_RESOLUTION = 32


class MoleculeRenderer:
    def __init__(self, molecule: Xyz):
        self.mol: Xyz = molecule
        self.bonds: list[tuple[Atom, Atom]] = self._bonds_by_radius()

    def spawn(self, fig: go.Figure) -> None:
        self.spawn_atoms(fig)
        self.spawn_bonds(fig)

    def spawn_atoms(self, fig: go.Figure) -> None:
        for atom in self.mol.atoms:
            atom_mesh = self.create_atom_mesh(atom)
            fig.add_trace(atom_mesh)

    def spawn_bonds(self, fig: go.Figure) -> None:
        for bond in self.bonds:
            bond_mesh = self.create_bond_mesh(bond)
            fig.add_trace(bond_mesh)

    def _bonds_by_radius(self, scale=BOND_DETECTION_SCALE) -> list[tuple]:
        """Detect bonds based on atomic radii (using a scaling factor).

        Returns a list of tuples of atom indices that are bonded.
        """
        bonds = []
        for idx, i in enumerate(self.mol.atoms):
            for j in self.mol.atoms[:idx]:
                distance = float(np.linalg.norm(j.coords - i.coords))

                bonding_radius = (
                    (i.element["atomic_radius"] + j.element["atomic_radius"]).item()
                    / 100  # convert to angstrom
                    * scale
                )

                if distance <= bonding_radius:
                    bonds.append((i, j))
        return bonds

    def _create_sphere(self, center, radius=BOND_SCALE, n_steps=BOND_RESOLUTION):
        """
        Create mesh data for a sphere centered at `center`.
        Returns (x, y, z, i, j, k) for a Plotly Mesh3d trace.
        """
        cx, cy, cz = center
        theta_vals = np.linspace(0, np.pi, n_steps + 1)
        phi_vals = np.linspace(0, 2 * np.pi, n_steps, endpoint=False)
        theta_grid, phi_grid = np.meshgrid(theta_vals, phi_vals, indexing="ij")

        x_2d = cx + radius * np.sin(theta_grid) * np.cos(phi_grid)
        y_2d = cy + radius * np.sin(theta_grid) * np.sin(phi_grid)
        z_2d = cz + radius * np.cos(theta_grid)

        x_all = x_2d.ravel()
        y_all = y_2d.ravel()
        z_all = z_2d.ravel()

        i_list, j_list, k_list = [], [], []

        def idx(t, p):
            return t * n_steps + (p % n_steps)

        for t in range(n_steps):
            for p in range(n_steps):
                i0 = idx(t, p)
                i1 = idx(t, p + 1)
                i2 = idx(t + 1, p)
                i3 = idx(t + 1, p + 1)
                # First triangle
                i_list.append(i0)
                j_list.append(i1)
                k_list.append(i2)
                # Second triangle
                i_list.append(i1)
                j_list.append(i3)
                k_list.append(i2)

        return x_all, y_all, z_all, i_list, j_list, k_list

    def create_atom_mesh(
        self,
        atom: Atom,
        scale: float = ATOM_SCALE,
    ) -> go.Mesh3d:
        radius = atom.element["atomic_radius"].item() / 100 * scale

        color = f"#{atom.element['hex_color'].item()}"

        x_sphere, y_sphere, z_sphere, i_sphere, j_sphere, k_sphere = (
            self._create_sphere(
                center=atom.coords,
                radius=radius,
                n_steps=ATOM_RESOLUTION,
            )
        )

        atom_mesh = go.Mesh3d(
            x=x_sphere,
            y=y_sphere,
            z=z_sphere,
            i=i_sphere,
            j=j_sphere,
            k=k_sphere,
            color=color,
            opacity=1.0,
            lighting=dict(
                ambient=0.85,
                diffuse=0.2,
                specular=0.6,
                roughness=0.5,
                fresnel=0.5,
            ),
            name=str(atom),
            hoverinfo="skip",
        )
        return atom_mesh

    def _create_cylinder(
        self, start_point, end_point, radius=0.05, n_segments=48, add_caps=True
    ):
        """
        Create mesh data for a cylinder from start_point to end_point.
        Returns (x, y, z, i, j, k) for a Plotly Mesh3d trace.
        """
        p0 = np.array(start_point, dtype=float)
        p1 = np.array(end_point, dtype=float)
        d = p1 - p0
        length = np.linalg.norm(d)
        if length < 1e-12:
            # Degenerate case: return a point.
            return [p0[0]], [p0[1]], [p0[2]], [], [], []

        d /= length
        if abs(d[0]) < 1e-4 and abs(d[1]) < 1e-4:
            up = np.array([0, 1, 0], dtype=float)
        else:
            up = np.array([0, 0, 1], dtype=float)

        v = np.cross(d, up)
        v /= np.linalg.norm(v)
        w = np.cross(d, v)

        angles = np.linspace(0, 2 * np.pi, n_segments, endpoint=False)
        circle_bottom = (
            p0[:, None]
            + radius * np.cos(angles)[None, :] * v[:, None]
            + radius * np.sin(angles)[None, :] * w[:, None]
        )
        circle_top = (
            p1[:, None]
            + radius * np.cos(angles)[None, :] * v[:, None]
            + radius * np.sin(angles)[None, :] * w[:, None]
        )

        x = np.hstack([circle_bottom[0, :], circle_top[0, :]])
        y = np.hstack([circle_bottom[1, :], circle_top[1, :]])
        z = np.hstack([circle_bottom[2, :], circle_top[2, :]])

        i_list, j_list, k_list = [], [], []
        for seg in range(n_segments):
            seg_next = (seg + 1) % n_segments
            b0 = seg
            b1 = seg_next
            t0 = seg + n_segments
            t1 = seg_next + n_segments

            # Two triangles per segment
            i_list.extend([b0, b1])
            j_list.extend([b1, t0])
            k_list.extend([t0, b0])
            i_list.extend([b1])
            j_list.extend([t1])
            k_list.extend([t0])

        if add_caps:
            bottom_center_idx = len(x)
            top_center_idx = len(x) + 1
            x = np.append(x, [p0[0], p1[0]])
            y = np.append(y, [p0[1], p1[1]])
            z = np.append(z, [p0[2], p1[2]])

            # Bottom cap
            for seg in range(n_segments):
                seg_next = (seg + 1) % n_segments
                i_list.append(bottom_center_idx)
                j_list.append(seg_next)
                k_list.append(seg)
            # Top cap
            for seg in range(n_segments):
                seg_next = (seg + 1) % n_segments
                i_list.append(top_center_idx)
                j_list.append(seg + n_segments)
                k_list.append(seg_next + n_segments)
        return x, y, z, i_list, j_list, k_list

    def create_bond_mesh(
        self,
        bond: tuple,
        color="gray",
        radius=BOND_SCALE,
    ):
        """
        Build a Plotly Figure by adding cylinder meshes for each bond.
        """
        ADD_CAPS = True

        x_cyl, y_cyl, z_cyl, i_cyl, j_cyl, k_cyl = self._create_cylinder(
            start_point=(bond[0].coords),
            end_point=(bond[1].coords),
            radius=radius,
            n_segments=BOND_RESOLUTION,
            add_caps=ADD_CAPS,
        )

        bond_mesh = go.Mesh3d(
            x=x_cyl,
            y=y_cyl,
            z=z_cyl,
            i=i_cyl,
            j=j_cyl,
            k=k_cyl,
            color=color,
            opacity=1.0,
            lighting=dict(
                ambient=0.85,
                diffuse=0.2,
                specular=0.6,
                roughness=0.5,
                fresnel=0.5,
            ),
            flatshading=False,
            name=f"bond_{bond}",
            hoverinfo="skip",
        )

        return bond_mesh
