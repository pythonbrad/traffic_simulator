from bge import logic
import random


def main(con):
	camera = con.actuators['Camera']
	scene = logic.getCurrentScene()

	while 1:
	    obj = random.choice(scene.objects)
	    if 'ia' in str(obj):
	        camera.object = obj
	        break