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

import math

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
line_angle = 0
Angle = 0
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
color_str = ["Yellow", "Red", "Blue", "Green", "Black"]
color_bgr = [(0, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 0, 255)]

color_num = [0, 1, 2, 3, 4]  # 노빨파초검

h_max = [130, 100, 70, 80, 30]
h_min = [100, 50, 30, 40, 10]

s_max = [100, 130, 150, 140, 140]
s_min = [70, 100, 120, 110, 100]

v_max = [200, 230, 130, 120, 135]
v_min = [170, 160, 90, 90, 115]

min_area = [10, 20, 20, 40, 120]

now_color = 0
serial_use = 1

serial_port = None
Temp_count = 0
Read_RX = 0

mx, my = 0, 0

threading_Time = 5 / 1000.

Config_File_Name = 'hsv_data.dat'


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


# -----------------------------------------------
'''


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
    global Area, Angle, line_angle

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
    return (math.atan2(dec_val_v, dec_val_y) * (180.0 / math.pi))


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
    global color_num, min_area
    global h_max, h_min, s_max, s_min, v_max, v_min

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

    '''
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

    # First -> Start Code Send
    TX_data(serial_port, 250)
    TX_data(serial_port, 250)
    TX_data(serial_port, 250)
    '''
    old_time = clock()

    View_select = 0
    msg_one_view = 0
    # -------- Main Loop Start --------
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()  # 카메라로 이미지 캡쳐

        if args.get("video") and not grabbed:  # 이미지 캡쳐가 실패하면
            break  # while loop 탈출

        # frame = frame[int(H_View_size / 2):H_View_size, 0:W_View_size]
        for i in color_num:  # 5가지 색(color_num)에 대하여 영상 인식
            now_color = color_num[i]  # 현재 색 설정
            hsv_Lower = (h_min[now_color], s_min[now_color], v_min[now_color])  # now_color의 색 범위(lower threshold)
            hsv_Upper = (h_max[now_color], s_max[now_color], v_max[now_color])  # now_color의 색 범위(upper threshold)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)  # HSV => YUV
            mask = cv2.inRange(hsv, hsv_Lower, hsv_Upper)  # 컬러 이미지를 흑백이미지로 변환(더 효율적)

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
                    cv2.drawContours(frame, [box], -1, color_bgr[i], 3)

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

                    # contour의 무게중심값을 255_point 변수에 저장
                    X_255_point[i] = np.int0((XY_Point1[0] + XY_Point2[0] + XY_Point3[0] + XY_Point4[0]) / 4)
                    Y_255_point[i] = np.int0((XY_Point1[1] + XY_Point2[1] + XY_Point3[1] + XY_Point4[1]) / 4)

                    # 화면에 contour의 무게중심 표시
                    cv2.circle(frame, (np.int0((W_View_size / 255.5) * X_255_point[i]),
                                       np.int0((H_View_size / 255.5) * Y_255_point[i])), 10, color_bgr[i], -1)


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

        if now_color == 4:
            Frame_time = (clock() - old_time) * 1000.
            old_time = clock()

        if View_select == 0:  # Fast operation
            print(" " + str(W_View_size) + " x " + str(H_View_size) + " =  %.1f ms" % (Frame_time))
            # temp = Read_RX
            # pass

        elif View_select == 1:  # Debug
            if msg_one_view > 0:
                msg_one_view = msg_one_view + 1
                cv2.putText(frame, "SAVE!", (50, int(H_View_size / 2)),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), thickness=5)

                if msg_one_view > 10:
                    msg_one_view = 0

            if now_color == 4:
                draw_str2(frame, (3, 15),
                          'Yellow X: %.1d, Y: %.1d, Area: %.1d' % (X_255_point[0], Y_255_point[0], Area[0]))
                draw_str2(frame, (3, 30),
                          'Red    X: %.1d, Y: %.1d, Area: %.1d' % (X_255_point[1], Y_255_point[1], Area[1]))
                draw_str2(frame, (3, 45),
                          'Blue   X: %.1d, Y: %.1d, Area: %.1d' % (X_255_point[2], Y_255_point[2], Area[2]))
                draw_str2(frame, (3, 60),
                          'Green  X: %.1d, Y: %.1d, Area: %.1d' % (X_255_point[3], Y_255_point[3], Area[3]))
                draw_str2(frame, (3, 75),
                          'Black  X: %.1d, Y: %.1d, Area: %.1d' % (X_255_point[4], Y_255_point[4], Area[4]))
                draw_str2(frame, (3, 90), 'Line Angle: %.1d' % line_angle)

            draw_str2(frame, (3, H_View_size - 5), 'View: %.1d x %.1d Time: %.1f ms  Space: Fast <=> Video and Mask.'
                      % (W_View_size, H_View_size, Frame_time))

        # ------mouse pixel hsv -------------------------------
        mx2 = mx
        my2 = my
        if mx2 < W_View_size and my2 < H_View_size:
            pixel = hsv[my2, mx2]
            set_H = pixel[0]
            set_S = pixel[1]
            set_V = pixel[2]
            pixel2 = frame[my2, mx2]
            if my2 < (H_View_size / 2):
                if mx2 < (W_View_size / 2):
                    x_p = -30
                elif mx2 > (W_View_size / 2):
                    x_p = 60
                else:
                    x_p = 30
                draw_str2(frame, (mx2 - x_p, my2 + 15), '-HSV-')
                draw_str2(frame, (mx2 - x_p, my2 + 30), '%.1d' % (pixel[0]))
                draw_str2(frame, (mx2 - x_p, my2 + 45), '%.1d' % (pixel[1]))
                draw_str2(frame, (mx2 - x_p, my2 + 60), '%.1d' % (pixel[2]))
            else:
                if mx2 < (W_View_size / 2):
                    x_p = -30
                elif mx2 > (W_View_size / 2):
                    x_p = 60
                else:
                    x_p = 30
                draw_str2(frame, (mx2 - x_p, my2 - 60), '-HSV-')
                draw_str2(frame, (mx2 - x_p, my2 - 45), '%.1d' % (pixel[0]))
                draw_str2(frame, (mx2 - x_p, my2 - 30), '%.1d' % (pixel[1]))
                draw_str2(frame, (mx2 - x_p, my2 - 15), '%.1d' % (pixel[2]))

        else:
            pass
        # ----------------------------------------------

        cv2.imshow('mini CTS5 - Video', frame)
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

