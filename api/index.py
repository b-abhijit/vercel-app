from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

DATA = [
  {"region":"apac","service":"recommendations","latency_ms":173.04,"uptime_pct":98.624},
  {"region":"apac","service":"catalog","latency_ms":157.9,"uptime_pct":98.594},
  {"region":"apac","service":"payments","latency_ms":123.25,"uptime_pct":97.848},
  {"region":"apac","service":"recommendations","latency_ms":177.39,"uptime_pct":98.426},
  {"region":"apac","service":"catalog","latency_ms":205.19,"uptime_pct":99.253},
  {"region":"apac","service":"analytics","latency_ms":155.96,"uptime_pct":97.188},
  {"region":"apac","service":"recommendations","latency_ms":170.81,"uptime_pct":97.491},
  {"region":"apac","service":"payments","latency_ms":226.51,"uptime_pct":98.419},
  {"region":"apac","service":"catalog","latency_ms":185.52,"uptime_pct":97.789},
  {"region":"apac","service":"checkout","latency_ms":134.64,"uptime_pct":97.881},
  {"region":"apac","service":"analytics","latency_ms":161.54,"uptime_pct":97.815},
  {"region":"apac","service":"catalog","latency_ms":206.24,"uptime_pct":99.123},
  {"region":"emea","service":"recommendations","latency_ms":141.83,"uptime_pct":98.014},
  {"region":"emea","service":"checkout","latency_ms":214.33,"uptime_pct":98.256},
  {"region":"emea","service":"catalog","latency_ms":219.4,"uptime_pct":98.225},
  {"region":"emea","service":"catalog","latency_ms":153.45,"uptime_pct":97.277},
  {"region":"emea","service":"support","latency_ms":220.35,"uptime_pct":98.756},
  {"region":"emea","service":"analytics","latency_ms":121.78,"uptime_pct":97.458},
  {"region":"emea","service":"recommendations","latency_ms":229.69,"uptime_pct":97.488},
  {"region":"emea","service":"checkout","latency_ms":139.96,"uptime_pct":97.459},
  {"region":"emea","service":"catalog","latency_ms":178.6,"uptime_pct":97.726},
  {"region":"emea","service":"analytics","latency_ms":114.46,"uptime_pct":99.068},
  {"region":"emea","service":"recommendations","latency_ms":178.74,"uptime_pct":99.376},
  {"region":"emea","service":"catalog","latency_ms":146.63,"uptime_pct":98.735},
  {"region":"amer","service":"support","latency_ms":196.95,"uptime_pct":97.591},
  {"region":"amer","service":"payments","latency_ms":170.9,"uptime_pct":97.418},
  {"region":"amer","service":"analytics","latency_ms":178.4,"uptime_pct":97.822},
  {"region":"amer","service":"checkout","latency_ms":142.52,"uptime_pct":97.863},
  {"region":"amer","service":"support","latency_ms":121.92,"uptime_pct":97.301},
  {"region":"amer","service":"checkout","latency_ms":152.33,"uptime_pct":97.973},
  {"region":"amer","service":"catalog","latency_ms":146.81,"uptime_pct":97.165},
  {"region":"amer","service":"analytics","latency_ms":137.16,"uptime_pct":99.181},
  {"region":"amer","service":"recommendations","latency_ms":137.62,"uptime_pct":97.983},
  {"region":"amer","service":"payments","latency_ms":216.61,"uptime_pct":99.067},
  {"region":"amer","service":"support","latency_ms":207.45,"uptime_pct":98.282},
  {"region":"amer","service":"analytics","latency_ms":211.99,"uptime_pct":98.336},
]

H = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

class Query(BaseModel):
    regions: List[str]
    threshold_ms: float

def p95(data):
    s = sorted(data)
    n = len(s)
    if n == 0: return 0
    idx = 0.95 * (n-1)
    lo, hi = int(idx), min(int(idx)+1, n-1)
    return s[lo] + (idx - lo) * (s[hi] - s[lo])

@app.options("/")
async def options():
    return JSONResponse({}, headers=H)

@app.post("/")
async def analyze(q: Query):
    result = {}
    for region in q.regions:
        rows = [r for r in DATA if r["region"] == region]
        lat = [r["latency_ms"] for r in rows]
        upt = [r["uptime_pct"] for r in rows]
        result[region] = {
            "avg_latency": round(sum(lat)/len(lat), 2) if lat else 0,
            "p95_latency": round(p95(lat), 2) if lat else 0,
            "avg_uptime": round(sum(upt)/len(upt), 2) if upt else 0,
            "breaches": sum(1 for l in lat if l > q.threshold_ms),
        }
    return JSONResponse({"regions": result}, headers=H)

@app.get("/")
async def root():
    return JSONResponse({"status": "ok"}, headers=H)\

@app.post("/api/latency")
async def analyze_latency(q: Query):
    return await analyze(None, q)
