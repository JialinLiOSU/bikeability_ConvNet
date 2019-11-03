# check whether vehicle is in the lane polygon
from geom import point_in_polygon
from point_in_polygon import pip_cross
from point_in_polygon import *
from geom.point import *
from lane_width import *
import csv
import json

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

def swap (a,b):
    temp = a
    a = b
    b = temp
    return a, b

if __name__ == '__main__': 
    # read object detection results pickles "results"
    # read filtered polygon results pickles "polygons"
    
    # pgon = polygons[i]

    # bbox = [7,6,11,2]
    # pgon = [[0,0],[4,4],[8,4],[4,0],[0,0]]
    # pgon = [[Point(p[0],p[1]) for p in pgon]]
    # test = vehicleInPolygon(bbox,pgon)
    # print(test)
    bboxInfo = []
    results = []
    path = 'C:\\Users\\jiali\\Desktop\\bikeability_ConvNet\\data\\results\\json\\'
    with open(path + '239_n_tvN2Q9V4G7TbqXs-wHZg_191_2016_8_forward.json','r') as f:
        distros_dict = json.load(f)
        for distro in distros_dict:
            print(distro['Name'])
        # for row in csv_reader:
        #     if row[0]['class_ids'] == 3:
        #         bboxInfo.append(row[0])
        #         results.append(row[0]['rois'])

    polyIdx, polygonsTemp, widthTemp = compare_widths(pgonsLuyu)

    if widthTemp[0] > widthTemp[1] :
        widthTemp[0], widthTemp[1] = swap(widthTemp[0], widthTemp[1])
        polyIdx[0], polyIdx[1] = swap(polyIdx[0], polyIdx[1])
        polygonsTemp[0], polygonsTemp[1] = swap(polygonsTemp[0], polygonsTemp[1])

    (pgon,IsOtherPgonExld) = returnPgon(results,polygonsTemp)
    listIndBbox = []
    for i in range(len(results)): # i --- index of bbox
        vip = vehicleInPolygon(results[i],pgon)
        listIndBbox.append(i)
    


