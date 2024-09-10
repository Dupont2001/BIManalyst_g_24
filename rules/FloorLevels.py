import ifcopenshell
from bonsai.bim.ifc import IfcStore

# Load the IFC file
file = IfcStore.get_file()

# Get all IfcBuildingStorey objects
data = file.by_type('IfcBuildingStorey')

print("Number of Floor Levels:", len(data))

# Extract the level elevation from each IfcBuildingStorey object and count how many are greater than 0
count = 0
for storey in data:
    elevation = storey.Elevation
    if elevation > 0:
        count += 1

print("Highest Floor Level:", count)
