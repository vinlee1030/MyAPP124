import io

import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import calendar
from datetime import datetime
import database as db
import Note as nt
import StockPricePred as spp
import pandas as pd
import os
from io import BytesIO, StringIO
from PIL import Image
import pytz
import random
import ast

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1
# local_tz = pytz.timezone('Europe/Moscow')
# def utc_to_local(utc_dt):
#     local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
#     return local_tz.normalize(local_dt) # .normalize might be unnecessary
# def aslocaltimestr(utc_dt):
#     return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

                                                                                                                   #+8_
TODAY = str(datetime.now()).split(":")[0].split(" ")[0]+" "+str(int(str(datetime.now()).split(":")[0].split(" ")[1])+8) +":"+ str(datetime.now()).split(":")[1]+" "+str(datetime.now()).split(":")[2]
# -------------- SETTINGS --------------
incomes = ["Salary", "Allowance", 'Interests',"Other Income"]
expenses = ["Breakfast",'Brunch','Lunch','Dinner','Drinks', "Transportation","Daily Necessities","Education","Entertainment", "Investments", "Groceries", "Other Expenses", "Saving"]
currency = "NTD"
page_title = "My Life App"
page_icon = ":full_moon_with_face:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])


# --- DATABASE INTERFACE ---
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---

with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    selected = option_menu(
        menu_title="Main Menu", #None
        options=["Home","My Notes","Income&Expense Tracker","To Do List","SIR Model Simulation","Health Form","Stock Price Prediction"], #Contact
        icons=["house","book","coin",'clipboard-data','bar-chart','bandaid',"currency-bitcoin"], #envelope
        menu_icon="cast",
        default_index=0,
        orientation="vertical" #optional

    )
    st.image("http://www.constructcityparticularlynet.com.tw/SYN/Totem/easy/mo5.jpg")
#st.title("My App")
#n_quiz = []
if selected == "Home":
    st.title(f"<{selected}>")
    # st.write('''
    # #This
    #
    #          _AAAAA_''')
    st.text(nt.Note.i)
if selected == "My Notes":
    st.title(f"<{selected}>")
if selected == "Income&Expense Tracker":
    st.title(f"<{selected}>")
if selected == "To Do List":
    st.title(f"<{selected}>")
#-----------My Notes Tab------------------------
subjects = ['','Macroeconomics','Engineering Math','Mandarin','Biology','BioStats','Env.Hygiene','Psychology','Ideas','Lecture','Future Plannings','Journal','Work','Others']
categories = ['Lecture Notes','Exam','Quiz','HW']
importance = ['Memorization','Concept','Eziness','Advanced']
#db.insert_sub(subjects,TODAY) #FUTURE: Create Subjects!
if selected == 'My Notes':
    st.info("Welcome")
    STYLE = """
    <style>
    img {
        max-width: 100%;
    }
    </style>
    """
    st.markdown(STYLE, unsafe_allow_html=True)

    selected3 = option_menu(
        menu_title=None,
        options=subjects,
        icons=["search", "currency-exchange", 'infinity','translate','heart',
               'bar-chart-line','flower3','emoji-smile-upside-down-fill','lightbulb-fill',
               'collection-play-fill','card-checklist','journal-richtext','person-workspace','motherboard'],  # https://icons.getbootstrap.com/  bar-chart-fill
        orientation="horizontal",
    )
    if selected3 != '':
        lst_file = []  # db.list_files()[-1:]
        # st.write(lst_file)
        # lst_file.insert(0, " ")  # <----This way u can type the query!!
        # chart = db.fetch_all_chart()[-2:]
        wnote = []
        all_wnote = db.fetch_all_wnote()
        #st.text(all_wnote)
        for i in range(len(all_wnote)):
            if selected3 in all_wnote[i]['title']:
                wnote.append(all_wnote[i])
        if wnote == []:
            st.text("No notes found! You should start taking notes!!")
        else:
            st.text(wnote)
        # for i in range(len(chart)):
        #     lst_file.append("[chart]: " + chart[i]["key"])
        for k in range(len(wnote)):
            try:
                lst_file.append("[wnote]: " + wnote[k]["title"])  # + "- #{Content}" + str(wnote[k]["comment"]))
            except KeyError:
                pass
        lst_file = list(reversed(lst_file))
        for i in range(0, len(lst_file)):
            selected_file = lst_file[i]
            st.write(selected_file)

            if "wnote" in selected_file:
                # st.text(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])
                try:
                    imp_plt = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["importance"]
                    imp_plt["Advanced"] = [imp_plt["Advanced"]]
                    # st.text(imp_plt)
                    fig = px.bar(imp_plt, title='Level')
                    st.plotly_chart(fig)
                except IndexError:
                    pass

                w_srch = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["key"]  # ==TODAY
                # st.text(db.fetch_wnote({"title": selected_file.replace("[wnote]: ","")})[0]["importance"])

                # if len(uploaded_file) != 0: <-----This causes number of photos/notes retricted by current uploaded_file!!!
                if len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0][
                           "comment"]) != 0:  # <---always >=1; doesn't need this
                    # st.text(len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]))
                    for i in range(
                            len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])):
                        try:

                            # Get data from database
                            photos = db.fetch_notes("[Pic]: " + w_srch + "---" + str(i + 1))
                            content = photos.read()
                            st.image(content)
                            st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                           "Comment" + str(i + 1) + ": "])
                        except AttributeError:
                            try:
                                st.success(
                                    db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                        "Comment" + str(i + 1) + ": "])
                            except TypeError:
                                # st.text("No data exists")
                                pass

                    try:

                        ct = db.fetch_chart({"key": w_srch})
                        # Get data from database
                        if ct:
                            # st.dataframe(ct)
                            ct = db.fetch_chart({"key": w_srch})
                            import json

                            jsonStr = json.dumps(ct)
                            df = pd.read_json(jsonStr)
                            st.dataframe(df)
                    except AttributeError:
                        pass

                else:
                    st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                   "Comment1" + ": "])

                # st.json(db.fetch_wnote(
                #     {"title": selected_file.replace("[wnote]: ", "")}))  # <--May Reapeat! Search by title name
                st.dataframe(db.fetch_wnote(
                    {"title": selected_file.replace("[wnote]: ", "")}))  # selected_file.replace("wnote: ","")
                # st.text(db.fetch_wnote("3ooonwy6z6f2"))
            elif "[chart]" in selected_file:
                w_srch = selected_file.replace("[chart]: ", "")
                ct = db.fetch_chart({"key": w_srch})
                # import json
                # jsonStr = json.dumps(ct)
                # df = pd.read_json(jsonStr)
                #
                # #df.to_csv('dataset.csv', index=None)
                # st.dataframe(df)
                st.dataframe(ct)
            elif '[Pic]' in selected_file:
                # w_srch = selected_file.replace("[Pic]: ", "")
                # if "---" in w_srch:
                #     w_srch = w_srch[:w_srch.find('---')]
                # st.text(w_srch)
                photos = db.fetch_notes(selected_file)
                content = photos.read()
                st.image(content)
        #st.title("Challenge Time!")
        nt.Note.Mem_quiz(wnote)
    selected2 = option_menu(
        menu_title=None,
        options=["Notes Entry", "Notes Search", "Review Notes"],
        icons=["pencil-fill", "search",'controller'],  # https://icons.getbootstrap.com/  bar-chart-fill
        orientation="horizontal",
    )

    a = False
    b = False
    c = False
    d = False
    ct = 3
    comment = {}
    cm = []
    if selected2 == "Notes Entry":
        st.header('+ Create Notes +')
        st.subheader("Upload Your Image")
        img_num = 0

        uploaded_file = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        if uploaded_file:
            for file in uploaded_file:
                img_num += 1

                if isinstance(file, BytesIO):
                    bytes_data = file.getvalue()
                    # st.text(bytes_data)
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(' ')

                    with col2:
                        # st.image("https://static.streamlit.io/examples/dog.jpg")
                        st.image(bytes_data)  # , width=350
                    with col3:
                        st.write(' ' + str(img_num))

        st.subheader("Upload Your Chart")
        uploaded_file2 = st.file_uploader("Upload Your Chart", type=['csv'])
        if uploaded_file2:
            df = pd.read_csv(uploaded_file2, index_col=None)
            s = df.to_json(orient='columns')  #
            # st.text(s) s = df.to_csv()
            st.text(s)
            db.insert_chart(TODAY, s)
            # df.to_csv('dataset.csv', index=None)
            st.dataframe(df)

        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            col1.selectbox("Select Subject:", subjects, key = "sub")
            col2.selectbox("Select Categories:", categories, key = "cat")

            "---"
            with st.expander("Title"):
                title = st.text_area("Title for search:", placeholder="Enter a comment here ...")
            with st.expander("Importance"):
                im_value = []
                for im in importance:
                    #st.number_input(f"{im}", min_value=0, format="%i", step=1, key=im) #<----For number input option
                    im_value.append(st.slider('['+im+']'+": "+"scale between 0-10", value=0, max_value= 10))
                    #st.text(im_value)
            with st.expander("Comment"):
                cm.append(st.text_area("", placeholder="Enter a comment here ..."))


            for i in range(2,img_num+1):
                with st.expander("Comment" + str(i)):
                    cm.append(st.text_area("#"+str(i), placeholder="Enter a comment here ..."))
            submitted = st.form_submit_button("Save Data")
            if submitted:
                for i in range(len(cm)):
                    comment.update({'Comment'+str(i+1)+': ': cm[i]})
                #st.success("Comment saved!")
                st.text(comment)

            # submitted = st.form_submit_button("Save Data")
            # if submitted:
                sub = str(st.session_state["sub"])
                cat = str(st.session_state["cat"])
                #importance = {im: st.session_state[im] for im in importance}
                n_imp = importance
                importance = {im: im_value for im in importance}
                #st.text((im_value))
                #st.text((n_imp))
                #st.text((importance))
                for k in range(len(im_value)):
                    try:
                        importance[n_imp[k]] = im_value[k]
                        #st.text(importance)
                    except IndexError:
                        pass
                title = sub + '-' + cat + "-" + title + "- #{Content}" + str(comment)
                st.text(TODAY)
                st.text(sub)
                st.text(importance)
                # db.insert_period(TODAY,sub,importance,comment)
                # db.insert_chart(TODAY,importance)
                db.insert_wnote(TODAY, sub, cat, importance,comment, title)
                # uploaded_file2 = st.file_uploader("Upload Your Chart", type=['csv'])
                # if uploaded_file2:
                # df = pd.read_csv(uploaded_file2, index_col=None)
                # s = df.to_json(orient='columns')
                # db.insert_chart(TODAY, s)
                i = 0
                for file in uploaded_file:
                    bytes_data = file.getvalue()
                    #fn = os.path.basename(file.name)
                    # path = os.path.abspath(file.name)
                    # st.text(path)
                    db.photos_upload("[Pic]: "+TODAY+"---"+str(i+1), bytes_data)
                    i += 1

                #db.photos_upload(uploaded_file2, uploaded_file2) <---Deta Drive seems not able to take in charts

                # df = pd.read_csv(uploaded_file2)
                # s = df.to_json(orient = 'index')
                # #db.insert_chart(s)

                #chart = db.fetch_chart()
                #st.text(chart[0]["key"])
                #st.dataframe(chart)
                st.success("Data saved!")


    if selected2 == "Notes Search":
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False
        def callback():
            st.session_state.button_clicked = True
        st.header("Notes Search")
        with st.form("saved_periods"):
            lst_file = db.list_files()[-5:]
            lst_file.insert(0," ") #<----This way u can type the query!!
            chart = db.fetch_all_chart()[-2:]
            wnote = db.fetch_all_wnote()[-10:]
            #st.text(wnote)
            for i in range(len(chart)):
                lst_file.append("[chart]: "+chart[i]["key"])
            for k in range(len(wnote)):
                try:
                    lst_file.append("[wnote]: "+wnote[k]["title"])# + "- #{Content}" + str(wnote[k]["comment"]))
                except KeyError:
                    pass

            selected_file = st.selectbox("Select Results:", lst_file)
            submitted = st.form_submit_button("Load Notes", on_click=callback())
            if submitted or st.session_state.button_clicked:

                updates = {}
                if "wnote" in selected_file:
                    #st.text(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])
                    try:
                        imp_plt = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["importance"]
                        imp_plt["Advanced"] = [imp_plt["Advanced"]]
                        # st.text(imp_plt)
                        fig = px.bar(imp_plt, title='Level')
                        st.plotly_chart(fig)
                    except IndexError:
                        pass

                    w_srch = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["key"] #==TODAY
                    # st.text(db.fetch_wnote({"title": selected_file.replace("[wnote]: ","")})[0]["importance"])

                    #if len(uploaded_file) != 0: <-----This causes number of photos/notes retricted by current uploaded_file!!!
                    if len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]) != 0: #<---always >=1; doesn't need this
                        #st.text(len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]))
                        for i in range(len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])):

                            try:

                                # Get data from database
                                photos = db.fetch_notes("[Pic]: "+ w_srch+"---"+str(i+1))
                                content = photos.read()
                                st.image(content)
                                st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]["Comment"+str(i+1)+": "])
                                update_comment = st.text_area('',
                                    db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                        "Comment" + str(i + 1) + ": "])
                                updates.update({f'Comment{i+1}: ':update_comment})
                            except AttributeError:
                                try:
                                    st.success(
                                    db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                        "Comment" + str(i + 1) + ": "]) #fetch: returns the whole dictionary when one key is searched  db.fetch({"age": 30})-->returns whole dict with this element
                                    update_comment = st.text_area('', db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                        "Comment" + str(i + 1) + ": "])
                                    updates.update({f'Comment{i + 1}: ': update_comment})
                                except AttributeError:
                                    st.text("No data exists")
                                #pass

                        try:

                            ct = db.fetch_chart({"key": w_srch})
                            # Get data from database
                            if ct:

                                #st.dataframe(ct)
                                ct = db.fetch_chart({"key": w_srch})
                                import json
                                jsonStr = json.dumps(ct)
                                df = pd.read_json(jsonStr)
                                st.dataframe(df)
                        except AttributeError:
                            pass

                    else:
                        st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]["Comment1"+ ": "])
                        update_comment = st.text_area('',db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                         "Comment" + str(i + 1) + ": "])
                        updates.update({f'Comment{i + 1}: ': update_comment})
                    st.json(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})) #<--May Reapeat! Search by title name
                    st.dataframe(db.fetch_wnote(
                        {"title": selected_file.replace("[wnote]: ", "")}))  # selected_file.replace("wnote: ","")
                    # st.text(db.fetch_wnote("3ooonwy6z6f2"))
                elif "[chart]" in selected_file:
                    w_srch = selected_file.replace("[chart]: ", "")
                    ct = db.fetch_chart({"key": w_srch})
                    # import json
                    # jsonStr = json.dumps(ct)
                    # df = pd.read_json(jsonStr)
                    #
                    # #df.to_csv('dataset.csv', index=None)
                    # st.dataframe(df)
                    st.dataframe(ct)
                elif '[Pic]' in selected_file:
                    # w_srch = selected_file.replace("[Pic]: ", "")
                    # if "---" in w_srch:
                    #     w_srch = w_srch[:w_srch.find('---')]
                    # st.text(w_srch)
                    photos = db.fetch_notes(selected_file)
                    content = photos.read()
                    st.image(content)
                #st.write(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["key"])
                try:
                    update_key = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["key"]
                except IndexError:
                    pass
        #with st.form("Update_notes"):
                submit = st.form_submit_button("Update Notes")
                if submit:
                    st.success("Updated")

                    for i in updates:
                        st.write(updates[i])
                        n_updates = {f"comment.{i}":updates[i]}
                        db.update_wnote(n_updates, update_key)
                    note_title = selected_file.replace("[wnote]: ", "")
                    note_title = note_title[:note_title.find("#{Content}")+10] + str(updates)
                    st.write(note_title)
                    title_update = {'title':note_title}
                    db.update_wnote(title_update, update_key)
    if selected2 == "Review Notes":
        st.header("Review")
        #db.insert_quiz('[]',TODAY,["C"],["D"],True)
        wnote = db.fetch_all_wnote()
        #st.write(wnote)
        #quiz = []
        for i in range(len(wnote)):
            #st.write()
            num = wnote[i]['title'].find('{Content}')
            dic_comment = eval(wnote[i]['title'][num+9:])
            if dic_comment['Comment1: '] != '':
                st.write(wnote[i]['title'])
            for k in dic_comment:
                b_split = dic_comment[k].split("//")
                for b in b_split:
                    n_split = b.split("::")
                    if n_split[0] != '':
                        df = pd.DataFrame(n_split).T
                        df2 = pd.DataFrame()
                        df2 = pd.concat([df2,df],axis=1)
                        #quiz.append(n_split)
                        st.dataframe(df2)
                # temp = ['col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','col11']
                # for n in n_split:
                #     n_split = st.columns(len(n_split))
                    #st.write(n_split)
        #st.header("Memory Quiz")
        nt.Note.Mem_quiz(wnote)

        st.header("Challenge")

        with st.form("entry_form", clear_on_submit=True):
            # submitted1 = st.form_submit_button("Shuffle")
            # if submitted1:
            wnote = db.fetch_all_wnote()
            quiz = []
            for i in range(len(wnote)):
                # st.write()
                num = wnote[i]['title'].find('{Content}')
                dic_comment = eval(wnote[i]['title'][num + 9:])
                # if dic_comment['Comment1: '] != '':
                # st.write(wnote[i]['title'])
                for k in dic_comment:
                    b_split = dic_comment[k].split("//")
                    for b in b_split:
                        n_split = b.split("::")
                        if n_split[0] != '':
                            df = pd.DataFrame(n_split).T
                            df2 = pd.DataFrame()
                            df2 = pd.concat([df2, df], axis=1)
                            quiz.append(n_split)
                            # st.dataframe(df2)
            try:
                try:
                    submit = st.form_submit_button("R")
                    if submit:
                        try:
                            for i in range(len(db.fetch_quiz())):
                                st.write(db.fetch_quiz()[i]["key"])
                                db.delete_quiz(db.fetch_quiz()[i]["key"])

                        except IndexError:
                            st.write("Deleted Cache")
                    if db.fetch_quiz()[-1]["key"] == "[]" or db.fetch_quiz()[-1]["Ans"] == [] or db.fetch_quiz()[-1]["Question"] == []:
                        db.delete_quiz(db.fetch_quiz()[-1]["key"])
                        st.write("Delete []")
                        st.success("All Clear!")
                        try:
                            for i in range(len(db.fetch_quiz())):
                                st.write(db.fetch_quiz()[i]["key"])
                                db.delete_quiz(db.fetch_quiz()[i]["key"])

                        except IndexError:
                            st.write("Deleted Cache")
                        submit = st.form_submit_button("Restart")
                        if submit:
                            st.write(db.fetch_quiz())
                            n_quiz = []            #Bug For  FUTURE FIX-->RESART WOULD TRIGGER SHUFFLING AFTER EVERY SUBMISSION
                            n_ques = []
                            n_ans = []
                        # n_quiz = []            #Bug For  FUTURE FIX-->RESART WOULD TRIGGER SHUFFLING AFTER EVERY SUBMISSION
                        # n_ques = []
                        # n_ans = []
                        # n_quiz = ast.literal_eval(db.fetch_quiz()[0]["key"])
                        # n_ques = db.fetch_quiz()[0]["Question"]
                        # n_ans = db.fetch_quiz()[0]["Ans"]
                            try:
                                for i in range(len(db.fetch_quiz())):
                                    st.write(db.fetch_quiz()[i]["key"])
                                    db.delete_quiz(db.fetch_quiz()[i]["key"])

                            except IndexError:
                                st.write("Deleted Cache")
                    else:
                        try:
                            # n_quiz = []
                            n_quiz = ast.literal_eval(db.fetch_quiz()[-1]["key"])
                            # st.write("quiz")
                            # st.write(quiz)
                            n_ques = db.fetch_quiz()[-1]["Question"]
                            n_ans = db.fetch_quiz()[-1]["Ans"]
                            # st.write("NL")
                            #st.write(db.fetch_quiz()[-1])
                        except IndexError:
                            st.write("INDEXERROR")
                            n_quiz = []
                            n_ques = []
                            n_ans = []
                            pass

                        try:
                            if n_quiz != []:
                                quiz = n_quiz
                            if n_ques != []:
                                question_shuffle = n_quiz
                            if n_ans != []:
                                ans_shuffle = n_ans
                        except NameError:
                            st.write("NAMEERROR")
                            pass
                except NameError:
                    pass
            except IndexError:
                try:
                    # n_quiz = []
                    n_quiz = ast.literal_eval(db.fetch_quiz()[-1]["key"])
                    # st.write("quiz")
                    # st.write(quiz)
                    n_ques = db.fetch_quiz()[-1]["Question"]
                    n_ans = db.fetch_quiz()[-1]["Ans"]
                    # st.write("NL")
                    st.write(db.fetch_quiz()[-1])
                except IndexError:
                    st.write("INDEXERROR")
                    n_quiz = []
                    n_ques = []
                    n_ans = []
                    pass

                try:
                    if n_quiz != []:
                        quiz = n_quiz
                    if n_ques != []:
                        question_shuffle = n_quiz
                    if n_ans != []:
                        ans_shuffle = n_ans
                except NameError:
                    st.write("NAMEERROR")
                    pass
                pass

            # st.write("quiz")
            # st.write(quiz)
            # st.write("n_quiz")
            #
            # st.write(n_quiz)
            # st.write(type(n_quiz))
            question = []
            ans = []
            try:
                if n_ques == [] and n_ans == []:
                    st.write("SHUF")
                    for i in range(len(quiz)):
                        question.append(quiz[i][:-1])
                        ans.append(quiz[i][-1])
                    # submitted1 = st.form_submit_button("Shuffle")
                    # if submitted1:
                    ans_shuffle = [n for n in ans]
                    question_shuffle = [q for q in question]
                    for k in range(len(ans)):
                        rand = random.randint(0,len(ans)-1)
                        temp = ans_shuffle[k]
                        ans_shuffle[k] = ans_shuffle[rand]
                        ans_shuffle[rand] = temp

                    for k in range(len(ans)):
                        rand = random.randint(0, len(question) - 1)
                        temp = question_shuffle[k]
                        question_shuffle[k] = question_shuffle[rand]
                        question_shuffle[rand] = temp
                        #checkbox_val = st.checkbox("Form checkbox")
                    #db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), False)
                    # n_quiz = question_shuffle
                    # n_ans = ans_shuffle
                else:
                    st.write("NOT SHUF")
                    question = []
                    ans = []
                    for i in range(len(quiz)):
                        question.append(quiz[i][:-1])
                        ans.append(quiz[i][-1])
                    #db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
                    question_shuffle = n_ques
                    ans_shuffle = n_ans
                col1, col2 = st.columns(2)
                sq = col1.selectbox("Select Question:", question_shuffle)#, key="month"
                sa = col2.selectbox("Select Ans:", ans_shuffle)#, key="year"
            except NameError:
                pass
            try:
                question = []
                ans = []
                for i in range(len(quiz)):
                    question.append(quiz[i][:-1])
                    ans.append(quiz[i][-1])
                try:
                    if question.index(sq) == ans.index(sa):
                        st.write("Correct=True1")
                        correct = True
                        #if quiz != []:
                        db.insert_quiz(str(quiz), TODAY,(question_shuffle),(ans_shuffle),correct)

                    else:
                        st.write("Correct=False1")
                        correct = False

                        db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)
                except ValueError:
                    st.write("VALUEＥＲＲＯＲ1")
                    pass

                submitted2 = st.form_submit_button("Submit Answer")
                n_correct = db.fetch_quiz()[-1]["Correct"]
                if submitted2:
                    try:
                        # n_quiz = []
                        n_quiz = ast.literal_eval(db.fetch_quiz()[-1]["key"])
                        #st.write("quiz")
                        #st.write(quiz)
                        n_ques = db.fetch_quiz()[-1]["Question"]
                        n_ans = db.fetch_quiz()[-1]["Ans"]
                        # st.write("NL")
                        # st.write(n_quiz)
                    except IndexError:
                        n_quiz = []
                        n_ques = []
                        n_ans = []
                        pass

                    try:
                        if n_quiz != []:
                            quiz = n_quiz
                            # try:
                            #     value_test = n_quiz[0][0]
                            #     quiz = n_quiz
                            # except AttributeError:
                            #     nn_quiz = []
                            #     quiz = nn_quiz.append(n_quiz)
                        if n_ques != []:
                            question_shuffle = n_ques
                        if n_ans != []:
                            ans_shuffle = n_ans
                    except NameError:
                        st.write("NAMEERROR")
                        pass
                    try:
                        # quiz = ast.literal_eval(db.fetch_quiz()[-1]["key"])
                        # temp = []
                        # quiz = temp.append(quiz)
                        # question = []
                        # ans = []
                        # st.write("quiz")
                        # st.write(quiz)
                        for i in range(len(quiz)):
                            question.append(quiz[i][:-1])
                            ans.append(quiz[i][-1])
                        #n_correct = db.fetch_quiz()[-1]["Correct"]
                    # for k in range(len(ans)):
                    #     rand = random.randint(0,len(ans)-1)
                    #     temp = ans_shuffle[k]
                    #     ans_shuffle[k] = ans_shuffle[rand]
                    #     ans_shuffle[rand] = temp
                    #     ans_shuffle = {}
                    #     question_shuffle = {}
                    #     st.write(quiz)
                    #     st.write(ans_shuffle)
                    #     st.write(question_shuffle)
                        # st.write(ans)
                        # st.write(ans_shuffle)
                        # st.write(question.index(sq))
                        # st.write(ans.index(sa))
                        # st.write((sq))
                        #st.write((sa))
                        # st.write(question)
                        # st.write(ans)
                        try:
                            if question.index(sq) == ans.index(sa):
                                st.write("Correct=True")
                                n_correct = True
                                #db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)
                            else:
                                st.write("Correct=False")
                                n_correct = False
                                #db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)
                        except ValueError:
                            st.write("VALUEＥＲＲＯＲ")
                            pass
                        # st.write("n_correct")
                        # st.write((n_correct))
                        # st.write(quiz)
                        st.write(sq)
                        st.write(sa)
                        if n_correct:
                            #st.write("question_shuffle")

                            st.success(str(sq) + '-->' + str(sa) + "       [AC]")
                            for i in range(len(quiz)):
                                try:
                                    if quiz[i][:-1] == sq:
                                        quiz.remove(quiz[i])
                                        db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
                                except IndexError:
                                    pass
                                try:
                                    if question_shuffle[i] == sq:
                                        #st.write(question_shuffle)
                                        question_shuffle.remove(question_shuffle[i])
                                        db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
                                except IndexError:
                                    pass

                                try:
                                    if ans_shuffle[i] == sa:
                                        ans_shuffle.remove(ans_shuffle[i])
                                        db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
                                except IndexError:
                                    pass
                            #db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
                            # ans_shuffle = [n for n in ans]
                            # question_shuffle = [q for q in question]
                            # col1, col2 = st.columns(2)
                            # sq = col1.selectbox("Select Question:", question_shuffle)  # , key="month"
                            # sa = col2.selectbox("Select Ans:", ans_shuffle)  # , key="year"
                            submitted3 = st.form_submit_button("Continue")
                            #if submitted3:
                        else:
                            submitted3 = st.form_submit_button("Continue")
                            st.warning("[WA]")
                            db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)

                    except ValueError:
                        st.write("ALL CLEAR")
                        # for i in range(len(wnote)):
                        #     # st.write()
                        #     num = wnote[i]['title'].find('{Content}')
                        #     dic_comment = eval(wnote[i]['title'][num + 9:])
                        #     #if dic_comment['Comment1: '] != '':
                        #         #st.write(wnote[i]['title'])
                        #     for k in dic_comment:
                        #         b_split = dic_comment[k].split("//")
                        #         for b in b_split:
                        #             n_split = b.split("::")
                        #             if n_split[0] != '':
                        #                 df = pd.DataFrame(n_split).T
                        #                 df2 = pd.DataFrame()
                        #                 df2 = pd.concat([df2, df], axis=1)
                        #                 quiz.append(n_split)
                        #db.insert_quiz(quiz, TODAY)
                        #submitted = st.form_submit_button("Restart")
                        #if submitted:
                            #db.insert_quiz([],TODAY)
                        #pass
                # elif submitted2 and n_correct==False:
                #     st.warning("WA")
            except NameError:
                pass
# --- 'Income&Expense Tracker' Tab/ INPUT & SAVE PERIODS ---

if selected == 'Income&Expense Tracker':
    selected2 = option_menu(
        menu_title=None,
        options=["Data Entry", "Data Visualization"],
        icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    if selected2 == "Data Entry":
        st.header(f"Data Entry in {currency}")
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            # col1.selectbox("Select Month:", months, key="month")
            # col2.selectbox("Select Year:", years, key="year")
            period = str(st.date_input("Today's Balance"))
            #st.text(type(period))
            "---"
            with st.expander("Income"):
                for income in incomes:
                    st.number_input(f"{income}:", min_value=0, format="%i", step=100, key=income)
            with st.expander("Expenses"):
                for expense in expenses:
                    st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
            with st.expander("Comment"):
                comment = st.text_area("", placeholder="Enter a comment here ...")

            "---"
            submitted = st.form_submit_button("Save Data")
            if submitted:
                #period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])

                incomes = {income: st.session_state[income] for income in incomes}
                expenses = {expense: st.session_state[expense] for expense in expenses}
                db.insert_period(period, incomes, expenses, comment)
                st.success("Data saved!")


    # --- PLOT PERIODS ---
    if selected2 == "Data Visualization":
        st.header("Data Visualization")
        with st.form("saved_periods"):
            period = st.selectbox("Select Period:", get_all_periods())
            submitted = st.form_submit_button("Plot Period")
            if submitted:
                # Get data from database
                period_data = db.get_period(period)
                #st.write(period_data)
                comment = period_data.get("comment")
                expenses = period_data.get("expenses")
                #st.write(expenses)
                incomes = period_data.get("incomes")
                #st.write(incomes)

                # Create metrics
                total_income = sum(incomes.values())
                total_expense = sum(expenses.values())
                remaining_budget = total_income - total_expense
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Income", f"${total_income} {currency}")
                col2.metric("Total Expense", f"${total_expense} {currency}")
                col3.metric("Remaining Budget", f"${remaining_budget} {currency}")
                st.text(f"Comment: {comment}")

                # Create sankey chart
                label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
                source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
                target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
                value = list(incomes.values()) + list(expenses.values())

                # Data to dict, dict to sankey
                link = dict(source=source, target=target, value=value)
                node = dict(label=label, pad=20, thickness=30, color="#E694FF")
                data = go.Sankey(link=link, node=node)

                # Plot it!
                fig = go.Figure(data)
                fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                st.plotly_chart(fig, use_container_width=True)

                # Get data from database

                total_income = 0
                total_expense = 0
                all_periods = get_all_periods()
                st.metric("Balance Logs", len(all_periods),"Days")
                income_keys = {}
                expenses_keys = {}
                for p in all_periods:
                    period_data = db.get_period(p)
                    #st.write(p)
                    expenses = period_data.get("expenses")
                    incomes = period_data.get("incomes")
                    total_income += sum(incomes.values())
                    total_expense += sum(expenses.values())
                    for i in incomes:
                        if i not in income_keys:
                            income_keys.update({i:incomes[i]})
                        else:
                            income_keys[i] += incomes[i]
                    for j in expenses:
                        if j not in expenses_keys:
                            expenses_keys.update({j:expenses[j]})
                        else:
                            expenses_keys[j] += expenses[j]
                # st.text(income_keys)
                # st.text(expenses_keys)
                # Create metrics
                remaining_budget = total_income - total_expense
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Income", f"${total_income} {currency}")
                col2.metric("Total Expense", f"${total_expense} {currency}")
                col3.metric("Remaining Budget", f"${remaining_budget} {currency}")


                # Create sankey chart
                label = list(income_keys.keys()) + ["Total Income"] + list(expenses_keys.keys())
                source = list(range(len(income_keys))) + [len(income_keys)] * len(expenses_keys)
                target = [len(income_keys)] * len(income_keys) + [label.index(expense) for expense in expenses_keys.keys()]
                value = list(income_keys.values()) + list(expenses_keys.values())
                #
                # Data to dict, dict to sankey
                link = dict(source=source, target=target, value=value)
                node = dict(label=label, pad=20, thickness=30, color = 'rgba(255,0,255,0.8)')
                data = go.Sankey(link=link, node=node)

                # Plot it!
                fig = go.Figure(data)
                fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                st.plotly_chart(fig, use_container_width=True)

#----------------To Do List--------------------------------------------
from db_fxns import *
import streamlit.components.v1 as stc
# Data Viz Pkgs
import plotly.express as px
if selected == 'To Do List':
    menu = ["Create", "Read", "Update", "Delete", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_table()

    if choice == "Create":
        st.subheader("Add Item")
        col1, col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success("Added ::{} ::To Task".format(task))


    elif choice == "Read":
        # st.subheader("View Items")
        with st.expander("View All"):
            result = view_all_data()
            st.write(result[0])

            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame()
            # st.dataframe(task_df)
            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names='index', values='Status')
            st.plotly_chart(p1, use_container_width=True)


    elif choice == "Update":
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            result = view_all_data()
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Task", list_of_tasks)
        task_result = get_task(selected_task)
        # st.write(task_result)

        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            col1, col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Task To Do", task)

            with col2:
                new_task_status = st.selectbox(task_status, ["ToDo", "Doing", "Done"])
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                st.success("Updated ::{} ::To {}".format(task, new_task))

            with st.expander("View Updated Data"):
                result = view_all_data()
                # st.write(result)
                clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
                st.dataframe(clean_df)


    elif choice == "Delete":
        st.subheader("Delete")
        with st.expander("View Data"):
            result = view_all_data()
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        unique_list = [i[0] for i in view_all_task_names()]
        delete_by_task_name = st.selectbox("Select Task", unique_list)
        if st.button("Delete"):
            delete_data(delete_by_task_name)
            st.warning("Deleted: '{}'".format(delete_by_task_name))

        with st.expander("Updated Data"):
            result = view_all_data()
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

    else:
        st.subheader("About ToDo List App")
        st.info("Built with Streamlit")
        st.info("Do your tasks faithfully")
        st.text("Work hard Play hard")

if selected == "Home":
    #st.title(':moneybag:')
    m_sum = 0
    for i in range(len(db.fetch_coin())):
        m_sum += int(db.fetch_coin()[i]['Earnings'])
    #st.write(m_sum)
    col1, col2, col3 = st.columns(3)
    col2.title(':moneybag:')
    col2.metric('Account',f"${m_sum}",'Tokens')
    #st.write(db.fetch_coin()[0]['Earnings'])


    # -------------Plot daily loading bar chart
    result = view_all_data()
    data = {'Task': [], 'Status': [], 'Date': []}

    for i in range(len(result)):  # how many tasks in the list
        count = 0
        for key in data:
            if result[i][1] == 'ToDo':
                data[key].append(result[i][count])
                count += 1

    clean_data = {'Date': [], "Tasks": []}
    for key in data:
        if key == "Date":
            temp = []
            clean_data['Date'].append(data['Date'][0])
            for i in range(len(data['Date'])):

                if data['Date'][i] not in clean_data['Date']:
                    clean_data['Date'].append(data['Date'][i])
            for k in range(len(clean_data["Date"])):
                for p in range(len(clean_data["Date"])):
                    try:
                        if int(clean_data["Date"][k][-5:-3]) >= int(clean_data["Date"][k + p][-5:-3]):
                            if int(clean_data["Date"][k][-2:]) > int(clean_data["Date"][k + p][-2:]):
                                temp = clean_data["Date"][k + p]
                                clean_data["Date"][k + p] = clean_data["Date"][k]
                                clean_data["Date"][k] = temp
                    except IndexError:
                        pass

            for j in range(len(clean_data['Date'])):
                clean_data['Tasks'].append(data['Date'].count(clean_data['Date'][j]))

    # st.write(data['Date'])
    # st.write(clean_data)
    # data.update({"Tasks":tasks})
    df = pd.DataFrame.from_dict(clean_data)
    fig = px.bar(df, x='Date', y='Tasks',
                 hover_data=['Tasks'], color='Tasks',
                 labels={'Tasks': 'Up coming tasks'}, height=400)
    # fig.show()
    st.plotly_chart(fig)
    # st.subheader("View Items")
    st.header("Tasks")
    #with st.expander("View All"):
    result = view_all_data()
    # st.write(result)
    clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
    st.dataframe(clean_df)

    #with st.expander("Task Status"):
    task_df = clean_df['Status'].value_counts().to_frame()
    # st.dataframe(task_df)
    task_df = task_df.reset_index()
    st.dataframe(task_df)

    p1 = px.pie(task_df, names='Status', values='count')
    st.plotly_chart(p1, use_container_width=True)

    # Get data from database
    st.title("Spendings")
    total_income = 0
    total_expense = 0
    all_periods = get_all_periods()
    st.metric("Balance Logs", len(all_periods), "Days")
    income_keys = {}
    expenses_keys = {}
    for p in all_periods:
        period_data = db.get_period(p)
        # st.write(p)
        expenses = period_data.get("expenses")
        incomes = period_data.get("incomes")
        total_income += sum(incomes.values())
        total_expense += sum(expenses.values())
        for i in incomes:
            if i not in income_keys:
                income_keys.update({i: incomes[i]})
            else:
                income_keys[i] += incomes[i]
        for j in expenses:
            if j not in expenses_keys:
                expenses_keys.update({j: expenses[j]})
            else:
                expenses_keys[j] += expenses[j]
    # st.text(income_keys)
    # st.text(expenses_keys)
    # Create metrics
    remaining_budget = total_income - total_expense
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income} {currency}")
    col2.metric("Total Expense", f"${total_expense} {currency}")
    col3.metric("Remaining Budget", f"${remaining_budget} {currency}")

    # Create sankey chart
    label = list(income_keys.keys()) + ["Total Income"] + list(expenses_keys.keys())
    source = list(range(len(income_keys))) + [len(income_keys)] * len(expenses_keys)
    target = [len(income_keys)] * len(income_keys) + [label.index(expense) for expense in expenses_keys.keys()]
    value = list(income_keys.values()) + list(expenses_keys.values())
    #
    # Data to dict, dict to sankey
    link = dict(source=source, target=target, value=value)
    node = dict(label=label, pad=20, thickness=30, color='rgba(0,255,255,0.4)')#'rgba(255,0,255,0.8)'
    data = go.Sankey(link=link, node=node)

    # Plot it!
    fig = go.Figure(data)
    fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
    st.plotly_chart(fig, use_container_width=True)



    #-------------Load review notes---------------------

    lst_file = []#db.list_files()[-1:]
    #st.write(lst_file)
    # lst_file.insert(0, " ")  # <----This way u can type the query!!
    # chart = db.fetch_all_chart()[-2:]
    try:
        wnote = db.fetch_all_wnote()[-2:]
    except IndexError:
        try:
            wnote = db.fetch_all_wnote()[-1:]
        except IndexError:
            st.write("No notes found! You should start taking notes!!")
    # st.text(wnote)
    # for i in range(len(chart)):
    #     lst_file.append("[chart]: " + chart[i]["key"])
    for k in range(len(wnote)):
        try:
            lst_file.append("[wnote]: " + wnote[k]["title"])  # + "- #{Content}" + str(wnote[k]["comment"]))
        except KeyError:
            pass
    lst_file = list(reversed(lst_file))
    for i in range(0,len(lst_file)):
        selected_file = lst_file[i]
        st.write(selected_file)

        if "wnote" in selected_file:
            # st.text(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])
            try:
                imp_plt = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["importance"]
                imp_plt["Advanced"] = [imp_plt["Advanced"]]
                # st.text(imp_plt)
                fig = px.bar(imp_plt, title='Level')
                st.plotly_chart(fig)
            except IndexError:
                pass

            w_srch = db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["key"]  # ==TODAY
            # st.text(db.fetch_wnote({"title": selected_file.replace("[wnote]: ","")})[0]["importance"])

            # if len(uploaded_file) != 0: <-----This causes number of photos/notes retricted by current uploaded_file!!!
            if len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0][
                       "comment"]) != 0:  # <---always >=1; doesn't need this
                # st.text(len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]))
                for i in range(
                        len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])):
                    try:

                        # Get data from database
                        photos = db.fetch_notes("[Pic]: " + w_srch + "---" + str(i + 1))
                        content = photos.read()
                        st.image(content)
                        st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                       "Comment" + str(i + 1) + ": "])
                    except AttributeError:
                        try:
                            st.success(
                                db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                                    "Comment" + str(i + 1) + ": "])
                        except TypeError:
                            #st.text("No data exists")
                            pass

                try:

                    ct = db.fetch_chart({"key": w_srch})
                    # Get data from database
                    if ct:
                        # st.dataframe(ct)
                        ct = db.fetch_chart({"key": w_srch})
                        import json

                        jsonStr = json.dumps(ct)
                        df = pd.read_json(jsonStr)
                        st.dataframe(df)
                except AttributeError:
                    pass

            else:
                st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"][
                               "Comment1" + ": "])

            # st.json(db.fetch_wnote(
            #     {"title": selected_file.replace("[wnote]: ", "")}))  # <--May Reapeat! Search by title name
            st.dataframe(db.fetch_wnote(
                {"title": selected_file.replace("[wnote]: ", "")}))  # selected_file.replace("wnote: ","")
            # st.text(db.fetch_wnote("3ooonwy6z6f2"))
        elif "[chart]" in selected_file:
            w_srch = selected_file.replace("[chart]: ", "")
            ct = db.fetch_chart({"key": w_srch})
            # import json
            # jsonStr = json.dumps(ct)
            # df = pd.read_json(jsonStr)
            #
            # #df.to_csv('dataset.csv', index=None)
            # st.dataframe(df)
            st.dataframe(ct)
        elif '[Pic]' in selected_file:
            # w_srch = selected_file.replace("[Pic]: ", "")
            # if "---" in w_srch:
            #     w_srch = w_srch[:w_srch.find('---')]
            # st.text(w_srch)
            photos = db.fetch_notes(selected_file)
            content = photos.read()
            st.image(content)

    st.title("Today's Challenge")
    nt.Note.Mem_quiz(wnote)
    nt.Note.quizzing(wnote)
    st.title("Quiz Search")
    with st.form("Quick Search"):
        query = st.text_input('Query')
        sub = st.form_submit_button("Search")
        import openai
        if sub:
            openai.api_key = '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'

            response = openai.Completion.create(
                engine="text-davinci-003",  # select model
                prompt= query,#"ChatGPT是什麼？",
                max_tokens=512,  # response tokens
                temperature=1,  # diversity related
                top_p=0.75,  # diversity related
                n=1,  # num of response
            )

            completed_text = response["choices"][0]["text"]
            st.write(completed_text)
#---------------------------SIR Model----------------------
if selected == 'SIR Model Simulation':
    import matplotlib.pyplot as plt
    import numpy as np
    settings = ['ndays','dt','beta','gamma']
    with st.form("Model"):
        with st.expander("Settings"):
            s_value = []
            for s in settings:
                # st.number_input(f"{im}", min_value=0, format="%i", step=1, key=im) #<----For number input option
                s_value.append(st.slider('[' + s + ']' + ": " + "scale between 0-10", value=0.1, max_value=100.0))
            # for s in settings:
            #
            #     ndays = st.slider('ndays',value=10, max_value= 1000)#100
            #     s_value.append(ndays)
            #
            #     dt = st.slider('dt',value=0.1, max_value= 1)#0.1
            #     s_value.append(dt)
            #
            #     beta = st.slider('Beta Value',value=0, max_value= 0.1)#(1.0/3.0)
            #     s_value.append(beta)
            #
            #     gamma = st.slider('Gamma Value',value=0, max_value= 1)#(1.0/14.0)
            #     s_value.append(gamma)
        sub2 = st.form_submit_button("Load Model")
        if sub2:
            ndays = s_value[0]
            dt = s_value[1]
            beta = s_value[2]
            gamma = s_value[3]
            npts = int(ndays / dt)
            S = np.zeros(npts)
            I = np.zeros(npts)
            R = np.zeros(npts)
            t = np.arange(npts)*dt

            I[0] = 0.001#st.slider('Initial Infected',value=0.0, max_value= 0.1)#
            S[0] = 1 - I[0]
            R[0] = 0

            for i in range(npts-1):
                S[i+1] = S[i] - beta*(S[i]*I[i])*dt
                I[i+1] = I[i] + (beta*S[i]*I[i]-gamma*I[i])*dt
                R[i+1] = R[i] + (gamma*I[i])*dt
            fig = plt.figure(1); fig.clf()
            plt.plot(t,S,'r', lw = 3, label = 'Susceptible')
            plt.plot(t, I, 'g', lw=3, label='Infective')
            plt.plot(t,R,'o', lw = 3, label = "Recovered")
            fig.legend();plt.xlabel("Days");plt.ylabel("Fraction of Population")
            st.plotly_chart(fig)

if selected == "Health Form":
    with st.form("Entry_Hform", clear_on_submit=True):
        states = ['N','F','W','A']
        illness = ['None','Diarrhea','Blister','Nausea','Stomachache','BackPain','MusclePain','Flu','Rashes']
        #col1, col2 = st.columns(2)
        st.selectbox("Select States:", states, key="states")
        st.multiselect("Feeling Sick?", illness, key = 'illness')
        #col1.selectbox("Select Categories:", categories, key="cat")

        "---"
        daily_ques = ['H2O Intake','# of Meals','Appetite','Fruit/Veggie/Cellulose','Proteins','Fats','Carbohydrate','Meals Quality','Hours of Sleep','Naps'
                      'Hours of Exercises','Intensity of Exercises','#1','#2','Tiredness','Mood','WakeUpTime','BedTime']
        with st.expander("Daily Survey"):
            d_value = []
            for d in daily_ques:
                # st.number_input(f"{im}", min_value=0, format="%i", step=1, key=im) #<----For number input option
                d_value.append(st.slider('[' + d + ']' + ": " + "scale between 0-15", value=0.0, max_value=15.0,step = 0.5))
                # st.text(im_value)

        with st.expander("Desciptions"):
            des = st.text_area("Extra Comment:", placeholder="Enter a comment here ...")
        submitted = st.form_submit_button("Save Data")
        if submitted:

            sta = str(st.session_state["states"])
            ill = str(st.session_state["illness"])
            #cat = str(st.session_state["cat"])
            # importance = {im: st.session_state[im] for im in importance}
            n_dq = daily_ques
            daily_ques = {d: d_value for d in n_dq}
            for k in range(len(d_value)):
                try:
                    daily_ques[n_dq[k]] = d_value[k]
                    # st.text(importance)
                except IndexError:
                    pass

            db.insert_hform(TODAY, daily_ques, sta, des, ill)
            st.success("“Physical fitness is the first requisite of happiness.” – Joseph Pilates")

if selected == 'Stock Price Prediction':
    spp.SPP.s_pred(spp.SPP)
