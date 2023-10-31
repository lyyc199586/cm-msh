import gmsh
import numpy as np


class GmshReader:
    '''a wrapper to read gmsh mesh into numpy arraies, only for 2D for now
    '''

    def __init__(self, msh_file, dim):
        self.msh_file = msh_file
        self.dim = dim

    def get_mesh(self):
        '''currently just return verts and elements (faces in 2D)
        '''
        gmsh.initialize()
        gmsh.open(self.msh_file)
        
        # get all nodes
        _, coords, _ = gmsh.model.mesh.getNodes()
        verts = coords.reshape((-1, 3))  # [[x, y, z], ...]
        elems = []

        # elements of types:
        # 1: 2-nodes lines; 2: 3-node triangles; 3: 4-node quadrilaterals
        # 4: 4-node tetrahedra; 5: 8-node hexahedra; 6: 6-node prims; 7: 5-node pyramids
        
        # get entities
        entities = gmsh.model.getEntities(dim = self.dim)
         
        for entity in entities:
            node_tags, node_coords, _ = gmsh.model.mesh.getNodes(entity[0], entity[1])
            _, elem_tags, _ = gmsh.model.mesh.getElements(entity[0], entity[1])
            
            for elem_tag in elem_tags[0]:
                _, elem_node_tags, _, _ = gmsh.model.mesh.getElement(elem_tag)
                elems.extend([elem_node_tags - 1])
                
        gmsh.finalize()
        
        return np.array(verts).reshape((-1, 3)), np.array(elems)
            


