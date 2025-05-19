from pathlib import Path
import pytest
import gmsh

from cm_msh.gen.hex_poly_gen import HexPolyGenerator


@pytest.fixture
def temp_msh_file(tmp_path: Path):
    msh_path = tmp_path / "test_hex_poly.msh"
    yield msh_path
    if msh_path.exists():
        msh_path.unlink()


def test_hex_poly_generator_runs(temp_msh_file: Path):
    num_grains = 16  # 4x4
    mesh_size = 0.1

    gen = HexPolyGenerator(num_grains=num_grains, mesh_size=mesh_size, msh_dir=str(temp_msh_file))
    gen.gen()

    assert temp_msh_file.is_file(), "Output .msh file not generated"

    gmsh.initialize()
    gmsh.open(str(temp_msh_file))

    # check number of physical groups (1 per grain + 4 boundaries)
    phys = gmsh.model.getPhysicalGroups(dim=2)
    assert len(phys) >= num_grains, f"Expected at least {num_grains} grains as physical groups, got {len(phys)}"

    gmsh.finalize()
