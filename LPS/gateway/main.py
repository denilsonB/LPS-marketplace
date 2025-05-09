#uvicorn main:app --host 0.0.0.0 --port 8000
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import httpx

app = FastAPI()

# Dicionário com os serviços registrados e suas URLs
SERVICES = {
    "catalog": "http://localhost:8001",
    "cart": "http://localhost:8002",
    "order": "http://localhost:8003",
    "payment": "http://localhost:8004",
    "shipping": "http://localhost:8005",
    "recommendation": "http://localhost:8006",
}

@app.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        return JSONResponse(status_code=404, content={"error": f"Serviço '{service_name}' não encontrado. Use um desses: {', '.join(SERVICES.keys())}"})

    target_url = f"{SERVICES[service_name]}/{path}"

    if path.startswith(f"{service_name}/"):
        path = path[len(service_name)+1:]
    
    body = await request.body()

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={key: value for key, value in request.headers.items() if key.lower() != "host"},
                content=body,
                params=request.query_params,
            )
        except httpx.RequestError as e:
            return JSONResponse(status_code=503, content={"error": f"Erro ao contatar o serviço '{service_name}': {str(e)}"})

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type", "application/json")
    )