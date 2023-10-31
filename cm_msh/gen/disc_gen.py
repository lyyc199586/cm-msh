import gmsh
import numpy as np
from math import sqrt, pi, cos, sin, floor

class DiscGenerator:
    """generating disc mesh for Brazilian tests
    """
    
    def __init__(self, mesh_size, msh_dir, radius, thickness=0):

        self.mesh_size = mesh_size
        self.msh_dir = msh_dir
        self.r = radius
        self.t = thickness
        
    def gen(self, add_contact:bool = False):
        """if add_contact=True, add flat contact platens to left and right
        of the disk
        """
      
        gmsh.initialize()
        gmsh.model.add("disc")
        
        if (self.t != 0):
            dim = 3
        else:
            dim = 2
        
        # add center: 1
        gmsh.model.geo.addPoint(0, 0, 0, self.mesh_size, 1)
        
        # outer points:2, 3, 4, 5
        for i in range(4):
            x = self.r*cos(i*pi/2 + pi/4)
            y = self.r*sin(i*pi/2 + pi/4)
            gmsh.model.geo.addPoint(x, y, 0, self.mesh_size, i+2)
            
        # inner points: 6, 7, 8, 9
        for i in range(4):
            x = self.r*cos(i*pi/2 + pi/4)/2
            y = self.r*sin(i*pi/2 + pi/4)/2
            gmsh.model.geo.addPoint(x, y, 0, self.mesh_size, i+6)
            
        # add arcs: 1, 2, 3, 4
        for i in range(4):
            gmsh.model.geo.addCircleArc(i+2, 1, (i+1)%4+2, i+1)
            
        # add inner lines: 5, 6, 7, 8
        for i in range(4):
            gmsh.model.geo.addLine(i+6, (i+1)%4+6, i+5)
            
        # add 4 connect lines: 9, 10, 11, 12
        for i in range(4):
            gmsh.model.geo.addLine(i+2, i+6, i+9)
        
        # add platens
        if(add_contact):
            r = self.r
            h = 1.2*self.r
            w = 0.2*h

            # add left platen points: 10, 11, 12, 13
            gmsh.model.geo.addPoint(-r, h/2, 0, self.mesh_size, 10)
            gmsh.model.geo.addPoint(-r-w, h/2, 0, self.mesh_size, 11)
            gmsh.model.geo.addPoint(-r-w, -h/2, 0, self.mesh_size, 12)
            gmsh.model.geo.addPoint(-r, -h/2, 0, self.mesh_size, 13)

            # add right platen points: 14, 15, 16, 17
            gmsh.model.geo.addPoint(r, h/2, 0, self.mesh_size, 14)
            gmsh.model.geo.addPoint(r+w, h/2, 0, self.mesh_size, 15)
            gmsh.model.geo.addPoint(r+w, -h/2, 0, self.mesh_size, 16)
            gmsh.model.geo.addPoint(r, -h/2, 0, self.mesh_size, 17)

            # add left platen lines: 13, 14, 15, 16
            for i in range(4):
                gmsh.model.geo.addLine(i+10, (i+1)%4+10, i+13)

            # add right platen lines: 17, 18, 19, 20
            for i in range(4):
                gmsh.model.geo.addLine(i+14, (i+1)%4+14, i+17)


        gmsh.model.geo.synchronize()
        
        # add center square surface
        gmsh.model.geo.addCurveLoop([5, 6, 7, 8], 1)
        
        # add 4 outer shapes
        gmsh.model.geo.addCurveLoop([4, 9, -8, -12], 2)
        gmsh.model.geo.addCurveLoop([1, 10, -5, -9], 3)
        gmsh.model.geo.addCurveLoop([2, 11, -6, -10], 4)
        gmsh.model.geo.addCurveLoop([3, 12, -7, -11], 5)
        
        # add plane surfaces
        for i in range(5):
            gmsh.model.geo.addPlaneSurface([i+1], i+1)
        
        # add physical group
        gmsh.model.addPhysicalGroup(2, [1, 2, 3, 4, 5], tag=-1, name='disc')
        
        if(add_contact):
            # add physical platens
            gmsh.model.geo.addCurveLoop([13, 14, 15, 16], 6)
            gmsh.model.geo.addCurveLoop([17, 18, 19, 20], 7)
            gmsh.model.geo.addPlaneSurface([6], 6)
            gmsh.model.geo.addPlaneSurface([7], 7)
            gmsh.model.addPhysicalGroup(2, [6], tag=-1, name="left_platen")
            gmsh.model.addPhysicalGroup(2, [7], tag=-1, name="right_platen")
            gmsh.model.addPhysicalGroup(1, [14], tag=-1, name="left_platen_left")
            gmsh.model.addPhysicalGroup(1, [16], tag=-1, name="left_platen_right")
            gmsh.model.addPhysicalGroup(1, [20], tag=-1, name="right_platen_left")
            gmsh.model.addPhysicalGroup(1, [18], tag=-1, name="right_platen_right")

        gmsh.model.geo.synchronize()

        # set transfinite
        nx = floor(self.r/self.mesh_size)
        
        for curve in gmsh.model.getEntities(1):
            gmsh.model.mesh.setTransfiniteCurve(curve[1], nx)
        
        if(add_contact):
            cnx = floor(w/self.mesh_size)
            cny = floor(h/self.mesh_size)
            for c in [14, 16, 18, 20]:
                gmsh.model.mesh.setTransfiniteCurve(c, cny)
            for c in [13, 15, 17, 19]:
                gmsh.model.mesh.setTransfiniteCurve(c, cnx)

        for surface in gmsh.model.getEntities(2):
            gmsh.model.mesh.setTransfiniteSurface(surface[1])
            gmsh.model.mesh.setRecombine(surface[0], surface[1])
        
        # generate mesh and output
        gmsh.model.mesh.generate(dim)
        gmsh.write(self.msh_dir)
        
        gmsh.finalize()
        
