import ifcopenshell  # Import IFCOpenShell

# Konstant for tyngdeacceleration (i meter per sekund kvadrat)
g = 9.81

# Funktion til at beregne overfladelast for en slab
def beregn_surface_load(area, thickness, densitet):
    # Konverter tykkelse fra mm til meter
    thickness_m = thickness / 1000.0
    volumen = area * thickness_m
    dead_load = g * densitet * volumen
    surface_load = dead_load / area
    return dead_load, surface_load

# Funktion til at hente dimensioner fra property sets
def get_dimensions_from_psets(slab):
    psets = ifcopenshell.util.element.get_psets(slab, psets_only=True)
    
    # Hent dimensioner fra 'Dimensions' property set
    if 'Dimensions' in psets:
        dims = psets['Dimensions']
        area = dims.get('Area')           # Hent fra IFC, hvis ikke tilgængelig, returner None
        thickness = dims.get('Thickness') # Hent fra IFC, hvis ikke tilgængelig, returner None
        if area is not None and thickness is not None:
            return float(area), float(thickness)
    return None, None

# Funktion til at hente densitet fra property sets
def get_material_density_from_psets(slab):
    psets = ifcopenshell.util.element.get_psets(slab, psets_only=True)
    
    # Hent densitet fra 'Materials and Finishes' property set
    if 'Materials and Finishes' in psets:
        pset = psets['Materials and Finishes']
        material = pset.get('Structural Material')
        if material is not None:
            # Returner densitet baseret på materialet, her kræves en mapping eller en specifik regel
            if material == 'Concrete 16':
                return 2400  # kg/m³ for Concrete 16, kan tilpasses hvis du har en mere præcis metode
    return None

# Funktion til at beregne overfladelast for slabs i modellen
def checkRule(model):
    # Hent alle objekter af typen IfcSlab
    slabs = model.by_type('IfcSlab')
    
    results = []
    
    for slab in slabs:
        # Hent dimensioner og densitet
        area, thickness = get_dimensions_from_psets(slab)
        densitet = get_material_density_from_psets(slab)

        if area is not None and thickness is not None and densitet is not None:
            # Beregn overfladelast
            dead_load, surface_load = beregn_surface_load(area, thickness, densitet)

            # Formatér resultatet
            result = (f"Slab '{slab.GlobalId}': "
                      f"Dimensions (Area x Thickness): {area:.2f} m² x {thickness:.2f} mm, "
                      f"Dead load (G_k): {dead_load:.2f} N, "
                      f"Surface load: {surface_load:.2f} N/m²")
            results.append(result)
        else:
            results.append(f"Slab '{slab.GlobalId}' mangler nødvendige dimensioner eller densitet.")

    return results
