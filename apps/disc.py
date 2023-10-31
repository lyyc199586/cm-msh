'''generate disc mesh for Brazilian tests, in 2d and 3d
'''

#%% gen
from cm_msh.gen.disc_gen import DiscGenerator

mesh_size = 1
radius = 25
msh_file = "../out/mesh/disc_mortar_r{}_h{}.msh".format(radius, mesh_size)

mesh_generator = DiscGenerator(mesh_size, msh_file, radius)
mesh_generator.gen(add_contact=True)

# %% plot
import matplotlib.pyplot as plt
from cm_msh.post.mesh_plotter import GMSHPlotter

mesh_plotter = GMSHPlotter(msh_file)

plt.style.use("../misc/elsevier.mplstyle")
ax = mesh_plotter.plot(lw=0.25)
# %%
