from fastapi import FastAPI, Form, Request
from starlette.responses import FileResponse, HTMLResponse 
from dbconnect import dbconnect
import datetime
import requests
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Connect to database
conn = dbconnect()

class Item(BaseModel):
    postcode: str

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse('./templates/index.html')

@app.get("/decided-last-week", response_class=HTMLResponse)
def weekly_list(request: Request):
    """Return a list of weekly planning applications -- decided in the last week"""
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    results = conn.queryJSON(f"""SELECT * FROM applications WHERE DecisionDate >= {last_week.strftime("%Y/%m/%d")}""")
    return templates.TemplateResponse("results.html", {"request": request, "results": results})



@app.get("/received-last-week")
def sub_weekly_list():
    """Return a list of weekly planning applications -- received in the last week"""
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    results = conn.queryJSON(f"""SELECT * FROM applications WHERE DateReceived >= {last_week.strftime("%Y/%m/%d")}""")
    return results

@app.post("/near-me/")
async def near_me(postcode: str = Form()):
    """Return a list of all postcodes near the inputed postcode"""
    results = requests.get(f"https://api.postcodes.io/postcodes/{postcode}/nearest")
    nearby = [x.get('postcode') for x in results.json()['result']]
    # Create a string of postcodes for the SQL query
    codes = "\'"
    for postcode in nearby:
        codes += postcode
        if postcode != nearby[-1]:
            codes += "\', \'"
    codes += '\''
    results = conn.queryJSON(f"""SELECT * FROM applications WHERE postcode in ({codes})""")
    if len(results['results']) == 0:
        return "There are no nearby planning applications"
    return results 