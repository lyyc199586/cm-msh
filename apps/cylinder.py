#%% gen

from cm_msh.gen.cylender_gen import Cylinder

mesh_size = 1
radius = 20
height = 30
msh_file = f"../out/mesh/quarter_cylinder_r{20}_t{30}_h{1}.msh"

mesh_gen = Cylinder(mesh_size, msh_file, radius, height)
mesh_gen.gen(quarter=True)
# %%
