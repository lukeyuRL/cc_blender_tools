# Copyright (C) 2021 Victor Soupday
# This file is part of CC/iC Blender Tools <https://github.com/soupday/cc_blender_tools>
#
# CC/iC Blender Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CC/iC Blender Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CC/iC Blender Tools.  If not, see <https://www.gnu.org/licenses/>.

import bpy
import mathutils
from math import pi, atan

from . import utils, vars
from rna_prop_ui import rna_idprop_ui_create


def cmp_rl_bone_names(name, bone_name):
    if bone_name.startswith("RL_"):
        bone_name = bone_name[3:]
    elif bone_name.startswith("CC_Base_"):
        bone_name = bone_name[8:]
    if name.startswith("RL_"):
        name = name[3:]
    elif name.startswith("CC_Base_"):
        name = name[8:]
    return name == bone_name


def get_rl_edit_bone(rig, name):
    if name:
        if name in rig.data.edit_bones:
            return rig.data.edit_bones[name]
        # remove "CC_Base_" from start of bone name and try again...
        if name.startswith("CC_Base_"):
            name = name[8:]
            if name in rig.data.edit_bones:
                return rig.data.edit_bones[name]
        if name.startswith("RL_"):
            name = name[3:]
            if name in rig.data.edit_bones:
                return rig.data.edit_bones[name]
    return None


def get_rl_bone(rig, name):
    if name:
        if name in rig.data.bones:
            return rig.data.bones[name]
        # remove "CC_Base_" from start of bone name and try again...
        if name.startswith("CC_Base_"):
            name = name[8:]
            if name in rig.data.bones:
                return rig.data.bones[name]
        if name.startswith("RL_"):
            name = name[3:]
            if name in rig.data.bones:
                return rig.data.bones[name]
    return None


def get_rl_pose_bone(rig, name):
    if name:
        if name in rig.pose.bones:
            return rig.pose.bones[name]
        # remove "CC_Base_" from start of bone name and try again...
        if name.startswith("CC_Base_"):
            name = name[8:]
            if name in rig.pose.bones:
                return rig.pose.bones[name]
        if name.startswith("RL_"):
            name = name[3:]
            if name in rig.pose.bones:
                return rig.pose.bones[name]
    return None


def get_edit_bone(rig, name):
    if name:
        if type(name) is list:
            for n in name:
                if n in rig.data.edit_bones:
                    return rig.data.edit_bones[n]
        else:
            if name in rig.data.edit_bones:
                return rig.data.edit_bones[name]
    return None


def get_bone(rig, name):
    if name:
        if type(name) is list:
            for n in name:
                if n in rig.data.bones:
                    return rig.data.bones[n]
        else:
            if name in rig.data.bones:
                return rig.data.bones[name]
    return None


def get_pose_bone(rig, name):
    if name:
        if type(name) is list:
            for n in name:
                if n in rig.pose.bones:
                    return rig.pose.bones[n]
        else:
            if name in rig.pose.bones:
                return rig.pose.bones[name]
    return None


def rename_bone(rig, from_name, to_name):
    if utils.edit_mode_to(rig):
        bone = get_edit_bone(rig, from_name)
        if bone and to_name not in rig.data.edit_bones:
            bone.name = to_name
        else:
            utils.log_error(f"Bone {from_name} cannot be renamed as {to_name} already exists in rig!")



def copy_edit_bone(rig, src_name, dst_name, parent_name, scale):
    if utils.edit_mode_to(rig):
        src_bone = get_edit_bone(rig, src_name)
        if src_bone and dst_name not in rig.data.edit_bones:
            dst_bone = rig.data.edit_bones.new(dst_name)
            dst_bone.head = src_bone.head
            dst_bone.tail = src_bone.head + (src_bone.tail - src_bone.head) * scale
            dst_bone.roll = src_bone.roll
            if parent_name != "":
                if parent_name in rig.data.edit_bones:
                    dst_bone.parent = rig.data.edit_bones[parent_name]
                else:
                    utils.log_error(f"Unable to find parent bone {parent_name} in rig!")
            return dst_bone
        else:
            if src_name not in rig.data.edit_bones:
                utils.log_error(f"Unable to find source bone {src_name} in rig!")
            if dst_name in rig.data.edit_bones:
                utils.log_warn(f"Destination bone {dst_name} already exists in rig!")
    else:
        utils.log_error(f"Unable to edit rig!")
    return None


def new_edit_bone(rig, bone_name, parent_name):
    if utils.edit_mode_to(rig):
        if bone_name not in rig.data.edit_bones:
            bone = rig.data.edit_bones.new(bone_name)
            bone.head = mathutils.Vector((0,0,0))
            bone.tail = bone.head + mathutils.Vector((0,0,0.05))
            bone.roll = 0
            if parent_name != "":
                if parent_name in rig.data.edit_bones:
                    bone.parent = rig.data.edit_bones[parent_name]
                else:
                    utils.log_error(f"Unable to find parent bone {parent_name} in rig!")
            return bone
        else:
            utils.log_warn(f"Destination bone {bone_name} already exists in rig!")
    else:
        utils.log_error(f"Unable to edit rig!")
    return None


def reparent_edit_bone(rig, bone_name, parent_name):
    if utils.edit_mode_to(rig):
        if bone_name in rig.data.bones:
            bone = rig.data.edit_bones[bone_name]
            if bone:
                if parent_name != "":
                    parent_bone = get_edit_bone(rig, parent_name)
                    if parent_bone:
                        bone.parent = parent_bone
                        return bone
                    else:
                        utils.log_error(f"Could not find parent bone: {parent_name} in Rig!")
        else:
            utils.log_error(f"Could not find target bone: {bone_name} in Rig!")
    else:
        utils.log_error(f"Unable to edit rig!")
    return None


def copy_rl_edit_bone(cc3_rig, dst_rig, cc3_name, dst_name, dst_parent_name, scale):
    if utils.edit_mode_to(cc3_rig):
        src_bone = get_rl_edit_bone(cc3_rig, cc3_name)
        if src_bone:
            # cc3 rig is usually scaled by 0.01, so calculate the world positions.
            head_pos = cc3_rig.matrix_world @ src_bone.head
            tail_pos = cc3_rig.matrix_world @ src_bone.tail
            roll = src_bone.roll
            if utils.edit_mode_to(dst_rig):
                # meta and rigify rigs are at 1.0 scale so all bones are in world space (at the origin)
                dst_bone = dst_rig.data.edit_bones.new(dst_name)
                dst_bone.head = head_pos
                dst_bone.tail = head_pos + (tail_pos - head_pos) * scale
                dst_bone.roll = roll
                if dst_parent_name != "":
                    parent_bone = get_edit_bone(dst_rig, dst_parent_name)
                    if parent_bone:
                        dst_bone.parent = parent_bone
                    else:
                        utils.log_error(f"Could not find parent bone: {dst_parent_name} in target Rig!")
                return dst_bone
            else:
                utils.log_error(f"Unable to edit target rig!")
        else:
            utils.log_error(f"Could not find bone: {cc3_name} in CC3 Rig!")
    else:
        utils.log_error(f"Unable to edit CC3 rig!")
    return None


def get_edit_bone_subtree_defs(rig, bone : bpy.types.EditBone, tree = None):

    if tree is None:
            tree = []

    # bone must have a parent for it to be a sub-tree
    if utils.edit_mode_to(rig) and bone.parent:

        bone_data = [bone.name,
                    rig.matrix_world @ bone.head,
                    rig.matrix_world @ bone.tail,
                    bone.head_radius,
                    bone.tail_radius,
                    bone.roll,
                    bone.parent.name]

        tree.append(bone_data)

        for child_bone in bone.children:
            get_edit_bone_subtree_defs(rig, child_bone, tree)

    return tree


def copy_rl_edit_bone_subtree(cc3_rig, dst_rig, cc3_name, dst_name, dst_parent_name, layer):

    src_bone_defs = None

    # copy the cc3 bone sub-tree to the destination rig
    if utils.edit_mode_to(cc3_rig):
        cc3_bone = get_edit_bone(cc3_rig, cc3_name)
        src_bone_defs = get_edit_bone_subtree_defs(cc3_rig, cc3_bone)

        if utils.edit_mode_to(dst_rig):

            for bone_def in src_bone_defs:
                name = bone_def[0]
                if name == cc3_name:
                    name = dst_name
                head = bone_def[1]
                tail = bone_def[2]
                head_radius = bone_def[3]
                tail_radius = bone_def[4]
                roll = bone_def[5]
                parent_name = bone_def[6]

                bone : bpy.types.EditBone = dst_rig.data.edit_bones.new(name)
                bone.head = head
                bone.tail = tail
                bone.head_radius = head_radius
                bone.tail_radius = tail_radius
                bone.roll = roll

                # store the name of the newly created bone (in case Blender has changed it)
                bone_def.append(bone.name)

                # set the edit bone layers
                for l in range(0, 32):
                    bone.layers[l] = l == layer

                # set the bone parent
                parent_bone = get_edit_bone(dst_rig, parent_name)
                if parent_bone:
                    bone.parent = parent_bone

            # set the tree parent
            dst_bone = get_edit_bone(dst_rig, dst_name)
            dst_parent_bone = get_edit_bone(dst_rig, dst_parent_name)
            if dst_bone and dst_parent_bone:
                dst_bone.parent = dst_parent_bone

            # finally set pose bone layers
            if utils.set_mode("OBJECT"):
                for bone_def in src_bone_defs:
                    name = bone_def[7]
                    pose_bone = dst_rig.data.bones[name]
                    for l in range(0, 32):
                        pose_bone.layers[l] = l == layer

    return src_bone_defs


def add_copy_transforms_constraint(from_rig, to_rig, from_bone, to_bone, influence = 1.0, space="WORLD"):
    try:
        if utils.set_mode("OBJECT"):
            to_pose_bone : bpy.types.PoseBone = to_rig.pose.bones[to_bone]
            c : bpy.types.CopyTransformsConstraint = to_pose_bone.constraints.new(type="COPY_TRANSFORMS")
            c.target = from_rig
            c.subtarget = from_bone
            c.head_tail = 0
            c.mix_mode = "REPLACE"
            c.target_space = space
            c.owner_space = space
            c.influence = influence
            return c
    except:
        utils.log_error(f"Unable to add copy transforms constraint: {to_bone} {from_bone}")
        return None


def add_copy_rotation_constraint(from_rig, to_rig, from_bone, to_bone, influence = 1.0, space="WORLD"):
    try:
        if utils.set_mode("OBJECT"):
            to_pose_bone : bpy.types.PoseBone = to_rig.pose.bones[to_bone]
            c : bpy.types.CopyRotationConstraint = to_pose_bone.constraints.new(type="COPY_ROTATION")
            c.target = from_rig
            c.subtarget = from_bone
            c.use_x = True
            c.use_y = True
            c.use_z = True
            c.invert_x = False
            c.invert_y = False
            c.invert_z = False
            c.mix_mode = "REPLACE"
            c.target_space = space
            if space == "LOCAL_OWNER_ORIENT":
                space = "LOCAL"
            c.owner_space = space
            c.influence = influence
            return c
    except:
        utils.log_error(f"Unable to add copy transforms constraint: {to_bone} {from_bone}")
        return None


def add_copy_location_constraint(from_rig, to_rig, from_bone, to_bone, influence = 1.0, space="WORLD"):
    try:
        if utils.set_mode("OBJECT"):
            to_pose_bone : bpy.types.PoseBone = to_rig.pose.bones[to_bone]
            c : bpy.types.CopyLocationConstraint = to_pose_bone.constraints.new(type="COPY_LOCATION")
            c.target = from_rig
            c.subtarget = from_bone
            c.use_x = True
            c.use_y = True
            c.use_z = True
            c.invert_x = False
            c.invert_y = False
            c.invert_z = False
            c.target_space = space
            if space == "LOCAL_OWNER_ORIENT":
                space = "LOCAL"
            c.owner_space = space
            c.influence = influence
            return c
    except:
        utils.log_error(f"Unable to add copy transforms constraint: {to_bone} {from_bone}")
        return None


def add_damped_track_constraint(rig, bone_name, target_name, influence):
    try:
        if utils.set_mode("OBJECT"):
            pose_bone : bpy.types.PoseBone = rig.pose.bones[bone_name]
            c : bpy.types.DampedTrackConstraint = pose_bone.constraints.new(type="DAMPED_TRACK")
            c.target = rig
            c.subtarget = target_name
            c.head_tail = 0
            c.track_axis = "TRACK_Y"
            c.influence = influence
            return c
    except:
        utils.log_error(f"Unable to add damped track constraint: {bone_name} {target_name}")
        return None


def add_limit_distance_constraint(from_rig, to_rig, from_bone, to_bone, distance, influence = 1.0, space="WORLD"):
    try:
        if utils.set_mode("OBJECT"):
            to_pose_bone : bpy.types.PoseBone = to_rig.pose.bones[to_bone]
            c : bpy.types.LimitDistanceConstraint = to_pose_bone.constraints.new(type="LIMIT_DISTANCE")
            c.target = from_rig
            c.subtarget = from_bone
            c.distance = distance
            c.limit_mode = "LIMITDIST_ONSURFACE"
            c.target_space = space
            c.owner_space = space
            c.influence = influence
            return c
    except:
        utils.log_error(f"Unable to add limit distance constraint: {to_bone} {from_bone}")
        return None


def set_edit_bone_flags(edit_bone, flags, deform):
    edit_bone.use_connect = True if "C" in flags else False
    edit_bone.use_local_location = True if "L" in flags else False
    edit_bone.use_inherit_rotation = True if "R" in flags else False
    edit_bone.use_deform = deform


def set_bone_layer(rig, bone_name, layer):
    if utils.edit_mode_to(rig):
        set_edit_bone_layer(rig, bone_name, layer)
    if utils.set_mode("OBJECT"):
        set_pose_bone_layer(rig, bone_name, layer)


def set_edit_bone_layer(rig, bone_name, layer):
    edit_bone = rig.data.edit_bones[bone_name]
    for l in range(0, 32):
        edit_bone.layers[l] = l == layer


def set_pose_bone_layer(rig, bone_name, layer):
    pose_bone = rig.data.bones[bone_name]
    for l in range(0, 32):
        pose_bone.layers[l] = l == layer


def copy_position(rig, bone, copy_bones, offset):
    if utils.edit_mode_to(rig):
        if bone in rig.data.edit_bones:
            edit_bone = rig.data.edit_bones[bone]
            head_position = mathutils.Vector((0,0,0))
            tail_position = mathutils.Vector((0,0,0))
            num = 0
            for copy_name in copy_bones:
                if copy_name in rig.data.edit_bones:
                    copy_bone = rig.data.edit_bones[copy_name]
                    dir = (copy_bone.tail - copy_bone.head).normalized()
                    head_position += copy_bone.head + dir * offset
                    tail_position += copy_bone.tail + dir * offset
                    num += 1
            head_position /= num
            tail_position /= num
            edit_bone.head = head_position
            edit_bone.tail = tail_position
            return edit_bone
        else:
            utils.log_error(f"Cannot find bone {bone} in rig!")
    return None


def set_bone_group(rig, bone, group):
    if utils.set_mode("OBJECT"):
        if bone in rig.pose.bones:
            bone_group = rig.pose.bone_groups[group]
            rig.pose.bones[bone].bone_group = bone_group
            return True
        else:
            utils.log_error(f"Cannot find pose bone {bone} in rig!")
    else:
        utils.log_error("Unable to edit rig!")


def get_distance_between(rig, bone_a_name, bone_b_name):
    if utils.edit_mode_to(rig):
        if bone_a_name in rig.data.edit_bones and bone_b_name in rig.data.edit_bones:
            bone_a = rig.data.edit_bones[bone_a_name]
            bone_b = rig.data.edit_bones[bone_b_name]
            delta : mathutils.Vector = bone_b.head - bone_a.head
            return delta.length
        else:
            utils.log_error(f"Could not find all bones: {bone_a_name} and {bone_b_name} in Rig!")
    else:
        utils.log_error(f"Unable to edit rig!")
    return 0


def generate_eye_widget(rig, bone_name, bones, distance, scale):
    wgt : bpy.types.Object = None
    if utils.set_mode("OBJECT"):
        if len(bones) == 1:
            bpy.ops.mesh.primitive_circle_add(vertices=16, radius=1, rotation=[0,0,11.25])
            bpy.ops.object.transform_apply(rotation=True)
            wgt = utils.get_active_object()
        else:
            bpy.ops.mesh.primitive_circle_add(vertices=16, radius=1.35, rotation=[0,0,11.25])
            bpy.ops.object.transform_apply(rotation=True)
            wgt = utils.get_active_object()
            mesh : bpy.types.Mesh = wgt.data
            vert: bpy.types.MeshVertex
            for vert in mesh.vertices:
                if vert.co.x < -0.01:
                    vert.co.x -= 0.5 * distance / scale
                elif vert.co.x > 0.01:
                    vert.co.x += 0.5 * distance / scale
        if wgt:
            collection : bpy.types.Collection
            for collection in bpy.data.collections:
                if collection.name.startswith("WGTS_rig"):
                    collection.objects.link(wgt)
                elif wgt.name in collection.objects:
                    collection.objects.unlink(wgt)
            if bone_name in rig.pose.bones:
                pose_bone : bpy.types.PoseBone
                pose_bone = rig.pose.bones[bone_name]
                pose_bone.custom_shape = wgt
                wgt.name = "WGT-rig_" + bone_name
    return wgt


def add_pose_bone_custom_property(rig, pose_bone_name, prop_name, prop_value):
    if utils.set_mode("OBJECT"):
        if pose_bone_name in rig.pose.bones:
            pose_bone = rig.pose.bones[pose_bone_name]
            rna_idprop_ui_create(pose_bone, prop_name, default=prop_value, overridable=True, min=0, max=1)


def add_constraint_scripted_influence_driver(rig, pose_bone_name, data_path, variable_name, constraint_type, expression = ""):
    if utils.set_mode("OBJECT"):
        if pose_bone_name in rig.pose.bones:
            pose_bone = rig.pose.bones[pose_bone_name]
            con : bpy.types.Constraint = None
            for con in pose_bone.constraints:
                if con.type == constraint_type:
                    if expression:
                        driver = make_driver(con, "influence", "SCRIPTED", expression)
                    else:
                        driver = make_driver(con, "influence", "SUM")
                    if driver:
                        var = make_driver_var(driver, "SINGLE_PROP", variable_name, rig, data_path = data_path)


def make_driver_var(driver, var_type, var_name, target, data_path = "", bone_target = "", transform_type = "", transform_space = ""):
    """
    var_type = "SINGLE_PROP", "TRANSFORMS"
    var_name = variable name
    target = target object/bone
    target_data_path = "..."
    """
    var : bpy.types.DriverVariable = driver.variables.new()
    var.name = var_name
    if var_type == "SINGLE_PROP":
        var.type = var_type
        var.targets[0].id_type = "OBJECT"
        var.targets[0].id = target.id_data
        var.targets[0].data_path = data_path
    elif var_type == "TRANSFORMS":
        var.targets[0].id = target.id_data
        var.targets[0].bone_target = bone_target
        var.targets[0].rotation_mode = "AUTO"
        var.targets[0].transform_type = transform_type
        var.targets[0].transform_space = transform_space
    return var


def make_driver(source, prop_name, driver_type, driver_expression = ""):
    """
    prop_name = "value", "influence"
    driver_type = "SUM", "SCRIPTED"
    driver_expression = "..."
    """
    driver = None
    if source:
        fcurve : bpy.types.FCurve
        fcurve = source.driver_add(prop_name)
        driver : bpy.types.Driver = fcurve.driver
        if driver_type == "SUM":
            driver.type = driver_type
        elif driver_type == "SCRIPTED":
            driver.type = driver_type
            driver.expression = driver_expression
    return driver



def get_data_path_pose_bone_property(pose_bone_name, variable_name):
    data_path = f"pose.bones[\"{pose_bone_name}\"][\"{variable_name}\"]"
    return data_path


def get_data_rigify_limb_property(limb_id, variable_name):
    """
    limb_id = "LEFT_LEFT", "RIGHT_LEFT", "LEFT_ARM", "RIGHT_ARM", "TORSO", "JAW", "EYES"\n
    variable_name = "IK_Stretch", "IK_FK", "neck_follow", "head_follow", "mouth_lock", "eyes_follow"
    """
    if limb_id == "LEFT_LEG":
        return get_data_path_pose_bone_property("thigh_parent.L", variable_name)
    elif limb_id == "RIGHT_LEFT":
        return get_data_path_pose_bone_property("thigh_parent.R", variable_name)
    elif limb_id == "LEFT_ARM":
        return get_data_path_pose_bone_property("upper_arm_parent.L", variable_name)
    elif limb_id == "RIGHT_ARM":
        return get_data_path_pose_bone_property("upper_arm_parent.R", variable_name)
    elif limb_id == "TORSO":
        return get_data_path_pose_bone_property("torso", variable_name)
    elif limb_id == "JAW":
        return get_data_path_pose_bone_property("jaw_master", variable_name)
    elif limb_id == "EYES":
        return get_data_path_pose_bone_property("eyes", variable_name)
    return ""


def add_bone_prop_driver(rig, pose_bone_name, bone_data_path, bone_data_index, props, prop_name, variable_name):
    if utils.set_mode("OBJECT"):
        pose_bone : bpy.types.PoseBone
        if pose_bone_name in rig.pose.bones:
            pose_bone = rig.pose.bones[pose_bone_name]
            fcurve : bpy.types.FCurve
            fcurve = pose_bone.driver_add(bone_data_path, bone_data_index)
            driver : bpy.types.Driver = fcurve.driver
            driver.type = "SUM"
            var : bpy.types.DriverVariable = driver.variables.new()
            var.name = variable_name
            var.type = "SINGLE_PROP"
            var.targets[0].id_type = "SCENE"
            var.targets[0].id = props.id_data
            var.targets[0].data_path = props.path_from_id(prop_name)


def clear_constraints(rig, pose_bone_name):
    if pose_bone_name:
        if utils.set_mode("OBJECT"):
            if pose_bone_name in rig.pose.bones:
                pose_bone = rig.pose.bones[pose_bone_name]
                constraints = []
                for con in pose_bone.constraints:
                    constraints.append(con)
                for con in constraints:
                    pose_bone.constraints.remove(con)


def clear_drivers(rig):
    drivers = rig.animation_data.drivers
    if drivers:
        fcurves = []
        for fc in drivers:
            fcurves.append(fc)
        for fc in fcurves:
            drivers.remove(fc)


def get_bone_name_from_data_path(data_path):
    if data_path.startswith("pose.bones[\""):
        start = utils.safe_index_of(data_path, '"', 0) + 1
        end = utils.safe_index_of(data_path, '"', start)
        return data_path[start:end]
    return None


def get_roll(bone):
    mat = bone.matrix_local.to_3x3()
    quat = mat.to_quaternion()
    if abs(quat.w) < 1e-4:
        roll = pi
    else:
        roll = 2*atan(quat.y/quat.w)
    return roll


def clear_pose(arm):
    # select all bones in pose mode
    arm.data.pose_position = "POSE"
    utils.object_mode_to(arm)
    utils.set_mode("POSE")
    bone : bpy.types.Bone
    for bone in arm.data.bones:
        bone.select = True

    # unlock the bones
    pose_bone : bpy.types.PoseBone
    for pose_bone in arm.pose.bones:
        pose_bone.lock_location = [False, False, False]
        pose_bone.lock_rotation = [False, False, False]
        pose_bone.lock_rotation_w = False
        pose_bone.lock_scale = [False, False, False]

    # clear pose
    bpy.ops.pose.transforms_clear()

    utils.object_mode_to(arm)


def reset_root_bone(arm):
    if utils.edit_mode_to(arm):
        root_bone = arm.data.edit_bones[0]
        if "root" in root_bone.name.lower():
            head = root_bone.head
            length = root_bone.length
            tail = head + mathutils.Vector((0,-1,0)) * length
            root_bone.tail = tail
            root_bone.align_roll(mathutils.Vector((0,0,1)))
    utils.set_mode("OBJECT")


def bone_mapping_contains_bone(bone_mappings, bone_name):
    for bone_mapping in bone_mappings:
            if cmp_rl_bone_names(bone_mapping[1], bone_name):
                return True
    return False


def get_accessory_root_bone(bone_mappings, bone):
    root = None
    if not bone_mapping_contains_bone(bone_mappings, bone.name):
        while bone.parent:
            if not bone_mapping_contains_bone(bone_mappings, bone.parent.name):
                root = bone.parent
            bone = bone.parent
    return root


def bone_parent_in_list(bone_list, bone):
    if bone:
        while bone.parent:
            if bone.parent.name in bone_list:
                return True
            bone = bone.parent
    return False


def find_accessory_bones(bone_mappings, rig):
    accessory_bones = []
    for bone in rig.data.bones:
        bone_name = bone.name
        if not bone_mapping_contains_bone(bone_mappings, bone_name):
            if bone_name not in accessory_bones and not bone_parent_in_list(accessory_bones, bone):
                utils.log_info(f"Accessory Bone: {bone_name}")
                accessory_bones.append(bone_name)
    return accessory_bones