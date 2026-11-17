"""Feature search with sealed holdout. Procedure: docs/gauquelin/PRE-STATED-SEARCH.md (pushed first)."""
import csv, re, datetime as dt
from statistics import NormalDist
from engine.chart import build_chart
from engine.shadbala import shadbala

ND=NormalDist()
def geo(s):
    m=re.match(r'^(\d+)([NSEW])\s*(\d*)$',s.strip())
    d=int(m.group(1))+(int(m.group(3) or 0))/60.0
    return -d if m.group(2) in "SW" else d
def load_html(path):
    body=re.search(r'<pre>(.*?)</pre>',open(path,encoding='utf-8',errors='replace').read(),re.S).group(1)
    out=[]
    for l in body.split('\n'):
        p=l.split('\t')
        if len(p)<13 or not p[0].strip().isdigit(): continue
        try:
            d=dt.datetime(int(p[0]),int(p[1]),int(p[2]),int(p[6]),int(p[7]),int(p[8]),
                          tzinfo=dt.timezone(dt.timedelta(hours=int(p[9])))).astimezone(dt.timezone.utc)
            out.append((d,geo(p[10]),geo(p[11])))
        except Exception: pass
    return sorted(out)
def load_csv(path):
    out=[]
    for r in csv.DictReader(open(path,encoding='utf-8',errors='replace')):
        try:
            d=dt.datetime.fromisoformat(r["DATE"]).astimezone(dt.timezone.utc)
            out.append((d,float(r["LAT"]),float(r["LON"])))
        except Exception: pass
    return sorted(out)
def match(g1,g2):
    used=set(); pairs=[]
    for a in g1:
        best=bd=None
        for j,b in enumerate(g2):
            if j in used: continue
            dd=abs((b[0]-a[0]).days)
            if bd is None or dd<bd: bd,best=dd,j
        if best is not None and bd<=730: used.add(best); pairs.append((a,g2[best]))
    return pairs
PL=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]
SB=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
K={1,4,7,10}; T={1,5,9}; D={6,8,12}
def features(d,lat,lon):
    ds,ts=d.strftime("%Y-%m-%d"),d.strftime("%H:%M")
    c=build_chart(ds,ts,lat,lon,"UTC"); s=shadbala(ds,ts,lat,lon,tz_off=0.0)["planets"]
    lag=c["lagna"]["rashi"]; P=c["planets"]; moon=P["Moon"]["rashi"]
    f={}
    for p in PL:
        h=(P[p]["rashi"]-lag)%12+1; hm=(P[p]["rashi"]-moon)%12+1
        for i in range(1,13): f[f"{p}_h{i}"]= (h==i)
        f[f"{p}_kendra"]=h in K; f[f"{p}_trikona"]=h in T; f[f"{p}_dusthana"]=h in D
        f[f"{p}_moonK"]=hm in K
        f[f"{p}_retro"]=bool(P[p].get("retro")); f[f"{p}_comb"]=bool(P[p].get("combust"))
    for p in SB: f[f"{p}_sb"]=s[p]["ratio"]
    for i in range(1,13): f[f"lagna_{i}"]=(lag==i); f[f"moon_{i}"]=(moon==i)
    return f
def paired_stat(F,key):
    n=hit=0
    for fa,fb in F:
        a,b=fa[key],fb[key]
        if isinstance(a,bool):
            if a==b: continue
            n+=1; hit+=1 if a and not b else 0
        else:
            if a==b: continue
            n+=1; hit+=1 if a>b else 0
    if n==0: return 0,0,1.0
    z=(hit-n/2)/(n**0.5/2); p=2*(1-ND.cdf(abs(z)))
    return hit,n,p
def run(name,pairs):
    F=[(features(*a),features(*b)) for a,b in pairs]
    train=[F[i] for i in range(0,len(F),2)]; hold=[F[i] for i in range(1,len(F),2)]
    keys=sorted(F[0][0].keys())
    print(f"== {name}: {len(pairs)} pairs ({len(train)} train, {len(hold)} holdout), {len(keys)} features")
    surv=[]
    for k in keys:
        h,n,p=paired_stat(train,k)
        if p<0.001 and n>=50: surv.append((k,h,n,p,h>n/2))
    print("training survivors at p<0.001 (chance expects ~%.1f):"%(len(keys)*0.001), len(surv))
    for k,h,n,p,d in surv:
        h2,n2,p2=paired_stat(hold,k)
        same=(h2>n2/2)==d; acc=h2/n2 if n2 else 0
        ok=same and p2<0.01 and n2>=100 and max(acc,1-acc)>=0.53
        print(f"  {k:16s} train {h}/{n} p={p:.1e} | holdout {h2}/{n2}={acc*100:.1f}% p={p2:.2e} {'CONFIRMED' if ok else 'fails holdout'}")
    if not surv: print("  (none)")
def main():
    g5="/home/claude/g5data/g5/data/"
    run("sport-vs-science", match(load_csv(g5+"db/init/lerrcp-marked/A1.csv"),load_csv(g5+"db/init/lerrcp-marked/A2.csv")))
    run("military-vs-painters", match(load_html(g5+"raw/gauq/lerrcp/902gdA3y.html"),load_html(g5+"raw/gauq/lerrcp/902gdA4y.html")))
if __name__=="__main__": main()
