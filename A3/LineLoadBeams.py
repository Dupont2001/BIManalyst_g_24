import ifcopenshell.util.element
from pathlib import Path
from bonsai.bim.ifc import IfcStore

g = 9.81  # Gravitational acceleration in m/s²

def checkRule(model):
    beams = []
    
    # Collect beams with "DR22-250" in their name
    for beam in model.by_type("IfcBeam"):
        if "DR22-250" in beam.Name:
            beams.append(beam)
    
    if not beams:
        return ["No beams with 'DR22-250' found."]
    
    print(f"Number of beams found with 'DR22-250': {len(beams)}")
    
    # Dictionary to group beams with identical properties
    beam_groups = {}
    
    # Iterate over each qualifying beam
    for beam in beams:
        print(f"\nProcessing beam '{beam.GlobalId}'")
        
        psets = ifcopenshell.util.element.get_psets(beam)
        
        # Initialise values and density
        b = h = density = elevation_top = None
        
        # Attempt to get values from 'Dimensions' property set
        if 'Dimensions' in psets:
            dims = psets['Dimensions']
            
            # Get values to calculate thickness
            b = dims.get('b')
            h = dims.get('h')
            elevation_top = dims.get('Elevation at Top')
            
        # Attempt to get density from 'Materials and Finishes' property set
        if 'Materials and Finishes' in psets:
            materials = psets['Materials and Finishes']
            structural_material = materials.get('Structural Material')
            
            # Set density based on the structural material
            if "DR22-250" in beam.Name:
                density = 2400  # Density in kg/m³ for DR22-250
            else:
                density = 7700  # Density in kg/m³ for Steel
                
        # Check if all necessary values are available
        if b is not None and h is not None and density is not None and elevation_top is not None:
            # Convert values to metres
            b_m = b / 1000.0  # Convert mm to m
            h_m = h / 1000.0
            
            # Calculate the area in square metres
            area_m2 = b_m * h_m  # Area in m²
            
            # Calculate dead load in Newtons
            line_load_n = area_m2 * density * g  # Dead load in N/m
            
            # Create a unique key for beams with the same properties
            key = (elevation_top, area_m2, density, line_load_n)
            
            # Append beam GlobalId to the group of beams with the same key
            if key not in beam_groups:
                beam_groups[key] = {
                    "global_ids": [],
                    "b": b,
                    "h": h,
                    "elevation_top": elevation_top,
                    "area_m2": area_m2,
                    "density": density,
                    "line_load_n": line_load_n,
                    "structural_material": structural_material
                }
            beam_groups[key]["global_ids"].append(beam.GlobalId)
        
        else:
            print(f"  Beam '{beam.GlobalId}' has insufficient data for area or density calculation.")
    
    # Print the grouped results
    for properties, data in beam_groups.items():
        global_ids = ', '.join(data["global_ids"])
        print(f"\nBeams '{global_ids}' have identical properties:")
        print(f"  - b (width): {data['b']}")
        print(f"  - h (height): {data['h']}")
        print(f"  - Elevation at Top: {data['elevation_top']}")
        print(f"  - Structural Material: {data['structural_material']}")
        print(f"  - Calculated Area: {data['area_m2']:.6f} m²")
        print(f"  - Density: {data['density']} kg/m³")
        print(f"  - Line Load: {data['line_load_n']:.2f} N/m")

# Load the model
model_path = Path("C:/Users/psdup/OneDrive - Danmarks Tekniske Universitet/Kandidat/1. Semester/BIM2/CES_BLD_24_06_STR.ifc")
if not model_path.is_file():
    raise FileNotFoundError(f"No file found at {model_path}!")

model = ifcopenshell.open(model_path)

if model:
    checkRule(model)
else:
    print("Failed to load IFC model.")
