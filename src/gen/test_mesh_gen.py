# test
# %%
import pygmsh
import gmsh

with pygmsh.geo.Geometry() as geom:
    geom.add_polygon(
        [
            [0.0, 0.0],
            [1.0, -0.2],
            [1.1, 1.2],
            [0.1, 0.7],
        ],
        mesh_size=0.1,
    )
    mesh = geom.generate_mesh(dim=2)

    gmsh.write("../../mesh/test.msh")
    gmsh.clear()

# %%
