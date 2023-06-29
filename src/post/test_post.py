# %%
import meshio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mesh_plotter import MeshPlotter

msh_file = "../../mesh/test.msh"
mesh = meshio.read(msh_file)
mesh_plotter = MeshPlotter(mesh)

plt.style.use("../../misc/elsevier.mplstyle")
fig, ax = plt.subplots()
mesh_plotter.plot(ax=ax, edgecolor='k', facecolor='None', lw=0.5)

# %%
save_dir = "../../out/"
fig.savefig(save_dir + "test_mesh_plot.png")

# %%
