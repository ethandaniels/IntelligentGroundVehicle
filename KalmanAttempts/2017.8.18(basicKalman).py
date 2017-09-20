import numpy as np


#This will not be a function, will most likely sit above solving code

##Inital State
#Setup inital state (zero position) 1x6 x,y,x',y',x'',y''
x = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T

##Uncertanity Matrix
#Setup initial uncertainty 6x6 w/ highest uncertainty in pos and lowest in acc
P = np.diag([100.0, 100.0, 10.0, 10.0, 1.0, 1.0])

##State model
#Setup model (Standard kinematic equations) 6x6
dt = 0.1 #Fastest Sensor is 10Hz refresh rate

A = np.matrix([[1.0, 0.0, dt, 0.0, 1/2.0*dt**2, 0.0],
               [0.0, 1.0, 0.0, dt, 0.0, 1/2.0*dt**2],
               [0.0, 0.0, 1.0, 0.0, dt, 0.0],
               [0.0, 0.0, 0.0, 1.0, 0.0, dt],
               [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

##Measurment Matrix
#Setup matrix which defines what each sensor models (eg: GPS models position)
H = np.matrix([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])

##Measurment Covariance
#Measurement noise covariance; this is defined by the std deviation of
#each sensor, we will start with some standard threshold,
#NOTE:Sensor warmup can help define this varaince
ra = 10.0**2 #noise in acceleration measuremnt
rp = 100.0**2 #noise in position measurment
#standard noise covariance matrix,
R = np.matrix([[rp, 0.0, 0.0, 0.0],
               [0.0, rp, 0.0, 0.0],
               [0.0, 0.0, ra, 0.0],
               [0.0, 0.0, 0.0, ra]])

##Provess Covariance
#Process noise covariance; this is much harder to define
    #this essentially is added noise to the system from external "forces"
    #What is applied is a basic process noise known for kinematic equations
    #Note: Most process noise comes from accelerometer..
    #this makes sense because as they integrate over time their error gets even larger (+c)
sa = 0.001
G = np.matrix([[1/2.0*dt**2],
              [1/2.0*dt**2],
              [dt],
              [dt],
              [1.0],
              [1.0]])
Q = G*G.T*sa**2
##Identity Matrix
#Setup an identity matrix 6x6
I = np.eye(n)

while (!@goal):
    #call GPS Function
    #call ACC Function
    #call compass heading

    ##Position measurments
    sp = 1.0 #sigma applied to GPS
    px = posX #current GPS x position
    py = posY #current GPS y position

    mpx = np.array(px+sp)
    mpy = np.array(py+sp)

    ##Acceleration measuremnts
    #Acceleration module will be read when function is called
    sa= 0.1 # Sigma for acceleration
    ax = accX# in X
    ay = accY# in Y

    mx = np.array(ax+sa)
    my = np.array(ay+sa)

    ##Time Update (Prediction)
    #Project the state ahead
    x = A*x

    #Project the error covariance ahead
    P = A*P*A.T + Q

    #Create if statement to control to only complete measurment update every second
    if(GPS refresh):
        # Compute the Kalman Gain
        S = H*P*H.T + R
        K = (P*H.T) * np.linalg.pinv(S)


        # Update the estimate via z
        y = H*x                            # Innovation or Residual
        x = x + (K*y)

        # Update the error covariance
        P = (I - (K*H))*P

    #create new variable for current x and y and set according to position in matrix x

    ##Solve for next best Move

    #Avoid shit ahead of you

    #if its been a long time reset the kalman filter (function to clear kalman?)
