'''
Created on 23 Jun 2018

@author: atind
'''
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class GlobalConfig(metaclass=Singleton):
    minval = 0
    maxval = 100
    horizontalboundaryPercent = 0.25
    maxhorizontaldepth = 8
    maxvertdepth = 8
    noisefloor = 500
    maxmatchlength = 8
    matchadaptationfactor = 0.1
    maxlengthofrealityspeculatortobeprocessed = 32 #total number of RS actually considered for finding reality
    maxpatnodeperddo = 128 #max number of pat nodes to be used to define a RS or ddo. Note high emp once are selected first. increase this
                           #number to wider tree detection
    maxpatobjectscreated = 0
    maxvertnodeobjectcreated = 0
    maxhornodeobjectcreated = 0
    maxpatnodepernode = 64 #max number of pattern nodes for each detection nodes
    maxpatnodeovershoot = 128 #once this number exceeds the node trims pat nodes to this maxpatnodepernode
    printenable = 1
    minNetPatEmpToBeConsideredForBeingRS = 1000 # increase to reduce computation but it leads more to uniqueness detection
    minNumOfPatNodeForToBeConsideredForBeingRs = 36
    logfunc = None
    division = 128
    count = 0
    def log(self,s, enable):
        if(enable):
            self.logfunc(str(self.count) + ' :')
            self.logfunc(s)
            self.logfunc('\n')
            if(self.printenable):
                print(s)
            self.count += 1
    
    def printself(self):
        print('minval',self.minval)
        print('maxval',self.maxval)
        print('horizontalboundaryPercent',self.horizontalboundaryPercent)
        print('maxhorizontaldepth',self.maxhorizontaldepth)
        print('noisefloor',self.noisefloor)
        print('maxmatchlength',self.maxmatchlength)
        print('matchadaptationfactor',self.matchadaptationfactor)
        print('maxlengthofrealityspeculatortobeprocessed',self.maxlengthofrealityspeculatortobeprocessed)
        print('maxpatobjectscreated',self.maxpatobjectscreated)
        print('maxvertnodeobjectcreated',self.maxvertnodeobjectcreated)
        print('maxhornodeobjectcreated',self.maxhornodeobjectcreated)
        
