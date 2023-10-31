import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from cm_msh.gen.mesh_reader import GmshReader

class MeshPlotter:
    '''use matplotlib to plot mesh (only for 2D)
    '''

    def __init__(self, msh_file, dim):
        self.msh_file = msh_file
        self.dim = dim
    
    def plot(self, ax=None, **kwargs):
        
        # read mesh into verts and faces
        mesh = GmshReader(self.msh_file, self.dim)
        verts, faces = mesh.get_mesh()
        
        # plot with matplotlib
        # If no ax provided, create fig and ax
        if ax is None:
            if self.dim == 2:
                fig, ax = plt.subplots()
                ax.set_aspect("equal")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection="3d")
                ax.set_xlabel("$x$")
                ax.set_ylabel("$y$")
                ax.set_zlabel("$z$")
                
        # add poly collection
        if self.dim == 2:
            p = PolyCollection([verts[face][:, 0:2] for face in faces], **kwargs)
            ax.add_collection(p)
        
        return (ax, p)
        