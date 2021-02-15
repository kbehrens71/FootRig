'''
Author - Kaitlyn Behrens
Date - 2/12/2021

This tool sets up the foot rigging for a skeleton with pre-existing foot joints.

Import this module, and run the run() method for each foot you want to be setup:

import FootRig
FootRig.run("rt")
FootRig.run("lf")

'''

import maya.cmds

# Create ik handles
def create_ik_handles(foot):
    maya.cmds.ikHandle( sj='{0}_ankle_jnt'.format(foot), ee='{0}_toe_jnt'.format(foot), p=1, w=1, solver='ikSCsolver')
    maya.cmds.ikHandle( sj='{0}_toe_jnt'.format(foot), ee='{0}_toetip_jnt'.format(foot), p=1, w=1, solver='ikSCsolver')
    maya.cmds.rename('ikHandle1', '{0}_ball_ikHandle'.format(foot))
    maya.cmds.rename('ikHandle2', '{0}_toe_ikHandle'.format(foot))

# Group leg ik handle & center pivot point at ball
def group_leg_ik(foot):
    maya.cmds.group( '{0}_leg_ik'.format(foot), n='{0}_ankle_grp'.format(foot))
    pivot_position_ball = maya.cmds.xform ('{0}_toe_jnt'.format(foot), q = True, ws = True, rotatePivot = True)
    maya.cmds.xform ('{0}_ankle_grp'.format(foot), ws = True, pivots = pivot_position_ball)

# Group toe ik handle & center pivot point at ball
def group_toe_ik(foot):
    maya.cmds.group( '{0}_toe_ikHandle'.format(foot), n='{0}_toe_grp'.format(foot))
    pivot_position_ball = maya.cmds.xform ('{0}_toe_jnt'.format(foot), q = True, ws = True, rotatePivot = True)
    maya.cmds.xform ('{0}_toe_grp'.format(foot), ws = True, pivots = pivot_position_ball)

# Group ball ik handle with toe and leg groups
def combine_all_groups(foot):
    maya.cmds.group( '{0}_ball_ikHandle'.format(foot), '{0}_ankle_grp'.format(foot), '{0}_toe_grp'.format(foot), n='{0}_heel_grp'.format(foot) )
    pivot_position_heel = maya.cmds.xform ('{0}_ankle_jnt'.format(foot), q = True, ws = True, rotatePivot = True)
    maya.cmds.xform ('{0}_heel_grp'.format(foot), ws = True, pivots = (pivot_position_heel[0], 0, pivot_position_heel[2]))

def run(foot):

    # Print which foot is currently being set up
    print "setting up {0} foot".format(foot)

    create_ik_handles(foot)
    group_leg_ik(foot)
    group_toe_ik(foot)
    combine_all_groups(foot)

    # Parent foot joints to leg control
    maya.cmds.parentConstraint( '{0}_leg_ctrl_ik'.format(foot), '{0}_heel_grp'.format(foot), mo = True )



