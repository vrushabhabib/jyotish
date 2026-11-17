"""Test 2: military (A3) vs painters (A4). Rules in docs/gauquelin/PRE-STATED-RULES-2.md, pushed first."""
import re, datetime as dt
from statistics import NormalDist
from engine.chart import build_chart
from engine.shadbala import shadbala

LORD={1:"Mars",2:"Venus",3:"Mercury",4:"Moon",5:"Sun",6:"Mercury",7:"Venus",8:"Mars",9:"Jupiter",10:"Saturn",11:"Saturn",12:"Jupiter"}
OWN={"Mars":{1,8,10},"Venus":{2,7,12}}  # own signs + exaltation sign

def geo(s):
    m=re.match(r'^(\d+)([NSEW])\s*(\d*)$',s.strip())
    d=int(m.group(1))+ (int(m.group(3) or 0))/60.0
    return -d if m.group(2) in "SW" else d

def load(path):
    t=open(path,encoding='utf-8',errors='replace').read()
    body=re.search(r'<pre>(.*?)</pre>',t,re.S).group(1)
    out=[]
    for l in body.split('\n'):
        p=l.split('\t')
        if len(p)<13 or not p[0].strip().isdigit(): continue
        yea,mon,day,pro,num,cou,h,mn,sec,tz=p[:10]; lat,lon=p[10],p[11]
        try:
            d=dt.datetime(int(yea),int(mon),int(day),int(h),int(mn),int(sec),
                          tzinfo=dt.timezone(dt.timedelta(hours=int(tz)))).astimezone(dt.timezone.utc)
            out.append((d,geo(lat),geo(lon)))
        except Exception: pass
    return sorted(out)

def features(d,lat,lon):
    ds,ts=d.strftime("%Y-%m-%d"),d.strftime("%H:%M")
    c=build_chart(ds,ts,lat,lon,"UTC")
    s=shadbala(ds,ts,lat,lon,tz_off=0.0)["planets"]
    lag=c["lagna"]["rashi"]; P=c["planets"]
    h=lambda p:(P[p]["rashi"]-lag)%12+1
    return {"mars":s["Mars"]["ratio"],"ven":s["Venus"]["ratio"],
            "mars_h":h("Mars"),"ven_h":h("Venus"),
            "mars_own":P["Mars"]["rashi"] in OWN["Mars"],"ven_own":P["Venus"]["rashi"] in OWN["Venus"],
            "l10":LORD[(lag+9-1)%12+1],"m10":LORD[(P["Moon"]["rashi"]+9-1)%12+1]}

def main():
    raw="/home/claude/g5data/g5/data/raw/gauq/lerrcp/"
    mil=load(raw+"902gdA3y.html"); pai=load(raw+"902gdA4y.html")
    print("military",len(mil),"painters",len(pai))
    used=set(); pairs=[]
    for d,lat,lon in mil:
        best=bd=None
        for j,(d2,la2,lo2) in enumerate(pai):
            if j in used: continue
            dd=abs((d2-d).days)
            if bd is None or dd<bd: bd,best=dd,j
        if best is not None and bd<=730: used.add(best); pairs.append(((d,lat,lon),pai[best]))
    print("pairs:",len(pairs))
    F=[(features(*a),features(*b)) for a,b in pairs]
    def test(name,call):
        n=hit=0
        for fa,fb in F:
            v=call(fa,fb)
            if v is None: continue
            n+=1; hit+=v
        if n==0: print(f"{name:9s} no calls"); return
        acc=hit/n; z=(hit-n/2)/(n**0.5/2); p=2*(1-NormalDist().cdf(abs(z)))
        print(f"{name:9s} {hit:4d}/{n:4d} = {acc*100:5.1f}%   p={p:.2e}")
    K={1,4,7,10}
    t1=lambda a,b: a["mars"]>b["mars"] if a["mars"]!=b["mars"] else None
    t2=lambda a,b: a["ven"]<b["ven"] if a["ven"]!=b["ven"] else None
    test("R1_mars",t1)
    test("R2_venus",t2)
    test("R3_marsK", lambda a,b: ((a["mars_h"] in K)>(b["mars_h"] in K)) if (a["mars_h"] in K)!=(b["mars_h"] in K) else t1(a,b))
    test("R4_venK",  lambda a,b: ((a["ven_h"] in K)<(b["ven_h"] in K)) if (a["ven_h"] in K)!=(b["ven_h"] in K) else t2(a,b))
    def r56(key):
        def f(a,b):
            sa=1 if a[key]=="Mars" else (-1 if a[key]=="Venus" else 0)
            sb=1 if b[key]=="Mars" else (-1 if b[key]=="Venus" else 0)
            return None if sa==sb else sa>sb
        return f
    test("R5_10L",r56("l10")); test("R6_10Lmoon",r56("m10"))
    def r7(a,b):
        sa=(1 if a["mars_own"] else 0)-(1 if a["ven_own"] else 0)
        sb=(1 if b["mars_own"] else 0)-(1 if b["ven_own"] else 0)
        return None if sa==sb else sa>sb
    test("R7_dign",r7)
    test("R8_comb", lambda a,b: (a["mars"]-a["ven"])>(b["mars"]-b["ven"]))
if __name__=="__main__": main()
