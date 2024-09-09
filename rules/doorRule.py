import ifcopenshell

def checkRule(model):
    doors = model.by_type('IfcDoor')

    result = f"Doors: {len(doors)}"

    return result

