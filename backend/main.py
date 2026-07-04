from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware as CORS
import uvicorn
import socket
import httpx
from contextlib import asynccontextmanager


from api import (products,user,cart,inventory,orders,Authentication,address,health)
from tasks.email_task import send_welcome_email



@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.client = httpx.AsyncClient(timeout=10)
    yield
    await app.state.client.aclose()

app = FastAPI(
    title="E-Commerce Backend", lifespan=lifespan)

app.add_middleware(
    CORS,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(inventory.router)
app.include_router(Authentication.router)
app.include_router(address.router)
app.include_router(health.router)



@app.get("/ip")
async def get_ip(request: Request):
    # Get local IP address of the server
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return {
        "client_host": request.client.host,
        "server_local_ip": local_ip,
        "message": "Current system IP retrieved successfully"
    }

@app.post('/test')
async def test_task(email: str):
    try:
        print("Task is Being Queued")
        mail = send_welcome_email.delay(email)
        print("Task is Completed")
        return {"message" : f'success {mail.id} Status: {mail.status}'}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
#efkf krur sivv cflh
