from __future__ import annotations
import sympy
import numpy as np
import math
import classes
def point_calc(p:np.ndarray,v:np.ndarray,q:np.ndarray,w:np.ndarray):
    PQ2 = ( (q[0]+t*w[0]) - (p[0]+s*v[0]) )**2\
        +( (q[1]+t*w[1]) - (p[1]+s*v[1]) )**2\
        +( (q[2]+t*w[2]) - (p[2]+s*v[2]) )**2
    dPQ2_ds = sympy.diff(PQ2, s)
    dPQ2_dt = sympy.diff(PQ2, t)
    ans = sympy.solve([dPQ2_ds, dPQ2_dt])
    s, t = ans[s], ans[t] #ここでs, tは通常の変数に戻る
    x1, y1, z1 = p[0]+s*v[0], p[1]+s*v[1], p[2]+s*v[2]
    #それは直線２上のどこなのか
    x2, y2, z2 = q[0]+t*w[0], q[1]+t*w[1], q[2]+t*w[2]
    #最接近距離
    PQ2 = ( (q[0]+t*w[0]) - (p[0]+s*v[0]) )**2\
         +( (q[1]+t*w[1]) - (p[1]+s*v[1]) )**2\
         +( (q[2]+t*w[2]) - (p[2]+s*v[2]) )**2
    PQ:float = PQ2**0.5
    return (x1+x2)/2,(y1+y2)/2,(z1+z2)/2,PQ


class kp:#キーポイントとカメラ情報を引数にして位置ベクトルと方向ベクトルを導出するクラス(単体)
    def __init__(self,keypoints:list[tuple[float]],
                 scores:list[float],cam:classes.cam) -> None:
        self.kps:list[tuple[float]] =  keypoints
        self.scs:list[float] = scores
        self.ca:classes.cam = cam
        self.pvec = self.ca.pvec
        self.gdvecs :list[np.ndarray] = []
        for keypoint,score in zip(self.kps,self.scs):
            #ここからキーポイントの座標をカメラの情報と合わせることでカメラ原点のローカル座標系に変換する
            #方向ベクトルをカメラの回転行列との積を取ってカメラのローカル座標系を回転を補正したグローバルな方向ベクトルに変換する
            #角度を導出してそこから方向ベクトルを導出する
            w_deg:float = math.atan2(keypoint[0]/self.ca.w_tanth)
            h_deg:float = math.atan2(keypoint[1]/self.ca.h_tanth)
            #x,y,z-横がxで縦がy
            ldvec:np.ndarray = np.array([
                math.tan(w_deg),
                math.tan(h_deg),
                1])#ローカル順の方向ベクトル
            self.gdvecs.append(ldvec@self.ca.rmatrix)#グローバルの方向ベクトル

class twokp():
    def __init__(self,kp1:kp,kp2:kp) -> None:
        self.kp1:kp = kp1
        self.kp2:kp = kp2
        self.calc()
    def calc(self):
        self.poses:list[tuple[float]] =[]
        for gvec1,gvec2 in zip(self.kp1.gdvecs,self.kp2.gdvecs):
            self.x,self.y,self.z,self.d= point_calc(
                self.kp1.ca.pvec,gvec1,
                self.kp2.ca.pvec,gvec2)
            self.poses.append((self.x,self.y,self.z,self.d))

def data_prossessing(keypoints_list_list:list[list[list[tuple[float]]]],
                     scores_list_list:list[list[list[float]]],
                     cam_info):
    kp_list = []
    for keypoints_list,scores_list in zip(keypoints_list_list,scores_list_list):#2こだけ
        for keypoints,scores in zip(keypoints_list,scores_list):
            kp_list.append(kp(keypoints,scores,cam_info))#これは1カメラからの1人分のデータです
    #これは1人しかいない仮定のもとでしか動作しません
    person_pos = twokp(kp_list[0][0],kp_list[1][0])

    
