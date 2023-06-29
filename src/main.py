# %%
from gen.mesh_generator import HexPolyGenerator

num_grains = 16
mesh_size = 0.1
msh_file = "../mesh/hex_n{}_h{}.msh".format(num_grains, mesh_size)

mesh_generator = HexPolyGenerator(num_grains, mesh_size, msh_file)
mesh_generator.gen()


# %% plot
import meshio
import matplotlib.pyplot as plt
from post.mesh_plotter import MeshPlotter

msh_file = "../mesh/hex_n16_h0.1.msh"
mesh = meshio.read(msh_file)
mesh_plotter = MeshPlotter(mesh)

plt.style.use("../misc/elsevier.mplstyle")
ax = mesh_plotter.plot(edgecolor='k', facecolor='None')

# %% save fig
msh_plot = "../out/hex_n16_h0.1.png"
ax.figure.savefig(msh_plot)
# %%
