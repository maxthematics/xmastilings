import cadquery as cq

# parameter
height = 70
width = 70
branchNo = 3
thickness = 5



# geometry calculations
branchHeight = height/branchNo
branchWidthUnit = width/(2*(branchNo+1))


decofactor = .8
decoskip = (1-decofactor)/2
decoWidth = .5*branchWidthUnit

def makeTreeList():
    treeVertices = [(-2*branchWidthUnit,branchHeight), (0,0), (2*branchWidthUnit,branchHeight)]
    for b in range(1,branchNo):
        bx1 = b*branchWidthUnit
        bx2 = (b+2)*branchWidthUnit
        by1 = b*branchHeight
        by2 = (b+1)*branchHeight
        left = [(-bx2, by2), (-bx1,by1)]
        right = [(bx1, by1), (bx2,by2)]
        treeVertices = left + treeVertices + right
    return treeVertices

def makeDeco(x,y,side):
    if (side == "r"): 
        sign = (-1)
    else:
        sign = 1
    slope =branchHeight/(2*branchWidthUnit)
    xtop = x-(1.5*decofactor)*branchWidthUnit
    ytop = y+slope*(xtop-x)
    deco = [
        (sign*x,y),
        (sign*(x-decoWidth), y),
        (sign*(xtop-decoWidth), ytop),
        (sign*xtop, ytop)
        ]
    return deco



def makeDecoWire():
    decoWires = []
    for b in range (0, branchNo):
        for s in ["r","l"]:
            deco = makeDeco((b+2)*branchWidthUnit-(5*decoskip)*branchWidthUnit, (b+1)*branchHeight-decoskip*branchHeight, s)
            decoWire = cq.Workplane("XY").polyline(deco).close().val()
            decoWires.append(decoWire)
    return decoWires


#wireDeco = cq.Workplane("XY").polyline(deco).close()

mytree = makeTreeList();
mydeco = makeDecoWire();
decoSolid = cq.Workplane("XY").newObject(mydeco).toPending().extrude(thickness)

wireTree = cq.Workplane("XY").polyline(mytree).close()
treeSolid = wireTree.extrude(thickness) 


show_object(mydeco)
show_object(wireTree)



#sym axis
axisWidth = 1.5

axis_block = (
    cq.Workplane("XY")
    .center(0, height / 2)
    .rect(axisWidth, 0.9 * height, centered=(True, True))
    .extrude(thickness/2)
)

decoWithAxis = decoSolid.union(axis_block)


treeWithSymAxis = (
        treeSolid
        .faces(">Z or <Z")
        .edges()
        .chamfer(.8)
        .cut(decoWithAxis)
    )





show_object(treeWithSymAxis, options={"color": (0, 255, 0), "alpha": 1.0})
show_object(decoWithAxis, options={"color": (0, 136, 0), "alpha": 1.0})