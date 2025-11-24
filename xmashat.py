import cadquery as cq
from math import cos, sin, pi, atan2, degrees, hypot
from shapely.geometry import LineString
from shapely.affinity import translate
from shapely import offset_curve


# parameter
radius = 25.0
brimOffset = 7
height = 5


# helper
def hexPntCoord(mp, r, no):
    """
    Point on a regular hex pattern.
    Even indices = vertices at radius r.
    Odd indices  = edge midpoints at radius r*cos(30°).
    East is index 0; step is 30° CCW.
    """
    n = no % 12
    ang = n * (pi/6)
    rad = r if (n % 2 == 0) else r * cos(pi/6)
    return (mp[0] + rad * cos(ang), mp[1] + rad * sin(ang))

def square_on_edge(origin, pA, pB):
    x1, y1 = pA
    x2, y2 = pB
    ex, ey = x2 - x1, y2 - y1
    L = hypot(ex, ey)
    exn, eyn = ex/L, ey/L

    dx, dy = x1 - origin[0], y1 - origin[1]

    n1 = (-eyn, exn)
    n2 = ( eyn,-exn)
    nx, ny = n1 if n1[0]*dx + n1[1]*dy > n2[0]*dx + n2[1]*dy else n2

    nx, ny = -nx, -ny
    p3 = (x2 + nx*L, y2 + ny*L)
    p4 = (x1 + nx*L, y1 + ny*L)
    return [pA, pB, p3, p4]

c1 = (-radius, 0.0)
c2 = (radius * cos(-pi/3), radius * sin(-pi/3))
c3 = (radius * cos( pi/3), radius * sin( pi/3))


hat2D = [
    hexPntCoord(c1, radius, 7),
    hexPntCoord(c1, radius, 8),
    hexPntCoord(c1, radius, 10),
    hexPntCoord(c1, radius, 11),
    c2,
    hexPntCoord(c2, radius, 1),
    hexPntCoord(c2, radius, 2),
    hexPntCoord(c2, radius, 3),
    c3,
    hexPntCoord(c3, radius, 5),
    hexPntCoord(c3, radius, 6),
    hexPntCoord(c1, radius, 3),
    c1
]

brimBottom =[
    hexPntCoord(c1, radius, 7),
    hexPntCoord(c1, radius, 8),
    hexPntCoord(c1, radius, 10),
    hexPntCoord(c1, radius, 11),
    c2,
    hexPntCoord(c2, radius, 1)
]


bottom_ls = LineString(brimBottom)
offset_ls = offset_curve(bottom_ls, brimOffset, join_style="mitre")
brimTop = list(offset_ls.coords)[::-1] 

brim2D = brimBottom + brimTop



pompom2D = square_on_edge(c3, hexPntCoord(c3, radius, 5), hexPntCoord(c3, radius, 6))



wireHat = cq.Workplane("XY").polyline(hat2D).close()
wireBrim = cq.Workplane("XY").polyline(brim2D).close()
wirePomPom = cq.Workplane("XY").polyline(pompom2D).close()

hatOuter = cq.Workplane("XY").polyline(hat2D).close().extrude(height)
filletR = 0.8
hatOuterFilleted = hatOuter.edges(">Z or <Z").fillet(filletR)
filletNeg = hatOuter.cut(hatOuterFilleted)

mid = height/2

# Hut oben/unten
hat_bottom = wireHat.extrude(mid)
hat_top = cq.Workplane("XY").workplane(offset=mid).polyline(hat2D).close().extrude(mid)

# Trim oben/unten
brim_bottom = wireBrim.extrude(mid)
brim_top = cq.Workplane("XY").workplane(offset=mid).polyline(brim2D).close().extrude(mid)

pompom_bottom = wirePomPom.extrude(mid)
pompom_top = cq.Workplane("XY").workplane(offset=mid).polyline(pompom2D).close().extrude(mid)

trim_bottom = brim_bottom.union(pompom_bottom)
trim_top = brim_top.union(pompom_top)

# Hutkern oben/unten
hatCore_bottom = hat_bottom.cut(trim_bottom) 
hatCore_top = hat_top.cut(trim_top)

# Die zwei gewünschten Solids:
redSolid   = hatCore_top.union(trim_bottom).cut(filletNeg)
whiteSolid = trim_top.union(hatCore_bottom).cut(filletNeg)

# Visualisierung
show_object(redSolid,   options={"color": (255,0,0), "alpha":1})
show_object(whiteSolid, options={"color": (255,255,255), "alpha":1})

