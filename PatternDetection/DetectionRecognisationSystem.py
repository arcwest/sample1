'''
Created on 23 Jun 2018

@author: atind
'''
from Globals import GlobalConfig
from PatternDetector import PatternDetector
from PatternDetected import PatternDetected
from operator import itemgetter, attrgetter

class DetectionRecognisationSystem(object):
    '''
    classdocs
    '''

    class RealitySpeculator:
        
        def __init__(self, percent, reality, matchfunc):
            self.percent = percent
            self.reality = reality
            self.matchfunc = matchfunc
            self.point = 0
            
        def match(self,reality):
            return(self.matchfunc(reality, self.reality))
        
        def reset(self):
            self.point = 0

    def __init__(self, params):
        '''
        Constructor
        '''
        self.G = GlobalConfig() 
        self.PD = PatternDetected(params, self)
        self.PDR = PatternDetector(self.PD.AddNode)
        self.RSTray = {}
        self.reset()
        
    def reset(self):
        self.RSTray = {}
        
    def add2RsTray(self,rs):
        self.RSTray.update({rs:0})
        
        
    def input(self,inp):
        # reset to clear earlier detection
        self.reset()
        # insert the input to run the detection stage
        self.PDR.input(inp)
        # form the detected object tree for this match
        ddo = self.PD.formDDO()
        outlist = []
        
        # run over the excited releality speculator trees
        for rs in self.RSTray:
            # calculate match percent for each tree
            outlist += [[rs.calculateMatchPercent(),rs]]
            # reset the tree for next detection
            rs.reset()
            
        # sort the list to have the rs tree in descending order of importance
        sorted(outlist, key=itemgetter(0), reverse = True)
        
        # insert the current ddo which is also a reality speculator
        outlist.insert(0, ddo)
        
        # truncate the reality speculator outlist to desired amount 
        if(len(outlist) > self.G.maxlengthofrealityspeculatortobeprocessed):
            outlist = outlist[0:self.G.maxlengthofrealityspeculatortobeprocessed]
            
        # find the reality information from this list
        outlist = self.findreality(outlist)
        
        return(outlist)
    
    def findreality(self, ddomatchlist):
        rnlist = {}
        for el in self.ddomatchlist:
            mp = el[0]
            ddo = el[1]
            
            for rsnode in ddo.RealityNodelist:
                try:
                    rnlist[rsnode.reality]+= mp*rsnode.percent
                except KeyError:
                    rnlist.update({rsnode.reality:0})
                    
            
        finalrealitylist = []
        for el in rnlist:
            finalrealitylist += [[el,rnlist[el]]]
            
        sorted(finalrealitylist, key=itemgetter(1), reverse = True)
        
        sum1 = 0
        for el in finalrealitylist:
            sum1 += el[1]
            
        if(sum1 > 0):
            for el in finalrealitylist:
                el[1] = el[1] / sum1
        
        self.printinfo(finalrealitylist)
        
        return(finalrealitylist, ddomatchlist)
    
    def printinfo(self,finalrealitylist):
        for el in finalrealitylist:
            print('reality: ', el[0], 'match %: ', el[1])
            
    
    def assignreality(self, ddomatchlist, reality, matchfunc):
        for el in ddomatchlist:
            mp = el[0]
            ddo = el[1]
            
            for rsnode in ddo.RealityNodelist:
                if(rsnode.match(reality)):
                    if(rsnode.percent < mp):
                        rsnode.percent = mp
                    else:
                        rsnode.percent = rsnode.percent - (mp - rsnode.percent)*self.G.matchadaptationfactor
                else:
                    rn = self.RealitySpeculator(mp, reality, matchfunc)
                    ddo.AddRealityNode(rn)
            
            
                                     
    
    