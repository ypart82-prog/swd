from fastapi import FastAPI, HTTPException, Query
import aiohttp
import asyncio

app = FastAPI()

GARENA_AUTH_URL = "https://auth.garena.com/oauth/login"
GAME_JWT_URL = "https://client-api.us.freefiremobile.com/oauth/garena" # প্রয়োজন অনুযায়ী অঞ্চল/রিজন URL আপডেট করতে পারেন

@app.get("/")
def home():
    return {"message": "JWT Token Generator Service is Running!"}

@app.get("/token")
async def generate_token(
    uid: str = Query(..., description="User ID"),
    password: str = Query(..., description="Password")
):
    async with aiohttp.ClientSession() as session:
        # Step 1: Get Access Token from Garena
        auth_payload = {
            "account": uid,
            "password": password,
            "app_id": 100067,  # Free Fire App ID
            "grant_type": "password"
        }
        
        async with session.post(GARENA_AUTH_URL, data=auth_payload, timeout=10) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=400, detail="Garena Auth Failed")
            
            data = await resp.json()
            access_token = data.get("access_token")
            if not access_token:
                raise HTTPException(status_code=400, detail="Failed to retrieve access_token")

        # Step 2: Exchange Access Token for Game JWT Token
        jwt_payload = {
            "access_token": access_token,
            "app_id": 100067
        }
        
        async with session.post(GAME_JWT_URL, json=jwt_payload, timeout=10) as jwt_resp:
            if jwt_resp.status == 200:
                jwt_data = await jwt_resp.json()
                jwt_token = jwt_data.get("token") or jwt_data.get("jwt") or jwt_data.get("access_token")
                
                if jwt_token:
                    return {
                        "status": "success",
                        "token": jwt_token
                    }
            
            # Fallback in case exchange fails, return direct access_token
            return {
                "status": "success",
                "token": access_token
            }
