import gmsh
import numpy as np
from math import sqrt


class HexPolyGenerator:
    '''generating periodic polycrystal mesh of hexagon grains in unit square
    '''

    def __init__(self, num_grains, mesh_size, msh_dir):
        # num_grains should be a perfect square, and the square root should be even

        self.num_grains = num_grains
        self.mesh_size = mesh_size
        self.msh_dir = msh_dir


    def gen(self, **kwargs):

        gmsh.initialize()
        gmsh.model.add("hexpoly")
        dim = 2

        # create unit square
        square = gmsh.model.occ.addRectangle(0, 0, 0, 1, 1, 0) # tag=0

        def add_grain(x, y, w):
            vertices = [[x, y+0.6*w, 0], [x+w/2, y+0.4*w, 0], [x+w/2, y-0.4*w, 0], 
                        [x, y-0.6*w, 0], [x-w/2, y-0.4*w, 0], [x-w/2, y+0.4*w, 0]]
            vertices = np.array(vertices)
            # create points
            pts = [
                gmsh.model.occ.addPoint(vertices[i][0], vertices[i][1], vertices[i][2]) for i in range(6)
            ]

            # create lines
            ls = [
                gmsh.model.occ.addLine(pts[i], pts[(i+1)%6]) for i in range(6)
            ]

            # create curve loop and assign it to plane surface
            curve_loop = gmsh.model.occ.addCurveLoop(ls)
            grain = gmsh.model.occ.addPlaneSurface([curve_loop])

            return grain
        
        # define settings for grain width and spacing
        width = 1/self.num_grains
        n_columns = int(sqrt(self.num_grains)) + 1
        n_rows = n_columns
        # sub_id = 0

        grains = []
        for i in range(n_rows):
            for j in range(n_columns):
                # on even rows
                if i%2 == 0:
                    center_x = width/2 + width*j
                    center_y = width*i
                    grain = add_grain(center_x, center_y, width)
                    grains.append((dim, grain))
                else:
                    center_x = width*j
                    center_y = width*i
                    grain = add_grain(center_x, center_y, width)
                    grains.append((dim, grain))
        
        # fragment the grains to merge
        grains_union = gmsh.model.occ.fuse(grains, [(2, 0)])

        # synchronize
        gmsh.model.occ.synchronize()

        # generate and output
        gmsh.model.mesh.generate(dim)
        gmsh.write(self.msh_dir)

        gmsh.finalize()





        # with gmsh.model.occ as geom:
        #     # define unit square domain
        #     # square = geom.add_rectangle([0.0, 0.0, 0.0], 1.0, 1.0, mesh_size=self.mesh_size)
        #     num_columns = int(sqrt(self.num_grains)) + 1
        #     num_rows = num_columns
        #     width = 1/(num_columns - 1)

        #     # define grains
        #     # geom2 = pygmsh.occ.geometry.Geometry()
        #     grain_list = []
        #     domain_id = 0
        #     for i in range(num_rows):
        #         for j in range(num_columns):
        #             # on even rows
        #             if i%2 == 0:
        #                 center_x = width/2 + width*j
        #                 center_y = width*i
        #                 vertices = add_grain(center_x, center_y, width)
        #                 grain = geom.add_polygon(vertices, mesh_size=self.mesh_size, **kwargs)
        #                 grain_list.append(grain)
        #                 # geom.add_physical(grain, label=str(domain_id))
        #                 domain_id = domain_id + 1
        #             # on odd rows
        #             else:
        #                 center_x = width*j
        #                 center_y = width*i
        #                 vertices = add_grain(center_x, center_y, width)
        #                 grain = geom.add_polygon(vertices, mesh_size=self.mesh_size, **kwargs)
        #                 grain_list.append(grain)
        #                 # geom.add_physical(grain, label=str(domain_id))
        #                 domain_id = domain_id + 1

            # union grains
            # grains = geom.boolean_union(grain_list)

            # intersect grains with the square domain
            # inter = geom.boolean_intersection(grain_list)
            # intersection = geom.boolean_intersection([grain, square])

            # generate mesh
            # mesh = geom.generate_mesh()

        # def gen():
        #     # add unit square domain
        #     gmsh.model.add("hexpoly")
        #     gmsh.model.occ.addRectangle(0, 0, 0, 1, 1)
        #     gmsh.model.occ.synchronize()

            
        # return mesh


