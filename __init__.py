# -*- coding: utf8 -*-
# python
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {"name": "Sculpt/Paint Ref",
           "author": "CDMJ, Spirou4D",
           "version": (1, 00, 0),
           "blender": (2, 78, 0),
           "location": "Toolbar > Misc Tab > Sculpt/Paint Ref Panel",
           "description": "Sculpt And Paint Reference",
           "warning": "WIP",
           "category": "Paint"}


import bpy
from bpy.types import   AddonPreferences,\
                        Menu,\
                        Panel,\
                        UIList,\
                        Operator
from bpy.props import *
import math
import os


##################### Operators First

#--------------------------------------------------Create reference scene
class RefMakerScene(Operator):
    """Create Reference Scene"""
    bl_description = ""
    bl_idname = "object.create_reference_scene"
    bl_label = "Create Scene for Image Reference"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        for sc in bpy.data.scenes:
            if sc.name == "Refmaker":
                return False
        return context.area.type=='VIEW_3D'

    def execute(self, context):
        _name="Refmaker"
        for sc in bpy.data.scenes:
            if sc.name == "Refmaker":
                return {'FINISHED'}
        bpy.ops.scene.new(type='NEW') #add new scene & name it 'Brush'
        context.scene.name = _name

        #add camera to center and move up 4 units in Z
        bpy.ops.object.camera_add(
                    view_align=False,
                    enter_editmode=False,
                    location=(0, 0, 4),
                    rotation=(0, 0, 0)
                    )

        context.object.name="Refmaker Camera"      #rename selected camera

        #change scene size to HD
        _RenderScene = context.scene.render
        _RenderScene.resolution_x=1920
        _RenderScene.resolution_y=1080
        _RenderScene.resolution_percentage = 100

        #save scene size as preset
        bpy.ops.render.preset_add(name = "Refmaker")

        #change to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                break # this will break the loop after the first ran
        return {'FINISHED'}
    
class SculptView(bpy.types.Operator):
    """Sculpt View Reference Camera"""
    bl_idname = "object.sculpt_camera" 
                                     
     
    bl_label = "Sculpt Camera"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.camera_add(
                    view_align=False,
                    enter_editmode=False,
                    location=(0, -4, 0),
                    rotation=(1.5708, 0, 0)
                    )

        context.object.name="Reference Cam" #add camera to front view
        
        bpy.context.object.data.show_passepartout = False
        bpy.context.object.data.lens = 80


        #change to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                break # this will break the loop after the first ran
            
#            
        #bpy.ops.view3d.background_image_add()#ADD IMAGE TO BACKGROUND
        
        #bpy.context.space_data.show_background_images = True 
        
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        
        
    
        
        return {'FINISHED'}

class ToggleLock(bpy.types.Operator):
    """Lock Screen"""
    bl_idname = "object.lock_screen" 
                                     
     
    bl_label = "Lock Screen Toggle"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):
    
        A = context.space_data.lock_camera
        B = context.space_data.show_only_render
        if A and B == True:
            context.space_data.lock_camera = False
            context.space_data.show_only_render = False
        else:
            context.space_data.lock_camera = True
            context.space_data.show_only_render = True
        return {'FINISHED'}

class CustomFps(bpy.types.Operator):
    """Slow Play FPS"""
    bl_idname = "object.slow_play"
    
    bl_label = "Slow Play FPS"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):
        #bpy.context.scene.render.fps = 1
        #bpy.context.scene.render.fps_base = 12
        F = context.scene.render.fps
        if F == 1:
            context.scene.render.fps = 30
            context.scene.render.fps_base = 1
        else:
             bpy.context.scene.render.fps = 1
             bpy.context.scene.render.fps_base = 12 
               
        return {'FINISHED'}

class ImagesPlanes(bpy.types.Operator):
    """Generic Operator"""
    bl_idname = "object.images_planes" 
                                     
     
    bl_label = "operator for import images"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.import_image.to_plane() #import images
        
        return {'FINISHED'}



##################panel itself lol

class TestPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Reference Workflow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        ########reference maker scene#########
        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Ref Tool")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=True)
        row2.operator("object.create_reference_scene", text = "Refmaker Scene", icon = 'OUTLINER_OB_LAMP')
        row3 = row.split(align=True)
        row3.operator("object.images_planes", text="", icon='NODE_SEL')
        
        
        ########sculpt camera and lock toggle#####
        box = layout.box()                        
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Sculpt View")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=True)
        row2.operator("object.sculpt_camera", text = "Sculpt Ref View", icon = 'RENDER_REGION')
        row2.scale_x = 1.00
        row3 = row.split(align=True)
        if context.space_data.lock_camera == True:
            row3.operator("object.lock_screen", text="", icon='LOCKED')
        if context.space_data.lock_camera == False:
            row3.operator("object.lock_screen", text="", icon='UNLOCKED')
        row4 = row.split(align=True)
        if context.scene.render.fps > 1:
            row4.operator("object.slow_play", text="", icon='CLIP')
        if context.scene.render.fps == 1:
            row4.operator("object.slow_play", text="", icon='CAMERA_DATA')
        


def register():
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(TestPanel)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    #bpy.utils.unregister_class(TestPanel)
    
if __name__ == "__main__":
    register()
