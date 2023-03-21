#https://ezdxf.readthedocs.io/en/stable/addons/openscad.html
import ezdxf
from ezdxf.render.forms import cube, extrude
from ezdxf.addons import openscad, meshex

# create new DXF document
doc = ezdxf.new()
msp = doc.modelspace()

# create same geometric primitives as MeshTransformer() objects
cube1 = cube()
cube2 = cube().translate((1,0,0))

script = openscad.boolean_operation(openscad.UNION, cube1, cube2)
result = openscad.run(script)
with open(f'experiments/twoCubeUnion.obj', "w+") as fp:
    fp.write(meshex.obj_dumps(result))