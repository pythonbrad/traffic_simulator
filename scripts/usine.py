from bge import logic
import random

def main(con):
	# Recuperer l usine
	usine = con.owner
	# We verify if already init
	if not 'init' in usine:
		usine['init'] = True
		# We init the number of ia generated
		usine['nb_ia'] = 1
	elif usine['nb_ia'] < 50:
		# We increment the number of ia
		usine['nb_ia'] += 1
	else:
		# We disable the repeat
		sensor = usine.sensors['Delay']
		sensor.repeat = False
	# Recuperer la scene
	scene = logic.getCurrentScene()
	# Recuperer la voiture sur son calque invisible
	car = scene.objectsInactive[random.choice(["ia","ia2","ia3","ia4","ia5"])]
	car.actuators['Steering'].target = usine['begin']
	# Creer une instance
	instance = scene.addObject(car, usine, 0)