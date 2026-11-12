import numpy as np
def back(s): return lambda t: 1+(s+1)*(t-1)**3+s*(t-1)**2
E={'linear':lambda t:t,'sine.out':lambda t:np.sin(t*np.pi/2),'sine.inOut':lambda t:-(np.cos(np.pi*t)-1)/2,
'power1.out':lambda t:1-(1-t)**2,'power2.out':lambda t:1-(1-t)**3,'power3.out':lambda t:1-(1-t)**4,'power4.out':lambda t:1-(1-t)**5,
'expo.out':lambda t:np.where(t>=1,1,1-2**(-10*t)),'circ.out':lambda t:np.sqrt(1-(t-1)**2),
'power2.inOut':lambda t:np.where(t<.5,4*t**3,1-(-2*t+2)**3/2),'power3.inOut':lambda t:np.where(t<.5,8*t**4,1-(-2*t+2)**4/2),
'expo.inOut':lambda t:np.where(t<.5,2**(20*t-10)/2,(2-2**(-20*t+10))/2),'power2.in':lambda t:t**3,
'back.out(1.2)':back(1.2),'back.out(1.7)':back(1.7),'back.out(2.5)':back(2.5)}
def fit(f,p):
    f=np.asarray(f,float);p=np.asarray(p,float);best=None
    for n,e in E.items():
        for t0 in np.arange(f[0]-6,f[0]+12,0.5):
            for D in np.arange(3,60,0.5):
                t=np.clip((f-t0)/D,0,1);err=((e(t)-p)**2).mean()
                if best is None or err<best[0]: best=(err,n,t0,D)
    return dict(ease=best[1],t0=round(float(best[2]),1),dur=round(float(best[3]),1),rmse=round(float(np.sqrt(best[0])),3))
