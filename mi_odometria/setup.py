from setuptools import find_packages, setup

package_name = 'mi_odometria'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='julio',
    maintainer_email='julio@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'leer_orientacion = mi_odometria.leer_orientacion:main',
        'control_orientacion = mi_odometria.control_orientacion:main',
        'Ejercicio_01 = mi_odometria.Ejercicio_01:main',
        'Ejercicio_01_2 = mi_odometria.Ejercicio_01_2:main',
        'Ejercicio_02 = mi_odometria.Ejercicio_02:main',
        'Ejercicio_02_2 = mi_odometria.Ejercicio_02_2:main',
        'Ejercicio_03_server = mi_odometria.Ejercicio_03_server:main',
        'Ejercicio_03_client = mi_odometria.Ejercicio_03_client:main',
        'Ejercicio_04_server = mi_odometria.Ejercicio_04_server:main',
        'Ejercicio_04_client = mi_odometria.Ejercicio_04_client:main',
        'Ejercicio_05_server = mi_odometria.Ejercicio_05_server:main',
        'Ejercicio_05_client = mi_odometria.Ejercicio_05_client:main'
        ],
    },
)
