from example_interfaces.srv import AddTwoInts
from librerias_propias.srv import Ejercicio3


import rclpy


def main(args=None):
	#Creamos el nodo del cliente:
	rclpy.init(args=args)
	node = rclpy.create_node('minimal_client')
	#Creamos un cliente del mismo tipo que nuestro servidor
	cli = node.create_client(Ejercicio3, 'moving')
	#Solicitamos al usuario la distancia a recorrer por el robot
	req = Ejercicio3.Request()
	req.distancia = float(input("Introduzca la distancia que se moverá el robot: "))   #Distancia
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