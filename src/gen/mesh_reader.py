import gmsh
import numpy as np


class MshReader:
    '''read gmsh mesh
    '''

    def __init__(self, msh_file):
        self.mesh = msh_file

    def read(self):
        gmsh.initialize()
        gmsh.open(self.msh)

        # Get all nodes
        node_tags, coords, param_coord = gmsh.model.mesh.getNodes()
        coords = coords.reshape((-1, 3))  # [[x, y, z], ...]

        # Get elements of types:
        # 1: 2-nodes lines; 2: 3-node triangles; 3: 4-node quadrilaterals
        # 4: 4-node tetrahedra; 5: 8-node hexahedra; 6: 6-node prims; 7: 5-node pyramids
        elem_types = gmsh.model.mesh.getElementTypes()
        

        # Get entities
        entities = gmsh.model.getEntities()


