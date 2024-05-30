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


		'''

		#Subscriber
		self.subscription = self.create_subscription(Odometry,'/odom',self.get_position,10)

		'''
        #Publisher
		self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
 		
		#self.move_robot()
		self.twist = Twist()
		
		
        
	'''
	
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
		
        
	
	
		self.twist = Twist()
		

	'''
	
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

		#El robot se moverá durante el tiempo acordado y luego se parará. Entonces, 
		#haremos que self.final sea igual a 1 para salir del bucle

		while self.final==0:

			

			
			#El contador nos permite determinar el instante inicial:
			

			if self.contador==0:

				#Guardamos el instante inicial en self.t_inicial
	
				self.t_inicial=self.get_clock().now()

				self.tiempo=self.t_inicial

				#Actualizamos el contador

				self.contador+=1

			else:

				#Tomamos una medida del tiempo del reloj:

				self.tiempo=self.get_clock().now()

			#Calculamos el tiempo transcurrido entre el instante inicial y el actual
				
			self.tiempo_trascurrido=self.tiempo-self.t_inicial

			#Estas lineas nos permiten expresar el tiempo transcurrido en el formato adecuado (segundos)
			
			self.tiempo_trascurrido_sec=float(self.tiempo_trascurrido.to_msg().sec)

			self.tiempo_trascurrido_nanosec=float(self.tiempo_trascurrido.to_msg().nanosec)/1000000000.0

			self.tiempo_trascurrido=self.tiempo_trascurrido_sec+self.tiempo_trascurrido_nanosec

			print("Tiempo trascurrido: " + str(self.tiempo_trascurrido)+ " segundos.")

			#Si el robot llevá moviéndose más tiempo que el tiempo necesario para recorrer la
			#distancia especificada, paramos el movimiento del robot:

			if self.tiempo_trascurrido>=self.time_t_move:

				self.twist.linear.x=0.0

				self.publisher.publish(self.twist)

				self.get_logger().info("Ha trascurrido el tiempo definido por el usuario. Detenemos el movimiento.")

				#Actualizamos la condición de salida del bucle

				self.final=1

				



			self.publisher.publish(self.twist)






		
        
def main(args=None):
	# initialize the ROS communication
	rclpy.init(args=args)
	# declare the node constructor
	avanza_con_tiempo=Ejercicio_01()
	#Llamamos al método move_robot()
	avanza_con_tiempo.move_robot()
	#rclpy.spin(avanza_con_tiempo)
	avanza_con_tiempo.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
 	main()
