from bge import logic
import random


def main(con):
	camera = con.actuators['Camera']
	scene = logic.getCurrentScene()

	# We get only ia obj
	objs = [obj for obj in scene.objects if 'ia' in obj]
	# We verify if we have ia
	if objs:
		# We get a random ia
		obj = random.choice(objs)
		camera.object = obj