#https://ezdxf.readthedocs.io/en/stable/addons/openscad.html
import ezdxf
from ezdxf.render.forms import cube, extrude
from ezdxf.addons import openscad, meshex

# create new DXF document
doc = ezdxf.new()
msp = doc.modelspace()

# create same geometric primitives as MeshTransformer() objects
cube1 = cube()
slant = cube()

views = ["Full", "TopLeft", "TopRight", "BottomLeft", "BottomRight"]
front = [(0.5,-0.5,0.5), (-0.5,-0.5,0.5), (-0.5,0.5,0.5),(0.5,0.5,0.5)]
side = [(0.5,-0.5,-0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5),(0.5,0.5,-0.5)]
top = [(0.5,-0.5,-0.5), (-0.5,-0.5,-0.5), (-0.5,-0.5,0.5),(0.5,-0.5,0.5)]
tris = [[],[0,1,2],[3,0,1],[1,2,3],[2,3,0]]

def CreateTriPath(tri, verts):
    return [verts[tri[0]], verts[tri[1]], verts[tri[2]]]

result = cube1
for frontView in range(5):
    frontViewName = views[frontView]
    if frontView != 0:
        frontShape = extrude(CreateTriPath(tris[frontView], front), [(0, 0, 0.5),(0 ,0 ,-0.5)],True,True)
    for sideView in range(5):
        sideViewName = views[sideView]
        if sideView != 0:
            sideShape = extrude(CreateTriPath(tris[sideView], side), [(0.5, 0, 0),(-0.5, 0, 0)],True,True)
        for topView in range(5):
            topViewName = views[topView]
            if topView != 0:
                topShape = extrude(CreateTriPath(tris[topView], top), [(0, -0.5, 0),(0, 0.5, 0)],True,True)
            result = cube1
            if frontViewName != "Full":
                script = openscad.boolean_operation(openscad.DIFFERENCE, result, frontShape)
                result = openscad.run(script)
            if sideViewName != "Full":
                script = openscad.boolean_operation(openscad.DIFFERENCE, result, sideShape)
                result = openscad.run(script)
            if topViewName != "Full":
                script = openscad.boolean_operation(openscad.DIFFERENCE, result, topShape)
                result = openscad.run(script)
            with open(f'temp/{frontViewName}-front.obj', "w+") as fp:
                if frontViewName != "Full":
                    fp.write(meshex.obj_dumps(frontShape))
            with open(f'temp/{sideViewName}-side.obj', "w+") as fp:
                if sideViewName != "Full":
                    fp.write(meshex.obj_dumps(sideShape))
            with open(f'temp/{topViewName}-top.obj', "w+") as fp:
                if topViewName != "Full":
                    fp.write(meshex.obj_dumps(topShape))
            with open(f'results/{frontViewName}-{sideViewName}-{topViewName}.obj', "w+") as fp:
                fp.write(meshex.obj_dumps(result))