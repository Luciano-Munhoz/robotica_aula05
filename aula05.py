import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf
import math

I = 0
old_error = 0

kp = 1
ki = 0.01
kd = 1

odom = Odometry()
scan = LaserScan()

rospy.init_node('cmd_node')

# Auxiliar functions ------------------------------------------------
def getAngle(msg):
    quaternion = msg.pose.pose.orientation
    quat = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
    euler = tf.transformations.euler_from_quaternion(quat)
    yaw = euler[2]*180.0/math.pi
    return yaw

# CALLBACKS ---------------------------------------------------------
def odomCallBack(msg):
    global odom
    odom = msg
    
def scanCallBack(msg):
    global scan
    scan = msg
#--------------------------------------------------------------------

# TIMER - Control Loop ----------------------------------------------
def timerCallBack(event):
    global I
    global old_error
    """
    yaw = getAngle(odom)
    setpoint = -45
    error = (setpoint - yaw)
    
    if abs(error) > 180:
        if setpoint < 0:
            error += 360 
        else:
            error -= 360
    """
    """
    setpoint = (-1,-1)
    position = odom.pose.pose.position
    dist = setpoint[0] - position.x #math.sqrt((setpoint[0] - position.x)**2 + (setpoint[1] - position.y) **2)
    error = dist
    """
    
    setpoint = 0.5
    
    scan_len = len(scan.ranges)
    if scan_len > 0:
        read = min(scan.ranges[scan_len-10 : scan_len+10])

        error = -(setpoint - read)
        
        P = kp*error
        #I = I + error * ki
        #D = (error - old_error)*kd
        I = 0;
        D = 0;
        control = P+I+D
        old_error = error
        if control > 0.1:
            control = 0.1
        elif control < -0.1:
            control = -0.1
    else:
        control = 0        
    
    msg = Twist()
    msg.linear.x = control
    pub.publish(msg)
    

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
odom_sub = rospy.Subscriber('/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/scan', LaserScan, scanCallBack)
# 1/(((2+0+1+7+0+1+3+1+0+6)+(2+0+1+6+0+0+1+1+0+0)+(2+0+1+7+0+0+6+0+7+7)+(2+0+1+8+0+1+9+0+2+4))/4);

timer = rospy.Timer(rospy.Duration(0.04494382022), timerCallBack)

rospy.spin()
