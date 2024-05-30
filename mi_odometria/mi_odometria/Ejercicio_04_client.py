from example_interfaces.srv import AddTwoInts
from librerias_propias.srv import Ejercicio4
import math

import rclpy


def main(args=None):
	#Creamos el nodo del cliente:
	rclpy.init(args=args)
	node = rclpy.create_node('minimal_client')
	#Creamos un cliente del mismo tipo que nuestro servidor
	cli = node.create_client(Ejercicio4, 'moving')
	req = Ejercicio4.Request()
	#Solicitamos al usuario el tipo de movimiento a realizar por el robot (1 para movimiento lineal, 2 para rotación):
	req.movimiento = int(input("Introduzca el tipo de movimiento a ejecutar por el robot (1 para lineal, 2 para rotación): "))   
	if req.movimiento==1:
		#Solicitamos al usuario la distancia a recorrer por el robot:
		req.distancia= float(input("Introduzca la distancia a recorrer por el robot: "))  
		#No hay giro
		req.giro=0.0

	elif req.movimiento==2:
		#No hay traslación
		req.distancia= 0.0
		#Solicitamos al usuario la orientación deseada para el robot (en grados):
		req.giro=float(input("Introduzca la orientación deseada para el robot: ")) 
		#Ajustamos el valor de orientación introducido por si este supera los 360º
		if req.giro>360:

				req.giro=req.giro-360

	#Esperamos a que el servidor esté en línea:
	while not cli.wait_for_service(timeout_sec=1.0):
		node.get_logger().info('service not available, waiting again...')
	#Hacemos una petición al servidor
	future = cli.call_async(req)
	#Esperamos la respuesta del servidor
	rclpy.spin_until_future_complete(node, future)


	#Almacenamos la respuesta del servidor en la variable result (en este caso no la estamos utilizando)
	result = future.result()
	#Avismos al usuario del final del movimiento
	node.get_logger().info('Movimiento finalizado.')

	

	#Destruimos el nodo del cliente una vez que la petición se ha completado.

	node.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':
	main()