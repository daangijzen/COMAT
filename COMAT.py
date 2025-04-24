import bpy
import os
import pathlib

class COMATProperties(bpy.types.PropertyGroup):
    """Properties for the UI panel"""
    filepath: bpy.props.StringProperty(name="Animation File", subtype='FILE_PATH')

class COMAT_PT_MainPanel(bpy.types.Panel):
    """Main UI Panel for Copilot's Mixamo Animation Transfer"""
    bl_label = "COMAT - Mixamo Animation Transfer"
    bl_idname = "COMAT_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "COMAT"
    
    def draw(self, context):
        layout = self.layout
        comat_props = context.scene.comat_props
        
        layout.label(text="Select Mixamo Animation:")
        row = layout.row()
        row.prop(comat_props, "filepath", text="")
        row.operator("comat.browse_file", text="Browse")
        layout.separator()
        
        layout.operator("comat.load_mixamo_animation", text="Transfer Animation to Selected", icon='ANIM')
        
class COMAT_OT_BrowseFile(bpy.types.Operator):
    """Operator to browse for a Mixamo FBX file"""
    bl_idname = "comat.browse_file"
    bl_label = "Browse Mixamo Animation"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        context.scene.comat_props.filepath = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class COMAT_OT_LoadAnimation(bpy.types.Operator):
    """Operator to load and transfer a Mixamo animation from an imported rig
    to the originally selected rig as a new animation (via an NLA track).
    The original rig's T-Pose remains unchanged."""
    bl_idname = "comat.load_mixamo_animation"
    bl_label = "Transfer Animation"
    bl_options = {'REGISTER', 'UNDO'}  # <-- This enables undo functionality

    def execute(self, context):
        comat_props = context.scene.comat_props
        filepath = comat_props.filepath

        if not filepath or not os.path.exists(filepath):
            self.report({'WARNING'}, "Invalid file path!")
            return {'CANCELLED'}

        # The original rig should already be selected by the user.
        original_rig = bpy.context.object
        if not original_rig or original_rig.type != 'ARMATURE':
            self.report({'WARNING'}, "Please select the original rig (an ARMATURE) before running the script!")
            return {'CANCELLED'}

        # Import the new Mixamo animation from the FBX file.
        bpy.ops.import_scene.fbx(filepath=filepath)

        # From the imported objects, pick the new armature (which should not be the original rig).
        imported_objects = bpy.context.selected_objects
        mixamo_animation_rig = None
        for obj in imported_objects:
            if obj.type == 'ARMATURE' and obj != original_rig:
                mixamo_animation_rig = obj
                break

        if not mixamo_animation_rig:
            self.report({'WARNING'}, "No new Mixamo animation rig found!")
            return {'CANCELLED'}

        # Verify the imported rig has animation data.
        if not (mixamo_animation_rig.animation_data and mixamo_animation_rig.animation_data.action):
            self.report({'WARNING'}, "Imported Mixamo rig has no animation data.")
            bpy.data.objects.remove(mixamo_animation_rig, do_unlink=True)
            return {'CANCELLED'}

        # Extract the base file name from the FBX file (without extension)
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        # Setup the initial new action name
        unique_name = f"Mixamo_{base_name}"
        count = 1
        # Check for duplicate names in existing actions, and append _01, _02, etc. if needed.
        while unique_name in bpy.data.actions:
            unique_name = f"Mixamo_{base_name}_{count:02d}"
            count += 1

        # Copy the new animation from the imported rig and assign the unique name.
        new_action = mixamo_animation_rig.animation_data.action.copy()
        new_action.name = unique_name

        # Ensure the original rig has animation data.
        if original_rig.animation_data is None:
            original_rig.animation_data_create()

        # Add the new animation as a new NLA track (and strip) on the original rig.
        nla_tracks = original_rig.animation_data.nla_tracks
        new_track = nla_tracks.new()
        new_track.name = new_action.name

        # Convert the new action's starting frame to int
        start_frame = int(new_action.frame_range[0])
        new_track.strips.new(new_action.name, start_frame, new_action)

        self.report({'INFO'}, f"New animation '{new_action.name}' added as an NLA track to {original_rig.name}")

        # Clean up: Delete the imported Mixamo animation rig.
        bpy.data.objects.remove(mixamo_animation_rig, do_unlink=True)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(COMATProperties)
    bpy.utils.register_class(COMAT_PT_MainPanel)
    bpy.utils.register_class(COMAT_OT_BrowseFile)
    bpy.utils.register_class(COMAT_OT_LoadAnimation)
    bpy.types.Scene.comat_props = bpy.props.PointerProperty(type=COMATProperties)

def unregister():
    bpy.utils.unregister_class(COMATProperties)
    bpy.utils.unregister_class(COMAT_PT_MainPanel)
    bpy.utils.unregister_class(COMAT_OT_BrowseFile)
    bpy.utils.unregister_class(COMAT_OT_LoadAnimation)
    del bpy.types.Scene.comat_props

if __name__ == "__main__":
    register()
