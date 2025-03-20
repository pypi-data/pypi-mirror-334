# Author: Cameron F. Abrams <cfa22@drexel.edu>

import numpy as np
from scipy.interpolate import interp1d
from .satd import SATD
from .suph import SUPH


SteamTables=dict(
    satd=SATD(),
    suph=SUPH('V'),
    subc=SUPH('L')
)

class PHASE:
    def __init__(self):
        pass

LARGE=1.e99
NEGLARGE=-LARGE

class State:
    _p=['T','P','u','v','s','h','x']
    _sp=['T','P','VL','VV','UL','UV','HL','HV','SL','SV']
    def _resolve(self):
        """ Resolve the thermodynamic state of steam/water given specifications
        """
        self.spec=[p for p in self._p if self.__dict__[p]!=None]
        assert len(self.spec)==2,f'Error: must specify two properties (of {self._p}) for steam; found {self.spec}'
        if self.spec[1]=='x':
            ''' explicitly saturated '''
            self._resolve_satd()
        else:
            if self.spec==['T','P']:
                ''' T and P given explicitly '''
                self._resolve_subsup()
            elif 'T' in self.spec or 'P' in self.spec:
                ''' T OR P given, along with some other property (v,u,s,h) '''
                self._resolve_TPTh()
            else:
                raise Exception('If not explicitly saturated, you must specify either T or P')

    def _resolve_TPTh(self):
        ''' T or P along with one other property (th) are specified '''
        p=self.spec[0]
        cp='P' if p=='T' else 'T'
        th=self.spec[1]
        if self.satd.lim[p][0]<self.__dict__[p]<self.satd.lim[p][1]:
            ''' T or P is between saturation limits; may be a saturated state, so 
                check whether the second property value lies between its liquid
                and vapor phase values at this T or P '''
            thL=self.satd.interpolators[p][f'{th.upper()}L'](self.__dict__[p])
            thV=self.satd.interpolators[p][f'{th.upper()}V'](self.__dict__[p])
            self.__dict__[cp]=self.satd.interpolators[p][cp](self.__dict__[p])
            if thL<self.__dict__[th]<thV:
                ''' This is a saturated state! Use lever rule to get vapor fraction: '''
                self.x=(self.__dict__[th]-thL)/(thV-thL)
                self.Liquid=PHASE()
                self.Vapor=PHASE()
                self.Liquid.__dict__[th]=thL
                self.Vapor.__dict__[th]=thV
                for pp in self._sp:
                    if pp not in ['T','P',f'{th.upper()}V',f'{th.upper()}L']:
                        ppp=self.satd.interpolators[p][pp](self.__dict__[p])
                        if pp[-1]=='V':
                            self.Vapor.__dict__[pp[0].lower()]=ppp
                        elif pp[-1]=='L':
                            self.Liquid.__dict__[pp[0].lower()]=ppp
                for pp in self._p:
                    if pp not in [p,cp,'x']:
                        self.__dict__[pp]=self.x*self.Vapor.__dict__[pp]+(1-self.x)*self.Liquid.__dict__[pp]
            else:
                ''' even though T or P is between saturation limits, the other property is not '''
                specdict={p.upper():self.__dict__[p] for p in self.spec}
                if self.__dict__[th]<thL:
                    ''' Th is below its liquid-state value; assume this is a subcooled state '''
                    retdict=self.subc.Bilinear(specdict)
                    for p in self._p: 
                        if p not in self.spec and p!='x':
                            self.__dict__[p]=retdict[p.upper()]
                else:
                    ''' Th is above its vapor-state value; assume this is a superheated state '''
                    retdict=self.suph.Bilinear(specdict)
                    for p in self._p: 
                        if p not in self.spec and p!='x':
                            self.__dict__[p]=retdict[p.upper()]
        elif self.__dict__[p]>self.satd.lim[p][1]:
            ''' Th is above its vapor-state value; assume this is a superheated state '''
            specdict={p.upper():self.__dict__[p] for p in self.spec}
            retdict=self.suph.Bilinear(specdict)
            for p in self._p: 
                if p not in self.spec and p!='x':
                    self.__dict__[p]=retdict[p.upper()]
        else:
            ''' Th is below its liquid-state value; assume this is a subcooled state '''
            specdict={p.upper():self.__dict__[p] for p in self.spec}
            retdict=self.subc.Bilinear(specdict)
            for p in self._p: 
                if p not in self.spec and p!='x':
                    self.__dict__[p]=retdict[p.upper()]

    def _resolve_subsup(self):
        ''' T and P are both given explicitly.  Could be either superheated or subcooled state '''
        assert self.spec==['T','P']
        specdict={'T':self.T,'P':self.P}
        if self.satd.lim['T'][0]<self.T<self.satd.lim['T'][1]:
            Psat=self.satd.interpolators['T']['P'](self.T)
        else:
            Psat=LARGE
        if self.P>Psat:
            ''' P is higher than saturation: this is a subcooled state '''
            retdict=self.subc.Bilinear(specdict)
        else:
            ''' P is lower than saturation: this is a superheated state '''
            retdict=self.suph.Bilinear(specdict)
        for p in self._p: 
            if p not in self.spec and p!='x':
                self.__dict__[p]=retdict[p.upper()]

    def _resolve_satd(self):
        ''' This is an explicitly saturated state with vapor fraction (x) and one 
        other property (p) specified '''
        p=self.spec[0]
        self.Liquid=PHASE()
        self.Vapor=PHASE()
        if p=='T':
            ''' The other property is T; make sure it lies between saturation limits '''
            if self.T<self.satd.lim['T'][0] or self.T>self.satd.lim['T'][1]:
                raise Exception(f'Cannot have a saturated state at T = {self.T} C')
            ''' Assign all other property values by interpolation '''
            for q in self._sp:
                if q!='T':
                    prop=self.satd.interpolators['T'][q](self.T)
                    if q=='P': self.__dict__[q]=prop
                    if q[-1]=='V':
                        self.Vapor.__dict__[q[0].lower()]=prop
                    elif q[-1]=='L':
                        self.Liquid.__dict__[q[0].lower()]=prop
            for q in self._p:
                if not q in 'PTx':
                    self.__dict__[q]=self.x*self.Vapor.__dict__[q]+(1-self.x)*self.Liquid.__dict__[q]
        elif p=='P':
            ''' The other property is P; make sure it lies between saturation limits '''
            if self.P<self.satd.lim['P'][0] or self.P>self.satd.lim['P'][1]:
                raise Exception(f'Cannot have a saturated state at P = {self.P} MPa')
            ''' Assign all other property values by interpolation '''
            for q in self._sp:
                if q!='P':
                    prop=self.satd.interpolators['P'][q](self.P)
                    if q=='T': self.__dict__[q]=prop
                    if q[-1]=='V':
                        self.Vapor.__dict__[q[0].lower()]=prop
                    elif q[-1]=='L':
                        self.Liquid.__dict__[q[0].lower()]=prop
            for q in self._p:
                if not q in 'PTx':
                    self.__dict__[q]=self.x*self.Vapor.__dict__[q]+(1-self.x)*self.Liquid.__dict__[q]
        else:
            ''' The other property is neither T or P; must use a lever-rule-based interpolation '''
            self._resolve_satd_lever()

    def _resolve_satd_lever(self):
        p=self.spec[0]
        assert p!='T' and p!='P'
        ''' Vapor fraction and one other property value (not T or P) is given '''
        th=self.__dict__[p]
        x=self.__dict__['x']
        ''' Build an array of V-L mixed properties based on given value of x '''
        Y=np.array(self.satd.DF['T'][f'{p.upper()}V'])*x+np.array(self.satd.DF['T'][f'{p.upper()}L'])*(1-x)
        X=np.array(self.satd.DF['T']['T'])
        ''' define an interpolator '''
        f=interp1d(X,Y)
        try:
            ''' interpolate the Temperature '''
            self.T=f(x)
            ''' Assign all other property values '''
            for q in self._sp:
                if q!='T':
                    prop=self.satd.interpolators['T'][q](self.T)
                    if q=='P': self.__dict__[q]=prop
                    if q[-1]=='V':
                        self.Vapor.__dict__[q[0].lower()]=prop
                    elif q[-1]=='L':
                        self.Liquid.__dict__[q[0].lower()]=prop
            for q in self._p:
                if not q in 'PTx':
                    self.__dict__[q]=self.x*self.Vapor.__dict__[q]+(1-self.x)*self.Liquid.__dict__[q]
        except:
            raise Exception(f'Could not interpolate {p} = {th} at quality {x} from saturated steam table')
        
    def __init__(self,**kwargs):
        self.satd=SteamTables['satd']
        self.suph=SteamTables['suph']
        self.subc=SteamTables['subc']
        for p in self._p:
            self.__dict__[p]=kwargs.get(p,None)
        self._resolve()

class RandomSample(State):
    def __init__(self,phase='suph',satdDOF='T',seed=None,Prange=None,Trange=None):
        if phase=='satd':
            if satdDOF=='T':
                sample_this=SteamTables[phase].DF['T']
            else:
                sample_this=SteamTables[phase].DF['P']
        elif phase=='suph' or phase=='subc':
            sample_this=SteamTables[phase].data
        abs_mins={'T':sample_this['T'].min(),'P':sample_this['P'].min()}
        abs_maxs={'T':sample_this['T'].max(),'P':sample_this['P'].max()}
        sample=sample_this.sample(n=1,random_state=seed)
        T=sample['T'].values[0]
        P=sample['P'].values[0]
        if Trange and not Prange:
            if Trange[0]<abs_mins['T']:
                raise ValueError(f'Trange[0] ({Trange[0]}) is below the minimum T in the data ({abs_mins["T"]})')
            if Trange[1]>abs_maxs['T']:
                raise ValueError(f'Trange[1] ({Trange[1]}) is above the maximum T in the data ({abs_maxs["T"]})')
            while not Trange[0]<T<Trange[1]:
                sample=sample_this.sample(n=1)
                T=sample['T'].values[0]
        if Prange and not Trange:
            if Prange[0]<abs_mins['P']:
                raise ValueError(f'Prange[0] ({Prange[0]}) is below the minimum P in the data ({abs_mins["P"]})')
            if Prange[1]>abs_maxs['P']:
                raise ValueError(f'Prange[1] ({Prange[1]}) is above the maximum P in the data ({abs_maxs["P"]})')
            while not Prange[0]<P<Prange[1]:
                sample=sample_this.sample(n=1)
                P=sample['P'].values[0]
        if Prange and Trange:
            if Trange[0]<abs_mins['T']:
                raise ValueError(f'Trange[0] ({Trange[0]}) is below the minimum T in the data ({abs_mins["T"]})')
            if Trange[1]>abs_maxs['T']:
                raise ValueError(f'Trange[1] ({Trange[1]}) is above the maximum T in the data ({abs_maxs["T"]})')
            if Prange[0]<abs_mins['P']: 
                raise ValueError(f'Prange[0] ({Prange[0]}) is below the minimum P in the data ({abs_mins["P"]})')
            if Prange[1]>abs_maxs['P']: 
                raise ValueError(f'Prange[1] ({Prange[1]}) is above the maximum P in the data ({abs_maxs["P"]})')
            while not Prange[0]<P<Prange[1] or not Trange[0]<T<Trange[1]:
                sample=sample_this.sample(n=1)
                T=sample['T'].values[0]
                P=sample['P'].values[0]
        if phase=='satd':
            if satdDOF=='T':
                super().__init__(T=T,x=1.0)
            else:
                super().__init__(P=P,x=1.0)
        else:
            super().__init__(T=T,P=P)
    