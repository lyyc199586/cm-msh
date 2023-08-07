import gmsh
import numpy as np
from math import sqrt, pi, cos, sin, floor

class DiscGenerator:
    '''generating disc mesh for Brazilian tests
    '''
    
    def __init__(self, mesh_size, msh_dir, radius, thickness=0):

        self.mesh_size = mesh_size
        self.msh_dir = msh_dir
        self.r = radius
        self.t = thickness
        
    def gen(self):
      
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
            
        # innter points: 6, 7, 8, 9
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
        gmsh.model.geo.synchronize()
        gmsh.model.addPhysicalGroup(2, [1, 2, 3, 4, 5], tag=-1)
        
        # set transfinite
        nx = floor(self.r/self.mesh_size)
        
        for curve in gmsh.model.getEntities(1):
            gmsh.model.mesh.setTransfiniteCurve(curve[1], nx)
        for surface in gmsh.model.getEntities(2):
            gmsh.model.mesh.setTransfiniteSurface(surface[1])
            gmsh.model.mesh.setRecombine(surface[0], surface[1])
        
        # generate mesh and output
        gmsh.model.mesh.generate(dim)
        gmsh.write(self.msh_dir)
        
        gmsh.finalize()
        
