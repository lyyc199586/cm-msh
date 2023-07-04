# %%
from gen.mesh_generator import HexPolyGenerator

num_grains = 16
mesh_size = 0.025
msh_file = "../mesh/hex_n{}_h{}.msh".format(num_grains, mesh_size)

mesh_generator = HexPolyGenerator(num_grains, mesh_size, msh_file)
mesh_generator.gen()


# %% plot
import meshio
import matplotlib.pyplot as plt
from post.gmsh_plotter import GMSHPlotter

# num_grains = 4
# mesh_size = 0.025
msh_file = "../mesh/hex_n{}_h{}.msh".format(num_grains, mesh_size)
# mesh = meshio.read(msh_file)
mesh_plotter = GMSHPlotter(msh_file)

plt.style.use("../misc/elsevier.mplstyle")
ax = mesh_plotter.plot(lw=0.25)

# %% save fig
# num_grains = 4
# mesh_size = 0.025
msh_plot = "../mesh/hex_n{}_h{}.png".format(num_grains, mesh_size)
ax.figure.savefig(msh_plot)
# %%
