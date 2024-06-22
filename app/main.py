from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the API key and endpoint
API_KEY = "AIzaSyAk62M2KNZwk58OeUVsiUIwv4_EKwMkfIo"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# Define the request model
class RequestModel(BaseModel):
    text: str

# Define the response model
class ResponseModel(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.post("/generate-content", response_model=ResponseModel)
def generate_content(request: RequestModel):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": request.text
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()
        generated_text = json_response["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=response.status_code, detail=str(e))

    return ResponseModel(text=generated_text)




# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
