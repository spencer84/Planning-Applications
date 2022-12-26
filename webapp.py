from fastapi import FastAPI
from starlette.responses import FileResponse 
from dbconnect import dbconnect
import datetime
import requests
from pydantic import BaseModel

app = FastAPI()

# Connect to database
conn = dbconnect()

class Item(BaseModel):
    postcode: str


@app.get("/")
async def read_index():
    return FileResponse('./templates/index.html')

@app.get("/decided-last-week")
def weekly_list():
    """Return a list of weekly planning applications -- decided in the last week"""
    cur = conn.cursor
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    cur.execute(f"""SELECT * FROM applications WHERE DecisionDate >= {last_week.strftime("%Y/%m/%d")}""")
    results = cur.fetchall()
    return results


@app.post("/near-me/")
async def near_me(item: Item):
    """Return a list of all postcodes near the inputed postcode"""
    results = requests.get(f"https://api.postcodes.io/postcodes/{item.postcode}/nearest")
    nearby = [x.get('postcode') for x in results.json()['result']]
    codes = "\'"
    for postcode in nearby:
        codes += postcode
        if postcode != nearby[-1]:
            codes += "\', \'"
    codes += '\''
    cur = conn.cursor
    print(codes)
    cur.execute(f"""SELECT * FROM applications WHERE postcode in ({codes})""")
    applications = cur.fetchall()
    return applications