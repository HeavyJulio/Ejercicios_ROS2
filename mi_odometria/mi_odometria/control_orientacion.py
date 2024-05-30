
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf_transformations as tft
from math import pi



class ControlOrientacion(Node):
	def __init__(self):
		super().__init__('turn_to_orientacion')
		#Subscriber
		self.subscription = self.create_subscription(Odometry,'/odom',self.odometry_callback,10)
        #Publisher
		self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
 		#self.subscription
   
        #Orientación deseada en radianes:
		self.desired_orientation = pi/2
		#Ganancia proporcional para el giro
		self.p_gain= 1.0
		
        
	
	def odometry_callback(self, msg):
	# Obtenemos el cuaternio
		quaternion = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
 	# Convierte angulos de euler(roll, pitch, yaw)
		roll, pitch, yaw = tft.euler_from_quaternion(quaternion)
 		# Muestra los angulos de euler
		self.get_logger().info(f'Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}')
		
        #Calculamos el error
		angular_error=self.wrap_angle(self.desired_orientation - yaw)
        #Control proporcional para controlar la velocidad de giro
		angular_velocity = self.p_gain*angular_error
	
	#Publicamos esa velocidad
		twist = Twist()
		twist.angular.z=angular_velocity
		twist.linear.x =0.0
		self.publisher.publish(twist)


        # Log
		self.get_logger().info(f'Error: {angular_error:.2f}, Commanded Angular Velocity: {angular_velocity:.2f}')



	def wrap_angle(self,angle):
	

		while angle>pi:
			angle-=2*pi
		while angle<-pi:
			angle+=2*pi
		
		return angle
		
        
def main(args=None):
	rclpy.init(args=args)
	control_orientacion=ControlOrientacion()
	rclpy.spin(control_orientacion)
	control_orientacion.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
 	main()
