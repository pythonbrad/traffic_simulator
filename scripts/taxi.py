'''
    Author: pythonbrad
    Email: fomegnemeudje@outlook.com
    Github: http://github.com/pythonbrad

    This script manage an simulation of taxi via the map file generated by Target Generator

 * LICENSE
 * 
 * Copyright 2020 pythonbrad <fomegnemeudje@outlook.com>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
'''
from bge import logic, types
from mathutils import Vector
import random, pickle
from .path_finder import Path as PathFinder

# We get list_carrefour
if not 'carrefour_list' in logic.globalDict:
	f = open(logic.expandPath('//')+'data.bin', 'rb')
	logic.globalDict['carrefour_data'] = pickle.load(f)
	logic.globalDict['carrefour_list'] = [i for i in logic.globalDict['carrefour_data']]
	f.close()

#
#
#     LES TARGETS DOIVENT ETRE DE TYPE GHOST
#    VEHICULE IN LOW POLY
#		If problem of speed you can increase the number of skip if you use always Sensor
#
#
#
#

class Taxi(types.KX_GameObject):
	'''
		Link
		WARNING don't enable self_tetminated, it disable the steering of the object
		Sensor:Always->Controller:And>Actuator:Steering target should be the begin of each IA
		Sensor:Always with step=1->Controller:Python->Actuator:Steering
		Sensor:Near with property=target and distance 0.5->Controller:Python
	'''
	def __init__(self, own):
		con = logic.getCurrentController()
		self.steering = con.actuators['Steering']
		self.near = con.sensors['Near']
		# We convert to got in type str
		self.current_position = str(self.steering.target)
		self.previous_position = str(self.steering.target)
		# We config the finder of path
		self.path_finder = PathFinder(logic.globalDict['carrefour_data'])
		# Will be used to prevent some error
		self.previous_previous_position = str(self.steering.target)
		self.target_list = []
	def main(self):
		if self.target_terminated():
			self.previous_previous_position = self.previous_position
			self.previous_position = self.current_position
			self.current_position = str(self.steering.target)
			if self.target_list:
				self.next_target()
			else:
				#print('target_terminated')
				self.find_target()
	def target_terminated(self):
		return self.steering.target in [obj for obj in self.near.hitObjectList]
	def next_target(self):
		# We get and delete the next target
		self.steering.target = self.target_list.pop(0)
	def find_target(self):
		# We start the finder
		begin = self.current_position
		end = random.choice(logic.globalDict['carrefour_list'])
		# We verify if found
		if self.path_finder.find(begin, end):
			# We set the path
			self.target_list = self.path_finder.path
		else:
			self.target_list = []
			print('[ERROR] Path begin by %s and end by %s not found'%(begin, end))
		#print('find', self.target_list)

def main(con):
	own = con.owner
	if not 'init' in own:
		own['init'] = True
		Taxi(own)
	else:
		own.main()