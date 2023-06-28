import gmsh

gmsh.initialize()

gmsh.model.add("hexpoly")

# unit square
gmsh.model.occ.addRectangle(0, 0, 0, 1, 1, tag=0)
gmsh.model.occ.synchronize()

