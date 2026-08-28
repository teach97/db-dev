
# read_token.py
import base64
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

token = "eyJhbGciOiJFUzI1NiIsImtpZCI6ImIyMzk3NTlkLTA0ZDQtNDVkMy04MzNjLTFiYzlkNDI3MzczNSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3B1a2dsdmdycHB1aXR4bGxzb21pLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI5NTZkZmVmZS1lOTM5LTQyZGItYTFkYy05YzMwZTI1N2Q2MDIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg3NzEwMzk2LCJpYXQiOjE3ODc3MDY3OTYsImVtYWlsIjoicmxzLWJAZXhhbXBsZS5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoicmxzLWJAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiI5NTZkZmVmZS1lOTM5LTQyZGItYTFkYy05YzMwZTI1N2Q2MDIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc4NzcwNjc5Nn1dLCJzZXNzaW9uX2lkIjoiNGE3ZGFmMzUtZGQyOS00OGYwLWI3M2ItOTFkZGVlYTA1ZTljIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.3mGdfqvme0wvkixYEHDywXFRKMygeVBz5s-jPBGP0xH8WDVkHtasEHuR1nFk058mRDGjJjSk5TteRjY5NvU51Q"

payload = token.split(".")[1]
payload += "=" * (-len(payload) % 4)   # base64 는 길이가 4의 배수여야 한다

print(json.dumps(json.loads(base64.urlsafe_b64decode(payload)), indent=2, ensure_ascii=False))

{
  "iss": "https://pukglvgrppuitxllsomi.supabase.co/auth/v1",
  "sub": "956dfefe-e939-42db-a1dc-9c30e257d602",
  "aud": "authenticated",
  "exp": 1787710396,
  "iat": 1787706796,
  "email": "rls-b@example.com",
  "phone": "",
  "app_metadata": {
    "provider": "email",
    "providers": [
      "email"
    ]
  },
  "user_metadata": {
    "email": "rls-b@example.com",
    "email_verified": true,
    "phone_verified": false,
    "sub": "956dfefe-e939-42db-a1dc-9c30e257d602"
  },
  "role": "authenticated",
  "aal": "aal1",
  "amr": [
    {
      "method": "password",
      "timestamp": 1787706796
    }
  ],
  "session_id": "4a7daf35-dd29-48f0-b73b-91ddeea05e9c",
  "is_anonymous": false
}