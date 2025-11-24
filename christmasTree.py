import cadquery as cq

# parameter
height = 40
width = 40
branchNo = 3
thickness = 2


# geometry calculations
branchHeight = height/branchNo
branchWidthUnit = width/(2*(branchNo+1))


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

mytree = makeTreeList();

wireTree = cq.Workplane("XY").polyline(mytree).close()
treeSolid = wireTree.extrude(thickness) 


#sym axis
axisWidth = .6
axisDepth = .2

z_bottom = thickness - axisDepth
tol = 0.02
bottom_sel = cq.selectors.BoxSelector(
    (-axisWidth*1.1, -height*2, z_bottom - tol),
    ( axisWidth*1.1,  height*2, z_bottom + tol),
    boundingbox=False
)

treeWithSymAxis = (
        treeSolid
        .faces(">Z or <Z")
        .edges()
        .chamfer(.3)
        .faces(">Z").workplane(centerOption = "CenterOfBoundBox")
        .rect(axisWidth, .9*height, centered = (True, True))
        .cutBlind(-axisDepth)
        .edges("|Y")
        .edges(bottom_sel)
        .fillet(.1)
    )

show_object(treeWithSymAxis, options={"color": (0, 255, 0), "alpha": 1.0})