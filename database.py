import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

load_dotenv(".env")
#DETA_KEY = os.getenv("DETA_KEY")
DETA_KEY = st.secrets["DETA_KEY"] #<---This for st cloud

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("monthly_reports")

def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)

app = FastAPI()

photos = deta.Drive("images") # access to your drive

def photos_upload(file, data):
    fn =file.name
    path = os.path.abspath(fn) #<------return full path: C:\Users\ericn\PycharmProjects\MyAPP124\SingleBH.png
    return photos.put(fn, data) #<---------HAS TO FIT IN BYTES_DATA TO GENERATE IMAGE DATA!!

def fetch_notes(fn):
    res = photos.get(fn)
    return res

def list_files():
    res = photos.list()
    return res.get("names")
    # st.markdown(db.render(), unsafe_allow_html=True)
    #
    # st.text(db.app.post("/upload"))
    #db.upload_img(file)

# @app.get("/", response_class=HTMLResponse)
# def render():
#     return """
#     <form action="/upload" enctype="multipart/form-data" method="post">
#         <input name="file" type="file">
#         <input type="submit">
#     </form>
#     """
# @app.post("/upload")
# def upload_img(file: UploadFile = File(...)):
#     name = file.filename
#     f = file.file
#     res = drive.put(name, f)
#     return res

#@app.post("/upload")
# def upload_img(file, bytedata):
#     name = file.name
#     f = bytedata
#     res = db.put(name, f)
#     return res

#@app.get("/download/{name}")
# def download_img(name: str):
#     res = db.get(name)
#     return StreamingResponse(res.iter_chunks(1024), media_type="image/png")