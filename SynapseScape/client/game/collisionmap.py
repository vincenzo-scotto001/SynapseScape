from .worldpoint import WorldPoint

class CollisionMap:
    def n(self, x: int, y: int, z: int) -> bool:
        raise NotImplementedError()
    
    def e(self, x: int, y: int, z: int) -> bool:
        raise NotImplementedError()
    
    def s(self, x: int, y: int, z: int) -> bool:
        return self.n(x, y-1, z)
    
    def w(self, x: int, y: int, z: int) -> bool:
        return self.e(x-1, y, z)
    
    def ne(self, x: int, y: int, z: int) -> bool:
        return self.n(x, y, z) and self.e(x, y+1, z) and self.e(x, y, z) and self.n(x+1, y, z)
    
    def nw(self, x: int, y: int, z: int) -> bool:
        return self.n(x, y, z) and self.w(x, y+1, z) and self.w(x, y, z) and self.n(x-1, y, z)
    
    def se(self, x: int, y: int, z: int) -> bool:
        return self.s(x, y, z) and self.e(x, y-1, z) and self.e(x, y, z) and self.s(x+1, y, z)
    
    def sw(self, x: int, y: int, z: int) -> bool:
        return self.s(x, y, z) and self.w(x, y-1, z) and self.w(x, y, z) and self.s(x-1, y, z)
    
    def n_wp(self, wp: WorldPoint) -> bool:
        return self.n(wp.x, wp.y, wp.plane)
    
    def e_wp(self, wp: WorldPoint) -> bool:
        return self.e(wp.x, wp.y, wp.plane)
    
    def s_wp(self, wp: WorldPoint) -> bool:
        return self.s(wp.x, wp.y, wp.plane)
    
    def w_wp(self, wp: WorldPoint) -> bool:
        return self.w(wp.x, wp.y, wp.plane)
    
    def ne_wp(self, wp: WorldPoint) -> bool:
        return self.ne(wp.x, wp.y, wp.plane)
    
    def nw_wp(self, wp: WorldPoint) -> bool:
        return self.nw(wp.x, wp.y, wp.plane)
    
    def se_wp(self, wp: WorldPoint) -> bool:
        return self.se(wp.x, wp.y, wp.plane)
    
    def sw_wp(self, wp: WorldPoint) -> bool:
        return self.sw(wp.x, wp.y, wp.plane)
