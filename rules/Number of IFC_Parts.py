import ifcopenshell
from bonsai.bim.ifc import IfcStore 
file = IfcStore.get_file()

Beams = file.by_type('IfcBeam')
Columns = file.by_type('IfcColumn')
Walls = file.by_type('IfcWall')
Stairs = file.by_type('IfcStair')
Slabs = file.by_type('IfcSlab')
Railings = file.by_type('IfcRailing')
Coverings = file.by_type('IfcCovering')
Ramps = file.by_type('IfcRamp')
Stairflights = file.by_type('IfcStairFlight')


print("Number of Beams:", len(Beams))
print("Number of Columns:", len(Columns))
print("Number of Walls:", len(Walls))
print("Number of Stairs:", len(Stairs))
print("Number of Slabs:", len(Slabs))
print("Number of Railings:", len(Railings))
print("Number of Coverings:", len(Coverings))
print("Number of Ramps:", len(Ramps))
print("Number of Stairflights:", len(Stairflights))


