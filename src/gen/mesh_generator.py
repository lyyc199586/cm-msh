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
        square = gmsh.model.occ.addRectangle(0, 0, 0, 1, 1)

        def add_grain(x, y, w):
            vertices = [[x, y+0.6*w, 0], [x+w/2, y+0.4*w, 0], [x+w/2, y-0.4*w, 0], 
                        [x, y-0.6*w, 0], [x-w/2, y-0.4*w, 0], [x-w/2, y+0.4*w, 0]]
            vertices = np.array(vertices)
            # create points
            pts = [
                gmsh.model.occ.addPoint(vertices[i][0], vertices[i][1], vertices[i][2], meshSize=self.mesh_size) for i in range(6)
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
        n_columns = int(sqrt(self.num_grains)) + 1
        n_rows = n_columns
        width = 1/(n_columns - 1)

        grains = []
        for i in range(n_rows):
            for j in range(n_columns):
                # on even rows
                if i%2 == 0:
                    center_x = width/2 + width*j
                    center_y = width*i
                    grain = add_grain(center_x, center_y, width)
                    grains.append((dim, grain))
                # on odd rows
                else:
                    center_x = width*j
                    center_y = width*i
                    grain = add_grain(center_x, center_y, width)
                    grains.append((dim, grain))
        
        # fragment the grains to square
        entire, _ = gmsh.model.occ.fragment([(dim, square)], grains, removeObject=False)
        gmsh.model.occ.intersect([(dim, square)], entire)
        gmsh.model.occ.synchronize()

        # generate and output
        gmsh.model.mesh.generate(dim)
        gmsh.model.mesh.optimize()
        gmsh.model.mesh.recombine()
        gmsh.write(self.msh_dir)

        gmsh.finalize()