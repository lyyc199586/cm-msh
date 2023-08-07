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
        
        def mark_boundary(dim):
            eps = 1e-3
            vin = gmsh.model.getEntitiesInBoundingBox(-eps, -eps, -eps, 1+eps, 1+eps, eps, dim)
            bnds = gmsh.model.getBoundary(vin, False, False, True)
            gmsh.model.mesh.setSize(bnds, size=self.mesh_size)
            left_bnds = gmsh.model.getEntitiesInBoundingBox(-eps, -eps, -eps, eps, 1+eps, eps, dim-1)
            right_bnds = gmsh.model.getEntitiesInBoundingBox(1-eps, -eps, -eps, 1+eps, 1+eps, eps, dim-1)
            top_bnds = gmsh.model.getEntitiesInBoundingBox(-eps, 1-eps, -eps, 1+eps, 1+eps, eps, dim-1)
            bottom_bnds = gmsh.model.getEntitiesInBoundingBox(-eps, -eps, -eps, 1+eps, eps, eps, dim-1)
            gmsh.model.addPhysicalGroup(dim-1, [i[1] for i in left_bnds], tag=-1, name="left")
            gmsh.model.addPhysicalGroup(dim-1, [i[1] for i in right_bnds], tag=-1, name="right")
            gmsh.model.addPhysicalGroup(dim-1, [i[1] for i in top_bnds], tag=-1, name="top")
            gmsh.model.addPhysicalGroup(dim-1, [i[1] for i in bottom_bnds], tag=-1, name="bottom")
            
            
        
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
        inter, _ = gmsh.model.occ.intersect([(dim, square)], entire, removeObject=False)
        gmsh.model.occ.synchronize()
        
        # add physical groups
        # gmsh.model.addPhysicalGroup(2, [square], tag=0, name="grain_0")
        for i, block in enumerate(entire):
            gmsh.model.addPhysicalGroup(2, [block[1]], tag=i+1, name=f"grain_{i+1}")

        # set boundary
        mark_boundary(dim)

        # generate and output
        gmsh.option.setNumber("Mesh.Algorithm", 11)
        gmsh.model.mesh.generate(dim)
        gmsh.model.mesh.optimize("Relocate2D", force=True, niter=3)
        gmsh.option.setNumber("Mesh.RecombineAll", 1)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 3)
        gmsh.model.mesh.recombine()
        gmsh.model.mesh.optimize("QuadQuasiStructured", force=True, niter=3)
        gmsh.write(self.msh_dir)

        gmsh.finalize()
        

class 