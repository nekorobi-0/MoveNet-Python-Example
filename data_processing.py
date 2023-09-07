import math
def data_processing(keypoints_list,scores_list,conf_cam,disp_info):
    conf_deg = deg2rad(conf_cam)
    for i in len(conf_cam):
        keypoints = keypoints_list[i]
        keypoints
def deg2rad(conf_cam):
    deg_list = [[n*0.0174533 for n in i] for i in conf_cam]
    return deg_list