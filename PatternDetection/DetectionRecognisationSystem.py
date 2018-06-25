'''
Created on 23 Jun 2018

@author: atind
'''
from Globals import GlobalConfig
from PatternDetector import PatternDetector
from PatternDetected import PatternDetected, PatternClassifier
from operator import itemgetter, attrgetter
import math

class DetectionRecognisationSystem(object):
    '''
    classdocs
    '''

    class RealitySpeculator:
        
        def __init__(self, percent, reality, matchfunc):
            self.strength = percent
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
        self.PC = PatternClassifier(self)
        self.PDR = PatternDetector(self.PC.AddNode)
        self.RSTray = {}
        self.reset()
        self.RS = {}
        self.max = 0
        
    def reset(self):
        self.RSTray = {}
        
    def add2RsTray(self,rs):
        self.RSTray.update({rs:0})
        
        
    def input(self,inp):
        ### find the max
        if(self.max < inp):
            self.max = inp
        # reset to clear earlier detection
        self.reset()
        # insert the input to run the detection stage
        self.PDR.input(inp)
        # form the detected object tree for this match
        ddo = self.PC.formDDO()
        #print(len(ddo.DDO))
        self.RS.update({ddo:0})
        outlist = []

        self.G.log('inp: '+str(inp)+'  ddo patemp: '+str(ddo.netpatemp),0)
        if(len(ddo.DDO) > self.G.minNumOfPatNodeForToBeConsideredForBeingRs):
            # run over the excited releality speculator trees
            if(len(self.RSTray)):
                
                self.G.log('Total RS Found: '+str(len(self.RSTray)),1)
                # sort the rs as per there netpatemp
                self.RSTray = sorted(self.RSTray, key=lambda x:len(x.DDO), reverse = True)
                
                # truncate the reality speculator outlist to desired amount 
                if(len(self.RSTray) > self.G.maxlengthofrealityspeculatortobeprocessed):
                    self.RSTray = self.RSTray[0:self.G.maxlengthofrealityspeculatortobeprocessed]
                
                self.G.log('Total RS remained: '+str(len(self.RSTray)),1)
                
                # find best match
                for rs in self.RSTray:
                    # calculate match strength for each tree
                    outlist += [[rs.calculateMatchPercent(),rs]]
                    self.G.log('RS: netpatemp: '+str( rs.netpatemp)+ 'NumPat: '+str(len(rs.DDO))+'match%: '+str(rs.calculateMatchPercent()),1)
                    # reset the tree for next detection
                    rs.reset()
                    
                
                # insert the current ddo which is also a reality speculator
                
#                 outlist.insert(0, [1,ddo])
                self.G.log('RS ddo: netpatemp: '+str( ddo.netpatemp)+ 'NumPat: '+str(len(rs.DDO))+'match%: '+str(ddo.calculateMatchPercent()),1)
                
                    
                # find the reality information from this list
                if(len(outlist)):
                    outlist = self.findreality(outlist)
                
        if(len(outlist) < 2):
            outlist = [[],[]]
            ddo = None
            
        #print('max', self.max)
        self.max = 0
        return(outlist,ddo)
    
    def findreality(self, ddomatchlist):
        rnlist = {}
        sumnetmaxemp = 0
        for el in ddomatchlist:
            sumnetmaxemp += el[1].netpatemp
            
        for el in ddomatchlist:
            mp = el[0]
            ddo = el[1]
            
            for rsnode in ddo.RealityNodelist:
                try:
                    rnlist[rsnode.reality]+= mp*rsnode.strength
                    #print(ddo.printddo())
                except KeyError:
                    rnlist.update({rsnode.reality:mp*rsnode.strength})
                    #print(ddo.printddo())
                    
            
                    
            
        finalrealitylist = []
        for el in rnlist:
            finalrealitylist += [[el,rnlist[el]]]
            
        finalrealitylist = sorted(finalrealitylist, key=itemgetter(1), reverse = True)
        
#         sum1 = 0
#         for el in finalrealitylist:
#             sum1 += el[1]
#             
#         if(sum1 > 0):
#             for el in finalrealitylist:
#                 el[1] = el[1] / sum1
        
        #self.printinfo(finalrealitylist)
        
        return(finalrealitylist, ddomatchlist)
    
    def printinfo(self,finalrealitylist):
        print('---->')
        for el in finalrealitylist:
            print('reality: ', el[0], 'strength: ', el[1])
            
        print('<----')
        
    def assignreality(self, ddomatchlist, reality, matchfunc):
        
        if(reality):
            for el in ddomatchlist:
                mp = el[0]
                ddo = el[1]
                
                realitypresent = 0
                for rsnode in ddo.RealityNodelist:
                    if(rsnode.match(reality)):
                        realitypresent = 1
                        rsnode.strength += mp
                        
                    else:
                        rsnode.strength -= mp
                    
                        
                if(not realitypresent):
                    rn = self.RealitySpeculator(mp, reality, matchfunc)
                    ddo.AddRealityNode(rn)
            
            
                                     
    
    