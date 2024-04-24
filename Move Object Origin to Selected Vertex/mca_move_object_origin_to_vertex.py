# mca_move_object_origin_to_vertex.py.

# This script moves the object's origin to the selected vertex.
#
# Before running this script, make sure that you are in the 
# object editing mode and only a single vertex is selected.

# Version 0.1.

bl_info = {
    "name": "Move Object Origin to Selected Vertex",
    "description": "Move the object's origin to the selected vertex.",
    "category": "Mesh",
    "blender": (3, 1, 0),
    "author": "McArcher",
}

import bpy
import bmesh
from mathutils import Vector


class McaMOOTSV(bpy.types.Operator):
    """Move the object's origin to the selected vertex"""
    bl_idname = "object.mca_move_object_origin_to_vertex"
    bl_label = "Move the object's origin to the selected vertex"
    
    ResultCancel = 'CANCELLED'
    ResultSuccess = 'FINISHED'
    MeshEditMode = 'EDIT_MESH'

    @classmethod
    def poll(cls, context):
        return is_mesh_edit_mode_selected()

    def execute(self, context):
        return move_object_origin_to_vertex()


def register():
    bpy.utils.register_class(McaMOOTSV)


def unregister():
    bpy.utils.unregister_class(McaMOOTSV)


# Checks whether the mesh edit mode is selected.
def is_mesh_edit_mode_selected():
    return bpy.context.mode == McaMOOTSV.MeshEditMode


# Moves the object's origin to the selected vertex. 
# A single vertex must be selected in the object edit mode.",
def move_object_origin_to_vertex():
    mesh = bmesh.from_edit_mesh(bpy.context.edit_object.data)

    # Find and count the selected vertices.
    selected_verts = []
    selected_verts_count = 0
    for v in mesh.verts:
        if v.select:
            selected_verts.append(v)
            selected_verts_count += 1

    if selected_verts_count != 1:
        msg = "Multiple vertices are selected"
        raise Exception(msg)
        return {McaMOOTSV.ResultCancel}
    
    # Save the old position of 3D cursor.
    cur_old_pos = Vector(bpy.context.scene.cursor.location)
    
    # Move 3D cursor to the selected vertex.
    bpy.ops.view3d.snap_cursor_to_selected()
    
    # Set the object's new origin point to the 3D cursor.
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    # Restore the old position of 3D cursor.
    bpy.context.scene.cursor.location = cur_old_pos

    return {McaMOOTSV.ResultSuccess}
