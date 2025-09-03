import os
from flask import Flask, request, Response, jsonify
import requests

ELS = os.environ.get("ELS_API_KEY", "").strip()
assert ELS, "Falta variable de entorno ELS_API_KEY"

app = Flask(__name__)

@app.get("/health")
def health():
  return jsonify(status="ok")

@app.get("/scopus")
def scopus():
  query = request.args.get("query", "")
  if not query:
    return jsonify(error="missing query"), 400
  count = request.args.get("count", "3")

  params = {
    "query": query,
    "count": count,
    "httpAccept": "application/json",
  }
  r = requests.get(
    "https://api.elsevier.com/content/search/scopus",
    params=params,
    headers={
      "X-ELS-APIKey": ELS,
      "Accept": "application/json",
      "User-Agent": "RefCheckerGPT/1.0"
    },
    timeout=30
  )
  return Response(
    r.content,
    status=r.status_code,
    content_type=r.headers.get("Content-Type", "application/json")
  )

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
