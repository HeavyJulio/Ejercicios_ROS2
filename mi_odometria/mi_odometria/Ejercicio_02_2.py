import rclpy
import rclpy.clock
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import rclpy.time
import tf_transformations as tft
from math import pi
import math



class Ejercicio_02_2(Node):
	def __init__(self):
		super().__init__('avanza_con_odometria')

		#Creamos un subscriber que leerá la posición del robot del tópico de odometría

		self.subscription = self.create_subscription(Odometry,'/odom',self.get_position,10)
        
		#Creamos el publisher que publicará en el tópico de velocidad del robot	

		self.publisher = self.create_publisher(Twist,'/cmd_vel',10)

		#Inicializamos algunas de las variables de la clase

		self.Posicion_x=0.0

		self.Posicion_y=0.0

		self.max_linear_speed=0.2

		self.distance_to_move=1.0

		self.twist=Twist()

		self.twist.linear.x=self.max_linear_speed

  
		self.distancia_recorrida=0.0

		self.contador=0.0

		self.final=0

		self.timer_period = 0.5

		#Creamos el "timer" que ejecutará la función move_robot en intervalos regulares de tiempo
 		
		self.timer = self.create_timer(self.timer_period, self.move_robot)
		
		
        
	
	def get_position(self, msg):

		#Esta función extrae las variables de posición del robot de los mensajes obtenidos del tópico de odometría

		# Obtenemos el cuaternio
				
		quaternion = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
		
		# Convierte angulos de euler(roll, pitch, yaw)

		roll, pitch, self.yaw = tft.euler_from_quaternion(quaternion)
				
		self.Position=msg.pose.pose.position

		#Obtenemos la posición en x e y
			
		self.Posicion_x=self.Position.x
		self.Posicion_y=self.Position.y

	
	def move_robot(self):

		#Esta función se encarga controla el movimiento del robot en función de los parámetros especificados por el programa.

		#Esta linea evita que se ejecute la lógica del movimiento hasta que no se halla leido el primer mensaje de odometria


		if self.Posicion_x!=0 and self.Posicion_y!=0:

			#El contador nos permite tomar la posición inicial del robot


			if self.contador==0:

				self.get_logger().info("Iniciamos el movimiento:")

					
				
				self.Posicion_x_1=self.Posicion_x
				self.Posicion_y_1=self.Posicion_y
					
					

				#Actualizamos el contador	

				self.contador+=1

			else:

				#Tomamos una nueva muestra de la posición del robot


				self.Posicion_x_2=self.Posicion_x

				self.Posicion_y_2=self.Posicion_y

				#Calculamos la diferencia en la posición entre el instante anterior y el actual


				self.distancia_recorrida_x=abs(abs(self.Posicion_x_2)-abs(self.Posicion_x_1))

				self.distancia_recorrida_y=abs(abs(self.Posicion_y_2)-abs(self.Posicion_y_1))

				#Calculamos la distancia recorrida como la hipotenusa de la distancia recorrida en x e y. Actualizamos el valor de la distancia total recorrida
					

				self.distancia_recorrida=self.distancia_recorrida+math.sqrt(math.pow(self.distancia_recorrida_x,2)+math.pow(self.distancia_recorrida_y,2))

				self.get_logger().info("Distancia recorrida: " + str(self.distancia_recorrida) + " metros.")

				#Actualizamos el valor de la posición en el instante anterior para la siguiente iteración


				self.Posicion_x_1=self.Posicion_x_2

				self.Posicion_y_1=self.Posicion_y_2


			#Si la distancia recorrida por el robot supera la distancia especificada, detenemos el movimiento.			
				
				
				
			if self.distancia_recorrida>=self.distance_to_move:

				self.twist.linear.x=0.0

				self.publisher.publish(self.twist)

				self.get_logger().info("El robot ha recorrido " +str(self.distance_to_move) + " metros. Se detiene el movimiento.")
				
				#Detenemos el timer para que la función move_robot deje de ejecutarse.

				self.timer.cancel()

				

			



		self.publisher.publish(self.twist)






		
        
def main(args=None):
	# initialize the ROS communication
	rclpy.init(args=args)
	# declare the node constructor
	avanza_con_odometria=Ejercicio_02_2()
	rclpy.spin(avanza_con_odometria)
	avanza_con_odometria.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
 	main()
