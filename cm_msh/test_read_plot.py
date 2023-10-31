#%%
from cm_msh.mesh_reader import GmshReader

msh_file = "../out/mesh/test.msh"
mesh = GmshReader(msh_file, dim=2)
verts, faces = mesh.get_mesh()

print(verts)
print(faces)
# %% plot
from cm_msh.mesh_plotter import MeshPlotter

plotter = MeshPlotter(msh_file, dim=2)
plotter.plot()
# %%
