# check whether vehicle is in the lane polygon
from geom import point_in_polygon
from point_in_polygon import pip_cross
from point_in_polygon import *
from geom.point import *

def vehicleInPolygon(bbox, pgon):
    xMin = bbox[0]
    yMin = bbox[3]
    xMax = bbox[2]
    yMax = bbox[1]
    p1 = [xMin, yMin]
    p1 = Point(p1[0], p1[1])
    p2 = [xMax, yMin]
    p2 = Point(p2[0], p2[1])
    p1InPolygon = pip_cross2(p1, pgon)
    p2InPolygon = pip_cross2(p2, pgon)
    if p1InPolygon[0] and p2InPolygon[0]:
        return True
    else:
        [tenthPoint1,tenthPoint2]= calTwoTenthPoint(p1, p2)
        tenthPoint1 = Point(tenthPoint1[0],tenthPoint1[1])
        tenthPoint2 = Point(tenthPoint2[0],tenthPoint2[1])
        tenthPoint1InPolygon = pip_cross2(tenthPoint1, pgon)
        tenthPoint2InPolygon = pip_cross2(tenthPoint2, pgon)
        if tenthPoint1InPolygon[0] and tenthPoint2InPolygon[0]:
            return True
        else: 
            return False

def calTwoTenthPoint(p1, p2):
    deltaX = (p1[0]-p2[0])
    deltaY = (p1[1]-p2[1])
    tenthPoint1X = p2[0] + deltaX/10
    tenthPoint1Y = p2[1] + deltaY/10
    tenthPoint1 = [tenthPoint1X, tenthPoint1Y]

    tenthPoint2X = p2[0] + deltaX * 9 / 10
    tenthPoint2Y = p2[1] + deltaY * 9 / 10
    tenthPoint2 = [tenthPoint2X, tenthPoint2Y]
    return [tenthPoint1,tenthPoint2]

def returnPgon(results,polygons):
    # return (polygon, Exclude the other polygon)
    pgon = polygons[0]
    count = 0
    for i in range(len(results)):
        vip = vehicleInPolygon(results[i],pgon)
        if vip:
            count += 1
        if count >= 2:
            return (polygons[1], True)
    return (polygons[0],False)

if __name__ == '__main__': 
    # read object detection results pickles "results"
    # read filtered polygon results pickles "polygons"
    
    # pgon = polygons[i]

    # bbox = [7,6,11,2]
    # pgon = [[0,0],[4,4],[8,4],[4,0],[0,0]]
    # pgon = [[Point(p[0],p[1]) for p in pgon]]
    # test = vehicleInPolygon(bbox,pgon)
    # print(test)
    (pgon,IsOtherPgonExld) = returnPgon(results,polygons)
    listIndBbox = []
    for i in range(len(results)): # i --- index of bbox
        vip = vehicleInPolygon(results[i],pgon)
        listIndBbox.append(i)
    


