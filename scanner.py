import ezdxf

doc = ezdxf.readfile("template.dxf")
msp = doc.modelspace()

names = set(ent.dxf.name for ent in msp.query("INSERT"))
print("Найденные блоки:", list(names))
