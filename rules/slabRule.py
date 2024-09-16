import ifcopenshell

def checkRule(model):
    slabs = model.by_type('IfcSlab')

    result = f"slabs: {len(slabs)}"

    return result
