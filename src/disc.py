'''generate disc mesh for Brazilian tests, in 2d and 3d
'''

#%% gen
from gen.disc_gen import DiscGenerator

mesh_size = 1
radius = 25
msh_file = "../mesh/disc_mortar_r{}_h{}.msh".format(radius, mesh_size)

mesh_generator = DiscGenerator(mesh_size, msh_file, radius)
mesh_generator.gen(add_contact=True)

# %%
