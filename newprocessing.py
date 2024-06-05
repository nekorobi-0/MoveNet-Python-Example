from __future__ import annotations
import sympy
import numpy as np
import math
import classes
import pprint
import time
import drawer
def point_calc(p:np.ndarray,v:np.ndarray,q:np.ndarray,w:np.ndarray):
    s, t = sympy.symbols('s t')
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
def point_line_closest_point(a1:np.ndarray, b1:np.ndarray, a2:np.ndarray, b2:np.ndarray):
    cross_b1_b2 = np.cross(b1, b2)
    norm_cross_b1_b2 = np.linalg.norm(cross_b1_b2)
    
    if norm_cross_b1_b2 == 0:
        # b1とb2が平行な場合（直交しない場合）、特別なケースを扱う必要がある
        raise ValueError("The direction vectors are parallel or anti-parallel.")
    
    # 連立方程式の係数行列と右辺ベクトルを設定
    a = np.array([
        [np.dot(b1, b1), -np.dot(b1, b2)],
        [-np.dot(b1, b2), np.dot(b2, b2)]
    ])
    b = np.array([
        np.dot(a2 - a1, b1),
        np.dot(a2 - a1, b2)
    ])
    
    # 連立方程式を解いて t と s を求める
    t, s = np.linalg.solve(a, b)
    
    # 最近接点を計算
    closest_point_on_line1 = a1 + t * b1
    closest_point_on_line2 = a2 + s * b2
    
    # 最接近距離を計算
    min_distance = np.linalg.norm(closest_point_on_line1 - closest_point_on_line2)

    # 最接近点の中点を計算
    mid_point = (closest_point_on_line1 + closest_point_on_line2) / 2
    
    return mid_point[0],mid_point[1],mid_point[2], min_distance

# 例

class kp:#キーポイントとカメラ情報を引数にして位置ベクトルと方向ベクトルを導出するクラス(単体)
    def __init__(self,keypoints:list[tuple[float]],
                 scores:list[float],cam:classes.cam,sc:float) -> None:
        self.kps:list[tuple[float]] =  keypoints
        self.scs:list[float] = scores
        self.ca:classes.cam = cam
        self.pvec = self.ca.pvec
        self.gdvecs :list[np.ndarray] = []
        self.score:float = sc
    def calc(self):
        for keypoint,score in zip(self.kps,self.scs):
            #ここからキーポイントの座標をカメラの情報と合わせることでカメラ原点のローカル座標系に変換する
            #方向ベクトルをカメラの回転行列との積を取ってカメラのローカル座標系を回転を補正したグローバルな方向ベクトルに変換する
            #角度を導出してそこから方向ベクトルを導出する
            w_deg:float = math.atan2(keypoint[0],self.ca.w_tanth)
            h_deg:float = math.atan2(keypoint[1],self.ca.h_tanth)
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
        self.kp1.calc()
        self.kp2.calc()
        self.calc()
    def calc(self):
        self.poses:list[tuple[float]] =[]
        for gvec1,gvec2 in zip(self.kp1.gdvecs,self.kp2.gdvecs):
            self.x,self.y,self.z,self.d= point_line_closest_point(
                self.kp1.ca.pvec,gvec1,
                self.kp2.ca.pvec,gvec2)
            self.poses.append((self.x,self.y,self.z,self.d))
def scores_evaluation(scores:list[float]):
    scores = [score for score in scores if score>0.3]
    return 0 if len(scores)==0 else sum(scores)/len(scores)
def data_prossessing(keypoints_list_list:list[list[tuple[float]]],
                     scores_list_list:list[list[float]],
                     cam_infoes:list[classes.cam]):
    t1 = time.time()
    kp_list_list = []
    for keypoints_list,scores_list,cam_info in zip(keypoints_list_list,scores_list_list,cam_infoes):#2こだけ
        kp_list = []
        for keypoints,scores in zip(keypoints_list,scores_list):
            if (sc:=scores_evaluation(scores))<0.3:continue
            kp_list.append(kp(keypoints,scores,cam_info,sc))#これは1カメラからの1人分のデータです
        kp_list = sorted(kp_list,key=lambda x:x.score,reverse=True)
        kp_list_list.append(kp_list)
    t2 = time.time()
    #これは1人しかいない仮定のもとでしか動作しません
    if len(kp_list_list[0])==0 or len(kp_list_list[1])==0: return
    person_pos = twokp(kp_list_list[0][0],kp_list_list[1][0])
    person_pos.calc()
    t3 = time.time()
    datax = [i[0] for i in person_pos.poses]
    datay = [i[1] for i in person_pos.poses]
    dataz = [i[2] for i in person_pos.poses]
    drawer.draw(datax,datay,dataz)
    pass

    
