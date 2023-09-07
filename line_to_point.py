import numpy as np
import sympy
def point_calc(p,v,q,w):
    #直線１を表す点とベクトル
    """
    p = np.array([-1, 1, 1])位置ベクトル
    v = np.array([1, 0, -1])方向ベクトル
    """

    #直線２を表す点とベクトル
    """
    q = np.array([0, 3, 2])位置ベクトル
    w = np.array([1, 2, -1])方向ベクトル
    """

    #変数s, tを用意
    s = sympy.Symbol('s')
    t = sympy.Symbol('t') #ここからs, tは通常の変数ではなく記号として扱う

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
    x0, y0, z0 = p[0]+s*v[0], p[1]+s*v[1], p[2]+s*v[2]
    #それは直線２上のどこなのか
    x1, y1, z1 = q[0]+t*w[0], q[1]+t*w[1], q[2]+t*w[2]

    x,y,z = (x0+x1)/2,(y0+y1)/2,(z0+z1)/2
    return(x,y,z)
    #最接近距離
    PQ2 = ( (q[0]+t*w[0]) - (p[0]+s*v[0]) )**2\
         +( (q[1]+t*w[1]) - (p[1]+s*v[1]) )**2\
         +( (q[2]+t*w[2]) - (p[2]+s*v[2]) )**2
    PQ = PQ2**0.5
    print('min distance = {}'.format(PQ))
def data_prossessing(keypoint_score_th,keypoints_list,scores_list):
    pass
if __name__ == "__main__":
    point_calc()
