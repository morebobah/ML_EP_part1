from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})