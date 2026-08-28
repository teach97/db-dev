import hashlib
import json
import sys
import time
import urllib.request

from app.redis_client import r

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000"
TOKEN = "eyJhbGciOiJFUzI1NiIsImtpZCI6ImIyMzk3NTlkLTA0ZDQtNDVkMy04MzNjLTFiYzlkNDI3MzczNSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3B1a2dsdmdycHB1aXR4bGxzb21pLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJlNTAxNDlmOC1hNTZmLTRiMGItOTc1NS1kNTgyYTc5MjM2Y2IiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg3ODE1NTUwLCJpYXQiOjE3ODc4MTE5NTAsImVtYWlsIjoidGVzdC1hdXRoLTAxQGV4YW1wbGUuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6InRlc3QtYXV0aC0wMUBleGFtcGxlLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6ImU1MDE0OWY4LWE1NmYtNGIwYi05NzU1LWQ1ODJhNzkyMzZjYiJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzg3ODExOTUwfV0sInNlc3Npb25faWQiOiIyMzU3N2U2Mi1hODFmLTRkMmQtOTk2MC1iZjAxYmU5NDhlN2YiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.57RRHoD_6flwcQGu0fwbwqt_3JJR5970Q1Cww-LD5Y_NOZAJhxKXlFw4MqBSCRrXHb2quWSfQecRxm8RWR0i-Q"
CONVERSATION_ID = "e50149f8-a56f-4b0b-9755-d582a79236cb"


def call(path):
    req = urllib.request.Request(BASE + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    started = time.perf_counter()
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
    return body, (time.perf_counter() - started) * 1000


def measure(path, cache_key, times=3):
    """캐시를 비우고 같은 요청을 여러 번 보낸다."""
    r.delete(cache_key)          # 1회차가 확실히 MISS 가 되게 한다
    print(f"\n{path}")
    for i in range(1, times + 1):
        body, ms = call(path)
        count = len(body) if isinstance(body, list) else "-"
        print(f"  {i}회차  {ms:7.1f} ms  {count}건  남은 TTL {r.ttl(cache_key):>4}s")


# measure("/me", "session:" + hashlib.sha256(TOKEN.encode()).hexdigest())

measure(f"/conversations/{CONVERSATION_ID}/messages", f"messages:{CONVERSATION_ID}")