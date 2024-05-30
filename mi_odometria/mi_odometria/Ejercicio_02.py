
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
import math



class Ejercicio_02(Node):
	def __init__(self):
		super().__init__('avanza_con_odometria')
		#Subscriber
		self.subscription = self.create_subscription(Odometry,'/odom',self.get_position,10)
        #Publisher
		self.publisher = self.create_publisher(Twist,'/cmd_vel',10)

		self.Posicion_x=0

		self.Posicion_y=0

		self.max_linear_speed=0.2

		self.distance_to_move=1.0

		self.twist=Twist()

		self.twist.linear.x=self.max_linear_speed

  
		self.distancia_recorrida=0

		self.contador=0

		self.final=0

		#self.timer_period = 0.5
 		
		#self.timer = self.create_timer(self.timer_period, self.move_robot())
		

		self.move_robot()
		
        
	
	def get_position(self, msg):
	# Obtenemos el cuaternio
		quaternion = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
 	# Convierte angulos de euler(roll, pitch, yaw)
		roll, pitch, self.yaw = tft.euler_from_quaternion(quaternion)
 		# Muestra los angulos de euler
	    #self.get_logger().info(f'Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}')
		self.Position=msg.pose.pose.position
	
		self.Posicion_x=self.Position.x
		self.Posicion_y=self.Position.y

		

		

		#print(str(self.Posicion_x))
	
		#self.get_logger().info(f'Posición x: {self.Posicion_x:.2f}, Posición y: {self.Posicion_y:.2f}, Yaw: {self.yaw:.2f}')
  
		

	def wrap_angle(self,angle):
	

		while angle>pi:
			angle-=2*pi
		while angle<-pi:
			angle+=2*pi
		
		return angle
	
	def move_robot(self):

		#Indicamos la velocidad  de movimiento y la distancia a recorrer
		

		#Definimos un mensaje de velocidad para publicar en el tópico de velocidad

		

		#Escribimos en el mensaje la velocidad a la que deben girar los motores

		

		

		self.publisher.publish(self.twist)


		#while self.final==0:

		while self.final==0:

			self.get_logger().info(str(self.Posicion_x))

			if self.Posicion_x!=0 and self.Posicion_y!=0:

				self.get_logger().info("2")

				if self.contador==0:

					self.get_logger().info("Iniciamos el movimiento:")

						
					
					self.Posicion_x_1=self.Posicion_x
					self.Posicion_y_1=self.Posicion_y
						
						#self.distancia_recorrida=0
						#self.t_inicial=rclpy.clock.Clock.self.now()
			
						#self.t_inicial=self.get_clock().now()

						#self.tiempo=self.t_inicial

					self.contador+=1

				else:

					self.Posicion_x_2=self.Posicion_x

					self.Posicion_y_2=self.Posicion_y

					self.distancia_recorrida_x=abs(abs(self.Posicion_x_2)-abs(self.Posicion_x_1))

					self.distancia_recorrida_y=abs(abs(self.Posicion_y_2)-abs(self.Posicion_y_1))

					self.distancia_recorrida=self.distancia_recorrida+math.sqrt(math.pow(self.distancia_recorrida_x,2)+math.pow(self.distancia_recorrida_y,2))

					self.get_logger().info("Distancia recorrida: " + str(self.distancia_recorrida) + " metros.")





						#self.tiempo=self.get_clock().now()

						#self.tiempo_trascurrido=self.tiempo-self.t_inicial
			
					#self.tiempo_trascurrido=self.tiempo-self.t_inicial

					
				if self.distancia_recorrida>=self.distance_to_move:

					self.twist.linear.x=0.0

					self.publisher.publish(self.twist)

					self.get_logger().info("El robot ha recorrido " +str(self.distance_to_move) + " metros. Se detiene el movimiento.")
					self.final=1


			



			self.publisher.publish(self.twist)






		
        
def main(args=None):
	rclpy.init(args=args)
	
	avanza_con_odometria=Ejercicio_02()
	rclpy.spin(avanza_con_odometria)
	avanza_con_odometria.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
 	main()
