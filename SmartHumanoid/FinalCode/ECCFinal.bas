'후진걷기
DIM 후진보행횟수 AS BYTE
DIM 후진반복횟수 AS BYTE
DIM 후진보행순서 AS BYTE

'잡고후진걷기
DIM 잡고후진보행횟수 AS BYTE
DIM 잡고후진반복횟수 AS BYTE
DIM 잡고후진보행순서 AS BYTE

'문열기걷기
DIM 열기보행횟수 AS BYTE
DIM 열기반복횟수 AS BYTE
DIM 열기보행순서 AS BYTE
DIM 문열고턴 AS BYTE
DIM INITIAL AS BYTE

'잡고걷기
DIM DATA AS BYTE
DIM 잡고보행횟수 AS BYTE
DIM 잡고반복횟수 AS BYTE
DIM 잡고보행순서 AS BYTE

'걷기
DIM 보행횟수 AS BYTE
DIM 반복횟수 AS BYTE
DIM 보행순서 AS BYTE

'넘어지면일어나기
DIM CD AS BYTE
DIM DD AS BYTE
DIM i AS BYTE

' 기울기센서포트 설정

CONST 앞뒤기울기AD포트 = 0
CONST 좌우기울기AD포트 = 1


CONST 기울기확인시간 = 5  'ms
CONST MIN = 61         '뒤로넘어졌을때
CONST MAX = 107         '앞으로넘어졌을때
CONST COUNT_MAX = 20


DIM 적외선거리값  AS BYTE
CONST 적외선AD포트  = 4


'^^^^^^^^^^^^메인코딩용변수^^^^^^^^^^
DIM D AS BYTE
DIM B AS BYTE
DIM N AS BYTE

DIM X AS BYTE
DIM Y AS BYTE
DIM Z AS BYTE

DIM SPEAK AS BYTE
DIM STDR AS BYTE

D=1
'A=0
B=0
N=0

X=0
Y=0
Z=0

INITIAL = 0
SPEAK = 0
STDR = 2

DIM 오염여부 AS BYTE

'음성파일열기

PRINT "OPEN 20GongMo.mrs !"
PRINT "VOLUME 200 !"



' 변수선언---------------------------------------
'DIM a AS BYTE
'DIM b AS BYTE
DIM GYRO_ONOFF AS BYTE
'DIM A_old AS BYTE
'DIM X AS BYTE
'DIM Y AS BYTE
DIM A AS BYTE

'모터방향설정
DIR G6A,1,0,0,1,0,0   '왼쪽다리:모터0~5번
DIR G6D,0,1,1,0,1,0   '오른쪽다리:모터18~23번
DIR G6B,1,1,1,1,1,1   '왼쪽팔:모터6~11번
DIR G6C,0,0,0,0,0,0   '오른쪽팔:모터12~17번

'모터동시제어설정
PTP SETON       '단위그룹별 점대점동작 설정
PTP ALLON      '전체모터 점대점 동작 설정

'모터위치값피드백
GOSUB MOTOR_GET

DIM DIS AS BYTE


'모터사용설정
GOSUB MOTOR_ON
SPEED 5
GOSUB 기본자세
'-----------------------------------------------



'보행횟수로 걸음수 조절해~~~~~~
잡고보행횟수= 4
잡고반복횟수 = 0

열기보행횟수 = 8
열기반복횟수 = 0

보행횟수= 6
반복횟수 = 0

문열고턴 = 0

잡고후진보행횟수 = 10
잡고후진반복횟수 = 0

후진보행횟수 = 6
후진반복횟수 = 0


MAIN:

	DELAY 100

    GOSUB 앞뒤기울기측정
    GOSUB 좌우기울기측정

    IF STDR =0 THEN
        GOSUB 시작자세
        IF INITIAL = 0 THEN
           GOSUB 오른쪽으로
           DELAY 100
           GOSUB 오른쪽으로
           DELAY 100
           INITIAL = 1
       ENDIF
        ERX 4800, A, MAIN
        'A_old = A
        IF A = 101 THEN
            GOSUB NORTH
            STDR = 1

        ELSEIF A = 102 THEN
            GOSUB SOUTH
            STDR = 1

        ELSEIF A = 103 THEN
            GOSUB EAST
            STDR = 1

        ELSEIF A = 104 THEN
            GOSUB WEST
            STDR = 1

        ELSE
            GOTO MAIN
        ENDIF
        
        
        GOSUB 왼쪽으로
        GOSUB 왼쪽으로
        GOSUB 왼쪽으로
        GOSUB 왼쪽턴20
        GOSUB 문걸어가기
        DELAY 100
        
        GOSUB 기본자세
        GOSUB 오른쪽으로
        GOSUB 후진종종걸음
        
        GOSUB 기본자세
        DELAY 1000
    
    
    ELSEIF STDR = 1 THEN
       
        ERX 4800, A, MAIN
        IF A = 106 THEN
            B = 6
            GOSUB 전진종종걸음
            GOSUB 전진종종걸음
            DELAY 100
            GOSUB 전진종종걸음
            GOSUB 전진종종걸음
            DELAY 100
            GOSUB 왼쪽턴20
            GOSUB 왼쪽턴90
            GOSUB 오른쪽으로
            DELAY 100
            GOSUB 오른쪽으로
            DELAY 100
            GOSUB 오른쪽으로
            DELAY 100
            
            STDR = 2
        ELSEIF A = 105 THEN
            B = 5
            GOSUB 전진종종걸음
            GOSUB 전진종종걸음
            DELAY 100
            GOSUB 전진종종걸음
            GOSUB 전진종종걸음
            DELAY 100
            GOSUB 왼쪽턴20
            GOSUB 오른쪽턴90
            GOSUB 왼쪽으로
            DELAY 100
            GOSUB 왼쪽으로
            DELAY 100
            GOSUB 왼쪽으로
            DELAY 100
            STDR = 2
        ELSE
           GOTO MAIN
        ENDIF
        D = D + 1
        GOSUB 아래로기본자세
        
        DELAY 1000

        GOTO MAIN
    

   ELSEIF D < 2  THEN
       'MUSIC "C" 
        DELAY 100
        ERX 4800, A, MAIN
        'A_old = A           
         
        IF A = 115 THEN
        	MUSIC "A" 
            GOSUB 아래로왼쪽으로
            GOTO MAIN
   
        ELSEIF A = 120 THEN
        	MUSIC "A" 
            GOSUB 아래로오른쪽으로
            GOTO MAIN
   
        ELSEIF A = 110 THEN
        	MUSIC "B" 
            GOSUB 아래로종종걸음
            GOTO MAIN
               
        ELSEIF A = 111 THEN
        	MUSIC "C" 
            GOSUB 왼쪽턴20
            GOTO MAIN
            
        ELSEIF A = 112 THEN
        	MUSIC "C" 
            GOSUB 오른쪽턴20
            GOTO MAIN
   
        ELSEIF A = 203 THEN
        	MUSIC "D"
            GOSUB 기본자세
            DELAY 100
            GOSUB 왼쪽으로
            GOSUB 시작자세 
			GOSUB 확진여부말하기
            GOSUB 시민접근
            GOSUB 시민옮기기
            N = N+1
            GOSUB 오른쪽턴90
            GOSUB 오른쪽턴90
            GOSUB 전진종종걸음
            GOSUB 전진종종걸음
            GOSUB 왼쪽턴90
            GOTO MAIN
               
        ELSEIF A = 204 THEN
        	MUSIC "D"
            GOSUB 기본자세
            DELAY 100
            GOSUB 오른쪽으로
			GOSUB 시작자세 
			GOSUB 확진여부말하기
			GOSUB 시민접근
			GOSUB 시민옮기기                   
            N = N+1
            GOSUB 왼쪽턴90
            GOSUB 왼쪽턴90
            GOSUB 전진종종걸음
            GOSUB 전진종종걸음
            GOSUB 오른쪽턴90
            GOTO MAIN

   
        ELSEIF A = 205 THEN
        	MUSIC "E"
            IF N < 3 THEN
                GOTO 전진종종걸음
                GOTO MAIN
            ELSEIF N = 3 THEN
                GOTO 오른쪽턴90
                GOTO 문열기
                GOTO MAIN
            ENDIF
   
   
        ELSEIF A = 206 THEN
        	MUSIC "E"
            IF N < 3 THEN
                GOTO 전진종종걸음
                GOTO MAIN
            ELSEIF N = 3 THEN
                GOTO 왼쪽턴90
                GOTO 문열기
                GOTO MAIN
            ELSE
                A = 0
                GOTO MAIN
            ENDIF
        ENDIF
        GOTO MAIN
   
   
    ELSEIF D = 2 THEN
        IF X > 0 THEN
            GOSUB WARN
            SPEAK = X
            GOSUB SPEAKEND
            SPEAK = 0
        ENDIF
   
        IF Y > 0 THEN
            SPEAK = Y
            GOSUB SPEAKEND
            SPEAK = 0
        ENDIF
   
        IF Z > 0 THEN
            SPEAK = Z
            GOSUB SPEAKEND
            SPEAK = 0
        ENDIF
        
        GOSUB 기본자세
        STOP
   
    ELSE
        D = 0
        GOTO MAIN
    ENDIF

   
    GOTO MAIN   
    
    
    
    
화살표라인:
	ERX 4800, A, 화살표라인
	IF A = 115 THEN
    	MUSIC "A" 
        GOSUB 아래로왼쪽으로
        GOTO 화살표라인
        
    ELSEIF A = 120 THEN
    	MUSIC "A" 
        GOSUB 아래로오른쪽으로
        GOTO 화살표라인
       
    ELSEIF A = 111 THEN
    	MUSIC "C" 
        GOSUB 왼쪽턴20
        GOTO 화살표라인
        
    ELSEIF A = 112 THEN
    	MUSIC "C" 
        GOSUB 오른쪽턴20
        GOTO 화살표라인

    ELSEIF A = 110 THEN
    	MUSIC "B" 
    ENDIF
    
    RETURN
    


'***************확진여부 말하기************************
확진여부말하기:
    ERX 4800, A, 확진여부말하기
    IF A = 160 THEN
        GOSUB SAFE
        오염여부=0
                
    ELSEIF A = 165 THEN
        GOSUB WARN
        오염여부= 1
        GOSUB 확진지역저장
    ENDIF
    
    RETURN
            
'****************오염지역 저장**************************
확진지역저장:
    ERX 4800, A, 확진지역저장
    IF X = 0 THEN
        X = A
    ELSEIF Y = 0 THEN
        Y = A
    ELSEIF Z = 0 THEN
        Z = A
    ENDIF
                
    DELAY 2000
    RETURN
    '**********************회전******************************
왼쪽턴90:
    GOSUB 왼쪽턴20
    DELAY 100
    GOSUB 왼쪽턴20
    DELAY 100
    GOSUB 왼쪽턴20
    DELAY 100
    GOSUB 왼쪽턴20
    DELAY 100
    GOSUB 왼쪽턴20
    DELAY 100
    GOSUB 왼쪽턴20
    DELAY 100
'    GOSUB 왼쪽턴20
    WAIT
    RETURN

오른쪽턴90:
    GOSUB 오른쪽턴20
    DELAY 100
    GOSUB 오른쪽턴20
    DELAY 100
    GOSUB 오른쪽턴20
    DELAY 100
    GOSUB 오른쪽턴20
    DELAY 100
    GOSUB 오른쪽턴20
    DELAY 100
    GOSUB 오른쪽턴20
    DELAY 100
'    GOSUB 오른쪽턴20
'    GOSUB 오른쪽턴20
    WAIT
    RETURN


왼쪽턴20:
    GOSUB Leg_motor_mode2
    SPEED 6
    MOVE G6A,95,  96, 145,  73, 105, 100
    MOVE G6D,95,  56, 145,  113, 105, 100
    MOVE G6B,110
    MOVE G6C,90
    WAIT

    SPEED 8
    MOVE G6A,93,  96, 145,  73, 105, 100
    MOVE G6D,93,  56, 145,  113, 105, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    MOVE G6B,100,  30,  80
    MOVE G6C,100,  30,  80
    WAIT

    'GOSUB 기본자세
    GOSUB Leg_motor_mode1
    RETURN

오른쪽턴20:
    GOSUB Leg_motor_mode2
    SPEED 6
    MOVE G6A,95,  56, 145,  113, 105, 100
    MOVE G6D,95,  96, 145,  73, 105, 100
    MOVE G6B,90
    MOVE G6C,110
    WAIT

    SPEED 8
    MOVE G6A,93,  56, 145,  113, 105, 100
    MOVE G6D,93,  96, 145,  73, 105, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    MOVE G6B,100,  30,  80
    MOVE G6C,100,  30,  80
    WAIT

    'GOSUB 기본자세
    GOSUB Leg_motor_mode1
    RETURN

    '**********************문열기동작**************************
문걸어가기:
    적외선거리값 = AD(적외선AD포트)
    IF 적외선거리값 <= 80 THEN
        GOSUB 전진종종걸음
        GOTO 문걸어가기
    ELSEIF 적외선거리값 > 80 THEN
        MUSIC " C"
        GOSUB 문열기
    ENDIF

문열기:

    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100

    GOSUB 열기종종걸음

    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  80,  80, 100, 100, 100
    MOVE G6C,190,  80,  80, 100, 100, 100

    D = D + 1
    WAIT
    RETURN



열기종종걸음:

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF 열기보행순서 = 0 THEN
        열기보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,190,  10,  80, 100, 100, 100
        MOVE G6C,190,  10,  80, 100, 100, 100
        WAIT

        GOTO 열기종종걸음_1
    ELSE
        열기보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,190,  10,  80, 100, 100, 100
        MOVE G6C,190,  10,  80, 100, 100, 100
        WAIT

        GOTO 열기종종걸음_4
    ENDIF

열기종종걸음_1:

    열기반복횟수 = 열기반복횟수 + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT

열기종종걸음_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT

열기종종걸음_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF 열기반복횟수 >= 열기보행횟수 THEN
        열기반복횟수 = 0
        GOTO 열기종종걸음_멈춤
    ENDIF

열기종종걸음_4:

    열기반복횟수 = 열기반복횟수 + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT

열기종종걸음_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT

열기종종걸음_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT

    IF 열기반복횟수 >= 열기보행횟수 THEN
        열기반복횟수 = 0
        GOTO 열기종종걸음_멈춤
    ENDIF

    GOTO 열기종종걸음_1


열기종종걸음_멈춤:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB 열기안정화자세
    SPEED 10
    GOSUB 열기기본자세

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

열기안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT
    RETURN


열기기본자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT
    RETURN

    '**********************SPEAK*****************************

SPEAKEND:
   PRINT "M_ABCD.mrs !"
    PRINT "VOLUME 200 !"
    IF SPEAK = 125 THEN
      PRINT "SND 0 !"
      DELAY 1000
      RETURN
   
    ELSEIF SPEAK = 130 THEN
       PRINT "SND 1 !"
       DELAY 1000
       RETURN

    ELSEIF SPEAK = 135 THEN
       PRINT "SND 2 !"
       DELAY 1000
       RETURN

    ELSEIF SPEAK = 140 THEN
       PRINT "SND 3 !"
       DELAY 1000
       RETURN

    ELSE
        SPEAK = 0
    ENDIF
    RETURN

    '---------------------------------------------------

EAST:

    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,190,  30,  80, 100, 100, 100
    GOSUB SOUND_E
    GOSUB 기본자세
    WAIT
    RETURN

WEST:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    GOSUB SOUND_W
    GOSUB 기본자세
    WAIT
    RETURN

SOUTH:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,10,  30,  80, 100, 100, 100
    MOVE G6C,10,  30,  80, 100, 100, 100
    GOSUB SOUND_S
    GOSUB 기본자세
    WAIT
    RETURN

NORTH:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  30,  80, 100, 100, 100
    MOVE G6C,190,  30,  80, 100, 100, 100
    GOSUB SOUND_N
    GOSUB 기본자세
    WAIT
    RETURN


SAFE:

    GOSUB SOUND_SAFE
    RETURN

WARN:
    GOSUB SOUND_WARN
    RETURN

SOUND_E:
    PRINT "SND 0 !"
    DELAY 1500
    RETURN

SOUND_W:
    PRINT "SND 1 !"
    DELAY 1500
    RETURN

SOUND_S:
    PRINT "SND 2 !"
    DELAY 1500
    RETURN

SOUND_N:
    PRINT "SND 3 !"
    DELAY 1500
    RETURN      

SOUND_SAFE:
    PRINT "SND 4 !"
    DELAY 1500
    RETURN      

SOUND_WARN:
    PRINT "SND 5 !"
    DELAY 1500
    RETURN
    
    



    '*******************OBSTACLE********************
시민접근:
	ERX 4800, A, 시민접근
	IF A = 5 THEN
    	GOSUB 왼쪽으로
    ELSEIF A = 7 THEN
        GOSUB 오른쪽으로
    ELSEIF A = 9 THEN
        GOSUB 전진종종걸음   	
    ELSEIF A = 15 THEN
        GOSUB 아래로왼쪽으로
    ELSEIF A = 17 THEN
        GOSUB 아래로오른쪽으로
    ELSEIF A = 19 THEN
        GOSUB 아래로종종걸음
    ENDIF
    RETURN
    
시민옮기기:
	ERX 4800, A, 시민옮기기
	IF A = 20 THEN
    	GOSUB 물건잡기
        IF 오염여부=0 THEN
            GOSUB 잡고걷기
            GOSUB 물건놓기

        ELSEIF 오염여부=1 THEN
            GOSUB 잡고후진종종걸음
            GOSUB 물건놓기
		ENDIF
	ENDIF
    RETURN


물건잡기:
    '앉기
    MOVE G6A,100, 143,  28, 170, 100, 100
    MOVE G6D,100, 143,  28, 170, 100, 100
    MOVE G6B,150,  30,  80, 100, 100, 100
    MOVE G6C,150,  30,  80, 100, 100, 100
    WAIT
    GOTO 진짜잡기

진짜잡기:
    MOVE G6A,100, 143,  28, 170, 100, 100
    MOVE G6D,100, 143,  28, 170, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    GOTO 잡고일어나기

잡고일어나기:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    RETURN

    '-----------------------------------------


물건놓기:
    MOVE G6A,100,  143, 28, 170, 100, 100
    MOVE G6D,100,  143, 28, 170, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100


    MOVE G6A,100,  143, 28, 170, 100, 100
    MOVE G6D,100,  143, 28, 170, 100, 100
    MOVE G6B,150,  30,  80, 100, 100, 100
    MOVE G6C,150,  30,  80, 100, 100, 100

    MOVE G6A,100, 143,  28, 170, 100, 100
    MOVE G6D,100, 143,  28, 170, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    GOSUB 기본자세
    RETURN




    '-------------------------------------------

잡고걷기:
    '넘어진확인 = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF 잡고보행순서 = 0 THEN
        잡고보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 100, 100
        WAIT

        GOTO 잡고걷기_1
    ELSE
        잡고보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 100, 100
        WAIT

        GOTO 잡고걷기_4
    ENDIF

잡고걷기_1:

    잡고반복횟수 = 잡고반복횟수 + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT


잡고걷기_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT


잡고걷기_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF 잡고반복횟수 >= 잡고보행횟수 THEN
        잡고반복횟수 = 0
        GOTO 잡고걷기_멈춤
    ENDIF


잡고걷기_4:

    잡고반복횟수 = 잡고반복횟수 + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT


잡고걷기_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT


잡고걷기_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT


    IF 잡고반복횟수 >= 잡고보행횟수 THEN
        잡고반복횟수 = 0
        GOTO 잡고걷기_멈춤
    ENDIF

    GOTO 잡고걷기_1


잡고걷기_멈춤:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB 잡고안정화자세
    SPEED 10
    GOSUB 잡고기본자세

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

잡고안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    RETURN

잡고기본자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    RETURN


잡고후진종종걸음:
    '넘어진확인 = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF 잡고후진보행순서 = 0 THEN
        잡고후진보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 120, 100
        WAIT

        GOTO 잡고후진종종걸음_1
    ELSE
        잡고후진보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 120, 100
        WAIT

        GOTO 잡고후진종종걸음_4
    ENDIF


    '**********************

잡고후진종종걸음_1:
    잡고후진반복횟수 = 잡고후진반복횟수 + 1
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 120, 100
    WAIT


잡고후진종종걸음_2:
    MOVE G6A,95,  90, 135, 90, 104
    MOVE G6D,104,  77, 146,  91,  100
    WAIT

잡고후진종종걸음_3:
    MOVE G6A, 103,  79, 146,  89, 100
    MOVE G6D,95,   65, 146, 103,  102
    WAIT


    IF 잡고후진반복횟수 >= 잡고후진보행횟수 THEN
        잡고후진반복횟수 = 0
        GOTO 잡고후진종종걸음_멈춤
    ENDIF


    '*********************************

잡고후진종종걸음_4:
    잡고후진반복횟수 = 잡고후진반복횟수 + 1
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 120, 100
    WAIT


잡고후진종종걸음_5:
    MOVE G6A,104,  77, 146,  91,  100
    MOVE G6D,95,  90, 135, 90, 104
    WAIT

잡고후진종종걸음_6:
    MOVE G6D, 103,  79, 146,  89, 100
    MOVE G6A,95,   65, 146, 103,  102
    WAIT



    IF 잡고후진반복횟수 >= 잡고후진보행횟수 THEN
        잡고후진반복횟수 = 0
        GOTO 잡고후진종종걸음_멈춤
    ENDIF



    GOTO 잡고후진종종걸음_1


잡고후진종종걸음_멈춤:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB 잡고안정화자세
    SPEED 10
    GOSUB 잡고기본자세

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN


전진종종걸음:
    '넘어진확인 = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO 전진종종걸음_1
    ELSE
        보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO 전진종종걸음_4
    ENDIF
    '**************************************************

후진종종걸음:
    
    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF 후진보행순서 = 0 THEN
        후진보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO 후진종종걸음_1
    ELSE
        후진보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO 후진종종걸음_4
    ENDIF


    '**********************

후진종종걸음_1:
   후진반복횟수 = 후진반복횟수 + 1
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6B,115
    MOVE G6C,85
    WAIT


후진종종걸음_2:
    MOVE G6A,95,  90, 135, 90, 104
    MOVE G6D,104,  77, 146,  91,  100
    WAIT

후진종종걸음_3:
    MOVE G6A, 103,  79, 146,  89, 100
    MOVE G6D,95,   65, 146, 103,  102
    WAIT

    IF 후진반복횟수 >= 후진보행횟수 THEN
        후진반복횟수 = 0
        GOTO 후진종종걸음_멈춤
    ENDIF


    '*********************************

후진종종걸음_4:

   후진반복횟수 = 후진반복횟수 + 1
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6C,115
    MOVE G6B,85
    WAIT


후진종종걸음_5:
    MOVE G6A,104,  77, 146,  91,  100
    MOVE G6D,95,  90, 135, 90, 104
    WAIT

후진종종걸음_6:
    MOVE G6D, 103,  79, 146,  89, 100
    MOVE G6A,95,   65, 146, 103,  102
    WAIT

    IF 후진반복횟수 >= 후진보행횟수 THEN
        후진반복횟수 = 0
        GOTO 후진종종걸음_멈춤
    ENDIF



    GOTO 후진종종걸음_1


후진종종걸음_멈춤:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB 안정화자세
    SPEED 10
    GOSUB 기본자세

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN
    
    

전진종종걸음_1:

    반복횟수 = 반복횟수 + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B, 100
    MOVE G6C,100
    WAIT

    '**************************************************
전진종종걸음_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT

    '**************************************************
전진종종걸음_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF 반복횟수 >= 보행횟수 THEN
        반복횟수 = 0
        GOTO 전진종종걸음_멈춤
    ENDIF

    '***************************************************
전진종종걸음_4:

    반복횟수 = 반복횟수 + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6C, 100
    MOVE G6B,100
    WAIT

    '**************************************************
전진종종걸음_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT

    '**************************************************
전진종종걸음_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT


    IF 반복횟수 >= 보행횟수 THEN
        반복횟수 = 0
        GOTO 전진종종걸음_멈춤
    ENDIF

    GOTO 전진종종걸음_1


    '**************************************************
전진종종걸음_멈춤:
    HIGHSPEED SETOFF
    SPEED 15
    'GOSUB 안정화자세
    GOSUB 아래로안정화자세
    SPEED 10
    'GOSUB 기본자세
    GOSUB 아래로기본자세

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

    '*************************************************
안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    WAIT
    '자세 = 0

    RETURN



아래로종종걸음:
    '넘어진확인 = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,100,  30,  80, 100, 100, 100
        MOVE G6C,100,  30,  80, 100, 160, 100
        WAIT

        GOTO 아래로종종걸음_1
    ELSE
        보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO 아래로종종걸음_4
    ENDIF
    '**************************************************

아래로종종걸음_1:

    반복횟수 = 반복횟수 + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B, 100
    MOVE G6C,100
    WAIT

    '**************************************************
아래로종종걸음_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT

    '**************************************************
아래로종종걸음_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF 반복횟수 >= 보행횟수 THEN
        반복횟수 = 0
        GOTO 아래로종종걸음_멈춤
    ENDIF

    '***************************************************
아래로종종걸음_4:

    반복횟수 = 반복횟수 + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6C, 100
    MOVE G6B,100
    WAIT

    '**************************************************
아래로종종걸음_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT

    '**************************************************
아래로종종걸음_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT


    IF 반복횟수 >= 보행횟수 THEN
        반복횟수 = 0
        GOTO 아래로종종걸음_멈춤
    ENDIF

    GOTO 아래로종종걸음_1


    '**************************************************
아래로종종걸음_멈춤:
    HIGHSPEED SETOFF
    SPEED 15
    'GOSUB 안정화자세
    GOSUB 아래로안정화자세
    SPEED 10
    'GOSUB 기본자세
    GOSUB 아래로기본자세

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

    '**************************************************
아래로안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 160, 100
    WAIT
    '자세 = 0

    RETURN


아래로기본자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 160, 100
    WAIT
    RETURN
    '**************************************************

앞뒤기울기측정:
    FOR i = 0 TO COUNT_MAX
        CD = AD(앞뒤기울기AD포트)   '기울기 앞뒤
        IF CD > 250 OR CD < 5 THEN RETURN
        IF CD > MIN AND CD < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF CD < MIN THEN GOSUB 기울기앞
    IF CD > MAX THEN GOSUB 기울기뒤

    RETURN
    '**************************************************
기울기앞:
    CD = AD(앞뒤기울기AD포트)
    IF CD < MIN THEN  GOSUB 뒤로일어나기
    RETURN

기울기뒤:
    CD = AD(앞뒤기울기AD포트)
    IF CD > MAX THEN GOSUB 앞으로일어나기
    RETURN
    '**************************************************
좌우기울기측정:

    FOR i = 0 TO COUNT_MAX
        DD = AD(좌우기울기AD포트)   '기울기 좌우
        IF DD > 250 OR DD < 5 THEN RETURN
        IF DD > MIN AND DD < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF DD < MIN OR DD > MAX THEN
        SPEED 8
        MOVE G6B,140,  40,  80
        MOVE G6C,140,  40,  80
        WAIT
        GOSUB 기본자세
        RETURN

    ENDIF
    RETURN



    '********************************




뒤로일어나기:
    HIGHSPEED SETOFF
    PTP SETON
    PTP ALLON


    GOSUB All_motor_Reset

    SPEED 15
    GOSUB 기본자세

    MOVE G6A,90, 130, ,  80, 110, 100
    MOVE G6D,90, 130, 120,  80, 110, 100
    MOVE G6B,150, 160,  10, 100, 100, 100
    MOVE G6C,150, 160,  10, 100, 100, 100
    WAIT

    MOVE G6B,170, 140,  10, 100, 100, 100
    MOVE G6C,170, 140,  10, 100, 100, 100
    WAIT

    MOVE G6B,185,  20, 70,  100, 100, 100
    MOVE G6C,185,  20, 70,  100, 100, 100
    WAIT
    SPEED 10
    MOVE G6A, 80, 155,  85, 150, 150, 100
    MOVE G6D, 80, 155,  85, 150, 150, 100
    MOVE G6B,185,  20, 70,  100, 100, 100
    MOVE G6C,185,  20, 70,  100, 100, 100
    WAIT



    MOVE G6A, 75, 162,  55, 162, 155, 100
    MOVE G6D, 75, 162,  59, 162, 155, 100
    MOVE G6B,188,  10, 100, 100, 100, 100
    MOVE G6C,188,  10, 100, 100, 100, 100
    WAIT

    SPEED 10
    MOVE G6A, 60, 162,  30, 162, 145, 100
    MOVE G6D, 60, 162,  30, 162, 145, 100
    MOVE G6B,170,  10, 100, 100, 100, 100
    MOVE G6C,170,  10, 100, 100, 100, 100
    WAIT
    GOSUB Leg_motor_mode3
    MOVE G6A, 60, 150,  28, 155, 140, 100
    MOVE G6D, 60, 150,  28, 155, 140, 100
    MOVE G6B,150,  60,  90, 100, 100, 100
    MOVE G6C,150,  60,  90, 100, 100, 100
    WAIT

    MOVE G6A,100, 150,  28, 140, 100, 100
    MOVE G6D,100, 150,  28, 140, 100, 100
    MOVE G6B,130,  50,  85, 100, 100, 100
    MOVE G6C,130,  50,  85, 100, 100, 100
    WAIT
    DELAY 100

    MOVE G6A,100, 150,  33, 140, 100, 100
    MOVE G6D,100, 150,  33, 140, 100, 100
    WAIT
    SPEED 10
    GOSUB 기본자세

    DELAY 200


    RETURN

    '**********************************************
앞으로일어나기:

    HIGHSPEED SETOFF
    PTP SETON
    PTP ALLON

    GOSUB  All_motor_Reset


    SPEED 15
    MOVE G6A,100, 15,  70, 140, 100,
    MOVE G6D,100, 15,  70, 140, 100,
    MOVE G6B,20,  140,  15
    MOVE G6C,20,  140,  15
    WAIT

    SPEED 12
    MOVE G6A,100, 136,  35, 80, 100,
    MOVE G6D,100, 136,  35, 80, 100,
    MOVE G6B,20,  30,  80
    MOVE G6C,20,  30,  80
    WAIT

    SPEED 12
    MOVE G6A,100, 165,  70, 30, 100,
    MOVE G6D,100, 165,  70, 30, 100,
    MOVE G6B,30,  20,  95
    MOVE G6C,30,  20,  95
    WAIT

    SPEED 10
    MOVE G6A,100, 165,  45, 90, 100,
    MOVE G6D,100, 165,  45, 90, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 10
    GOSUB 기본자세

    RETURN



    '***************************************************

오른쪽으로:

    SPEED 12
    MOVE G6D, 93,  90, 120, 105, 104, 100
    MOVE G6A,103,  76, 145,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  77, 145, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 15
    MOVE G6D,98,  76, 145,  93, 100, 100
    MOVE G6A,98,  76, 145,  93, 100, 100
    WAIT

    SPEED 8

    'GOSUB 기본자세

    RETURN
    '**********************************************

왼쪽으로:

    SPEED 12
    MOVE G6A, 93,  90, 120, 105, 104, 100
    MOVE G6D,103,  76, 145,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  77, 145, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 15
    MOVE G6A,98,  76, 145,  93, 100, 100
    MOVE G6D,98,  76, 145,  93, 100, 100
    WAIT

    SPEED 8

    'GOSUB 기본자세
    RETURN



아래로오른쪽으로:

    SPEED 12
    MOVE G6D, 93,  90, 120, 105, 104, 100
    MOVE G6A,103,  76, 145,  93, 104, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 160, 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  77, 145, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 15
    MOVE G6D,98,  76, 145,  93, 100, 100
    MOVE G6A,98,  76, 145,  93, 100, 100
    WAIT

    SPEED 8

    'GOSUB 기본자세

    RETURN
    '**********************************************

아래로왼쪽으로:

    SPEED 12
    MOVE G6A, 93,  90, 120, 105, 104, 100
    MOVE G6D,103,  76, 145,  93, 104, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 160, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  77, 145, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 15
    MOVE G6A,98,  76, 145,  93, 100, 100
    MOVE G6D,98,  76, 145,  93, 100, 100
    WAIT

    SPEED 8

    'GOSUB 기본자세
    RETURN


    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=



    '***************************************
MOTOR_ON: '전포트서보모터사용설정
    MOTOR G24
    RETURN

    '***********************************
MOTOR_OFF: '전포트서보모터설정해제
    MOTOROFF G6B
    MOTOROFF G6C
    MOTOROFF G6A
    MOTOROFF G6D
    RETURN
    '***********************************
MOTOR_GET: '위치값피드백
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,0,0,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN


    '*******기본자세관련*****************
시작자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 120, 100
    WAIT
    RETURN


기본자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    WAIT
    RETURN
    '*************************************
차렷자세:
    MOVE G6A,100, 56, 182, 76, 100, 100
    MOVE G6D,100, 56, 182, 76, 100, 100
    MOVE G6B,100, 20, 90, 100, 100, 100
    MOVE G6C,100, 20, 90, 100, 100, 100
    WAIT
    RETURN
    '**************************************
앉은자세:

    MOVE G6A,100, 143,  28, 142, 100, 100
    MOVE G6D,100, 143,  28, 142, 100, 100
    MOVE G6B,100,  30,  80
    MOVE G6C,100,  30,  80
    WAIT
    RETURN
    '***************************************

    '************************************************
All_motor_Reset:

    MOTORMODE G6A,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1
    MOTORMODE G6B,1,1,1, , ,1
    MOTORMODE G6C,1,1,1

    RETURN
    '************************************************
All_motor_mode2:

    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    MOTORMODE G6B,2,2,2, , ,2
    MOTORMODE G6C,2,2,2

    RETURN
    '************************************************
All_motor_mode3:

    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    MOTORMODE G6B,3,3,3, , ,3
    MOTORMODE G6C,3,3,3

    RETURN
    '************************************************
Leg_motor_mode1:
    MOTORMODE G6A,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1
    RETURN
    '************************************************
Leg_motor_mode2:
    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    RETURN

    '************************************************
Leg_motor_mode3:
    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    RETURN
    '************************************************
Leg_motor_mode4:
    MOTORMODE G6A,3,2,2,1,3
    MOTORMODE G6D,3,2,2,1,3
    RETURN
    '************************************************
Leg_motor_mode5:
    MOTORMODE G6A,3,2,2,1,2
    MOTORMODE G6D,3,2,2,1,2
    RETURN
    '************************************************
    '************************************************
Arm_motor_mode1:
    MOTORMODE G6B,1,1,1
    MOTORMODE G6C,1,1,1
    RETURN
    '************************************************
Arm_motor_mode2:
    MOTORMODE G6B,2,2,2
    MOTORMODE G6C,2,2,2
    RETURN
    '************************************************
Arm_motor_mode3:
    MOTORMODE G6B,3,3,3
    MOTORMODE G6C,3,3,3
    RETURN

    '********************