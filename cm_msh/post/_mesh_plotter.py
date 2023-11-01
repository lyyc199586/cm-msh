import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class MeshPlotter:
    '''plot gmsh4 format mesh
        Args: meshio mesh
    '''

    def __init__(self, mesh):
        # mesh: meshio mesh object
        self.mesh = mesh

    def is_2d_mesh(self):
        # mesh dimension
        for cell in self.mesh.cells:
            if cell.type == "triangle" or cell.type == "quad":
                return True
        return False

    def plot(self, ax=None, **kwargs):
        # if no ax provided, create fig and ax
        if ax is None:
            if self.is_2d_mesh():
                fig, ax = plt.subplots()
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection="3d")

        # access mesh data
        points = self.mesh.points
        cells = self.mesh.cells

        # Set plot parameters
        if self.is_2d_mesh():
            ax.set_aspect("equal")
            ax.set_xlabel("$x$")
            ax.set_ylabel("$y$")
        else:
            ax.set_xlabel("$x$")
            ax.set_ylabel("$y$")
            ax.set_zlabel("$z$")

        # plot mesh over elements
        for cell in cells:
            cell_type = cell.type
            cell_data = cell.data
            if self.is_2d_mesh():
                if cell_type == "triangle":
                    for triangle in cell_data:
                        vertices = points[triangle]
                        ax.fill(
                            vertices[:, 0],
                            vertices[:, 1],
                            **kwargs
                        )
                else:
                    for quad in cell_data:
                        vertices = points[quad]
                        ax.fill(
                            vertices[:, 0],
                            vertices[:, 1],
                            **kwargs
                        )
            else:
                # pass 3d mesh for now
                pass

        return ax
