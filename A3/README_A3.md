# BIManalyst group 24
# Focus Area: Structural
# Claim: The line load for beams can be calculated through cross-sectional area X material density x gravitational acceleration. 
# Report and page number: CES_BLD_24_06_STR Page 11 Table 7
# Brief description: The script takes the dimensions and densities from the property sets and uses them to calculate the line load for the beams.



# A3a: 
# State the problem / claim that your tool is solving.
# The tool adresses the challenge of calculating surface load for building elements based on their dimensions and material properties. 
# The tools automates the process of retrieving necessary information from an IFCmodel such as area, thickness and density.
# This helps structur engineers assess building load requrements more efficently and reduce the effort involved in load analysis. 

# State where you found that problem.
# The problem was identified during the structrural analysis og beam-models, where calculating surface loads manually is time consuming and prone to errors. This issue often arrives in models, where detailed structural analysis is required for compliance with building codes or for optimizing material usage in construction. 

# Description of the tool?  
# The tool is a python script that uses the IFCopenshell liberarie to extract BIM elemnets from an IFCmodel and calculate surface load based on geometric properties (area, thickness and density)
# The script first check if the IFC-file exists, then retrives all Ifcbeam objects extract the necessary dimensions and material properties from the property sets and calculate the dead load and surface load for each beam. 

# Instructions to run the tool.
# Step 1: Install the requred liberarie: Insure that the IFCopenshall and any other dependencies are installed and you can install IFCopenshall using pip. 
# Step 2: Prepare the IFC file: Make sure that you valied IFC-file with beams defined and that the file path in the script match the location of your IFC-file. 
# Step 3: Run the script in Python: Open Python and execute it. The script will output the surface load for each beam. 

# What Advanced Building Design Stage (A,B,C or D) would your tool be usefuL?
# Stage C (Technical Design): The tool is most useful during Stage C, where detailed load calculations and structural checks are essential before finalizing designs.

# Which subjects might use it?
# Structural Engineering: To verify beam loads and structural safety.
# Architecture: To ensure design compatibility with structural requirements.
# Construction Management: To confirm design feasibility and material needs.

# What information is required in the model for your tool to work?
# Beam Geometry: Length and cross-sectional area. Material Properties: Density and type. Property Sets: Beam dimensions and material assignments in IfcPropertySets.
