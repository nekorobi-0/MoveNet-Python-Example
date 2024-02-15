class cam:
    def __init__(self,w:int,h:int,px:float,py:float,pz:float,deg_h:float,deg_w:float):
        self.height = h
        self.width = w
        self.origin = pos(px,py,pz)
        self.deg_h = deg_h
        self.deg_w = deg_h
class pos:
    def __init__(self,x:float,y:float,z:float):
        self.x = x
        self.y = y
        self.z = z