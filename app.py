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
  # Parámetros obligatorios/opcionales
  query = request.args.get("query", "")
  if not query:
    return jsonify(error="missing query"), 400

  count = request.args.get("count", "3")       # tamaño de página
  start = request.args.get("start", "0")       # desplazamiento (paginación)
  sort  = request.args.get("sort")             # ej: relevancy, citedby-count, coverDate:desc
  override_api_key = request.args.get("apiKey") # opcional: sobrescribir la key por query

  # Construye parámetros de Scopus
  params = {
    "query": query,
    "count": count,
    "start": start,
    "httpAccept": "application/json",
  }
  if sort:
    params["sort"] = sort

  # Cabeceras (puedes forzar JSON y un UA reconocible)
  headers = {
    "X-ELS-APIKey": override_api_key.strip() if override_api_key else ELS,
    "Accept": "application/json",
    "User-Agent": "RefCheckerGPT/1.1"
  }

  # Llamada a Elsevier Scopus
  r = requests.get(
    "https://api.elsevier.com/content/search/scopus",
    params=params,
    headers=headers,
    timeout=30
  )

  # Devuelve tal cual (status + cuerpo + content-type)
  return Response(
    r.content,
    status=r.status_code,
    content_type=r.headers.get("Content-Type", "application/json")
  )

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)