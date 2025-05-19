from pathlib import Path
from cm_msh.utils.inp2cmrl import inp2cmrl

inp2cmrl(
    input_path=Path("./meshes/composite/composite.inp"),
    output_dir=Path("./meshes/composite/")
)
