import math

class Mat:
    def __init__(self, width,length,main_spc,cross_spc,main_size,cross_size):
        #all dimensions in inches.
        self.width = width
        self.length = length
        self.main_spc = main_spc
        self.cross_spc = cross_spc

        #assume that wire area is the size/100.
        #May change this later to support metric.
        self.main_type,self.main_size = self._get_wire_size(main_size)
        self.cross_type,self.cross_size = self._get_wire_size(cross_size)

        #wire_parameters
        self.min_clr_from_edge = 0.5
        self.unit_wt=0.2836 #lbs/in**3

        #calculated values
        self.nmain = self._calc_wires(self.width, self.main_spc)
        self.ncross = self._calc_wires(self.length, self.cross_spc)

    def __str__(self):
        mat_desc=f'{self.width}"x{self.length}" {self.main_spc}"x{self.cross_spc}" D{self.main_size}/{self.cross_size}'
        wire_spc=f'{self.nmain} main wires, {self.ncross} cross wires'
        return mat_desc + "\n" + wire_spc

    def _get_wire_size(self, wire_size: str):
        if wire_size[0].lower() in ['d','w']:
            wire_type = wire_size[0]
            wire_size = wire_size[1:]
        else: raise ValueError("Wire size should start with D or W.")    

        try: 
            wire_size = float(wire_size)
        except ValueError:
            raise ValueError("Value after D or W is not a valid number.")

        return [wire_type, wire_size]

    def _calc_wires(self,length,spc):
        return math.floor((length - 2 * self.min_clr_from_edge)/spc)
    
    def get_weight(self):
        #assumes US units, weight in lbs
        main_vol=self.length*(self.main_size/100)*self.nmain
        cross_vol=self.width*(self.cross_size/100)*self.ncross
        return (main_vol+cross_vol)*self.unit_wt