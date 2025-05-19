from pathlib import Path
from cm_msh.gen.hex_poly_gen import HexPolyGenerator

example_dir = Path(__file__).parent
mesh_dir = example_dir / "meshes"
mesh_path = mesh_dir / "hex_6x6.msh"

mesh_dir.mkdir(parents=True, exist_ok=True)

# example params
num_grains = 36       # 6x6
mesh_size = 0.05

# mesh gen
gen = HexPolyGenerator(num_grains, mesh_size, str(mesh_path))
gen.gen()

print(f"Mesh generated at: {mesh_path}")
