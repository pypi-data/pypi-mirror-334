from dataclasses import dataclass, fields
from collections.abc import Mapping

from ._patch import (
      _patch as patch,
      layer,
      SectionGeometry
)

class Mesh:
    nodes: list
    elems: list

class Material:
    pass 

@dataclass
class _Fiber(Mapping):
    location: tuple
    area:     float
    warp:     list

    def __getitem__(self, key):
        # Allows accessing attributes by key.
        if key == "y":
            return self.location[0]
        elif key == "z":
            return self.location[1]
        else:
            try:
                return getattr(self, key)
            except AttributeError:
                raise KeyError(key)

    def __iter__(self):
        # Iterate over field names.
        return iter(["y", "z", "area", "warp"])

    def __len__(self):
        # Number of fields.
        return 4
    

@dataclass
class _Element:
    nodes: tuple # of int
  # gauss: tuple # of Gauss
    shape: str
    model: dict = None

@dataclass
class BasicSection(Mapping):
    iczy: float
    icyy: float
    iczz: float
    area: float

    def __getitem__(self, key):
        # Allows accessing attributes by key.
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __iter__(self):
        # Iterate over field names.
        return (f.name for f in fields(self))

    def __len__(self):
        # Number of fields.
        return len(fields(self))

    def centroid(self):
        pass

    def translate(self, location):
        pass


def create_mesh(patches: list, mesh_size: list=None):
    from .solvers import TriangleModel
    from .mesh import sect2gmsh
    mesh = sect2gmsh(patches, mesh_size)
    # meshio object, all tri3s
    GaussT3 = None
    nodes = mesh.points
    elems = [
        _Element(nodes=cell, shape="T3") for cell in mesh.cells[1].data
    ]
    return TriangleModel(nodes, elems) 


def _extract_model(geometry, size)->tuple:
    from .mesh import sect2gmsh
    nodes = {}
    elems = []

    mesh = sect2gmsh(geometry, size)
    # meshio object, all tri3s
    GaussT3 = None
    nodes = mesh.points
    elems = [
        _Element(nodes=cell, gauss=GaussT3, shape="T3") for cell in mesh.cells[1].data
    ]

    return nodes, elems, mesh

def _extract_fibers(geometry, nwarp:int = 0)->list:
    fibers = []
    if isinstance(geometry, list):
        for item in geometry:
            if True:
                fibers.append(_Fiber())

    return fibers

class GeneralSection:
    mesh: "Mesh"

    torsion: "TorsionAnalysis"
    flexure: "FlexureAnalysis"

    _exterior: "list" # of points representing a ring
    _interior: "list" # of rings

    _point_fibers: "list" # of Fiber

    def __init__(self, geometry,
                 warp_twist=True, 
                 warp_shear=True
        ):
        from .solvers import PlaneMesh, TriangleModel, TorsionAnalysis, FlexureAnalysis

        if isinstance(geometry, PlaneMesh):
            self.mesh = geometry
        else:
            nodes, elems, _ = _extract_model(geometry)
            self.mesh = TriangleModel(nodes, elems)

        self._warp_shear:bool = warp_shear 
        self._warp_twist:bool = warp_twist

        nwarp = 0
        if warp_twist:
            nwarp += 1
            self.torsion = TorsionAnalysis(self.mesh)
            # Update fibers
        else:
            self.torsion = None

        if warp_shear is True:
            nwarp += 2
            self.flexure = FlexureAnalysis(self.mesh)
            # Update fibers
        else:
            self.flexure = None

        self._point_fibers = _extract_fibers(geometry, nwarp=nwarp)

    def exterior(self):
        return self.mesh.exterior()

    def interior(self):
        return self.mesh.interior()
    
    def centroid(self):
        return self.torsion.centroid()

    def summary(self, symbols=False):
        s = ""
        tol=1e-13
        A = self.torsion.cnn()[0,0]

        cnw = self.torsion.cnw()
        cnm = self.torsion.cnm()
        Ay = cnm[0,1] # int z
        Az = cnm[2,0] # int y
        # Compute centroid
        cx, cy = float(Az/A), float(Ay/A)
        cx, cy = map(lambda i: i if abs(i)>tol else 0.0, (cx, cy))

        cmm = self.torsion.cmm()
        cmw = self.torsion.cmw()
        cnv = self.torsion.cnv()

        Ivv = self.torsion.cvv()[0,0]
        cmv = self.torsion.cmv()
        # Irw = self.torsion.cmv()[0,0]

        sx, sy = self.torsion.shear_center()
        sx, sy = map(lambda i: i if abs(i)>tol else 0.0, (sx, sy))

        cww = self.torsion.cww()
        # Translate to shear center to get standard Iww
        Iww = self.translate([sx, sy]).torsion.cww()[0,0]

        Isv = self.torsion.torsion_constant()

        s += f"""
  [nn]    Area               {A          :>10.4}
  [nm]    Centroid           {0.0        :>10.4}  {cx         :>10.4}, {cy         :>10.4}
  [nw|v]                     {cnw[0,0]/A :>10.4}  {cnv[1,0]/A :>10.4}, {cnv[2,0]/A :>10.4}

  [mm]    Flexural moments   {cmm[0,0]   :>10.4}  {cmm[1,1]   :>10.4}, {cmm[2,2]   :>10.4}, {cmm[1,2] :>10.4}
  [mv|w]                     {cmv[0,0]   :>10.4}  {cmw[1,0]   :>10.4}, {cmw[2,0]   :>10.4}

          Shear center       {0.0        :>10.4}  {sx         :>10.4}, {sy :>10.4}

  [ww]    Warping constant   {cww[0,0] :>10.4}  ({Iww      :>10.4} at S.C.)
          Torsion constant   {Isv :>10.4}
  [vv]    Bishear            {Ivv :>10.4}
        """

        return s


    def add_to(self, model, tag):
        pass

    def translate(self, offset):
        # TODO: translate fibers
        return GeneralSection(self.mesh.translate(offset),
                              warp_shear=self._warp_shear,
                              warp_twist=self._warp_twist,
                              ) 

    def rotate(self, angle):
        # TODO: rotate fibers
        return GeneralSection(self.mesh.rotate(angle),
                              warp_shear=self._warp_shear,
                              warp_twist=self._warp_twist,
                              ) 

    def linearize(self)->BasicSection:
        import numpy as np
        y, z = self.mesh.nodes.T
        e = np.ones(y.shape)
        return BasicSection(
            area=self.mesh.inertia(e, e),
            iczy=self.mesh.inertia(y, z),
            icyy=self.mesh.inertia(z, z),
            iczz=self.mesh.inertia(y, y)
        )

    def integrate(self, f: callable):
        pass

    def fibers(self, origin=None, center=None):
        if origin is not None:
            if origin == "centroid":
                yield from self.translate(self.torsion.centroid()).fibers(center=center)
            elif origin == "shear-center":
                yield from self.translate(self.torsion.shear_center()).fibers(center=center)
            else:
                yield from self.translate(origin).fibers(center=center)
            return

        for fiber in self._point_fibers:
            yield fiber

        model = self.mesh

        if center is None:
            twist = self.torsion
            w = self.torsion.solution() #warping() # 
        elif not isinstance(center, str):
            twist = self.translate(center).torsion
            w = twist.solution()
        elif center == "centroid":
            twist = self.translate(self.torsion.centroid()).torsion
            w = twist.solution()
        elif center == "shear-center":
            w = self.torsion.warping()
            twist = self.torsion


        if callable(self._warp_shear):
            psi = self._warp_shear
        else:
            psi = lambda y,z: 0.0

        for i,elem in enumerate(self.mesh.elems):
            # TODO: Assumes TriangleModel
            yz = sum(model.nodes[elem.nodes])/3
            yield _Fiber(
                location=yz,
                area=model.cell_area(i),
                warp=[
                    [twist.model.cell_solution(i, w), *twist.model.cell_gradient(i,  w)],
                    [0, psi(*yz), 0]
                ]
            )

