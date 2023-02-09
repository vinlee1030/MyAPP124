import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
import os
from dotenv import load_dotenv
#from fastapi import FastAPI, File, UploadFile
#from fastapi.responses import HTMLResponse, StreamingResponse

load_dotenv(".env")
#DETA_KEY = os.getenv("DETA_KEY")
DETA_KEY = st.secrets["DETA_KEY"] #<---This for st cloud

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("monthly_reports")
nt = deta.Base("Notes")
def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

def insert_chart(date,chart):
    return nt.put(chart,date)

def fetch_all_chart():
    res = nt.fetch()
    return res.items
#     res = nt.fetch()
#     all_items = res.items

#     # fetch until last is 'None'
#     while res.last:
#         res = nt.fetch(last=res.last)
#         all_items += res.items
#     return all_items
def fetch_chart(fn):
    res = nt.fetch(fn)
    return res.items

def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)

#app = FastAPI()

photos = deta.Drive("images") # access to your drive

def photos_upload(fn, data):
    #fn =file.name
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

sc = deta.Base("Search_Cache")
def insert_cache(key, date):
    return sc.put({"key": key, "date": date})

def fetch_cache():
    res = sc.fetch()
    return res.items

quiz = deta.Base("Quiz_Log")
def insert_quiz(n_quiz, date, shuf_ques, shuf_ans,correct):
    return quiz.put({"key": n_quiz,"Date": date, "Question": shuf_ques, 'Ans': shuf_ans,'Correct':correct})
#,"Ques":question,"Ans":ans})#,question,ans):
def fetch_quiz():
    res = quiz.fetch()
    return res.items
def delete_quiz(key):
    res = quiz.delete(key)
    return res

nt_srch = deta.Base("WritingNotes") #<---------Can't have spaces in name!!!'

def insert_wnote(dt,subject,category,importance,comment,title):
    return nt_srch.put({"key": dt,"subject": subject, "category": category, 'importance':importance, "comment": comment, "title":title})
#"key" can be changed to anything for search
def fetch_wnote(fn):
    res = nt_srch.fetch(fn)
    return res.items
def fetch_all_wnote():
    res = nt_srch.fetch()
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
        res = nt_srch.fetch(last=res.last)
        all_items += res.items
    return all_items

sub = deta.Base("Notes_Subjects")
def insert_sub(key, date):
    return sub.put(key, date)

def fetch_sub():
    res = sub.fetch()
    return res.items
#, "subject": subject})#, "category": category, 'importance':importance, "comment": comment})
#,subject):#, category,importance, comment
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
