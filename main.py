from fastapi import FastAPI, Query
import aiohttp
import asyncio

app = FastAPI()

@app.get("/token")
async def get_jwt_token(uid: str = Query(...), password: str = Query(...)):
    oauth_url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    payload = {
        'uid': uid,
        'password': password,
        'response_type': "token",
        'client_type': "2",
        'client_secret': "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        'client_id': "100067"
    }
    headers = {'User-Agent': "GarenaMSDK/4.0.19P9"}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(oauth_url, data=payload, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    access_token = data.get('access_token')
                    if access_token:
                        return {"status": "success", "token": access_token}
                return {"status": "error", "message": "Failed to authenticate with Garena"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    return {"message": "JWT Token Generator Service is Running!"}