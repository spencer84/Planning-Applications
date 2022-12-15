from fastapi import FastAPI
from starlette.responses import FileResponse 
from dbconnect import dbconnect
import datetime

app = FastAPI()

# Connect to database
conn = dbconnect()


@app.get("/")
async def read_index():
    return FileResponse('./templates/index.html')

@app.get("/decided-last-week")
def weekly_list():
    """Return a list of weekly planning applications"""
    cur = conn.cursor
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    cur.execute(f"""SELECT * FROM applications WHERE DecisionDate >= {last_week.strftime("%Y/%m/%d")}""")
    results = cur.fetchall()
    return results

