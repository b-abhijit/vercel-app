from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json, math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = [
  {"region":"apac","service":"recommendations","latency_ms":173.04,"uptime_pct":98.624,"timestamp":20250301},
  {"region":"apac","service":"catalog","latency_ms":157.9,"uptime_pct":98.594,"timestamp":20250302},
  {"region":"apac","service":"payments","latency_ms":123.25,"uptime_pct":97.848,"timestamp":20250303},
  {"region":"apac","service":"recommendations","latency_ms":177.39,"uptime_pct":98.426,"timestamp":20250304},
  {"region":"apac","service":"catalog","latency_ms":205.19,"uptime_pct":99.253,"timestamp":20250305},
  {"region":"apac","service":"analytics","latency_ms":155.96,"uptime_pct":97.188,"timestamp":20250306},
  {"region":"apac","service":"recommendations","latency_ms":170.81,"uptime_pct":97.491,"timestamp":20250307},
  {"region":"apac","service":"payments","latency_ms":226.51,"uptime_pct":98.419,"timestamp":20250308},
  {"region":"apac","service":"catalog","latency_ms":185.52,"uptime_pct":97.789,"timestamp":20250309},
  {"region":"apac","service":"checkout","latency_ms":134.64,"uptime_pct":97.881,"timestamp":20250310},
  {"region":"apac","service":"analytics","latency_ms":161.54,"uptime_pct":97.815,"timestamp":20250311},
  {"region":"apac","service":"catalog","latency_ms":206.24,"uptime_pct":99.123,"timestamp":20250312},
  {"region":"emea","service":"recommendations","latency_ms":141.83,"uptime_pct":98.014,"timestamp":20250301},
  {"region":"emea","service":"checkout","latency_ms":214.33,"uptime_pct":98.256,"timestamp":20250302},
  {"region":"emea","service":"catalog","latency_ms":219.4,"uptime_pct":98.225,"timestamp":20250303},
  {"region":"emea","service":"catalog","latency_ms":153.45,"uptime_pct":97.277,"timestamp":20250304},
  {"region":"emea","service":"support","latency_ms":220.35,"uptime_pct":98.756,"timestamp":20250305},
  {"region":"emea","service":"analytics","latency_ms":121.78,"uptime_pct":97.458,"timestamp":20250306},
  {"region":"emea","service":"recommendations","latency_ms":229.69,"uptime_pct":97.488,"timestamp":20250307},
  {"region":"emea","service":"checkout","latency_ms":139.96,"uptime_pct":97.459,"timestamp":20250308},
  {"region":"emea","service":"catalog","latency_ms":178.6,"uptime_pct":97.726,"timestamp":20250309},
  {"region":"emea","service":"analytics","latency_ms":114.46,"uptime_pct":99.068,"timestamp":20250310},
  {"region":"emea","service":"recommendations","latency_ms":178.74,"uptime_pct":99.376,"timestamp":20250311},
  {"region":"emea","service":"catalog","latency_ms":146.63,"uptime_pct":98.735,"timestamp":20250312},
  {"region":"amer","service":"support","latency_ms":196.95,"uptime_pct":97.591,"timestamp":20250301},
  {"region":"amer","service":"payments","latency_ms":170.9,"uptime_pct":97.418,"timestamp":20250302},
  {"region":"amer","service":"analytics","latency_ms":178.4,"uptime_pct":97.822,"timestamp":20250303},
  {"region":"amer","service":"checkout","latency_ms":142.52,"uptime_pct":97.863,"timestamp":20250304},
  {"region":"amer","service":"support","latency_ms":121.92,"uptime_pct":97.301,"timestamp":20250305},
  {"region":"amer","service":"checkout","latency_ms":152.33,"uptime_pct":97.973,"timestamp":20250306},
  {"region":"amer","service":"catalog","latency_ms":146.81,"uptime_pct":97.165,"timestamp":20250307},
  {"region":"amer","service":"analytics","latency_ms":137.16,"uptime_pct":99.181,"timestamp":20250308},
  {"region":"amer","service":"recommendations","latency_ms":137.62,"uptime_pct":97.983,"timestamp":20250309},
  {"region":"amer","service":"payments","latency_ms":216.61,"uptime_pct":99.067,"timestamp":20250310},
  {"region":"amer","service":"support","latency_ms":207.45,"uptime_pct":98.282,"timestamp":20250311},
  {"region":"amer","service":"analytics","latency_ms":211.99,"uptime_pct":98.336,"timestamp":20250312},
]

class Query(BaseModel):
    regions: List[str]
    threshold_ms: float

def percentile(data, p):
    s = sorted(data)
    n = len(s)
    if n == 0:
        return 0
    idx = (p/100) * (n-1)
    lo, hi = int(idx), min(int(idx)+1, n-1)
    return s[lo] + (idx - lo) * (s[hi] - s[lo])

@app.post("/")
def analyze(q: Query):
    result = {}
    for region in q.regions:
        rows = [r for r in DATA if r["region"] == region]
        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]
        result[region] = {
            "avg_latency": round(sum(latencies)/len(latencies), 2) if latencies else 0,
            "p95_latency": round(percentile(latencies, 95), 2) if latencies else 0,
            "avg_uptime": round(sum(uptimes)/len(uptimes), 2) if uptimes else 0,
            "breaches": sum(1 for l in latencies if l > q.threshold_ms),
        }
    return result

@app.get("/")
def root():
    return {"status": "ok"}
