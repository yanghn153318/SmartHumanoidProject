'�����ȱ�
DIM ��������Ƚ�� AS BYTE
DIM �����ݺ�Ƚ�� AS BYTE
DIM ����������� AS BYTE

'��������ȱ�
DIM �����������Ƚ�� AS BYTE
DIM ��������ݺ�Ƚ�� AS BYTE
DIM �������������� AS BYTE

'������ȱ�
DIM ���⺸��Ƚ�� AS BYTE
DIM ����ݺ�Ƚ�� AS BYTE
DIM ���⺸����� AS BYTE
DIM �������� AS BYTE
DIM INITIAL AS BYTE

'���ȱ�
DIM DATA AS BYTE
DIM �����Ƚ�� AS BYTE
DIM ���ݺ�Ƚ�� AS BYTE
DIM �������� AS BYTE

'�ȱ�
DIM ����Ƚ�� AS BYTE
DIM �ݺ�Ƚ�� AS BYTE
DIM ������� AS BYTE

'�Ѿ������Ͼ��
DIM CD AS BYTE
DIM DD AS BYTE
DIM i AS BYTE

' ���⼾����Ʈ ����

CONST �յڱ���AD��Ʈ = 0
CONST �¿����AD��Ʈ = 1


CONST ����Ȯ�νð� = 5  'ms
CONST MIN = 61         '�ڷγѾ�������
CONST MAX = 107         '�����γѾ�������
CONST COUNT_MAX = 20


DIM ���ܼ��Ÿ���  AS BYTE
CONST ���ܼ�AD��Ʈ  = 4


'^^^^^^^^^^^^�����ڵ��뺯��^^^^^^^^^^
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

DIM �������� AS BYTE

'�������Ͽ���

PRINT "OPEN 20GongMo.mrs !"
PRINT "VOLUME 200 !"



' ��������---------------------------------------
'DIM a AS BYTE
'DIM b AS BYTE
DIM GYRO_ONOFF AS BYTE
'DIM A_old AS BYTE
'DIM X AS BYTE
'DIM Y AS BYTE
DIM A AS BYTE

'���͹��⼳��
DIR G6A,1,0,0,1,0,0   '���ʴٸ�:����0~5��
DIR G6D,0,1,1,0,1,0   '�����ʴٸ�:����18~23��
DIR G6B,1,1,1,1,1,1   '������:����6~11��
DIR G6C,0,0,0,0,0,0   '��������:����12~17��

'���͵��������
PTP SETON       '�����׷캰 ���������� ����
PTP ALLON      '��ü���� ������ ���� ����

'������ġ���ǵ��
GOSUB MOTOR_GET

DIM DIS AS BYTE


'���ͻ�뼳��
GOSUB MOTOR_ON
SPEED 5
GOSUB �⺻�ڼ�
'-----------------------------------------------



'����Ƚ���� ������ ������~~~~~~
�����Ƚ��= 4
���ݺ�Ƚ�� = 0

���⺸��Ƚ�� = 8
����ݺ�Ƚ�� = 0

����Ƚ��= 6
�ݺ�Ƚ�� = 0

�������� = 0

�����������Ƚ�� = 10
��������ݺ�Ƚ�� = 0

��������Ƚ�� = 6
�����ݺ�Ƚ�� = 0


MAIN:

	DELAY 100

    GOSUB �յڱ�������
    GOSUB �¿��������

    IF STDR =0 THEN
        GOSUB �����ڼ�
        IF INITIAL = 0 THEN
           GOSUB ����������
           DELAY 100
           GOSUB ����������
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
        
        
        GOSUB ��������
        GOSUB ��������
        GOSUB ��������
        GOSUB ������20
        GOSUB ���ɾ��
        DELAY 100
        
        GOSUB �⺻�ڼ�
        GOSUB ����������
        GOSUB ������������
        
        GOSUB �⺻�ڼ�
        DELAY 1000
    
    
    ELSEIF STDR = 1 THEN
       
        ERX 4800, A, MAIN
        IF A = 106 THEN
            B = 6
            GOSUB ������������
            GOSUB ������������
            DELAY 100
            GOSUB ������������
            GOSUB ������������
            DELAY 100
            GOSUB ������20
            GOSUB ������90
            GOSUB ����������
            DELAY 100
            GOSUB ����������
            DELAY 100
            GOSUB ����������
            DELAY 100
            
            STDR = 2
        ELSEIF A = 105 THEN
            B = 5
            GOSUB ������������
            GOSUB ������������
            DELAY 100
            GOSUB ������������
            GOSUB ������������
            DELAY 100
            GOSUB ������20
            GOSUB ��������90
            GOSUB ��������
            DELAY 100
            GOSUB ��������
            DELAY 100
            GOSUB ��������
            DELAY 100
            STDR = 2
        ELSE
           GOTO MAIN
        ENDIF
        D = D + 1
        GOSUB �Ʒ��α⺻�ڼ�
        
        DELAY 1000

        GOTO MAIN
    

   ELSEIF D < 2  THEN
       'MUSIC "C" 
        DELAY 100
        ERX 4800, A, MAIN
        'A_old = A           
         
        IF A = 115 THEN
        	MUSIC "A" 
            GOSUB �Ʒ��ο�������
            GOTO MAIN
   
        ELSEIF A = 120 THEN
        	MUSIC "A" 
            GOSUB �Ʒ��ο���������
            GOTO MAIN
   
        ELSEIF A = 110 THEN
        	MUSIC "B" 
            GOSUB �Ʒ�����������
            GOTO MAIN
               
        ELSEIF A = 111 THEN
        	MUSIC "C" 
            GOSUB ������20
            GOTO MAIN
            
        ELSEIF A = 112 THEN
        	MUSIC "C" 
            GOSUB ��������20
            GOTO MAIN
   
        ELSEIF A = 203 THEN
        	MUSIC "D"
            GOSUB �⺻�ڼ�
            DELAY 100
            GOSUB ��������
            GOSUB �����ڼ� 
			GOSUB Ȯ�����θ��ϱ�
            GOSUB �ù�����
            GOSUB �ùοű��
            N = N+1
            GOSUB ��������90
            GOSUB ��������90
            GOSUB ������������
            GOSUB ������������
            GOSUB ������90
            GOTO MAIN
               
        ELSEIF A = 204 THEN
        	MUSIC "D"
            GOSUB �⺻�ڼ�
            DELAY 100
            GOSUB ����������
			GOSUB �����ڼ� 
			GOSUB Ȯ�����θ��ϱ�
			GOSUB �ù�����
			GOSUB �ùοű��                   
            N = N+1
            GOSUB ������90
            GOSUB ������90
            GOSUB ������������
            GOSUB ������������
            GOSUB ��������90
            GOTO MAIN

   
        ELSEIF A = 205 THEN
        	MUSIC "E"
            IF N < 3 THEN
                GOTO ������������
                GOTO MAIN
            ELSEIF N = 3 THEN
                GOTO ��������90
                GOTO ������
                GOTO MAIN
            ENDIF
   
   
        ELSEIF A = 206 THEN
        	MUSIC "E"
            IF N < 3 THEN
                GOTO ������������
                GOTO MAIN
            ELSEIF N = 3 THEN
                GOTO ������90
                GOTO ������
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
        
        GOSUB �⺻�ڼ�
        STOP
   
    ELSE
        D = 0
        GOTO MAIN
    ENDIF

   
    GOTO MAIN   
    
    
    
    
ȭ��ǥ����:
	ERX 4800, A, ȭ��ǥ����
	IF A = 115 THEN
    	MUSIC "A" 
        GOSUB �Ʒ��ο�������
        GOTO ȭ��ǥ����
        
    ELSEIF A = 120 THEN
    	MUSIC "A" 
        GOSUB �Ʒ��ο���������
        GOTO ȭ��ǥ����
       
    ELSEIF A = 111 THEN
    	MUSIC "C" 
        GOSUB ������20
        GOTO ȭ��ǥ����
        
    ELSEIF A = 112 THEN
    	MUSIC "C" 
        GOSUB ��������20
        GOTO ȭ��ǥ����

    ELSEIF A = 110 THEN
    	MUSIC "B" 
    ENDIF
    
    RETURN
    


'***************Ȯ������ ���ϱ�************************
Ȯ�����θ��ϱ�:
    ERX 4800, A, Ȯ�����θ��ϱ�
    IF A = 160 THEN
        GOSUB SAFE
        ��������=0
                
    ELSEIF A = 165 THEN
        GOSUB WARN
        ��������= 1
        GOSUB Ȯ����������
    ENDIF
    
    RETURN
            
'****************�������� ����**************************
Ȯ����������:
    ERX 4800, A, Ȯ����������
    IF X = 0 THEN
        X = A
    ELSEIF Y = 0 THEN
        Y = A
    ELSEIF Z = 0 THEN
        Z = A
    ENDIF
                
    DELAY 2000
    RETURN
    '**********************ȸ��******************************
������90:
    GOSUB ������20
    DELAY 100
    GOSUB ������20
    DELAY 100
    GOSUB ������20
    DELAY 100
    GOSUB ������20
    DELAY 100
    GOSUB ������20
    DELAY 100
    GOSUB ������20
    DELAY 100
'    GOSUB ������20
    WAIT
    RETURN

��������90:
    GOSUB ��������20
    DELAY 100
    GOSUB ��������20
    DELAY 100
    GOSUB ��������20
    DELAY 100
    GOSUB ��������20
    DELAY 100
    GOSUB ��������20
    DELAY 100
    GOSUB ��������20
    DELAY 100
'    GOSUB ��������20
'    GOSUB ��������20
    WAIT
    RETURN


������20:
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

    'GOSUB �⺻�ڼ�
    GOSUB Leg_motor_mode1
    RETURN

��������20:
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

    'GOSUB �⺻�ڼ�
    GOSUB Leg_motor_mode1
    RETURN

    '**********************�����⵿��**************************
���ɾ��:
    ���ܼ��Ÿ��� = AD(���ܼ�AD��Ʈ)
    IF ���ܼ��Ÿ��� <= 80 THEN
        GOSUB ������������
        GOTO ���ɾ��
    ELSEIF ���ܼ��Ÿ��� > 80 THEN
        MUSIC " C"
        GOSUB ������
    ENDIF

������:

    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100

    GOSUB ������������

    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  80,  80, 100, 100, 100
    MOVE G6C,190,  80,  80, 100, 100, 100

    D = D + 1
    WAIT
    RETURN



������������:

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF ���⺸����� = 0 THEN
        ���⺸����� = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,190,  10,  80, 100, 100, 100
        MOVE G6C,190,  10,  80, 100, 100, 100
        WAIT

        GOTO ������������_1
    ELSE
        ���⺸����� = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,190,  10,  80, 100, 100, 100
        MOVE G6C,190,  10,  80, 100, 100, 100
        WAIT

        GOTO ������������_4
    ENDIF

������������_1:

    ����ݺ�Ƚ�� = ����ݺ�Ƚ�� + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT

������������_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT

������������_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF ����ݺ�Ƚ�� >= ���⺸��Ƚ�� THEN
        ����ݺ�Ƚ�� = 0
        GOTO ������������_����
    ENDIF

������������_4:

    ����ݺ�Ƚ�� = ����ݺ�Ƚ�� + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT

������������_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT

������������_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT

    IF ����ݺ�Ƚ�� >= ���⺸��Ƚ�� THEN
        ����ݺ�Ƚ�� = 0
        GOTO ������������_����
    ENDIF

    GOTO ������������_1


������������_����:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB �������ȭ�ڼ�
    SPEED 10
    GOSUB ����⺻�ڼ�

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

�������ȭ�ڼ�:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,190,  10,  80, 100, 100, 100
    MOVE G6C,190,  10,  80, 100, 100, 100
    WAIT
    RETURN


����⺻�ڼ�:
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
    GOSUB �⺻�ڼ�
    WAIT
    RETURN

WEST:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    GOSUB SOUND_W
    GOSUB �⺻�ڼ�
    WAIT
    RETURN

SOUTH:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,10,  30,  80, 100, 100, 100
    MOVE G6C,10,  30,  80, 100, 100, 100
    GOSUB SOUND_S
    GOSUB �⺻�ڼ�
    WAIT
    RETURN

NORTH:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,190,  30,  80, 100, 100, 100
    MOVE G6C,190,  30,  80, 100, 100, 100
    GOSUB SOUND_N
    GOSUB �⺻�ڼ�
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
�ù�����:
	ERX 4800, A, �ù�����
	IF A = 5 THEN
    	GOSUB ��������
    ELSEIF A = 7 THEN
        GOSUB ����������
    ELSEIF A = 9 THEN
        GOSUB ������������   	
    ELSEIF A = 15 THEN
        GOSUB �Ʒ��ο�������
    ELSEIF A = 17 THEN
        GOSUB �Ʒ��ο���������
    ELSEIF A = 19 THEN
        GOSUB �Ʒ�����������
    ENDIF
    RETURN
    
�ùοű��:
	ERX 4800, A, �ùοű��
	IF A = 20 THEN
    	GOSUB �������
        IF ��������=0 THEN
            GOSUB ���ȱ�
            GOSUB ���ǳ���

        ELSEIF ��������=1 THEN
            GOSUB ���������������
            GOSUB ���ǳ���
		ENDIF
	ENDIF
    RETURN


�������:
    '�ɱ�
    MOVE G6A,100, 143,  28, 170, 100, 100
    MOVE G6D,100, 143,  28, 170, 100, 100
    MOVE G6B,150,  30,  80, 100, 100, 100
    MOVE G6C,150,  30,  80, 100, 100, 100
    WAIT
    GOTO ��¥���

��¥���:
    MOVE G6A,100, 143,  28, 170, 100, 100
    MOVE G6D,100, 143,  28, 170, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    GOTO ����Ͼ��

����Ͼ��:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    RETURN

    '-----------------------------------------


���ǳ���:
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
    GOSUB �⺻�ڼ�
    RETURN




    '-------------------------------------------

���ȱ�:
    '�Ѿ���Ȯ�� = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF �������� = 0 THEN
        �������� = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 100, 100
        WAIT

        GOTO ���ȱ�_1
    ELSE
        �������� = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 100, 100
        WAIT

        GOTO ���ȱ�_4
    ENDIF

���ȱ�_1:

    ���ݺ�Ƚ�� = ���ݺ�Ƚ�� + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT


���ȱ�_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT


���ȱ�_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF ���ݺ�Ƚ�� >= �����Ƚ�� THEN
        ���ݺ�Ƚ�� = 0
        GOTO ���ȱ�_����
    ENDIF


���ȱ�_4:

    ���ݺ�Ƚ�� = ���ݺ�Ƚ�� + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT


���ȱ�_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT


���ȱ�_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT


    IF ���ݺ�Ƚ�� >= �����Ƚ�� THEN
        ���ݺ�Ƚ�� = 0
        GOTO ���ȱ�_����
    ENDIF

    GOTO ���ȱ�_1


���ȱ�_����:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB ������ȭ�ڼ�
    SPEED 10
    GOSUB ���⺻�ڼ�

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

������ȭ�ڼ�:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    RETURN

���⺻�ڼ�:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 100, 100
    WAIT
    RETURN


���������������:
    '�Ѿ���Ȯ�� = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF �������������� = 0 THEN
        �������������� = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 120, 100
        WAIT

        GOTO ���������������_1
    ELSE
        �������������� = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,150,  10,  60, 100, 100, 100
        MOVE G6C,150,  10,  60, 100, 120, 100
        WAIT

        GOTO ���������������_4
    ENDIF


    '**********************

���������������_1:
    ��������ݺ�Ƚ�� = ��������ݺ�Ƚ�� + 1
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 120, 100
    WAIT


���������������_2:
    MOVE G6A,95,  90, 135, 90, 104
    MOVE G6D,104,  77, 146,  91,  100
    WAIT

���������������_3:
    MOVE G6A, 103,  79, 146,  89, 100
    MOVE G6D,95,   65, 146, 103,  102
    WAIT


    IF ��������ݺ�Ƚ�� >= �����������Ƚ�� THEN
        ��������ݺ�Ƚ�� = 0
        GOTO ���������������_����
    ENDIF


    '*********************************

���������������_4:
    ��������ݺ�Ƚ�� = ��������ݺ�Ƚ�� + 1
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6B,150,  10,  60, 100, 100, 100
    MOVE G6C,150,  10,  60, 100, 120, 100
    WAIT


���������������_5:
    MOVE G6A,104,  77, 146,  91,  100
    MOVE G6D,95,  90, 135, 90, 104
    WAIT

���������������_6:
    MOVE G6D, 103,  79, 146,  89, 100
    MOVE G6A,95,   65, 146, 103,  102
    WAIT



    IF ��������ݺ�Ƚ�� >= �����������Ƚ�� THEN
        ��������ݺ�Ƚ�� = 0
        GOTO ���������������_����
    ENDIF



    GOTO ���������������_1


���������������_����:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB ������ȭ�ڼ�
    SPEED 10
    GOSUB ���⺻�ڼ�

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN


������������:
    '�Ѿ���Ȯ�� = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF ������� = 0 THEN
        ������� = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO ������������_1
    ELSE
        ������� = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO ������������_4
    ENDIF
    '**************************************************

������������:
    
    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF ����������� = 0 THEN
        ����������� = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO ������������_1
    ELSE
        ����������� = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO ������������_4
    ENDIF


    '**********************

������������_1:
   �����ݺ�Ƚ�� = �����ݺ�Ƚ�� + 1
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6B,115
    MOVE G6C,85
    WAIT


������������_2:
    MOVE G6A,95,  90, 135, 90, 104
    MOVE G6D,104,  77, 146,  91,  100
    WAIT

������������_3:
    MOVE G6A, 103,  79, 146,  89, 100
    MOVE G6D,95,   65, 146, 103,  102
    WAIT

    IF �����ݺ�Ƚ�� >= ��������Ƚ�� THEN
        �����ݺ�Ƚ�� = 0
        GOTO ������������_����
    ENDIF


    '*********************************

������������_4:

   �����ݺ�Ƚ�� = �����ݺ�Ƚ�� + 1
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6C,115
    MOVE G6B,85
    WAIT


������������_5:
    MOVE G6A,104,  77, 146,  91,  100
    MOVE G6D,95,  90, 135, 90, 104
    WAIT

������������_6:
    MOVE G6D, 103,  79, 146,  89, 100
    MOVE G6A,95,   65, 146, 103,  102
    WAIT

    IF �����ݺ�Ƚ�� >= ��������Ƚ�� THEN
        �����ݺ�Ƚ�� = 0
        GOTO ������������_����
    ENDIF



    GOTO ������������_1


������������_����:
    HIGHSPEED SETOFF
    SPEED 15
    GOSUB ����ȭ�ڼ�
    SPEED 10
    GOSUB �⺻�ڼ�

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN
    
    

������������_1:

    �ݺ�Ƚ�� = �ݺ�Ƚ�� + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B, 100
    MOVE G6C,100
    WAIT

    '**************************************************
������������_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT

    '**************************************************
������������_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF �ݺ�Ƚ�� >= ����Ƚ�� THEN
        �ݺ�Ƚ�� = 0
        GOTO ������������_����
    ENDIF

    '***************************************************
������������_4:

    �ݺ�Ƚ�� = �ݺ�Ƚ�� + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6C, 100
    MOVE G6B,100
    WAIT

    '**************************************************
������������_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT

    '**************************************************
������������_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT


    IF �ݺ�Ƚ�� >= ����Ƚ�� THEN
        �ݺ�Ƚ�� = 0
        GOTO ������������_����
    ENDIF

    GOTO ������������_1


    '**************************************************
������������_����:
    HIGHSPEED SETOFF
    SPEED 15
    'GOSUB ����ȭ�ڼ�
    GOSUB �Ʒ��ξ���ȭ�ڼ�
    SPEED 10
    'GOSUB �⺻�ڼ�
    GOSUB �Ʒ��α⺻�ڼ�

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

    '*************************************************
����ȭ�ڼ�:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    WAIT
    '�ڼ� = 0

    RETURN



�Ʒ�����������:
    '�Ѿ���Ȯ�� = 0

    SPEED 10
    HIGHSPEED SETON
    GOSUB All_motor_mode3

    IF ������� = 0 THEN
        ������� = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  77, 145,  93, 98
        MOVE G6B,100,  30,  80, 100, 100, 100
        MOVE G6C,100,  30,  80, 100, 160, 100
        WAIT

        GOTO �Ʒ�����������_1
    ELSE
        ������� = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  77, 145,  93, 98
        MOVE G6B,100,  35
        MOVE G6C,100,  35
        WAIT

        GOTO �Ʒ�����������_4
    ENDIF
    '**************************************************

�Ʒ�����������_1:

    �ݺ�Ƚ�� = �ݺ�Ƚ�� + 1

    MOVE G6A,95,  95, 120, 100, 104
    MOVE G6D,104,  77, 146,  91,  102
    MOVE G6B, 100
    MOVE G6C,100
    WAIT

    '**************************************************
�Ʒ�����������_2:
    MOVE G6A,95,  85, 130, 103, 104
    MOVE G6D,104,  79, 146,  89,  100
    WAIT

    '**************************************************
�Ʒ�����������_3:
    MOVE G6A,103,   85, 130, 103,  100
    MOVE G6D, 95,  79, 146,  89, 102
    WAIT


    IF �ݺ�Ƚ�� >= ����Ƚ�� THEN
        �ݺ�Ƚ�� = 0
        GOTO �Ʒ�����������_����
    ENDIF

    '***************************************************
�Ʒ�����������_4:

    �ݺ�Ƚ�� = �ݺ�Ƚ�� + 1

    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 146,  91,  102
    MOVE G6C, 100
    MOVE G6B,100
    WAIT

    '**************************************************
�Ʒ�����������_5:
    MOVE G6D,95,  85, 130, 103, 104
    MOVE G6A,104,  79, 146,  89,  100
    WAIT

    '**************************************************
�Ʒ�����������_6:
    MOVE G6D,103,   85, 130, 103,  100
    MOVE G6A, 95,  79, 146,  89, 102
    WAIT


    IF �ݺ�Ƚ�� >= ����Ƚ�� THEN
        �ݺ�Ƚ�� = 0
        GOTO �Ʒ�����������_����
    ENDIF

    GOTO �Ʒ�����������_1


    '**************************************************
�Ʒ�����������_����:
    HIGHSPEED SETOFF
    SPEED 15
    'GOSUB ����ȭ�ڼ�
    GOSUB �Ʒ��ξ���ȭ�ڼ�
    SPEED 10
    'GOSUB �⺻�ڼ�
    GOSUB �Ʒ��α⺻�ڼ�

    DELAY 400

    GOSUB Leg_motor_mode1
    RETURN

    '**************************************************
�Ʒ��ξ���ȭ�ڼ�:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 160, 100
    WAIT
    '�ڼ� = 0

    RETURN


�Ʒ��α⺻�ڼ�:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 160, 100
    WAIT
    RETURN
    '**************************************************

�յڱ�������:
    FOR i = 0 TO COUNT_MAX
        CD = AD(�յڱ���AD��Ʈ)   '���� �յ�
        IF CD > 250 OR CD < 5 THEN RETURN
        IF CD > MIN AND CD < MAX THEN RETURN
        DELAY ����Ȯ�νð�
    NEXT i

    IF CD < MIN THEN GOSUB �����
    IF CD > MAX THEN GOSUB �����

    RETURN
    '**************************************************
�����:
    CD = AD(�յڱ���AD��Ʈ)
    IF CD < MIN THEN  GOSUB �ڷ��Ͼ��
    RETURN

�����:
    CD = AD(�յڱ���AD��Ʈ)
    IF CD > MAX THEN GOSUB �������Ͼ��
    RETURN
    '**************************************************
�¿��������:

    FOR i = 0 TO COUNT_MAX
        DD = AD(�¿����AD��Ʈ)   '���� �¿�
        IF DD > 250 OR DD < 5 THEN RETURN
        IF DD > MIN AND DD < MAX THEN RETURN
        DELAY ����Ȯ�νð�
    NEXT i

    IF DD < MIN OR DD > MAX THEN
        SPEED 8
        MOVE G6B,140,  40,  80
        MOVE G6C,140,  40,  80
        WAIT
        GOSUB �⺻�ڼ�
        RETURN

    ENDIF
    RETURN



    '********************************




�ڷ��Ͼ��:
    HIGHSPEED SETOFF
    PTP SETON
    PTP ALLON


    GOSUB All_motor_Reset

    SPEED 15
    GOSUB �⺻�ڼ�

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
    GOSUB �⺻�ڼ�

    DELAY 200


    RETURN

    '**********************************************
�������Ͼ��:

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
    GOSUB �⺻�ڼ�

    RETURN



    '***************************************************

����������:

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

    'GOSUB �⺻�ڼ�

    RETURN
    '**********************************************

��������:

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

    'GOSUB �⺻�ڼ�
    RETURN



�Ʒ��ο���������:

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

    'GOSUB �⺻�ڼ�

    RETURN
    '**********************************************

�Ʒ��ο�������:

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

    'GOSUB �⺻�ڼ�
    RETURN


    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=



    '***************************************
MOTOR_ON: '����Ʈ�������ͻ�뼳��
    MOTOR G24
    RETURN

    '***********************************
MOTOR_OFF: '����Ʈ�������ͼ�������
    MOTOROFF G6B
    MOTOROFF G6C
    MOTOROFF G6A
    MOTOROFF G6D
    RETURN
    '***********************************
MOTOR_GET: '��ġ���ǵ��
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,0,0,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN


    '*******�⺻�ڼ�����*****************
�����ڼ�:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 120, 100
    WAIT
    RETURN


�⺻�ڼ�:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80, 100, 100, 100
    MOVE G6C,100,  30,  80, 100, 100, 100
    WAIT
    RETURN
    '*************************************
�����ڼ�:
    MOVE G6A,100, 56, 182, 76, 100, 100
    MOVE G6D,100, 56, 182, 76, 100, 100
    MOVE G6B,100, 20, 90, 100, 100, 100
    MOVE G6C,100, 20, 90, 100, 100, 100
    WAIT
    RETURN
    '**************************************
�����ڼ�:

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