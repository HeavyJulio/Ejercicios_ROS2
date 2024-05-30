from librerias_propias.srv import Ejercicio4
import rclpy
from rclpy.executors import MultiThreadedExecutor
import rclpy.clock
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import rclpy.time
import tf_transformations as tft
from math import pi
import math
from rclpy.callback_groups import ReentrantCallbackGroup

g_node = None

#Definimos la clase del servidor

class Service(Node):


	def __init__(self):
			
		super().__init__('service_moving')

		#Creamos un ReentrantCallbackGroup para gestionar varias llamadas al mismo tiempo
			
		self.CallbackGroup = ReentrantCallbackGroup()

		#Creamos el servidor de servicio:

		self.srv = self.create_service(Ejercicio4, 'moving', self.move_robot,callback_group=self.CallbackGroup)
		
		#Creamos el publisher que publicará en el tópico de velocidad del robot	

		self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10,callback_group=self.CallbackGroup)
		
		#Creamos un subscriber que leerá la posición del robot del tópico de odometría

		self.subscriber= self.create_subscription(Odometry, '/odom', self.get_position, 10, callback_group=self.CallbackGroup)
		
		#Inicializamos algunas de las variables de la clase

		self.Posicion_x=0
		self.Posicion_y=0
		self.distancia_recorrida=0
		self.twist=Twist()
		self.Contador=0
		self.kp=0.05
			
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


	
	
	def move_robot(self,request,response):

		#Esta función se encarga controla el movimiento del robot en función de la petición realizada por el cliente del servicio:

		#Movimiento lineal

		if request.movimiento==1:  
			
			#Reiniciamos el Contador y la distancia recorrida entre distintas peticiones al servidor        
 

			self.Contador=0

			self.distancia_recorrida=0

			#La distancia que el robot debe moverse viene contenida en la petición del cliente

			
			
			self.distance_to_move=request.distancia
				
			#Iniciamos el movimiento del robot en linea recta	
				

			self.twist.linear.x=0.1	

			self.publisher_.publish(self.twist)	

			#El movimiento continuará mientras que no se halla recorrido la distancia especificada


			while self.distancia_recorrida<=self.distance_to_move:

				
				rclpy.spin_once(self, timeout_sec=1.0) #Sigue siendo esto necesario??????????????????????????????????????????
				
				#Esta linea evita que se ejecute la lógica del movimiento hasta que no se halla leido el primer mensaje de odometria


				if self.Posicion_x!=0 and self.Posicion_y!=0:

					#El contador nos permite tomar la posición inicial del robot

					if self.Contador==0:

						self.get_logger().info("Iniciamos el movimiento:")

							
						
						self.Posicion_x_1=self.Posicion_x
						self.Posicion_y_1=self.Posicion_y
							
						#Actualizamos el contador
							
						self.Contador+=1

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

						self.publisher_.publish(self.twist)

						self.get_logger().info("El robot ha recorrido " +str(self.distance_to_move) + " metros. Se detiene el movimiento.")
						
						#Devolvemos una respuesta al cliente (0 indica que todo ha salido bien)

						response.respuesta=0

						return response
					
		#Movimiento de rotación del robot						

		elif request.movimiento==2:

			#El usuario nos indica por petición la orientación que quiere para el robot en grados. Tenemos que pasar este valor a radianes:

			target_rad=request.giro*math.pi/180

			#Guardamos la medida de la orientación del robot en la variable "angulo"
		
			angulo=self.yaw

			#Iniciamos el giro del robot

			self.twist.angular.z=0.2

			self.publisher_.publish(self.twist)

			#El error_giro es la diferencia entre la orientación deseada y la orientación actual del robot:

			error_giro=abs(target_rad-angulo)

			#El giro se llevará a cabo mientras que el error en la orientación supere el umbral definido por self.kp:


			while error_giro>self.kp:

				rclpy.spin_once(self, timeout_sec=1.0)  #Esto sigue haciendo falta?????????????????????

				#Orientación actual del robot

				angulo=self.yaw

				#El tópico de odometría trabaja con ángulos definidos entre 0,pi y -pi,0. Cuando el ángulo medido pasa a ser negativo, le sumamos 2pi para que este venga representado
				#en el rango 0,2pi:

				if angulo<0:

					angulo=angulo+2*math.pi

				#Error en la orientación

				error_giro=abs(target_rad-angulo)

				self.get_logger().info("Posición angular: " +str(angulo) + " radianes.")
						
				self.get_logger().info("Posición objetivo: " +str(target_rad) + " radianes.")

				self.get_logger().info("Error de posición: " +str(error_giro) + " radianes.")

				#Si el error disminuye por debajo del umbral, detenemos el movimiento:

				if error_giro<self.kp:

					self.twist.angular.z=0.0

					self.publisher_.publish(self.twist)

					self.get_logger().info("El robot ha alcanzado la posición solicitada. Fin del movimiento.")

					#Devolvemos una respuesta al cliente (0 indica que todo ha salido bien)

					response.respuesta=0

					return response


	
	


def main(args=None):
	# initialize the ROS communication
	rclpy.init(args=args)
	# declare the node constructor
	moving_service = Service()
	
	# El "executor" nos permite trabajar con varios hilos, lo cual permite atender a varias llamadas al mismo tiempo (servicios, publisher, subscriber, etc...)


	executor = MultiThreadedExecutor(num_threads=3)
	executor.add_node(moving_service)

	'''

	try:
		executor.spin()
	finally:
		moving_service.destroy_node()
		rclpy.shutdown()

	'''

	#Esperamos nuevas llamadas al servidor??????????????????????????????????????????????????????


	executor.spin()



	rclpy.shutdown	

	#rclpy.spin(moving_service)
	# shutdown the ROS communication
	#rclpy.shutdown()


if __name__ == '__main__':
	main()