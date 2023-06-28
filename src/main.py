# %%
import gmsh
import meshio
from gen.mesh_generator import HexPolyGenerator
from post.mesh_plotter import MeshPlotter

num_grains = 4 # 2*2
mesh_size = 0.1
msh_dir = "../mesh/hex_n4_h0.1.msh"

mesh_generator = HexPolyGenerator(num_grains, mesh_size, msh_dir)

mesh = mesh_generator.gen()


# mesh_plotter = MeshPlotter(mesh)

# mesh_plotter.plot(edgecolor='k', facecolor='None')


# %%
