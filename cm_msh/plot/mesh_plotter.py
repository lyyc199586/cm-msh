"""
mesh_plotter.py

This module provides functionality to visualize 2D meshes using matplotlib.
It supports displaying node and element IDs for better understanding of the mesh structure.

Author: Yangyuanchen Liu
Date: 2025-05-19

Classes:
    MeshPlotter: Represents the mesh plotter for visualizing 2D meshes.

Functions:
    plot: Plots the 2D mesh with optional node and element IDs.
"""

from pathlib import Path
import meshio
import matplotlib.pyplot as plt


class MeshPlotter:
    """
    A class to handle the visualization of 2D meshes.

    Attributes:
        msh_path (Path): Path to the mesh file.
        mesh (meshio.Mesh): The mesh object loaded from the file.
    """

    def __init__(self, msh_path: Path):
        """
        Initializes the MeshPlotter with the given mesh file path.

        Args:
            msh_path (Path): Path to the mesh file to be visualized.
        """
        self.msh_path = Path(msh_path)
        self.mesh = meshio.read(self.msh_path)

    def plot(
        self,
        show_node_ids: bool = False,
        show_element_ids: bool = False,
        ax: plt.Axes = None,
    ) -> plt.Axes:
        """
        Plots the 2D mesh using matplotlib.

        Args:
            show_node_ids (bool): Whether to display node IDs on the plot. Defaults to False.
            show_element_ids (bool): Whether to display element IDs on the plot. Defaults to False.
            ax (plt.Axes, optional): Matplotlib Axes object to plot on. If None, a new figure is created.

        Returns:
            plt.Axes: The matplotlib Axes object with the plotted mesh.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 6))

        for cell_block in self.mesh.cells:
            if cell_block.type not in ["triangle", "quad"]:
                continue

            points = self.mesh.points
            elements = cell_block.data

            for i, element in enumerate(elements):
                polygon = points[element]
                polygon = polygon[:, :2]  # x, y
                polygon = list(polygon) + [polygon[0]]  # close polygon

                xs, ys = zip(*polygon)
                ax.plot(xs, ys, color="black", linewidth=0.5)

                if show_element_ids:
                    centroid = polygon[:-1]
                    cx = sum(x for x, y in centroid) / len(centroid)
                    cy = sum(y for x, y in centroid) / len(centroid)
                    ax.text(cx, cy, str(i), color="blue", fontsize=6)

        if show_node_ids:
            for i, point in enumerate(self.mesh.points):
                x, y = point[:2]
                ax.text(x, y, str(i), fontsize=6, color="red", alpha=0.5)

        ax.set_aspect("equal")
        ax.set_title(f"Mesh: {self.msh_path.name}")
        ax.axis("off")
        return ax
