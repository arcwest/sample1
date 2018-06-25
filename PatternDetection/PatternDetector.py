'''
Created on 22 Jun 2018

@author: atind
'''
from cgi import valid_boundary
from Globals import GlobalConfig

def IsTimeAvailable():
    return(True)



class HorizontalDetectorNode:
    
    def __init__(self, vertlevel, dir , dirv):
        self.ChildNode = None
        self.G = GlobalConfig()
        self.min = self.G.minval
        self.max = self.G.maxval
        self.div = self.G.division
        self.markerfunc = None
        self.vertlevel = vertlevel
        self.vert = 0
        self.RealitySpecList = []
        self.patlist = []
        self.id = dir
        self.idv = dirv
        self.val = 0
        self.slotnum = 0
        
        
        self.G.maxhornodeobjectcreated += 1
        
    def AddRealitySpec(self,RS):
        self.RealitySpecList += [RS]
        
    def setmarker(self,func):
        self.markerfunc = func
        
    def input(self,val):
      
           
        self.mark(self)
        self.adjust(val)
        self.excite()
        
        
    def isinrange(self,val):
        return(val > self.Range[0] and val < self.Range[1] and abs(val) > self.G.noisefloor)
    
    def adjust(self,val):
        
        self.val = val
        self.slotnum = ((val - self.min)*self.div)/(self.max - self.min)
        
    def mark(self,obj):
        if(self.markerfunc):
            self.markerfunc(obj)
            
    def addrspatnode(self, rspat):
        if(len(self.patlist) > self.G.maxpatnodeovershoot):
            self.patlist = sorted(self.patlist, key= lambda x: x.P.emp, reverse = True)
            self.patlist = self.patlist[0:self.G.maxpatnodepernode]
            
        self.patlist += [rspat]
        
        
            
    def excite(self):
        for el in self.patlist:
            el.excite()
        

class VerticalDetectorNode:
    
    def __init__(self, level, dir):
        self.Hnode = None
        self.ChildNode = None
        self.lastinput = 0
        self.downsampleflag = 1
        self.G = GlobalConfig()
        self.level = level
        self.vert = 1
        self.G.maxvertnodeobjectcreated += 1
        self.id = dir
        
    def setmarker(self,func):
        self.markerfunc = func
        
    def input(self,inp):
            
        if(IsTimeAvailable()):
            self.InsertHnode(inp)
           
        self.mark(self) 
        
        self.InsertChild(inp)
        
        self.lastinput = inp
        
        
            
    def InsertChild(self,inp):
        
        self.downsampleflag = (self.downsampleflag + 1) % 2;
        
        if(self.downsampleflag and IsTimeAvailable() and self.level < self.G.maxvertdepth):
            
            if(self.ChildNode == None):
                self.ChildNode = [VerticalDetectorNode(self.level + 1, self.id +'L'),VerticalDetectorNode(self.level + 1, self.id +'R')]
                self.ChildNode[0].setmarker(self.markerfunc)
                self.ChildNode[1].setmarker(self.markerfunc)
            
            # Apply hpf (pi/2) and lpf (pi/2) before downsampling the input by 2
            self.ChildNode[0].input((self.lastinput + inp) / 2) #LPF 
            
            self.ChildNode[1].input((inp - self.lastinput) / 2) #HPF 
            
    def InsertHnode(self, inp):
        if(self.Hnode == None):
            self.Hnode = HorizontalDetectorNode(self.G.minval, self.G.maxval, self.level, 0, 'O', self.id)
            self.Hnode.setmarker(self.markerfunc)
            
        
        self.Hnode.input(inp)
        
    def mark(self,obj):
        pass
#         if(self.markerfunc):
#             self.markerfunc(obj)
        
            
        

class PatternDetector(object):
    '''
    classdocs
    '''


    def __init__(self, markerfunc):
        '''
        Constructor
        '''
        self.markerfunc = markerfunc
        self.Vnode = VerticalDetectorNode(0,'O')
        self.Vnode.setmarker(self.markerfunc)
        
    def input(self,val):
        self.Vnode.input(val)
