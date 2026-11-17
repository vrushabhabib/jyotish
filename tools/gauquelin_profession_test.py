"""Gauquelin profession test. Rules fixed in docs/gauquelin/PRE-STATED-RULES.md BEFORE this ran.
Pairs each A1 sportsman with the unused A2 scientist born nearest in time (<=730 days), by date alone;
then asks each rule which of the two is the sportsman."""
import csv, sys, datetime as dt
from statistics import NormalDist
from engine.chart import build_chart
from engine.shadbala import shadbala

LORD = {1:"Mars",2:"Venus",3:"Mercury",4:"Moon",5:"Sun",6:"Mercury",7:"Venus",8:"Mars",9:"Jupiter",10:"Saturn",11:"Saturn",12:"Jupiter"}

def load(path):
    out=[]
    for r in csv.DictReader(open(path,encoding="utf-8",errors="replace")):
        try:
            d=dt.datetime.fromisoformat(r["DATE"]).astimezone(dt.timezone.utc)
            out.append((d,float(r["LAT"]),float(r["LON"]),r["NUM"]))
        except Exception: pass
    return out

def features(d,lat,lon):
    ds,ts=d.strftime("%Y-%m-%d"),d.strftime("%H:%M")
    c=build_chart(ds,ts,lat,lon,"UTC")
    s=shadbala(ds,ts,lat,lon,tz_off=0.0)["planets"]
    lag=c["lagna"]["rashi"]; P=c["planets"]
    h=lambda p:(P[p]["rashi"]-lag)%12+1
    moon=P["Moon"]["rashi"]
    return {"mars":s["Mars"]["ratio"],"merc":s["Mercury"]["ratio"],"jup":s["Jupiter"]["ratio"],
            "mars_h":h("Mars"),"l10":LORD[(lag+9-1)%12+1],"m10":LORD[(moon+9-1)%12+1]}

def main():
    g5="/home/claude/g5data/g5/data/db/init/lerrcp-marked/"
    sp=sorted(load(g5+"A1.csv")); sc=sorted(load(g5+"A2.csv"))
    used=set(); pairs=[]
    for d,lat,lon,num in sp:
        best=None;bd=None
        for j,(d2,lat2,lon2,n2) in enumerate(sc):
            if j in used: continue
            dd=abs((d2-d).days)
            if bd is None or dd<bd: bd, best = dd, j
        if best is not None and bd<=730:
            used.add(best); pairs.append(((d,lat,lon),sc[best][:3]))
    print("pairs:",len(pairs))
    F=[(features(*a),features(*b)) for a,b in pairs]
    def test(name,call):
        n=hit=0
        for fa,fb in F:
            v=call(fa,fb)
            if v is None: continue
            n+=1; hit+=1 if v else 0
        if n==0: print(f"{name:8s} no calls"); return
        acc=hit/n; z=(hit-n/2)/ (n**0.5/2); p=2*(1-NormalDist().cdf(abs(z)))
        print(f"{name:8s} {hit:4d}/{n:4d} = {acc*100:5.1f}%   p={p:.4f}")
    kend={1,4,7,10}; gz={12,9}
    def tie(fa,fb): return fa["mars"]>fb["mars"] if fa["mars"]!=fb["mars"] else None
    test("R1_mars", lambda a,b: a["mars"]>b["mars"] if a["mars"]!=b["mars"] else None)
    test("R2_kendra", lambda a,b: ((a["mars_h"] in kend)>(b["mars_h"] in kend)) if (a["mars_h"] in kend)!=(b["mars_h"] in kend) else tie(a,b))
    test("R3_gzone", lambda a,b: ((a["mars_h"] in gz)>(b["mars_h"] in gz)) if (a["mars_h"] in gz)!=(b["mars_h"] in gz) else tie(a,b))
    test("R4_merc", lambda a,b: a["merc"]<b["merc"] if a["merc"]!=b["merc"] else None)
    test("R5_jup",  lambda a,b: a["jup"]<b["jup"] if a["jup"]!=b["jup"] else None)
    def r67(key):
        def f(a,b):
            sa=1 if a[key]=="Mars" else (-1 if a[key] in ("Mercury","Jupiter") else 0)
            sb=1 if b[key]=="Mars" else (-1 if b[key] in ("Mercury","Jupiter") else 0)
            if sa==sb: return None
            return sa>sb
        return f
    test("R6_10L", r67("l10")); test("R7_10Lmoon", r67("m10"))
    test("R8_comb", lambda a,b: (a["mars"]-max(a["merc"],a["jup"]))>(b["mars"]-max(b["merc"],b["jup"])))
    # raw Gauquelin key-sector count, descriptive only
    gs=sum(1 for fa,_ in F if fa["mars_h"] in gz); gn=sum(1 for _,fb in F if fb["mars_h"] in gz)
    print(f"Mars in 12th/9th whole-sign: sportsmen {gs}/{len(F)} ({gs/len(F)*100:.1f}%)  scientists {gn}/{len(F)} ({gn/len(F)*100:.1f}%)  base 2/12=16.7%")
if __name__=="__main__": main()
