# check whether vehicle is in the lane polygon
from geom import point_in_polygon
from point_in_polygon import pip_cross
from point_in_polygon import *
from geom.point import *
from lane_width import *
import pickle
import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
    pgon = polygons[0][0]
    pgon = [[Point(p[0],p[1]) for p in pgon]]
    count = 0
    for i in range(len(results)):
        vip = vehicleInPolygon(results[i],pgon)
        if vip:
            count += 1
        if count >= 2:
            return (polygons[0][1], True)
    return (polygons[0][0],False)

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
    
    results = []
    path = 'C:\\Users\\li.7957\\Desktop\\bikeability_ConvNet\\data\\'
    # read pickle files about bbox information
    # fileList = os.listdir("somedirectory")
    file_name_p = path + 'results\\json\\13064_iO0Tec5ATvHhLM3niZg6WA_96_2015_8_forward.pickle'
    # for file_name in fileList:
    with open(file_name_p, 'rb') as handle:
        MaskRCNNResults = pickle.load(handle)
    for i in range(MaskRCNNResults['class_ids'].shape[0]):
        if MaskRCNNResults['class_ids'][i] == 3:
            results.append(MaskRCNNResults['rois'][i].tolist())

    # read json file about polygon information
    file_name_j = path + 'street_images_vectorize\\street_images_vectorize\\13064_iO0Tec5ATvHhLM3niZg6WA_96_2015_8_forward.json'
    # for file_name in fileList:
    pgonsLuyu = []
    with open(file_name_j, 'rb') as json_file:
        data_json = json.load(json_file)
    for i in range (len(data_json['features'])):
        pgonsLuyu.append(data_json['features'][i]['geometry']['coordinates'] + [data_json['features'][i]['geometry']['coordinates'][0]])
    pgonsLuyuSwap = []

    for i in range (len(pgonsLuyu)):
        pointList=[]
        for point in pgonsLuyu[i]:
            point = swap(point[0],point[1])
            pointList.append([point[0],point[1]])
        pgonsLuyuSwap.append(pointList)
    polyIdx, polygonsTemp, widthTemp = compare_widths(pgonsLuyu)

    if widthTemp[0] > widthTemp[1] :
        widthTemp[0], widthTemp[1] = swap(widthTemp[0], widthTemp[1])
        polyIdx[0], polyIdx[1] = swap(polyIdx[0], polyIdx[1])
        polygonsTemp[0], polygonsTemp[1] = swap(polygonsTemp[0], polygonsTemp[1])

    (pgon,IsOtherPgonExld) = returnPgon(results,[polygonsTemp])
    pgonPlot = pgon
    pgon = [[Point(p[0],p[1]) for p in pgon]]
    listIndBbox = []
    for i in range(len(results)): # i --- index of bbox
        vip = vehicleInPolygon(results[i],pgon)
        if vip == True:
            listIndBbox.append(i)
    
    print (listIndBbox)
    img=mpimg.imread('C:\\Users\\li.7957\\Desktop\\bikeability_ConvNet\\data\\most_images\\13064_iO0Tec5ATvHhLM3niZg6WA_96_2015_8_forward.jpg')
    p1 = plt.Polygon(pgonsLuyuSwap[2], closed=True, fill=True, facecolor='grey', edgecolor='blue', alpha=0.5)
    ax = plt.gca()
    ax.add_patch(p1)
    imgplot = plt.imshow(img)
    plt.show()

    


