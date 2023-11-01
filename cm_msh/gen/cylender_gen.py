import gmsh
from math import pi, cos, sin, floor

class Cylinder:
    """generate 3d cylinder mesh
    """
    
    def __init__(self, mesh_size, msh_dir, radius, thickness):
        
        self.mesh_size = mesh_size
        self.msh_dir = msh_dir
        self.r = radius
        self.t = thickness
        
    def gen(self, quarter:bool=False):
        """generate a quarter of cylinder when quarter=True
        """
        
        gmsh.initialize()
        gmsh.model.add("cylinder")
        
        # alias to generate geometry
        geometry = gmsh.model.geo
        
        if(quarter):
            # Geometry: a quarter circle on the bottom surface (z=0)
            # points
            p1 = geometry.addPoint(0, 0, 0, self.mesh_size)
            p2 = geometry.addPoint(self.r, 0, 0, self.mesh_size)
            p3 = geometry.addPoint(0, self.r, 0, self.mesh_size)
            p4 = geometry.addPoint(0.5*self.r, 0, 0, self.mesh_size)
            p5 = geometry.addPoint(0, 0.5*self.r, 0, self.mesh_size)
            p6 = geometry.addPoint(0.45*self.r, 0.45*self.r, 0, self.mesh_size)
            p7 = geometry.addPoint(self.r*cos(pi/4), self.r*sin(pi/4), 0, self.mesh_size)
            
            # lines
            l1 = geometry.addLine(p1, p4)
            l2 = geometry.addLine(p4, p2)
            l3 = geometry.addCircleArc(p2, p1, p7)
            l4 = geometry.addCircleArc(p7, p1, p3)
            l5 = geometry.addLine(p3, p5)
            l6 = geometry.addLine(p5, p1)
            l7 = geometry.addLine(p4, p6)
            l8 = geometry.addLine(p5, p6)
            l9 = geometry.addLine(p6, p7)
            
            # curve loops (3 region)
            cl1 = geometry.addCurveLoop([l1, l7, -l8, l6])
            cl2 = geometry.addCurveLoop([l2, l3, -l9, -l7])
            cl3 = geometry.addCurveLoop([l4, l5, l8, l9])
            
            # surfaces
            s1 = geometry.addPlaneSurface([cl1])
            s2 = geometry.addPlaneSurface([cl2])
            s3 = geometry.addPlaneSurface([cl3])
            
            # extrusions
            nz = floor(self.t/self.mesh_size)
            geometry.extrude([(2, s1), (2, s2), (2, s3)], 0, 0, self.t, [nz], recombine=True)
            geometry.synchronize()
            
            # Meshing
            meshgen = gmsh.model.mesh
            
            # transfinite curves
            nx = floor(0.5*self.r/self.mesh_size)
            for c in [l1, l2, l3, l4, l5, l6, l7, l8, l9]:
                meshgen.setTransfiniteCurve(c, nx)
            
            # transfinite surface
            for s in [s1, s2, s3]:
                meshgen.setTransfiniteSurface(s)
                
            # meshgen
            meshgen.generate(2)
            meshgen.recombine()
            meshgen.generate(3)
            
        else:
            pass
        
        # output
        gmsh.write(self.msh_dir)
        gmsh.fltk.run()
        
        gmsh.finalize()