# -*- coding: utf-8 -*-

import platform
import numpy as np
import argparse
import cv2
# import serial
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
turn_dir = 0  # turn_dir=0: 라인이 꺾여있지X, turn_dir=1: 라인이 ㄱ자, turn_dir=2: 라인이 ㄱ반대 모양

Angle = 0
length_12 = 0
length_14 = 0

line_onoff = 0
char_detect_onoff = 1

check_contamination = 0  # check_contamination = 1이면, 확진지역인지 아닌지 체크하기
check_dir = 0  # 0: 진행 방향 체크하기 전, 1: 진행 방향 체크 완료

contamination = 0  # 오염X(0), 오염O(1)
roi_num = 1  # 전체화면(0), 상단(1), 하단(2), 하단 오른쪽(3)
room_color = 0  # green(3), black(4)
citizen_color = 0  # red(1), blue(2)
direction = 0  # 화살표 방향: 왼쪽(106), 오른쪽(105)
room_name = 0  # 방 이름: A(125), B(130), C(135), D(140)
check_cardinal_point_1 = 0
check_cardinal_point_2 = 0
cardinal_point = 0  # 방위: N(101), E(102), W(103), S(104)
go_exit = 0  # go_exit = 1이면 탈출
room_1 = 0
room_2 = 0
room_3 = 0

k = 0
serial_count = 0
count_max = 10000
# -----------------------------------------------
Top_name = 'mini CTS5 setting'
hsv_Lower = 0
hsv_Upper = 0

hsv_Lower0 = 0
hsv_Upper0 = 0

hsv_Lower1 = 0
hsv_Upper1 = 0

# -----------
# 색 설정
# 0: 노란색
# 1: 빨간색
# 2: 파란색
# 3: 초록색
# 4: 검정색
color_num = [0, 1, 2, 3, 4]
color_str = ["Yellow", "Red", "Blue", "Green", "Black"]
color_bgr = [(0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 0, 255)]
'''
h_max = [255, 65, 196, 111, 80]
h_min = [55, 0, 158, 59, 0]

s_max = [162, 200, 223, 110, 155]
s_min = [114, 140, 150, 51, 90]

v_max = [77, 151, 239, 156, 141]
v_min = [0, 95, 104, 61, 104]
'''
# color[3] = green으로 test
h_max = [255, 65, 196, 138, 103]
h_min = [55, 0, 158, 53, 13]

s_max = [162, 200, 223, 210, 145]
s_min = [114, 140, 150, 125, 100]

v_max = [77, 151, 239, 114, 109]
v_min = [0, 95, 104, 74, 20]

min_area = [50, 50, 50, 10, 20]

now_color = 0
serial_use = 1

serial_port = None
Temp_count = 0
Read_RX = 0

mx, my = 0, 0

threading_Time = 5 / 1000.

Config_File_Name = 'Cts5_v1.dat'

# 문자 머신러닝을 위한 변수 --------------------------------------------------------------------------
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


# 문자 머신러닝을 위한 클래스 -------------------------------------------------------------------------
class ContourWithData():
    # member variables ############################################################################
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
    npaClassifications = np.loadtxt("classifications.txt", np.float32)
except:
    print("error, unable to open classifications.txt, exiting program\n")
    os.system("pause")

try:
    # read in training images
    npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
except:
    print("error, unable to open flattened_images.txt, exiting program\n")
    os.system("pause")

# reshape numpy array to 1d, necessary to pass to call to train
npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))

kNearest = cv2.ml.KNearest_create()  # instantiate KNN object

kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)


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


'''
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
'''


# -----------------------------------------------

# *************************
# mouse callback function
def mouse_move(event, x, y, flags, param):
    global mx, my

    if event == cv2.EVENT_MOUSEMOVE:
        mx, my = x, y


'''
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

'''


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
    W_View_size = 640  # 320  #640
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
    '''
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
            frame_roi = frame[int(H_View_size / 2):H_View_size, int(W_View_size / 2):W_View_size]  # 하단 오른쪽
        else:
            break

        for i in color_num:  # 5가지 색(color_num)에 대하여 영상 인식
            now_color = color_num[i]  # 현재 색 설정
            hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])  # now_color의 색 범위(lower threshold)
            hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])  # now_color의 색 범위(upper threshold)

            hsv = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2YUV)  # HSV => YUV
            mask = cv2.inRange(hsv, hsv_Lower, hsv_Upper)  # 컬러 이미지를 흑백이미지로 변환(효율성을 위해)
            # now_color에 해당하는 부분: 흰색, 그 외: 검정색
            # ex: now_color = 0(yellow)이면,
            # 노란색에 해당하는 부분은 흰색으로, 그 외는 검정색으로 처리

            # mask = cv2.erode(mask, None, iterations=1)
            # mask = cv2.dilate(mask, None, iterations=1)
            # mask = cv2.GaussianBlur(mask, (3, 3), 2)  # softly

            # now_color와 동일한 색의 물체의 contour 정보를 cnts에 저장
            # now_color와 동일한 색의 물체가 없으면 cnts에 아무 값도 저장 안 됨(NULL)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            center = None

            if len(cnts) > 0:  # cnts에 저장된 값이 있으면(now_color와 동일한 색의 물체가 있으면) 아래코드 수행
                c = max(cnts, key=cv2.contourArea)
                ((X, Y), radius) = cv2.minEnclosingCircle(c)

                Area[i] = int(cv2.contourArea(c) / min_area[now_color])  # 물체의 넓이 구하기

                if Area[i] > min_area[now_color]:  # 물체의 넓이가 임계값보다 크면 아래 코드 수행
                    minRect = cv2.minAreaRect(c)  # 물체에 접하는 사각형 정보를 minRect에 저장
                    box = cv2.boxPoints(minRect)  # 사각형의 4 꼭짓점을 box에 저장
                    box = np.int0(box)  # 꼭짓점의 좌표를 float -> integer형으로 변환

                    # 물체에 접하는 사각형(contour) 그리기
                    cv2.drawContours(frame_roi, [box], -1, color_bgr[i], 3)

                    # 화면에 contour의 꼭짓점 표시
                    cv2.circle(frame_roi, (box[0][0], box[0][1]), 10, color_bgr[i], -1)
                    cv2.circle(frame_roi, (box[1][0], box[1][1]), 10, color_bgr[i], -1)
                    cv2.circle(frame_roi, (box[2][0], box[2][1]), 10, color_bgr[i], -1)
                    cv2.circle(frame_roi, (box[3][0], box[3][1]), 10, color_bgr[i], -1)

                    # 꼭짓점의 XY 좌표를 255 pixel 단위로 변환하여 저장
                    XY_Point1[0] = np.int0((255.0 / W_View_size) * box[0][0])  # 1번째 꼭짓점의 X좌표
                    XY_Point1[1] = np.int0((255.0 / H_View_size) * box[0][1])  # 1번째 꼭짓점의 Y좌표
                    XY_Point2[0] = np.int0((255.0 / W_View_size) * box[1][0])  # 2번째 꼭짓점의 X좌표
                    XY_Point2[1] = np.int0((255.0 / H_View_size) * box[1][1])  # 2번째 꼭짓점의 Y좌표
                    XY_Point3[0] = np.int0((255.0 / W_View_size) * box[2][0])  # 3번째 꼭짓점의 X좌표
                    XY_Point3[1] = np.int0((255.0 / H_View_size) * box[2][1])  # 3번째 꼭짓점의 Y좌표
                    XY_Point4[0] = np.int0((255.0 / W_View_size) * box[3][0])  # 4번째 꼭짓점의 X좌표
                    XY_Point4[1] = np.int0((255.0 / H_View_size) * box[3][1])  # 4번째 꼭짓점의 Y좌표

                    # contour의 무게중심값을 255_point 변수에 저장
                    X_255_point[i] = np.int0((XY_Point1[0] + XY_Point2[0] + XY_Point3[0] + XY_Point4[0]) / 4)
                    Y_255_point[i] = np.int0((XY_Point1[1] + XY_Point2[1] + XY_Point3[1] + XY_Point4[1]) / 4)

                    # 화면에 counour의 무게중심 표시
                    cv2.circle(frame_roi,
                               (np.int0((W_View_size / 255.5) * X_255_point[i]),
                                np.int0((H_View_size / 255.5) * Y_255_point[i]))
                               , 10, color_bgr[i], -1)

                    # 문자 인식
                    if (now_color == 1 or now_color == 2 or now_color == 4) and char_detect_onoff == 1:
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
                            contourWithData.fltArea = cv2.contourArea(
                                contourWithData.npaContour)

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
                                break
                            elif len(char_arr) == 100:
                                strCurrentChar = Counter(char_arr).most_common()[0][0]
                                print("\n" + str(Counter(char_arr).most_common()[0:2]))
                                strFinalString = strFinalString + strCurrentChar  # append current char to full string
                                char_arr = []
                        # end for
                        print(
                            "character area: " + str(contourWithData.fltArea) + "\n" + strFinalString)
                        print("char_color: " + str(now_color))


                    # 마지막 색(검정)까지 인식한 후
                    if now_color == 4:
                        if check_contamination == 1:  # 확진지역 체크
                            if Area.argmax() == 3:  # 방이 확진지역이 아니면
                                #TX_data(serial_port, 160)  # 명령_오염 여부 말하기
                                #TX_data(serial_port, 160)
                                #TX_data(serial_port, 160)
                                check_contamination = 0
                                contamination = 0
                                roi_num = 0
                                break
                            elif Area.argmax() == 4:  # 방이 확진지역이면
                                #TX_data(serial_port, 165)  # 명령_오염 여부 말하기
                                #TX_data(serial_port, 165)
                                #TX_data(serial_port, 165)
                                check_contamination = 0
                                contamination = 1
                                roi_num = 0
                                break
                            else:
                                break

                        # 필요한 정보 화면 & command 창에 띄우기
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
                    time.sleep(0.3)

            else:

                x = 0
                y = 0
                XY_Point1 = [0, 0]
                XY_Point1 = [0, 0]
                X_255_point = [0, 0, 0, 0, 0]
                Y_255_point = [0, 0, 0, 0, 0]
                X_Size = [0, 0, 0, 0, 0]
                Y_Size = [0, 0, 0, 0, 0]
                Area = [0, 0, 0, 0, 0]
                Angle = 0

        Frame_time = (clock() - old_time) * 1000.
        old_time = clock()

        if View_select == 0:  # Fast operation
            draw_str2(frame_roi, (3, H_View_size - 5), 'View: %.1d x %.1d Time: %.1f ms  Fast Operation'
                      % (W_View_size, H_View_size, Frame_time))
            # print(" " + str(W_View_size) + " x " + str(H_View_size) + " =  %.1f ms" % (Frame_time))
            # temp = Read_RX
            # pass

        elif View_select == 1:  # Debug
            if msg_one_view > 0:
                msg_one_view = msg_one_view + 1
                cv2.putText(frame_roi, "SAVE!", (50, int(H_View_size / 2)),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), thickness=5)

                if msg_one_view > 10:
                    msg_one_view = 0

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