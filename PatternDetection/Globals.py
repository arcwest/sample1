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
    maxlengthofrealityspeculatortobeprocessed = 16
    maxpatnodeperddo = 128
    maxpatobjectscreated = 0
    maxvertnodeobjectcreated = 0
    maxhornodeobjectcreated = 0
    maxpatnodepernode = 64
    maxpatnodeovershoot = 128
    minemptoprocessDDO = 100
    printenable = 1
    logfunc = None
    count = 0
    def log(self,s):
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
        
