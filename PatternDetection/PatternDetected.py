'''
Created on 23 Jun 2018

@author: atind
'''
import math
from operator import itemgetter, attrgetter
from Globals import GlobalConfig

class PatternDetected(object):
    '''
    classdocs
    '''

    class PatNode:
        def __init__(self, vertlevel, horlevel, range1, P):
            self.vertlevel = vertlevel
            self.horlevel = horlevel
            self.range = range1
            self.netmatchsuccesscount = 0
            intval = math.ceil(abs(range1[1]))
            self.P = P
            self.node = None
            if(intval == 0):
                self.intensity = 0
            else:
                self.intensity = math.log10(math.ceil(abs(range1[1])))
            
            self.emp = self.calemphasis()
            
        def calemphasis(self):
            return((2** self.vertlevel)*(1 + self.horlevel)*self.intensity)

        def excite(self):
            self.P.add2tray(self)
    def __init__(self, params, P):
        '''
        Constructor
        '''
        self.nodelist = []
        self.RealityNodelist = {}
        self.netmatchcount = 0
        self.DDO = []
        self.verlist = [[]]*32
        self.tray = []
        self.marked = 0
        self.P = P
        self.emp = 0
        
        
  

    def AddRealityNode(self,R):
        self.RealityNodelist.update({R:0})
    
    def AddNode(self,node):
        self.nodelist += [node]
        
        
    def formDDO(self):
        patlist = []
        netemp = 0
        for el in self.nodelist:
            pat = self.formpatnode(el)
            if(pat):
                patlist += [pat]
                netemp += pat.emp
                
                
        # sort
        sorted(patlist, key=attrgetter('emp'), reverse = True)
        self.netemp = netemp
        self.DDO = patlist
        return(patlist)
    
    def clearNodelist(self):
        self.nodelist = [] 
        
    def formpatnode(self,node):
        pat = None
        if(node.vert == 0): #horizontal nodes
            pat = self.PatNode(node.vertlevel, node.level, node.Range, self)
            node.addrspatnode(pat)
            pat.node = node
        return(pat)
    
    def reset(self):
        self.tray = []
        self.marked = 0
        self.clearNodelist()
        
    def add2tray(self,pat):
        self.tray += [pat]
        if(not self.marked):
            self.P.add2RsTray(self)
            self.marked = 1
    
    def calculateMatchPercent(self):
        empn = 0
        for el in self.tray:
            empn += el.emp
         
        matchpercent = empn/self.netemp
        if(self.marked == 1):
            self.emp += matchpercent
            self.marked = 2
            
        return(matchpercent)
   

          