#!/usr/bin/python3
# _common toolkit (Blaque Baux inversion sleeve) — Alpaca SIP daily (adjustment=all → total return). Read-only.
import os, json, urllib.request, math
import numpy as np
H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2016-01-01", "2026-08-01"
_cache = {}
def bars(s):
    if s in _cache: return _cache[s]
    u=(f"https://data.alpaca.markets/v2/stocks/bars?symbols={s}&timeframe=1Day&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=40))
        _cache[s]={b["t"][:10]:(b["o"],b["h"],b["l"],b["c"]) for b in d.get("bars",{}).get(s,[])}
    except Exception: _cache[s]={}
    return _cache[s]
def panel(syms):
    D={s:bars(s) for s in syms}; D={s:v for s,v in D.items() if len(v)>250}
    if not D: return {},{},[]
    u=[s for s in syms if s in D]; dates=sorted(set.intersection(*[set(D[s]) for s in u]))
    C={s:np.array([D[s][d][3] for d in dates],float) for s in u}
    O={s:np.array([D[s][d][0] for d in dates],float) for s in u}
    return C,O,dates
def rets(px): return px[1:]/px[:-1]-1
def stats(r):
    r=np.asarray(r,float); r=r[np.isfinite(r)]
    if len(r)<20 or r.std()==0: return dict(sh=float("nan"),cagr=float("nan"),dd=float("nan"),vol=float("nan"))
    cum=np.cumprod(1+r)
    return dict(sh=r.mean()/r.std()*math.sqrt(252),cagr=cum[-1]**(252/len(r))-1,dd=float((cum/np.maximum.accumulate(cum)-1).min()),vol=r.std()*math.sqrt(252))
def skew_of(r):
    r=np.asarray(r,float); r=r[np.isfinite(r)]
    if len(r)<20 or r.std()==0: return float("nan")
    z=(r-r.mean())/r.std(); return float(np.mean(z**3))
def corr(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float); m=np.isfinite(a)&np.isfinite(b)
    return float(np.corrcoef(a[m],b[m])[0,1]) if m.sum()>30 else float("nan")
def roll(x,w):
    x=np.asarray(x,float); n=len(x); o=np.full(n,np.nan)
    for t in range(w,n): o[t]=x[t-w:t].sum()
    return o
