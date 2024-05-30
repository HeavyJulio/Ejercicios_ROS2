
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
"""

import rclpy
import rclpy.clock
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import rclpy.time
import tf_transformations as tft
from math import pi



class Ejercicio_01(Node):
	def __init__(self):
		super().__init__('avanza_con_tiempo')
		#Subscriber
		self.subscription = self.create_subscription(Odometry,'/odom',self.get_position,10)
        #Publisher
		self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
 		#self.subscription
   
        #Orientación deseada en radianes:
		#self.desired_orientation = pi/2
		#Ganancia proporcional para el giro
		#self.p_gain= 1.0
		self.move_robot()
		
        
	
	def get_position(self, msg):
	# Obtenemos el cuaternio
		quaternion = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
 	# Convierte angulos de euler(roll, pitch, yaw)
		roll, pitch, self.yaw = tft.euler_from_quaternion(quaternion)
 		# Muestra los angulos de euler
	#self.get_logger().info(f'Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}')
		self.Position=msg.pose.pose.linear
	
		self.Posicion_x=self.Position.x
		self.Posicion_y=self.Position.y
	
		self.get_logger().info(f'Posición x: {self.Posicion_x:.2f}, Posición y: {self.Posicion_y:.2f}, Yaw: {self.yaw:.2f}')
		
        #Calculamos el error
		#angular_error=self.wrap_angle(self.desired_orientation - yaw)
        #Control proporcional para controlar la velocidad de giro
		#angular_velocity = self.p_gain*angular_error
	
	#Publicamos esa velocidad
		self.twist = Twist()
		#twist.angular.z=angular_velocity
		#twist.linear.x =0.0
		#self.publisher.publish(twist)


        # Log
		#self.get_logger().info(f'Error: {angular_error:.2f}, Commanded Angular Velocity: {angular_velocity:.2f}')



	def wrap_angle(self,angle):
	

		while angle>pi:
			angle-=2*pi
		while angle<-pi:
			angle+=2*pi
		
		return angle
	
	def move_robot(self):

		#Indicamos la velocidad  de movimiento y la distancia a recorrer
		self.max_linear_speed=0.05

		self.distance_to_move=1.0

		#Definimos un mensaje de velocidad para publicar en el tópico de velocidad

		self.twist=Twist()

		#Escribimos en el mensaje la velocidad a la que deben girar los motores

		self.twist.linear.x=self.max_linear_speed

		#Tiempo necesario para mover el robot la distancia deseada:
  
		self.time_t_move=self.distance_to_move/self.max_linear_speed

		self.tiempo_trascurrido=0

		self.tiempo=0

		self.contador=0

		self.final=0

		self.get_logger().info("Iniciamos el movimiento:")

		while self.final==0:

			#reloj=rclpy.clock.Clock()

			

			

			if self.contador==0:

				#self.t_inicial=rclpy.clock.Clock.self.now()
	
				self.t_inicial=self.get_clock().now()

				self.tiempo=self.t_inicial

				self.contador+=1

			else:

				self.tiempo=self.get_clock().now()

				#self.tiempo_trascurrido=self.tiempo-self.t_inicial
	
			self.tiempo_trascurrido=self.tiempo-self.t_inicial

			#self.get_logger().info("Tiempo transcurrido: %f segundos", self.tiempo_trascurrido)
			#print("Tiempo transcurrido: " +str(self.tiempo_trascurrido)+ " segundos.")
			#self.get_logger().info("%s",str(self.tiempo_trascurrido))
   
			self.tiempo_trascurrido_sec=float(self.tiempo_trascurrido.to_msg().sec)

			self.tiempo_trascurrido_nanosec=float(self.tiempo_trascurrido.to_msg().nanosec)/1000000000.0

			self.tiempo_trascurrido=self.tiempo_trascurrido_sec+self.tiempo_trascurrido_nanosec

			print("Tiempo trascurrido: " + str(self.tiempo_trascurrido)+ " segundos.")

			if self.tiempo_trascurrido>=self.time_t_move:

				self.twist.linear.x=0.0

				self.publisher.publish(self.twist)

				self.get_logger().info("Ha trascurrido el tiempo definido por el usuario. Detenemos el movimiento.")

				self.final=1

				



			self.publisher.publish(self.twist)






		
        
def main(args=None):
	rclpy.init(args=args)
	
	avanza_con_tiempo=Ejercicio_01()
	#rclpy.spin(avanza_con_tiempo)
	avanza_con_tiempo.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
 	main()
