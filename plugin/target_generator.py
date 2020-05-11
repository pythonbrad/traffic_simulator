'''
    Author: pythonbrad
    Email: fomegnemeudje@outlook.com
    Github: http://github.com/pythonbrad

    This script generate target in using the vertices of a object, create a map and program to manage the moving
    An exemple is given in the exemple.blend

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

bl_info = {
    "name": "Target Generator",
    "author": "Fomegne Meudje",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "Properties > Scene",
    "description": "This script generate target in using the vertices of a object and create a map file to manage a path following",
    "warning": "In dev version",
    "wiki_url": "",
    "category": "Object",
    }



import bpy, bmesh
from mathutils import Vector
import time, pickle


class TargetGeneratorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Target Generetor Panel"
    bl_idname = "OBJECT_PT_target_generetor"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        tool_settings = context.tool_settings

        row = layout.row()
        row.label(text="Target generetor", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(tool_settings, "normal_size", text='Targets spacing')

        row = layout.row()
        row.operator("object.target_generator", text='Generate')

class TargetGenerator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.target_generator"
    bl_label = "Target generator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.carrefour_data = {}
        self.coords = {}
        begin_time = time.time()
        # We get data
        print('Getting data...')
        self.get_data(context)
        # We save data
        with open('data.bin', 'wb') as f:
        	pickle.dump(self.carrefour_data ,f)
        	f.close()
        # We build target
        print('Building target...')
        self.build_target(context)
        print('Finish in', time.time()-begin_time)
        return {'FINISHED'}

    def get_data(self, context):
        obj = context.active_object
        tool_settings = context.tool_settings
        # I not in edit mode we toggle
        if obj.mode != 'EDIT':
            bpy.ops.object.editmode_toggle()

        bm = bmesh.from_edit_mesh(obj.data)
        edges = bm.edges
        units = tool_settings.normal_size

        for edge in edges:
            for vert in edge.verts:
                # We save coords to create carrefour target
                co = obj.matrix_world * vert.co
                self.coords[str(vert.index)+'c'] = co + Vector((-units,units,0.0))
                self.coords[str(vert.index)+'a'] = co + Vector((-units,-units,0.0))
                self.coords[str(vert.index)+'b'] = co + Vector((units,-units,0.0))
                self.coords[str(vert.index)+'d'] = co + Vector((units,units,0.0))
                # We create carrefour_data of base
                self.carrefour_data[str(vert.index)+'c'] = [str(vert.index)+'a']
                self.carrefour_data[str(vert.index)+'b'] = [str(vert.index)+'d']
                self.carrefour_data[str(vert.index)+'d'] = [str(vert.index)+'c']
                self.carrefour_data[str(vert.index)+'a'] = [str(vert.index)+'b']
                # We get carrefour
                for e in vert.link_edges:
                    for v in e.verts:
                        if v != vert:
                            # We verify the orientation and create the others carrefours
                            if abs(v.co.x - vert.co.x) > abs(v.co.y - vert.co.y):
                                if v.co.x < vert.co.x:
                                    print(v.index, 'is left', vert.index)
                                    self.carrefour_data[str(vert.index)+'c'].append(str(v.index)+'d')
                                else:
                                    self.carrefour_data[str(vert.index)+'b'].append(str(v.index)+'a')
                                    print(v.index, 'is right', vert.index)
                            else:
                                if v.co.y < vert.co.y:
                                    print(v.index, 'is up', vert.index)
                                    self.carrefour_data[str(vert.index)+'a'].append(str(v.index)+'c')
                                else:
                                    print(v.index, 'is down', vert.index)
                                    self.carrefour_data[str(vert.index)+'d'].append(str(v.index)+'b')
    
    def build_target(self, context):
        scn = context.scene
        # We leave edit mode
        bpy.ops.object.editmode_toggle()
        # We create the obj source
        bpy.ops.mesh.primitive_cube_add(radius=.1)
        obj_src = bpy.context.selected_objects[0]
        bpy.ops.object.game_property_new(type='STRING', name='target')
        prop = obj_src.game.properties['target']
        obj_src.name = 'to_delete'
        #obj_src.show_name = 1
        obj_src.game.use_ghost = 1
        obj_src.game.use_actor = 1
        obj_src.hide_render = 1
        # We duplicate the obj_src
        for index in self.coords:
            new_obj = obj_src.copy()
            new_obj.name = index
            new_obj.location = self.coords[index]
            scn.objects.link(new_obj)

def register():
    bpy.utils.register_class(TargetGeneratorPanel)
    bpy.utils.register_class(TargetGenerator)


def unregister():
    bpy.utils.unregister_class(TargetGeneratorPanel)
    bpy.utils.unregister_class(TargetGenerator)


if __name__ == "__main__":
    register()
