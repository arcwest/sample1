'''
Created on 22 Jun 2018

@author: atind
'''
from cgi import valid_boundary

def IsTimeAvailable():
    return(True)



class HorizontalDetectorNode:
    
    def __init__(self, minval, maxval, horizontalboundaryPercent = 0.25):
        self.ChildNode = None
        self.Range = [0,0]
        self.horizontalboundaryPercent = horizontalboundaryPercent
        self.formRange(minval, maxval)
        self.markerfunc = None
        
    def setmarker(self,func):
        self.markerfunc = func
        
    def input(self,val):
      
        if(self.isinrange(val)):    
            self.mark(self)
            self.adjust(val)
            
        
    def isinrange(self,val):
        return(val > self.Range[0] and val < self.Range[1])
    
    def adjust(self,val):
        
        diff = abs(self.Range[1] - self.Range[0])
            
        if(self.ChildNode == None):
            if(val - self.Range[0] > self.horizontalboundaryPercent*diff or self.Range[1] - val > self.horizontalboundaryPercent*diff ):
                self.formchild()
        
        self.ChildNode[0].input(val)
        self.ChildNode[1].input(val)
        
            
    def formRange(self,leftval, rightval):
        self.Range = [leftval, rightval]
        
    def formchild(self):
        self.ChildNode = [HorizontalDetectorNode(self.horizontalboundaryPercent), HorizontalDetectorNode(self.horizontalboundaryPercent)]
        
    def mark(self,object):
        if(self.markerfunc):
            self.markerfunc(object)
        

class VerticalDetectorNode:
    
    def __init__(self, minval, maxval, horizontalboundaryPercent = 0.25):
        self.Hnode = None
        self.ChildNode = [None, None]
        self.lastinput = 0
        self.downsampleflag = 1
        self.minval = minval
        self.maxval = maxval
        self.horizontalboundaryPercent = horizontalboundaryPercent
        
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
        
        if(self.downsampleflag and IsTimeAvailable()):
            
            if(self.ChildNode[0] == None):
                self.ChildNode = [VerticalDetectorNode(),VerticalDetectorNode()]
            
            self.ChildNode[0].input((self.lastinput + inp) / 2) #LPF 
            
            self.ChildNode[1].input((inp - self.lastinput) / 2) #HPF 
            
    def InsertHnode(self, inp):
        if(self.Hnode == None):
            self.Hnode = HorizontalDetectorNode(self.minval, self.maxval, self.horizontalboundaryPercent)
            
        
        self.Hnode.input(inp)
        
    def mark(self,object):
        if(self.markerfunc):
            self.markerfunc(object)
        
            
        

class PatternDetector(object):
    '''
    classdocs
    '''


    def __init__(self, minval, maxval, markerfunc,  horizontalboundaryPercent = 0.25):
        '''
        Constructor
        '''
        self.markerfunc = markerfunc
        self.Vnode = VerticalDetectorNode(minval, maxval, horizontalboundaryPercent = 0.25)
        self.Vnode.setmarker(self.markerfunc)
        
    def input(self,val):
        self.Vnode.input(val)
