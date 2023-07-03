import gmsh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D


class GMSHPlotter:
    '''plot gmsh4 format mesh
        Args: gmsh .msh mesh file
    '''

    def __init__(self, msh_file):
        # mesh: gmsh mesh object
        self.mesh = msh_file
        self.dim = 3

    def plot(self, ax=None, **kwargs):
        # Initialize Gmsh and load mesh
        gmsh.initialize()
        gmsh.open(self.mesh)

        def is_2d_mesh(dims):
        # mesh dimension
            if 3 in dims:
                return False
            else:
                self.dim = 2
                return True
        
        # Retrive mesh info
        entities = gmsh.model.getEntities()
        dims = set(entity[0] for entity in entities)

        # Get nodes coords of mesh
        # coords: [x1, y1, z1, x2, y2, z2, ...]
        node_tags, coords, _ = gmsh.model.mesh.getNodes()
        coords = coords.reshape((-1, 3)) # [[x1, y1, z1], ...]

        # If no ax provided, create fig and ax
        if ax is None:
            if is_2d_mesh(dims):
                fig, ax = plt.subplots()
                ax.set_aspect("equal")
                ax.set_xlabel("$x$")
                ax.set_ylabel("$y$")
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection="3d")
                ax.set_xlabel("$x$")
                ax.set_ylabel("$y$")
                ax.set_zlabel("$z$")

        # Create a colormap for faces in each entity
        cmap = plt.get_cmap("tab10")

        # Plot over entites
        for entity in entities:
            dim, tag = entity

            # Only retrive entity of dim = self.dim
            if dim < self.dim - 1:
                continue

            # Get element info of entity
            # elem_types:
            # 1: 2-nodes lines; 2: 3-node triangles; 3: 4-node quadrilaterals
            # 4: 4-node tetrahedra; 5: 8-node hexahedra; 6: 6-node prims; 7: 5-node pyramids
            # elem_tag -> node_tags: [node1, node2 ...]
            _, elem_tags, _ = gmsh.model.mesh.getElements(dim, tag)

            # Plot faces over element
            face_colors = cmap(tag % cmap.N)
            for elem_tag in elem_tags[0]:
                _, elem_node_tags, _, _ = gmsh.model.mesh.getElement(elem_tag)
                face_nodes = coords[elem_node_tags - 1][:, 0:2]
                face_collection = plt.Polygon(
                    face_nodes, closed=True, edgecolor='k', facecolor=face_colors, **kwargs)
                ax.add_patch(face_collection)

        return ax
