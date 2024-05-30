from example_interfaces.srv import AddTwoInts
from librerias_propias.action import Ejercicio5
import math
from rclpy.node import Node
import rclpy
from rclpy.action import ActionClient

class Ejercicio5_Cliente(Node):


	
	def __init__(self):
		super().__init__('my_action_client')

		#Generamos un cliente de acción del tipo "Ejercicio5"

		self._action_client=ActionClient(self,Ejercicio5,'Ejercicio5')

		#Definimos un mensaje "Goal" de Ejercicio5 que usaremos más adelante

		self.Objetivo=Ejercicio5.Goal()
		
	
	

	def datos(self):

		#Esta función recibe los parámetros de movimiento del robot por parte del usuario y los almacena en el 
		#en el goal que se le mandará al servidor:

		#Selección del tipo de movimiento:

		self.Objetivo.movimiento = int(input("Introduzca el tipo de movimiento a ejecutar por el robot (1 para lineal, 2 para rotación): ")) 

		#Movimiento lineal  
	
		if self.Objetivo.movimiento==1:

			#Introducimos la distancia a recorrer por el robot (el valor del giro es 0.0)
		
			self.Objetivo.distancia= float(input("Introduzca la distancia a recorrer por el robot: "))  

			self.Objetivo.giro=0.0

		#Rotación

		elif self.Objetivo.movimiento==2:

			#Introducimos la orientación (ángulo en grados) que queremos para el robot (la distancia
			#a recorrer es 0.0)
		
			self.Objetivo.distancia= 0.0

			self.Objetivo.giro=float(input("Introduzca el ángulo que debe girar el robot: ")) 

			#Corregimos el giro para que este se encuentre en el rango [0,360] grados:

			if self.Objetivo.giro>360:

				self.Objetivo.giro=self.Objetivo.giro-360

		

	def send_goal(self,goal):

		#Este método recibe el goal generado por datos() y lo envía al servidor:

		#Esperamos a que el servidor esté en linea:

		self._action_client.wait_for_server()

		#Mandamos la petición al servidor (el feedback recibido será gestionado por
		#el método feedback_callback())

		self._send_goal_future = self._action_client.send_goal_async(
			goal, feedback_callback=self.feedback_callback)
		
		#Espera una respuesta del servidor y llama al método goal_response_callback():

		self._send_goal_future.add_done_callback(self.goal_response_callback)  

	def goal_response_callback(self, future):

		#Este método comprueba si la petición ha sido aceptada por el servidor

		
		goal_handle = future.result()
		if not goal_handle.accepted:
			self.get_logger().info('Goal rejected :(')
			return

		self.get_logger().info('Goal accepted :)')

		#Si la meta ha sido aceptada, le pedimos al servidor que la lleve a cabo

		self._get_result_future = goal_handle.get_result_async()  

		#Una vez recibido el resultado del servidor, se llama al método "get_result_callback()"

		self._get_result_future.add_done_callback(self.get_result_callback)

	def get_result_callback(self, future):
		
		#Muestra el resultado de la llamada al servidor por pantalla:

		result = future.result().result

		
		self.get_logger().info('Result: {0}'.format(result.resultado))
		rclpy.shutdown()
	

		
	
	def feedback_callback(self, feedback_msg):

		#Este método gestiona el feedback recibido por el servidor (el desplazamiento del robot y el error en la orientación):

		desplazamiento = feedback_msg.feedback.desplazamiento
		error=feedback_msg.feedback.angulo

		#Si se ha seleccionado un tipo de movimiento lineal, se muestra la distancia desplazada por el robot

		if self.Objetivo.movimiento==1:


			self.get_logger().info('Desplazamiento:' + str(desplazamiento))

		#Si se ha seleccionado una rotación, se muestra el error entre la orientación del robot y la orientación objetivo

		elif self.Objetivo.movimiento==2:

			self.get_logger().info('Error en el ángulo:' + str(error)+ 'radianes.')


def main(args=None):

	#Creamos el nodo del cliente del action

	rclpy.init(args=args)

	action_client = Ejercicio5_Cliente()

	#Solicitamos los datos de la petición al usuario:

	action_client.datos()

	#Enviamos la petición:

	action_client.send_goal(action_client.Objetivo)

	rclpy.spin(action_client)
	
	


	
	#rclpy.shutdown()


if __name__ == '__main__':
	main()