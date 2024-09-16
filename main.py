import ifcopenshell

#from .rules import windowRule
#from .rules import doorRule
from .rules import slabRule

model = ifcopenshell.open("path/to/ifcfile.ifc")

#windowResult = windowRule.checkRule(model)
#doorResult = doorRule.checkRule(model)
slabResult = slabRule.checkRule(model)

#print("Window result:", windowResult)
#print("Door result:", doorResult)
print("slab result:", slabResult)

