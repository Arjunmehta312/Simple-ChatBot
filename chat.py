from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Enable CORS for your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://icy-river-0f21cad0f.4.azurestaticapps.net"],  # Frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files for serving CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template configuration
templates = Jinja2Templates(directory="templates")

# Azure AI Project setup
project_connection_string = "ADD_YOUR_PROJECT_CONNECTION_STRING_HERE" # Add your Azure AI Project connection string here
project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential()
)
chat = project.inference.get_chat_completions_client()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-response")
async def generate_response(request: Request):
    data = await request.json()
    first_name = data.get("first_name", "User")
    last_name = data.get("last_name", "")
    user_message = data.get("message", "")

    # Create system prompt
    system_prompt = f"""
    You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig? 
    Refer to the user by their first name, try to work their last name into a pun.

    The user's first name is {first_name} and their last name is {last_name}.
    """
    
    # Get AI response
    response = chat.complete(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    ai_response = response.choices[0].message.content

    return JSONResponse({"response": ai_response})
