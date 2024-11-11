'''python
import ifcopenshell.util.element
from pathlib import Path

g = 9.82  # Gravitational acceleration in m/s²

def checkRule(model):
    beams = []
    
    # Collect beams with specific names
    for beam in model.by_type("IfcBeam"):
        if "DR22-250" in beam.Name:
            beams.append(beam)
        elif "D22-400" in beam.Name:
            beams.append(beam)
        elif "D50-500" in beam.Name:
            beams.append(beam)
        elif "DR26-230" in beam.Name:
            beams.append(beam)
    
    if not beams:
        return ["No beams with specified names found."]
    
    print(f"Number of beams found: {len(beams)}")
    
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
            if "DR22-250" or "D22-400" or "D50-500" or "DR26-230" in beam.Name:
                density = 2400  # Density in kg/m³ for DR22-250
            else:
                density = 7700  # Density in kg/m³ for Steel
                
        # Check if all necessary values are available
        if b is not None and h is not None and density is not None and elevation_top is not None:
            # Convert values to metres
            b_m = b / 1000.0  # Convert mm to m
            h_m = h / 1000.0
            elevation_top_m = elevation_top / 1000.0
            
            # Calculate the area in square metres
            area_m2 = b_m * h_m  # Area in m²
            
            # Calculate dead load in Newtons
            line_load_kn = (area_m2 * density * g) / 1000  # Dead load in kN/m
            
            # Create a unique key for beams with the same properties
            key = (elevation_top_m, area_m2, density, line_load_kn)
            
            # Append beam GlobalId to the group of beams with the same key
            if key not in beam_groups:
                beam_groups[key] = {
                    "global_ids": [],
                    "b": b,
                    "h": h,
                    "elevation_top": elevation_top_m,
                    "area_m2": area_m2,
                    "density": density,
                    "line_load_kn": line_load_kn,
                    "structural_material": structural_material
                }
            beam_groups[key]["global_ids"].append(beam.GlobalId)
        
        else:
            print(f"  Beam '{beam.GlobalId}' has insufficient data for area or density calculation.")
    
    # Print the grouped results
    for properties, data in beam_groups.items():
        global_ids = ', '.join(data["global_ids"])
        beam_type = ""
        
        # Determine the beam type based on the name
        for beam_id in data["global_ids"]:
            beam = model.by_guid(beam_id)
            if "DR22-250" in beam.Name:
                beam_type = "DR22-250"
            elif "D22-400" in beam.Name:
                beam_type = "D22-400"
            elif "D50-500" in beam.Name:
                beam_type = "D50-500"
            elif "DR26-230" in beam.Name:
                beam_type = "DR26-230"
        
        print(f"\nBeams '{global_ids}' have identical properties:")
        print(f"  - Type: {beam_type}")  # This line prints the beam type
        print(f"  - b (width): {data['b']} mm")
        print(f"  - h (height): {data['h']} mm")
        print(f"  - Elevation at Top: {data['elevation_top']} m")
        print(f"  - Structural Material: {data['structural_material']}")
        print(f"  - Calculated Area: {data['area_m2']:.6f} m²")
        print(f"  - Density: {data['density']} kg/m³")
        print(f"  - Line Load: {data['line_load_kn']:.2f} kN/m")

# Load the model
model_path = Path("C:/Users/psdup/OneDrive - Danmarks Tekniske Universitet/Kandidat/1. Semester/BIM2/CES_BLD_24_06_STR.ifc")
if not model_path.is_file():
    raise FileNotFoundError(f"No file found at {model_path}!")

model = ifcopenshell.open(model_path)

if model:
    checkRule(model)
else:
    print("Failed to load IFC model.")
'''
