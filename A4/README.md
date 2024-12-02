# [Tutorial Link](https://www.youtube.com/watch?v=ReWDtk9iQa4&ab_channel=MohamadAhmed)

# Introduction: 
The chosen OpenBIM role is "Analyst Level 3", as a standalone Python programme using IfcOpenshell. The tutorial video explains how to correctly calculate the line load for beams in a building.
The selected OpenBIM role focuses on the automation of beam load calculations, designed to demonstrate how to work with BlenderBIM scripting for structural analysis. This introductory script showcases how to filter specific beams based on naming conventions, retrieve key properties like dimensions and material density, and calculate the self-weight load for each beam. It further groups beams with identical properties, providing a summary for easy comparison.

The purpose of this OpenBIM task is to show how BlenderBIM can be used to fill in missing data or perform custom analyses, making it useful for both newcomers and experienced users. By using scripting, the self-weight of beams is calculated accurately and saved, allowing for detailed documentation or further analysis.

This focus on structural load calculations is relevant for engineers and designers aiming to ensure the safety and efficiency of building structures. Proper load calculations contribute to the structural integrity of a building, ensuring that it can withstand applied forces while remaining energy-efficient. Additionally, accurate load calculations help building owners and stakeholders make informed decisions on materials and design, potentially lowering material costs and enhancing sustainability through optimized structural design.

# Guide:
This is a guide on how to install _**Blender**_ and _**Blender Add-ons**_. Additionally, we'll demonstrate how to use a script on an IFC file in Blender BIM.

1. Download and install Blender:
First you have to download [Blender](https://www.blender.org/download/), which is a free and open-source program for 3D authoring. _**Blender**_ works on Linux, Mac, and Windows. You need to choose your preference. Once you have downloaded _**Blender**_, click on the completed download and open the _**Blender**_ setup. Click "Next". Now you will proceed to the "End-User License Agreement", where you accept the terms. Click "Next". In the new window "Custom Setup", click "Next" again. Now you are ready to instal Blender, so click "Install". Once the installation is complete, click "Finish". Now _**Blender**_ is installed as a program on your computer. Open _**Blender**_, where you will need toperform a quick setup. Click "Next". The program is now ready for use.

2. Download BlenderBIM Add-on:
Now we need to install BlenderBIM Add-on _**Bonsai**_.
_**Bonsai**_ is a native building information model authoring platform using IFC based on the IfcOpenShell library.
After Opening Blender, click on **Edit** > **Prederences**.
![Edit](IMG/Edit.png)
Select the **Get Extensions** tab and press **Allow Online Access** on the left. Then search for _**Bonsai**_ in the top left search bar. Now press the **install** bottom to the right. Now _**Bonsai**_ has been installed and you can see it available in your add-ons list. ![Bonsai](IMG/Bonsai.png)

4. Import an IFC-file in Blender:
Now you have to import an IFC-file in Blender. In the upper left corner, you'll find the shortcut 'File.' Select 'Open IFC Project' and choose your preferred model.Your building will now appear.

# Tool to calculate line load for beams:
The Python script without comments

```python
import ifcopenshell.util.element
from pathlib import Path

g = 9.82

def checkRule(model):    
    beams = []    
    
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
        
    beam_groups = {}
    
    for beam in beams:
        print(f"\nProcessing beam '{beam.GlobalId}'")
        
        psets = ifcopenshell.util.element.get_psets(beam)
        
        b = h = density = elevation_top = None
        
        if 'Dimensions' in psets:
            dims = psets['Dimensions']
            
            b = dims.get('b')
            h = dims.get('h')
            elevation_top = dims.get('Elevation at Top')
            
        
        if "DR22-250" or "D22-400" or "D50-500" or "DR26-230" in beam.Name:
            density = 2400  
        else:
            density = 7700  
                
        if b is not None and h is not None and density is not None and elevation_top is not None:
            b_m = b / 1000.0  
            h_m = h / 1000.0
            elevation_top_m = elevation_top / 1000.0
            
            area_m2 = b_m * h_m  
            
            line_load_kn = (area_m2 * density * g) / 1000  
            
            key = (elevation_top_m, area_m2, density, line_load_kn)
            
            if key not in beam_groups:
                beam_groups[key] = {
                    "global_ids": [],
                    "b": b,
                    "h": h,
                    "elevation_top": elevation_top_m,
                    "area_m2": area_m2,
                    "density": density,
                    "line_load_kn": line_load_kn
                }
            beam_groups[key]["global_ids"].append(beam.GlobalId)
        
        else:
            print(f"  Beam '{beam.GlobalId}' has insufficient data for area or density calculation.")
    
    for properties, data in beam_groups.items():
        global_ids = ', '.join(data["global_ids"])
        beam_type = ""
        
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
        print(f"  - Type: {beam_type}")  
        print(f"  - b (width): {data['b']} mm")
        print(f"  - h (height): {data['h']} mm")
        print(f"  - Elevation at Top: {data['elevation_top']} m")
        print(f"  - Calculated Area: {data['area_m2']:.6f} m²")
        print(f"  - Density: {data['density']} kg/m³")
        print(f"  - Line Load: {data['line_load_kn']:.2f} kN/m")

model_path = Path("C:/Users/psdup/OneDrive - Danmarks Tekniske Universitet/Kandidat/1. Semester/BIM2/CES_BLD_24_06_STR.ifc")
if not model_path.is_file():
    raise FileNotFoundError(f"No file found at {model_path}!")

model = ifcopenshell.open(model_path)

if model:
    checkRule(model)
else:
    print("Failed to load IFC model.")
```

Tool Explanation
1. Importing Libraries:
   * `ifc.openshell.util.element`: Provides utility functions for handling IFC elements
   ```python
   import ifcopenshell.util.element
   ```
   * `Path`: Used to manage the file path to the IFC model
   ```python
   from pathlib import Path
   ```
2. Defining Constants:
   * `g`: The gravitational acceleration is assumed to be 9.82 $\frac{m}{s^2}$
   ```python
   g = 9.82
   ```
3. Defining the `checkRule` Function:
   * Beam Collection: Searches for beams named `DR22-250`, `D22-400`, `D50-500` and `DR26-230`. 
   ```python
   def checkRule(model):
       beams = []
    
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
   ```
   * Iteration for each qualifying beam
   1. Property Extraction: For each beam, the script retrieves the "Dimensions" property sets.
   ```python
       beam_groups = {}

       for beam in beams:
           print(f"\nProcessing beam '{beam.GlobalId}'")
        
           psets = ifcopenshell.util.element.get_psets(beam)

           b = h = density = elevation_top = None
        
           if 'Dimensions' in psets:
               dims = psets['Dimensions']
               b = dims.get('b')
               h = dims.get('h')
               elevation_top = dims.get('Elevation at Top')
   ```
   2. Density Assignment: Density is set depending on the beam's structural material. For the given beam types, the density is given as 2400 $\frac{kg}{m^3}$
   ```python
           if "DR-250" or "D22-400" or "D50-500" or "DR26-230" in beam.Name:
               density = 2400
           else:
               density = 7700
   ``` 
   3. Calculation of Properties:
      * Converting measurements from $mm$ to $m$
      * Calculating the cross-sectional area in $m^2$
      * Calculating the line load in $\frac{kN}{m}$ by multiplying area, density and gravitational acceleration
   ```python
           if b is not None and h is not None and density is not None and elevation_top is not None:
               b_m = b / 1000.0 
               h_m = h / 1000.0
               elevation_top_m = elevation_top / 1000.0
            
               area_m2 = b_m * h_m  
            
               line_load_kn = (area_m2 * density * g) / 1000      
   ```         
   4. Grouping Beams: Beams with identical properties are grouped and stored in a dictionary
   ```python
               key = (elevation_top_m, area_m2, density, line_load_kn)

               if key not in beam_groups:
                   beam_groups[key] = {
                       "global_ids": [],
                       "b": b,
                       "h": h,
                       "elevation_top": elevation_top_m,
                       "area_m2": area_m2
                       "density": density,
                       "line_load_kn": line_load_kn
                   }
               beam_groups[key]["global_ids"].append(beam.GlobalId)

           else:
               print(f"  Beam '{beam.GlobalId}' has insufficient data for area or density calculation.")
   ```
4. Displaying the results: The script displays information about each group, such as beam type, dimensions, area, density and calculated line load
```python
       for properties, data in beam_groups.items():
           global_ids = ', '.join(data["global_ids"])
           beam_type = ""
        
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
           print(f"  - Type: {beam_type}")  
           print(f"  - b (width): {data['b']} mm")
           print(f"  - h (height): {data['h']} mm")
           print(f"  - Elevation at Top: {data['elevation_top']} m")
           print(f"  - Calculated Area: {data['area_m2']:.6f} m²")
           print(f"  - Density: {data['density']} kg/m³")
           print(f"  - Line Load: {data['line_load_kn']:.2f} kN/m")
```
5. Loading the IFC Model: The model is loaded from a specified path, with error handling in case the file is missing.
```python
model_path = Path("C:/Users/psdup/OneDrive - Danmarks Tekniske Universitet/Kandidat/1. Semester/BIM2/CES_BLD_24_06_STR.ifc")
if not model_path.is_file():
    raise FileNotFoundError(f"No file found at {model_path}!")

model = ifcopenshell.open(model_path)

if model:
    checkRule(model)
else:
    print("Failed to load IFC model.")
```
Summary of `ifcopenshell` Functions Used
* `open(path): Opens the IFC file`: Opens the IFC file
* `by_type(type_name)`: Finds all elements of a specific type (e.g., IfcBeam)
* `by_guid(guid)`: Retrieves an element by its GlobalId
* `util.element.get.psets(element)`: Retrieves property sets of an element  


