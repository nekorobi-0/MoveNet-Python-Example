import numpy as np
import sympy
import math
import classes
#座標系の定義
#z-upな左手系な座標系とする
def point_calc(p:np.ndarray,v:np.ndarray,q:np.ndarray,w:np.ndarray):
    """#直線１を表す点とベクトル
    p = np.array([-1, 1, 1])#位置ベクトル
    v = np.array([1, 0, -1])#方向のベクトル

    #直線２を表す点とベクトル
    q = np.array([0, 3, 2])#位置ベクトル
    w = np.array([1, 2, -1])#方向のベクトル

    #変数s, tを用意
    s = sympy.Symbol('s')
    t = sympy.Symbol('t') #ここからs, tは通常の変数ではなく記号として扱う"""

    """
    直線１を成す点Pの座標は次の通り
        (x, y, z) = (p[0]+s*v[0], p[1]+s*v[1], p[2]+s*v[2])
    直線２を成す点Qの座標は次の通り
        (x, y, z) = (q[0]+t*w[0], q[1]+r*w[1], q[2]+r*w[2])
    """
    #点Pと点Qの距離の２乗
    PQ2 = ( (q[0]+t*w[0]) - (p[0]+s*v[0]) )**2\
        +( (q[1]+t*w[1]) - (p[1]+s*v[1]) )**2\
        +( (q[2]+t*w[2]) - (p[2]+s*v[2]) )**2
    #これを偏微分
    dPQ2_ds = sympy.diff(PQ2, s)
    dPQ2_dt = sympy.diff(PQ2, t)
    print('dPQ2/ds = {}'.format(dPQ2_ds))
    print('dPQ2/dt = {}'.format(dPQ2_dt))
    #偏導関数＝０を連立方程式として解く
    ans = sympy.solve([dPQ2_ds, dPQ2_dt])
    print('ans = {}'.format(ans))
    s, t = ans[s], ans[t] #ここでs, tは通常の変数に戻る
    print('(s, t) = ({}, {})'.format(s, t))

    """"
    最接近時のs, tが求められた
    """
    #直線1上のどこか
    x1, y1, z1 = p[0]+s*v[0], p[1]+s*v[1], p[2]+s*v[2]
    #それは直線２上のどこなのか
    x2, y2, z2 = q[0]+t*w[0], q[1]+t*w[1], q[2]+t*w[2]
    return (x1+x2)/2,(y1+y2)/2,(z1+z2)/2
    #最接近距離
    PQ2 = ( (q[0]+t*w[0]) - (p[0]+s*v[0]) )**2\
         +( (q[1]+t*w[1]) - (p[1]+s*v[1]) )**2\
         +( (q[2]+t*w[2]) - (p[2]+s*v[2]) )**2
    PQ = PQ2**0.5
    print('min distance = {}'.format(PQ))



def data_prossessing(keypoints_list_list,scores_list_list,cam_info):
    for keypoints_list,scores_list in zip(keypoints_list_list,scores_list_list):
        cam_infos = [cam_info for i in len(keypoints_list)]
        k = [kp(k,sc,cam) for k,sc,cam in zip(keypoints_list,scores_list,cam_infos)]
        for p in k:
            p
             
             
class twoDpos:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
class kp:#キーポイントとカメラ情報を引数にして位置ベクトルと方向ベクトルを導出するクラス(単体)
    def __init__(self,keypoint,score,cam) -> None:
        self.kp:twoDpos =  keypoint
        self.sc = score
        self.ca:classes.cam = cam
        self.pvec = self.ca.pvec
    def avg(self,other):#もう一方の点との結果を統合して新しくクラスに取り込む
        pass
    def calc(self):
        #ここからキーポイントの座標をカメラの情報と合わせることでカメラ原点のローカル座標系に変換する
        for i in range(2):
            math.cos()
        gdvec :np.ndarray = [
            
        ]#x,y,z-横がxで縦がy
        self.gdvec :np.ndarray = np.array(self.ldvec)*self.ca.rvec
        #方向ベクトルをカメラの回転行列との積を取ってカメラのローカル座標系を回転を補正したグローバルな方向ベクトルに変換する
    def calcdeg(self):#角度を導出してそこから方向ベクトルを導出する
        self.w_deg:float = math.atan2(self.kp.x/self.ca.w_tanth)
        self.h_deg:float = math.atan2(self.kp.y/self.ca.h_tanth)
        #x,y,z-横がxで縦がy
        self.ldvec:np.ndarray = np.array([
            math.tan(self.w_deg),
            math.tan(self.h_deg),
            1])



if __name__ == "__main__":
    point_calc()