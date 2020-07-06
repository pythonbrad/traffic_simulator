from bge import logic
import random

def main(con):
	# Recuperer la scene
	scene = logic.getCurrentScene()
	# We get all target near of the camera
	origin_list = [obj for obj in scene.objects if 'target' in obj and int(obj.getDistanceTo('Camera')) in range(100, 200)]
	# We verify if not empty
	if origin_list:
		# Recuperer un origin
		origin = random.choice(origin_list)
		# Recuperer la voiture sur son calque invisible
		car = scene.objectsInactive[random.choice(["ia","ia2","ia3","ia4","ia5"])]
		car.actuators['Steering'].target = origin
		# Creer une instance
		instance = scene.addObject(car, origin, 0)
	else:
		pass