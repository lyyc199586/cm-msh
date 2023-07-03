# %%
import meshio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from gmsh_plotter import GMSHPlotter

msh_file = "../../mesh/test.msh"
# mesh = meshio.read(msh_file)
mesh_plotter = GMSHPlotter(msh_file)

plt.style.use("../../misc/elsevier.mplstyle")
ax = mesh_plotter.plot(lw=0.5)
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)

# %%
save_dir = "../../out/"
ax.figure.savefig(save_dir + "test_gmsh_plot.png")

# %%
