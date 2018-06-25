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
            GlobalConfig().maxpatobjectscreated += 1
            
        def calemphasis(self):
            return((2** self.vertlevel)*(1 + self.horlevel)*self.intensity)

        def excite(self):
            self.P.add2tray(self)
    def __init__(self, params, P):
        '''
        Constructor
        '''
        
        self.RealityNodelist = {}
        self.netmatchcount = 0
        self.DDO = []
        self.verlist = [[]]*32
        self.tray = []
        self.marked = 0
        self.P = P
        self.emp = 0
        self.G = GlobalConfig()
        self.netpatemp = 0
  

    def AddRealityNode(self,R):
        self.RealityNodelist.update({R:0})
    
    
        
        
    def formDDO(self, nodelist):
        patlist = []
        for el in nodelist:
            pat = self.formpatnode(el)
            if(pat):
                patlist += [pat]
                
                
                
        # sort
        patlist = sorted(patlist, key=attrgetter('emp'), reverse = True)
        
        # reduce the patlist
        if(len(patlist) > self.G.maxpatnodeperddo):
            patlist = patlist[0:self.G.maxpatnodeperddo]
            
        self.netpatemp = 0    
        for el in patlist:
            self.netpatemp += el.emp
            # link the pat to node for excitation
          
        self.G.log('total pat: '+str(len(patlist)) + ' netemp: '+str(self.netpatemp), 1)      
        if(len(patlist) > self.G.minNumOfPatNodeForToBeConsideredForBeingRs):
            for el in patlist:
                el.node.addrspatnode(el)
        else:
            patlist = []
            
            
        self.DDO = patlist
        
    
        
    def formpatnode(self,node):
        pat = None
        if(node.vert == 0): #horizontal nodes
            pat = self.PatNode(node.vertlevel, node.level, node.Range, self)
            #node.addrspatnode(pat)
            pat.node = node
        return(pat)
    
    def reset(self):
        self.tray = []
        self.marked = 0
        
        
    def add2tray(self,pat):
        self.tray += [pat]
        if(not self.marked):
            self.P.P.add2RsTray(self)
            self.marked = 1
    
    def calculateMatchPercent(self):
        empn = 0
        for el in self.tray:
            empn += el.emp
         
        matchpercent = empn/self.netpatemp
        if(self.marked == 1):
            self.emp += matchpercent
            self.marked = 2
            
        return(matchpercent)
    
    def printddo(self):
        print(len(self.DDO))
        for el in self.DDO:
            print(' VL: ',el.vertlevel, ' HL: ',el.horlevel, 'Id: ', el.node.id, 'Idv: ', el.node.idv, 'R:', el.range, ' emp: ', el.emp, 'obj: ', print(el.node))
    
class PatternClassifier:
    
    def __init__(self,P):
        self.nodelist = {}
        self.P = P
   
    def AddNode(self,node):
        self.nodelist.update({node:0})
        
    def clearNodelist(self):
        self.nodelist = {}
        
    def formDDO(self):
        DDO = PatternDetected([], self)
        DDO.formDDO(list(self.nodelist.keys()))
        self.clearNodelist()
        return(DDO)
        
          