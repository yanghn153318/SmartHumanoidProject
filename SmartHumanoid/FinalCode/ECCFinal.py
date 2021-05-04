# -*- coding: utf-8 -*-

import platform
import numpy as np
import argparse
import cv2
import serial
import time
import sys
from threading import Thread
import csv
import os
import operator
import math
from collections import Counter

# line 315에서 해상도 조절
XY_Point1 = [0, 0]
XY_Point2 = [0, 0]
XY_Point3 = [0, 0]
XY_Point4 = [0, 0]
X_255_point = [0, 0, 0, 0, 0]
Y_255_point = [0, 0, 0, 0, 0]
X_Size = [0, 0, 0, 0, 0]
Y_Size = [0, 0, 0, 0, 0]
Area = [0, 0, 0, 0, 0]
char_arr = []

line_check = 0
line_top_point = 0
line_angle = 0
turn_dir = 106  # turn_dir=0: 라인이 꺾여있지X, turn_dir=105: 라인이 ㄱ자, turn_dir=106: 라인이 ㄱ반대 모양

Angle = 0
length_12 = 0
length_14 = 0

enLT = 1
enCharDetection = 0
enCheckContamination = 0  # enCheckContamination = 1이면, 확진지역인지 아닌지 체크하기
enExit = 0  # enExit = 1이면 탈출

check_dir = 1  # 0: 진행 방향 체크하기 전, 1: 진행 방향 체크 완료

mask = None
frame_roi = None
c = None
minRect = None

roi_num = 2  # 전체화면(0), 상단(1), 하단(2), 하단 오른쪽(3)
citizen_color = 0  # red(1), blue(2)
direction = 106  # 화살표 방향: 왼쪽(106), 오른쪽(105)
check_cardinal_point_1 = 1
check_cardinal_point_2 = 0
cardinal_point = 0  # 방위: N(101), E(102), W(103), S(104)

enMoveCitizen = 0  # enMoveCitizen = 1이면 시민 옮기기 수
citizen_min_area = 1000

room1 = 0
room2 = 0
room3 = 0
room1_name = 0  # 방 이름: A(125), B(130), C(135), D(140)
room2_name = 0
room3_name = 0
room1_color = 0  # green(3), black(4)
room2_color = 0
room3_color = 0
room1_contamination = 0  # 0: 안전, 1: 오염
room2_contamination = 0
room2_contamination = 0
room_name = 0
room_color = 0
room_contamination = 0
contamination = 0  # 오염X(0), 오염O(1)

serial_count = 0
counter = 0
count_max = 1000
# -----------------------------------------------
Top_name = 'mini CTS5 setting'
Frame_time = 0
hsv_Lower = 0
hsv_Upper = 0

hsv_Lower0 = 0
hsv_Upper0 = 0

hsv_Lower1 = 0
hsv_Upper1 = 0

# -----------
# 색 설정
color_str = ["Yellow", "Red", "Blue", "Green", "Black"]
color_bgr = [(0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 0, 255)]  # 노빨파초핑

color_num = [0, 1, 2, 3, 4]  # 노빨파초검

h_max = [130, 100, 70, 80, 30]
h_min = [100, 50, 30, 40, 10]

s_max = [100, 130, 150, 140, 140]
s_min = [70, 100, 120, 110, 100]

v_max = [200, 230, 130, 120, 135]
v_min = [170, 160, 90, 90, 115]

min_area = [10, 10, 10, 40, 40]

now_color = 0
serial_use = 1

serial_port = None
Temp_count = 0
Read_RX = 0

mx, my = 0, 0

threading_Time = 5 / 1000.

Config_File_Name = 'hsv_data.dat'


# XY point 구하는 함수 ---------------------------------------------------------------------------
def get_XY(ObjectColor):
    global frame_roi, W_View_size, H_View_size
    global c, minRect
    global XY_Point1, XY_Point2, XY_Point3, XY_Point4
    global line_angle

    minRect = cv2.minAreaRect(c)  # 물체에 접하는 사각형 정보를 minRect에 저장
    box = cv2.boxPoints(minRect)  # 사각형의 4 꼭짓점을 box에 저장
    box = np.int0(box)  # 꼭짓점의 좌표를 float -> integer형으로 변환

    # 물체에 접하는 사각형(contour) 그리기
    cv2.drawContours(frame_roi, [box], -1, ObjectColor, 3)

    # 화면에 contour의 꼭짓점 표시
    # cv2.circle(frame_roi, (box[0][0], box[0][1]), 10, color_bgr[i], -1)
    # cv2.circle(frame_roi, (box[1][0], box[1][1]), 10, color_bgr[i], -1)
    # cv2.circle(frame_roi, (box[2][0], box[2][1]), 10, color_bgr[i], -1)
    # cv2.circle(frame_roi, (box[3][0], box[3][1]), 10, color_bgr[i], -1)

    # 꼭짓점의 XY 좌표를 255 pixel 단위로 변환하여 저장
    XY_Point1[0] = np.int0((255.0 / W_View_size) * box[0][0])  # 1번째 꼭짓점의 X좌표
    XY_Point1[1] = np.int0((255.0 / H_View_size) * box[0][1])  # 1번째 꼭짓점의 Y좌표
    XY_Point2[0] = np.int0((255.0 / W_View_size) * box[1][0])  # 2번째 꼭짓점의 X좌표
    XY_Point2[1] = np.int0((255.0 / H_View_size) * box[1][1])  # 2번째 꼭짓점의 Y좌표
    XY_Point3[0] = np.int0((255.0 / W_View_size) * box[2][0])  # 3번째 꼭짓점의 X좌표
    XY_Point3[1] = np.int0((255.0 / H_View_size) * box[2][1])  # 3번째 꼭짓점의 Y좌표
    XY_Point4[0] = np.int0((255.0 / W_View_size) * box[3][0])  # 4번째 꼭짓점의 X좌표
    XY_Point4[1] = np.int0((255.0 / H_View_size) * box[3][1])  # 4번째 꼭짓점의 Y좌표

    length_12 = GetLengthTwoPoints(XY_Point1, XY_Point2)
    length_14 = GetLengthTwoPoints(XY_Point1, XY_Point4)

    # 라인의 각도 line_angle 구하기
    if length_12 > length_14:
        line_angle = GetAngleTwoPoints(XY_Point1, XY_Point2)
    else:
        line_angle = GetAngleTwoPoints(XY_Point1, XY_Point4)

    # contour의 무게중심값을 255_point 변수에 저장
    center_X = np.int0((XY_Point1[0] + XY_Point2[0] + XY_Point3[0] + XY_Point4[0]) / 4)
    center_Y = np.int0((XY_Point1[1] + XY_Point2[1] + XY_Point3[1] + XY_Point4[1]) / 4)

    # 화면에 contour의 무게중심 표시
    cv2.circle(frame_roi, (np.int0((W_View_size / 255.5) * X), np.int0((H_View_size / 255.5) * Y)),
               10, ObjectColor, -1)

    return center_X, center_Y


# 라인트레이싱 함수 --------------------------------------------------------------------------------
def line_tracing(X, Y, A):
    global frame_roi, roi_num
    global XY_Point1, XY_Point2, XY_Point4, line_angle
    global direction, room3
    global serial_port, serial_count, count_max
    global enExit, enCharDetection, enLT

    # 라인이 90도 꺾여 있으면 방으로...
    # 이 때 y좌표 측정해서 조건문에 넣어야 함
    if line_angle < -40 and X < 110:  # 라인이 왼쪽으로 비스듬하게 위치
        draw_str2(frame_roi, (3, 120), 'start character detection')
        # print("\n", XY_Point2[0])
        print("라인이 왼쪽으로 90도 꺾임")

        time.sleep(6)
        for serial_count in range(10):
            TX_data(serial_port, 204)  # 명령_고개들고 방인식
        serial_count = 0
        # time.sleep(1)

        roi_num = 0  # 관심 영역: 화면 전체로 설정 -> 방 알파벳 인식 하려고..
        turn_dir = 105
        enCharDetection = 1  # 방 문자 인식(ABCD)
        enLT = 0  # 라인 트레이싱 중지
        print("라인트레이싱 중지")

    elif line_angle > 40 and X > 150:  # 라인이 오른쪽으로 비스듬하게 위치
        draw_str2(frame_roi, (3, 120), 'start character detection')
        # print("\n", XY_Point2[0])
        print("라인이 오른쪽으로 90도 꺾임")

        time.sleep(6)
        for serial_count in range(10):
            TX_data(serial_port, 203)  # 명령_고개들고 방인식
        serial_count = 0
        # time.sleep(1)

        roi_num = 0  # 관심 영역: 화면 전체로 설정 -> 방 알파벳 인식 하려고..
        turn_dir = 106
        enCharDetection = 1  # 방 문자 인식(ABCD)
        enLT = 0  # 라인 트레이싱 중지
        print("라인트레이싱 중지")

    # 라인이 로봇의 중심에 오도록 조정하며 따라가기
    elif line_angle < -15 and line_angle > -40:  # 라인이 왼쪽으로 비스듬하게 위치
        draw_str2(frame_roi, (3, 120), 'turn left 20 degree')
        print("왼쪽턴 20")

        TX_data(serial_port, 111)  # 명령_왼쪽턴 20도
        TX_data(serial_port, 10)
        TX_data(serial_port, 10)
        time.sleep(0.5)

    elif line_angle > 15 and line_angle < 40:  # 라인이 오른쪽으로 비스듬하게 위치
        draw_str2(frame_roi, (3, 120), 'turn right 20 degree')
        print("오른쪽턴 20")

        TX_data(serial_port, 112)  # 명령_오른쪽턴 20도
        TX_data(serial_port, 10)
        TX_data(serial_port, 10)
        time.sleep(0.5)

    elif X > 0 and X < 107:  # 라인이 왼쪽에 위치하면
        draw_str2(frame_roi, (3, 120), 'go left')
        print("왼쪽으로 이동")

        TX_data(serial_port, 115)  # 명령_왼쪽으로 이동
        TX_data(serial_port, 10)
        TX_data(serial_port, 10)
        time.sleep(0.5)

    elif X >= 107 and X <= 147:  # 라인이 중심에 위치하면
        draw_str2(frame_roi, (3, 120), 'go straight')
        print("직진")

        TX_data(serial_port, 110)  # 명령_직진
        TX_data(serial_port, 10)
        TX_data(serial_port, 10)
        time.sleep(0.5)

    elif X > 147 and X <= 255:  # 라인이 오른쪽에 위치하면
        draw_str2(frame_roi, (3, 120), 'go right')
        print("오른쪽으로 이동")

        TX_data(serial_port, 120)  # 명령_오른쪽으로 이동
        TX_data(serial_port, 10)
        TX_data(serial_port, 10)
        time.sleep(0.5)

    # 모든 미션 수행 후 나가기
    elif (X > 147 and Y > 100 and Y < 157 and A > 15000 and direction == 105 and room3 == 1):
        print("오른쪽 문 열고 탈출")
        time.sleep(4)
        for serial_count in range(count_max):  # 명령_오른쪽으로 90도 회전 + 문열기
            TX_data(serial_port, 205)
        print("serial count end")
        serial_count = 0
        time.sleep(3)

        enExit = 1
        enCharDetection == 1
        enLT = 0
        roi_num = 0  # 화면 영역: 전체

    elif (X < 107 and Y > 100 and Y < 157 and A > 15000 and direction == 106 and room3 == 1):
        print("왼쪽 문 열고 탈출")
        time.sleep(4)
        for serial_count in range(count_max):  # 명령_왼쪽으로 90도 회전 + 문열기
            TX_data(serial_port, 206)
        print("serial count end")
        serial_count = 0
        time.sleep(3)

        enExit = 1
        enCharDetection == 1
        enLT = 0
        roi_num = 0  # 화면 영역: 전체


# 문자 머신러닝을 위한 변수 --------------------------------------------------------------------------
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


# 문자 머신러닝을 위한 클래스 -------------------------------------------------------------------------
class ContourWithData():
    # member variables
    npaContour = None  # contour
    boundingRect = None  # bounding rect for contour
    intRectX = 0  # bounding rect top left corner x location
    intRectY = 0  # bounding rect top left corner y location
    intRectWidth = 0  # bounding rect width
    intRectHeight = 0  # bounding rect height
    fltArea = 0.0  # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):  # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):  # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False  # much better validity checking would be necessary
        return True


# 미리 제작해 둔 training_chars_2.png 파일로 문자 인식을 위한 머신러닝 수행(k-nearest neighbor 알고리즘 사용)--------------------
try:
    # read in training classifications
    npaClassifications = np.loadtxt("classifications_2.txt", np.float32)
except:
    print("error, unable to open classifications_2.txt, exiting program\n")
    os.system("pause")

try:
    # read in training images
    npaFlattenedImages = np.loadtxt("flattened_images_2.txt", np.float32)
except:
    print("error, unable to open flattened_images_2.txt, exiting program\n")
    os.system("pause")

# reshape numpy array to 1d, necessary to pass to call to train
npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))

kNearest = cv2.ml.KNearest_create()  # instantiate KNN object

kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)


# 문자 인식 ----------------------------------------------------------------------
def character_detection():
    global cnts, mask, char_arr
    global RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT

    allContoursWithData = []  # declare empty lists,
    validContoursWithData = []  # we will fill these shortly

    for npaContour in cnts:  # for each contour
        contourWithData = ContourWithData()  # instantiate a contour with data object
        contourWithData.npaContour = npaContour  # assign contour to contour with data

        # get the bounding rect
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)

        # get bounding rect info
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()

        # calculate the contour area
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)

        # add contour with data object to list of all contours with data
        allContoursWithData.append(contourWithData)
    # end for

    for contourWithData in allContoursWithData:  # for all contours
        if contourWithData.checkIfContourIsValid():  # check if valid
            validContoursWithData.append(contourWithData)  # if so, append to valid contour list
        # end if
    # end for

    if len(validContoursWithData) > 0:
        max_ctn_area = validContoursWithData[0].fltArea
        ctn_max_area_idx = 0
        for j in range(len(validContoursWithData)):
            if validContoursWithData[j].fltArea > max_ctn_area:
                max_ctn_area = validContoursWithData[j].fltArea
                ctn_max_area_idx = j

        contourWithData = validContoursWithData[j]

    # sort contours from left to right
    # validContoursWithData.sort(key=operator.attrgetter("intRectX"))

    # declare final string, this will have the final number sequence by the end of the program
    strFinalString = ""

    if len(validContoursWithData) > 0:
        # draw a rect around the current char
        cv2.rectangle(mask,  # draw rectangle on original testing image
                      (contourWithData.intRectX, contourWithData.intRectY),  # upper left corner
                      (contourWithData.intRectX + contourWithData.intRectWidth,
                       contourWithData.intRectY + contourWithData.intRectHeight),
                      # lower right corner
                      color_bgr[i],  # 글자 색깔과 동일한 색으로 contour 그림
                      2)  # thickness

        # crop char out of threshold image
        imgROI = mask[
                 contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                 contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

        # resize image, this will be more consistent for recognition and storage
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

        # flatten image into 1d numpy array
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

        # convert from 1d numpy array of ints to 1d numpy array of floats
        npaROIResized = np.float32(npaROIResized)

        # call KNN function find_nearest
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=1)

        if char_arr is None or len(char_arr) < 100:
            char_arr.append(str(chr(int(npaResults[0][0]))))
            return None, None
        elif len(char_arr) == 100:
            strCurrentChar = Counter(char_arr).most_common()[0][0]
            print("\n" + str(Counter(char_arr).most_common()[0:2]))
            strFinalString = strFinalString + strCurrentChar  # append current char to full string
            char_arr = []
            return strFinalString, contourWithData.fltArea
        # strCurrentChar = str(chr(int(npaResults[0][0])))  # get character from results
        # strFinalString = strFinalString + strCurrentChar  # append current char to full string
    # end for


# 문자 인식 후 동작 -----------------------------------------------------------------
def action(DetectedChar, CharArea, CharColor):
    global roi_num, serial_port, serial_count, count_max
    global check_cardinal_point_1, check_cardinal_point_2, cardinal_point
    global check_dir, turn_dir
    global citizen_color, now_color
    global room1, room2, room3
    global enLT, enCharDetection, enCheckContamination, enCharDetection, enExit

    # 시작위치에서 방위 체크 + 문 열고 들어가기
    if check_cardinal_point_1 == 0:
        if DetectedChar == 'N':
            cardinal_point = 101
        elif DetectedChar == 'S':
            cardinal_point = 102
        elif DetectedChar == 'E':
            cardinal_point = 103
        elif DetectedChar == 'W':
            cardinal_point = 104
        else:
            return 1

        for serial_count in range(count_max):
            TX_data(serial_port, cardinal_point)
        serial_count = 0

        print("\ncharacter: " + DetectedChar + ", color: " + CharColor)
        print("area: " + str(CharArea))

        check_cardinal_point_1 = 1
        time.sleep(17)
        return 1

    # 화살표 방향 체크
    elif check_dir == 0:
        if DetectedChar == 'R':  # 화살표 방향 = 오른쪽
            direction = 105
        elif DetectedChar == 'L':  # 화살표 방향 = 왼쪽
            direction = 106
        else:
            return 1

        check_dir = 1
        for serial_count in range(count_max):
            TX_data(serial_port, direction)
        serial_count = 0

        print("\ncharacter: " + DetectedChar + ", color: " + CharColor)
        print("area: " + str(CharArea))

        time.sleep(13)
        enLT = 1
        enCharDetection = 0
        roi_num = 2
        return 1

    # 방 이름 인식
    elif check_cardinal_point_1 == 1 and check_dir == 1 and (
            room1 == 0 or room2 == 0 or room3 == 0) and enCheckContamination == 0:
        if DetectedChar == 'A':
            room_name = 125
        elif DetectedChar == 'B':
            room_name = 130
        elif DetectedChar == 'C':
            room_name = 135
        elif DetectedChar == 'D':
            room_name = 140
        else:
            return 1

        # for serial_count in range(count_max):
        #    TX_data(serial_port, room_name)
        # serial_count = 0
        # time.sleep(3)

        citizen_color = now_color  # 구출해야하는 시민 색

        if room1 == 0:
            room1 = 1
            room1_name = room_name
            print("\nroom1 name: " + DetectedChar + ", color: " + CharColor)
            print("area: " + str(CharArea))
        elif room1 == 1 and room2 == 0:
            room2 = 1
            room2_name = room_name
            print("\nroom2 name: " + DetectedChar + ", color: " + CharColor)
            print("area: " + str(CharArea))
        elif room1 == 1 and room2 == 1 and room3 == 0:
            room3 = 1
            room3_name = room_name
            print("\nroom3 name: " + DetectedChar + ", color: " + CharColor)
            print("area: " + str(CharArea))
        else:
            return 1

        # 확진지역 체크하기 위해 관심영역 재설정
        # if turn_dir == 105: # 회전 방향이 오른쪽이면
        # roi_num = 3  # 우하단
        # elif turn_dir == 106: # 회전 방향이 왼쪽이면
        # roi_num = 4  # 좌하단
        # else: return 1

        print("방이름 인식 완료")
        time.sleep(5)
        enCheckContamination = 1  # 다음 loop에서 방 확진지역여부 체크
        enCharDetection = 0
        return 1

    # 탈출하는 위치의 방위 체크 + 탈출
    if (check_cardinal_point_2 == 0 and enCheckContamination == 0 and enExit == 1 and now_color == 4):
        if DetectedChar == 'N':
            cardinal_point = 101
        elif DetectedChar == 'S':
            cardinal_point = 102
        elif DetectedChar == 'E':
            cardinal_point = 103
        elif DetectedChar == 'W':
            canial_point = 104
        else:
            return 1

        for serial_count in range(count_max):
            TX_data(serial_port, cardinal_point)
        print("serial count end")
        serial_count = 0
        time.sleep(15)

        print("\ncharacter: " + DetectedChar + ", color: " + CharColor)
        print("area: " + str(CharArea))
        check_cardinal_point_2 = 1
        return 1


# -----------------------------------------------
def nothing(x):
    pass


# -----------------------------------------------
def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color

    return image


# -----------------------------------------------
def draw_str2(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)


# -----------------------------------------------
def draw_str3(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), lineType=cv2.LINE_AA)


# -----------------------------------------------
def draw_str_height(dst, target, s, height):
    x, y = target
    cv2.putText(dst, s, (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, height, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, height, (255, 255, 255), lineType=cv2.LINE_AA)


# -----------------------------------------------
def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()


# -----------------------------------------------

def Trackbar_change(now_color):
    global hsv_Lower, hsv_Upper
    hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])
    hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])


# -----------------------------------------------
def Hmax_change(a):
    h_max[now_color] = cv2.getTrackbarPos('Hmax', Top_name)
    Trackbar_change(now_color)


# -----------------------------------------------
def Hmin_change(a):
    h_min[now_color] = cv2.getTrackbarPos('Hmin', Top_name)
    Trackbar_change(now_color)


# -----------------------------------------------
def Smax_change(a):
    s_max[now_color] = cv2.getTrackbarPos('Smax', Top_name)
    Trackbar_change(now_color)


# -----------------------------------------------
def Smin_change(a):
    s_min[now_color] = cv2.getTrackbarPos('Smin', Top_name)
    Trackbar_change(now_color)


# -----------------------------------------------
def Vmax_change(a):
    v_max[now_color] = cv2.getTrackbarPos('Vmax', Top_name)
    Trackbar_change(now_color)


# -----------------------------------------------
def Vmin_change(a):
    v_min[now_color] = cv2.getTrackbarPos('Vmin', Top_name)
    Trackbar_change(now_color)


# -----------------------------------------------
def min_area_change(a):
    min_area[now_color] = cv2.getTrackbarPos('Min_Area', Top_name)
    if min_area[now_color] == 0:
        min_area[now_color] = 1
        cv2.setTrackbarPos('Min_Area', Top_name, min_area[now_color])
    Trackbar_change(now_color)


# -----------------------------------------------
def Color_num_change(a):
    global now_color, hsv_Lower, hsv_Upper
    now_color = cv2.getTrackbarPos('Color_num', Top_name)
    cv2.setTrackbarPos('Hmax', Top_name, h_max[now_color])
    cv2.setTrackbarPos('Hmin', Top_name, h_min[now_color])
    cv2.setTrackbarPos('Smax', Top_name, s_max[now_color])
    cv2.setTrackbarPos('Smin', Top_name, s_min[now_color])
    cv2.setTrackbarPos('Vmax', Top_name, v_max[now_color])
    cv2.setTrackbarPos('Vmin', Top_name, v_min[now_color])
    cv2.setTrackbarPos('Min_Area', Top_name, min_area[now_color])

    hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])
    hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])


# -----------------------------------------------
def TX_data(ser, one_byte):  # one_byte= 0~255
    # ser.write(chr(int(one_byte)))          #python2.7
    ser.write(serial.to_bytes([one_byte]))  # python3


# -----------------------------------------------
def RX_data(serial):
    global Temp_count
    try:
        if serial.inWaiting() > 0:
            result = serial.read(1)
            RX = ord(result)
            return RX
        else:
            return 0
    except:
        Temp_count = Temp_count + 1
        print("Serial Not Open " + str(Temp_count))
        return 0
        pass


# -----------------------------------------------

# *************************
# mouse callback function
def mouse_move(event, x, y, flags, param):
    global mx, my

    if event == cv2.EVENT_MOUSEMOVE:
        mx, my = x, y


# *************************
def RX_Receiving(ser):
    global receiving_exit, threading_Time

    global X_255_point
    global Y_255_point
    global X_Size
    global Y_Size
    global Area, Angle

    receiving_exit = 1
    while True:
        if receiving_exit == 0:
            break
        time.sleep(threading_Time)

        while ser.inWaiting() > 0:
            result = ser.read(1)
            RX = ord(result)
            print("RX=" + str(RX))


def GetLengthTwoPoints(XY_Point1, XY_Point2):
    return math.sqrt((XY_Point2[0] - XY_Point1[0]) ** 2 + (XY_Point2[1] - XY_Point1[1]) ** 2)


# *************************
def FYtand(dec_val_v, dec_val_h):
    return (math.atan2(dec_val_v, dec_val_h) * (180.0 / math.pi))


# *************************
# degree 값을 라디안 값으로 변환하는 함수
def FYrtd(rad_val):
    return (rad_val * (180.0 / math.pi))


# *************************
# 라디안값을 degree 값으로 변환하는 함수
def FYdtr(dec_val):
    return (dec_val / 180.0 * math.pi)


# *************************
def GetAngleTwoPoints(XY_Point1, XY_Point2):
    xDiff = XY_Point2[0] - XY_Point1[0]
    yDiff = XY_Point2[1] - XY_Point1[1]
    cal = math.degrees(math.atan2(yDiff, xDiff)) + 90
    if cal > 90:
        cal = cal - 180
    return cal


# *************************


# ************************
def hsv_setting_save():
    global Config_File_Name, color_num
    global color_num, h_max, h_min
    global s_max, s_min, v_max, v_min, min_area

    try:
        # if 1:
        saveFile = open(Config_File_Name, 'w')
        i = 0
        color_cnt = len(color_num)
        while i < color_cnt:
            text = str(color_num[i]) + ","
            text = text + str(h_max[i]) + "," + str(h_min[i]) + ","
            text = text + str(s_max[i]) + "," + str(s_min[i]) + ","
            text = text + str(v_max[i]) + "," + str(v_min[i]) + ","
            text = text + str(min_area[i]) + "\n"
            saveFile.writelines(text)
            i = i + 1
        saveFile.close()
        print("hsv_setting_save OK")
        return 1
    except:
        print("hsv_setting_save Error~")
        return 0


# ************************
def hsv_setting_read():
    global Config_File_Name
    global color_num, h_max, h_min
    global s_max, s_min, v_max, v_min, min_area

    # try:
    if 1:
        with open(Config_File_Name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            i = 0

            for row in readCSV:
                color_num[i] = int(row[0])
                h_max[i] = int(row[1])
                h_min[i] = int(row[2])
                s_max[i] = int(row[3])
                s_min[i] = int(row[4])
                v_max[i] = int(row[5])
                v_min[i] = int(row[6])
                min_area[i] = int(row[7])

                i = i + 1

        csvfile.close()
        print("hsv_setting_read OK")
        return 1
    # except:
    #    print("hsv_setting_read Error~")
    #    return 0


# **************************************************
# **************************************************
# **************************************************
if __name__ == '__main__':

    # -------------------------------------
    print("-------------------------------------")
    print("(2020-1-20) mini CTS5 Program.  MINIROBOT Corp.")
    print("-------------------------------------")
    print("")
    os_version = platform.platform()
    print(" ---> OS " + os_version)
    python_version = ".".join(map(str, sys.version_info[:3]))
    print(" ---> Python " + python_version)
    opencv_version = cv2.__version__
    print(" ---> OpenCV  " + opencv_version)

    # -------------------------------------
    # ---- user Setting -------------------
    # -------------------------------------
    W_View_size = 320  # 320  #640
    # H_View_size = int(W_View_size / 1.777)
    H_View_size = int(W_View_size / 1.333)

    BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200
    serial_use = 1
    now_color = 0
    View_select = 0
    # -------------------------------------
    print(" ---> Camera View: " + str(W_View_size) + " x " + str(H_View_size))
    print("")
    print("-------------------------------------")

    # -------------------------------------
    try:
        hsv_setting_read()
    except:
        hsv_setting_save()

    # -------------------------------------
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    args = vars(ap.parse_args())

    img = create_blank(320, 100, rgb_color=(0, 0, 255))

    cv2.namedWindow(Top_name)
    cv2.moveWindow(Top_name, 0, 0)

    cv2.createTrackbar('Hmax', Top_name, h_max[now_color], 255, Hmax_change)
    cv2.createTrackbar('Hmin', Top_name, h_min[now_color], 255, Hmin_change)
    cv2.createTrackbar('Smax', Top_name, s_max[now_color], 255, Smax_change)
    cv2.createTrackbar('Smin', Top_name, s_min[now_color], 255, Smin_change)
    cv2.createTrackbar('Vmax', Top_name, v_max[now_color], 255, Vmax_change)
    cv2.createTrackbar('Vmin', Top_name, v_min[now_color], 255, Vmin_change)
    cv2.createTrackbar('Min_Area', Top_name, min_area[now_color], 255, min_area_change)
    cv2.createTrackbar('Color_num', Top_name, color_num[now_color], 4, Color_num_change)

    Trackbar_change(now_color)

    draw_str3(img, (15, 25), 'MINIROBOT Corp.')
    draw_str2(img, (15, 45), 'space: Fast <=> Video and Mask.')
    draw_str2(img, (15, 65), 's, S: Setting File Save')
    draw_str2(img, (15, 85), 'Esc: Program Exit')

    cv2.imshow(Top_name, img)
    # ---------------------------
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(args["video"])
    # ---------------------------
    camera.set(3, W_View_size)
    camera.set(4, H_View_size)
    camera.set(5, 60)
    time.sleep(0.5)
    # ---------------------------

    # ---------------------------
    (grabbed, frame) = camera.read()
    draw_str2(frame, (5, 15), 'X_Center x Y_Center =  Area')
    draw_str2(frame, (5, H_View_size - 5), 'View: %.1d x %.1d.  Space: Fast <=> Video and Mask.'
              % (W_View_size, H_View_size))
    draw_str_height(frame, (5, int(H_View_size / 2)), 'Fast operation...', 3.0)
    mask = frame.copy()
    cv2.imshow('mini CTS5 - Video', frame)
    cv2.imshow('mini CTS5 - Mask', mask)
    cv2.moveWindow('mini CTS5 - Mask', 322 + W_View_size, 36)
    cv2.moveWindow('mini CTS5 - Video', 322, 36)
    cv2.setMouseCallback('mini CTS5 - Video', mouse_move)

    # ---------------------------

    if serial_use != 0:  # python3
        # if serial_use <> 0:  # python2.7
        BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200
        # ---------local Serial Port : ttyS0 --------
        # ---------USB Serial Port : ttyAMA0 --------
        serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
        serial_port.flush()  # serial cls
        time.sleep(0.5)

        serial_t = Thread(target=RX_Receiving, args=(serial_port,))
        serial_t.daemon = True
        serial_t.start()
    '''
    # First -> Start Code Send
    TX_data(serial_port, 250)
    TX_data(serial_port, 250)
    TX_data(serial_port, 250)
    '''
    old_time = clock()

    View_select = 0
    msg_one_view = 0
    # -------- Main Loop Start --------
    while True:  # 무한 반복
        # grab the current frame
        (grabbed, frame) = camera.read()  # 카메라로 이미지 캡쳐

        if args.get("video") and not grabbed:  # 이미지 캡쳐가 실패하면
            break  # while loop 탈출

        # roi=frame[y:y+h, x:x+w] 관심영역 설정
        if roi_num == 0:
            frame_roi = frame[0:H_View_size, 0:W_View_size]  # 화면 전체
        elif roi_num == 1:
            frame_roi = frame[0:int(H_View_size / 2), 0:W_View_size]  # 상단
        elif roi_num == 2:
            frame_roi = frame[int(H_View_size / 2):H_View_size, 0:W_View_size]  # 하단
        elif roi_num == 3:
            frame_roi = frame[int(H_View_size / 2):H_View_size, int(W_View_size / 2):W_View_size]  # 우하단
        elif roi_num == 4:
            frame_roi = frame[int(H_View_size / 2):H_View_size, 0:int(W_View_size / 2)]  # 좌하단
        else:
            pass

        for i in color_num:
            now_color = color_num[i]
            hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])
            hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])

            hsv = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2YUV)  # HSV => YUV
            mask = cv2.inRange(hsv, hsv_Lower, hsv_Upper)  # 컬러 이미지를 흑백이미지로 변환
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            center = None

            if len(cnts) > 0:  # cnts에 저장된 값이 있으면(now_color와 동일한 색의 물체가 있으면) 아래코드 수행
                c = max(cnts, key=cv2.contourArea)
                ((X, Y), radius) = cv2.minEnclosingCircle(c)
                Area[i] = int(cv2.contourArea(c) / min_area[now_color])  # 물체의 넓이 구하기

                if Area[i] > min_area[now_color]:
                    X_255_point[i], Y_255_point[i] = get_XY(color_bgr[i])  # 물체의 중심점 및 라인 각도 구하기

                    # 라인트레이싱
                    if (enLT == 1 and enCharDetection == 0 and enMoveCitizen == 0
                            and enCheckContamination == 0 and now_color == 0):
                        line_tracing(X_255_point[i], Y_255_point[i], Area[i])

                    # 문자 인식(빨파검)
                    if (enCharDetection == 1 and enLT == 0 and enMoveCitizen == 0
                            and enCheckContamination == 0
                            and (now_color == 1 or now_color == 2 or now_color == 4)):

                        DetectedChar, CharArea = character_detection()
                        if DetectedChar == None:
                            break
                        else:
                            pass

                        enCDbreak = action(DetectedChar, CharArea, color_str[i])
                        if enCDbreak == 1:
                            break
                        else:
                            enCDbreak == 0

                    # 방의 오염 여부 체크
                    if enCheckContamination == 1 and enCharDetection == 0 and enLT == 0:
                        if counter == 10:
                            print(Area)
                            if Area[3] > Area[4] and Area[3] > 50:  # 방이 안전지역이면
                                contamination = 160
                                room_contamination = 0
                                print("clean")
                            elif Area[3] < Area[4] and Area[4] > 50:  # 방이 오염지역이면
                                contamination = 165
                                room_contamination = 1
                                print("contaminated")
                            else:
                                break

                            for serial_count in range(count_max):
                                TX_data(serial_port, contamination)  # 명령_확진지역 말하기
                            print("serial count end")
                            serial_count = 0
                            time.sleep(5)

                            for serial_count in range(count_max):
                                TX_data(serial_port, room_name)
                            print("serial count end")
                            serial_count = 0
                            time.sleep(3)

                            if room3 == 1:
                                room3_contamination = room_contamination
                            elif room2 == 1:
                                room2_contamination = room_contamination
                            elif room1 == 1:
                                room1_contamination = room_contamination

                            enCheckContamination = 0
                            enMoveCitizen = 1
                            enLT == 0
                            roi_num = 0  # 화면 영역: 전체
                            counter = 0
                            break
                        else:
                            counter = counter + 1

                    # 시민 옮기기
                    if (
                            enMoveCitizen == 1 and enCharDetection == 0 and enLT == 0 and enCheckContamination == 0 and now_color == citizen_color):
                        if Area[now_color] < citizen_min_area:  # 시민이 아직 멀리 있고
                            if X_255_point[i] > 0 and X_255_point[i] < 107:  # 시민이 왼쪽에 위치하면
                                draw_str2(frame_roi, (3, 120), 'go left')
                                print("왼쪽으로 이동")

                                TX_data(serial_port, 5)  # 명령_왼쪽으로 이동
                                TX_data(serial_port, 10)
                                TX_data(serial_port, 10)
                                TX_data(serial_port, 10)
                                time.sleep(0.5)
                                break

                            elif X_255_point[i] >= 117 and X_255_point[i] <= 147:  # 시민이 중심에 위치하면
                                draw_str2(frame_roi, (3, 9), 'go straight')
                                print("직진")

                                TX_data(serial_port, 9)  # 명령_직진
                                TX_data(serial_port, 10)
                                TX_data(serial_port, 10)
                                TX_data(serial_port, 10)
                                time.sleep(0.5)
                                break

                            elif X_255_point[i] > 147 and X_255_point[i] <= 255:  # 시민이 오른쪽에 위치하면
                                draw_str2(frame_roi, (3, 120), 'go right')
                                print("오른쪽으로 이동")
                                TX_data(serial_port, 7)  # 명령_오른쪽으로 이동
                                TX_data(serial_port, 10)
                                TX_data(serial_port, 10)
                                TX_data(serial_port, 10)
                                time.sleep(0.5)
                                break

                        elif X_255_point[i] >= 117 and X_255_point[i] <= 147 and Area[
                            citizen_color] > citizen_min_area:  # 시민이 바로 앞에 위치하면
                            draw_str2(frame_roi, (3, 120), 'catch the citizen')
                            print("직진")
                            if (room_contamination == 1):  # 오염지역일 때
                                for serial_count in range(count_max):
                                    TX_data(serial_port, 20)  # 명령_시민 들고 뒷걸음질 + 라인 돌아오는 것까지??
                                print("serial count end")

                            serial_count = 0
                            time.sleep(20)

                            enLT == 1
                            enMoveCitizen = 0
                            enCharDetection = 0
                            break


                else:
                    X_255_point[i] = 0
                    Y_255_point[i] = 0


            else:
                x = 0
                y = 0
                XY_Point1 = [0, 0]
                XY_Point2 = [0, 0]
                XY_Point3 = [0, 0]
                XY_Point4 = [0, 0]
                X_Size = [0, 0, 0, 0, 0]
                Y_Size = [0, 0, 0, 0, 0]
                Angle = 0

        # 마지막 색(검정)까지 인식한 후 필요한 정보 화면 & command 창에 띄우기
        if now_color == 4:
            Frame_time = (clock() - old_time) * 1000.
            old_time = clock()

        if View_select == 0:  # Fast operation
            # draw_str2(frame_roi, (3, H_View_size - 5), 'View: %.1d x %.1d Time: %.1f ms  Fast Operation'
            #          % (W_View_size, H_View_size, Frame_time))
            print(" " + str(W_View_size) + " x " + str(H_View_size) + " =  %.1f ms" % (Frame_time))
        # temp = Read_RX
        # pass

        elif View_select == 1:  # Debug
            if msg_one_view > 0:
                msg_one_view = msg_one_view + 1
                cv2.putText(frame_roi, "SAVE!", (50, int(H_View_size / 2)),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), thickness=5)

                if msg_one_view > 10:
                    msg_one_view = 0

            if now_color == 4:
                draw_str2(frame_roi, (3, 15),
                          'Yellow (%.1d, %.1d), Area: %.1d' % (X_255_point[0], Y_255_point[0], Area[0]))
                draw_str2(frame_roi, (3, 30),
                          'Red    (%.1d, %.1d), Area: %.1d' % (X_255_point[1], Y_255_point[1], Area[1]))
                draw_str2(frame_roi, (3, 45),
                          'Blue   (%.1d, %.1d), Area: %.1d' % (X_255_point[2], Y_255_point[2], Area[2]))
                draw_str2(frame_roi, (3, 60),
                          'Green  (%.1d, %.1d), Area: %.1d' % (X_255_point[3], Y_255_point[3], Area[3]))
                draw_str2(frame_roi, (3, 75),
                          'Black  (%.1d, %.1d), Area: %.1d' % (X_255_point[4], Y_255_point[4], Area[4]))
                draw_str2(frame_roi, (3, 90), 'Line Angle: %.1d' % line_angle)
                '''
                print("\n--------------------------------------------\n")
                print("Yellow (%.1d, %.1d), Area: %.1d " % (X_255_point[0], Y_255_point[0], Area[0]))
                print("Red    (%.1d, %.1d), Area: %.1d " % (X_255_point[1], Y_255_point[1], Area[1]))
                print("Blue   (%.1d, %.1d), Area: %.1d " % (X_255_point[2], Y_255_point[2], Area[2]))
                print("Green  (%.1d, %.1d), Area: %.1d " % (X_255_point[3], Y_255_point[3], Area[3]))
                print("Black  (%.1d, %.1d), Area: %.1d " % (X_255_point[4], Y_255_point[4], Area[4]))
                '''
            draw_str2(frame_roi, (3, H_View_size - 5), 'View: %.1d x %.1d Time: %.1f ms  Video and Mask.'
                      % (W_View_size, H_View_size, Frame_time))

        # ------mouse pixel hsv -------------------------------
        mx2 = mx
        my2 = my
        if mx2 < W_View_size and my2 < H_View_size:
            pixel = hsv[my2, mx2]
            set_H = pixel[0]
            set_S = pixel[1]
            set_V = pixel[2]
            pixel2 = frame_roi[my2, mx2]
            if my2 < (H_View_size / 2):
                if mx2 < (W_View_size / 2):
                    x_p = -30
                elif mx2 > (W_View_size / 2):
                    x_p = 60
                else:
                    x_p = 30
                draw_str2(frame_roi, (mx2 - x_p, my2 + 15), '-HSV-')
                draw_str2(frame_roi, (mx2 - x_p, my2 + 30), '%.1d' % (pixel[0]))
                draw_str2(frame_roi, (mx2 - x_p, my2 + 45), '%.1d' % (pixel[1]))
                draw_str2(frame_roi, (mx2 - x_p, my2 + 60), '%.1d' % (pixel[2]))
            else:
                if mx2 < (W_View_size / 2):
                    x_p = -30
                elif mx2 > (W_View_size / 2):
                    x_p = 60
                else:
                    x_p = 30
                draw_str2(frame_roi, (mx2 - x_p, my2 - 60), '-HSV-')
                draw_str2(frame_roi, (mx2 - x_p, my2 - 45), '%.1d' % (pixel[0]))
                draw_str2(frame_roi, (mx2 - x_p, my2 - 30), '%.1d' % (pixel[1]))
                draw_str2(frame_roi, (mx2 - x_p, my2 - 15), '%.1d' % (pixel[2]))

        else:
            pass
        # ----------------------------------------------

        cv2.imshow('mini CTS5 - Video', frame_roi)
        cv2.imshow('mini CTS5 - Mask', mask)

        key = 0xFF & cv2.waitKey(1)

        if key == 27:  # ESC  Key
            break
        elif key == ord(' '):  # spacebar Key
            if View_select == 0:
                View_select = 1
            else:
                View_select = 0
        elif key == ord('s') or key == ord('S'):  # s or S Key:  Setting valus Save
            hsv_setting_save()
            msg_one_view = 1

    # cleanup the camera and close any open windows
    receiving_exit = 0
    time.sleep(0.5)

    camera.release()
    cv2.destroyAllWindows()
