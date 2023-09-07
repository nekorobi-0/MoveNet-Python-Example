import math
def data_processing(keypoints_list,scores_list,conf_cam,disp_info):#画像座標を空間座標に変換
    conf_deg = deg2rad(conf_cam)
    for keypoint in len(keypoints_list[1]):#キーポイントの数だけループ
            #二直線の最接近点を出す
def deg2rads(conf_cam):#カメラ設定をラジアンに
    deg_list = [[deg2rad(n) for n in i] for i in conf_cam]
    return deg_list
def deg2rad(rad):
    return rad*0.0174533
