import ifcopenshell

def checkRule(model):
    windows = model.by_type('IfcWindow')

    result = f"Windows: {len(windows)}"

    return result

