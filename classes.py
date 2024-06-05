import math
import numpy as np
class cam:
    def __init__(self,w:int,h:int,px:float,py:float,pz:float,
            deg_h:float,deg_w:float,rvec:np.ndarray,pvec:np.ndarray,camid:int):
        self.height:int = h
        self.width:int = w
        self.origin:pos = pos(px,py,pz)
        self.deg_h:float = deg_h
        self.deg_w:float = deg_h
        self.h_tanth:float = self.height/math.tan(deg_h)
        self.w_tanth:float = self.width /math.tan(deg_w)
        self.rmatrix:np.ndarray = rvec
        self.pvec:np.ndarray = pvec
        self.camid :int = camid
class pos:
    def __init__(self,x:float,y:float,z:float):
        self.x:float = x
        self.y:float = y
        self.z:float = z