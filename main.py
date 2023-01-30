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
import pandas as pd
import os
from io import BytesIO, StringIO
from PIL import Image
import pytz

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1
# local_tz = pytz.timezone('Europe/Moscow')
# def utc_to_local(utc_dt):
#     local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
#     return local_tz.normalize(local_dt) # .normalize might be unnecessary
# def aslocaltimestr(utc_dt):
#     return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

                                                                                                                  #+8_
TODAY = str(datetime.now()).split(":")[0].split(" ")[0]+" "+str(int(str(datetime.now()).split(":")[0].split(" ")[1])+8) +":"+ str(datetime.now()).split(":")[1]
# -------------- SETTINGS --------------
incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]
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
    selected = option_menu(
        menu_title="Main Menu", #None
        options=["Home","My Notes","Income&Expense Tracker","To Do List"], #Contact
        icons=["house","book","coin"], #envelope
        menu_icon="cast",
        default_index=0,
        orientation="vertical" #optional

    )
#st.title("My App")

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
subjects = ['','Macroeconomics','Engineering Math','Mandarin','Biology','BioStats','Envir. Hygiene','Psy.','Idea','Lecture','Future Plannings','Others']
categories = ['Lecture Notes','Exam','Quiz','HW']
importance = ['Memorization','Concept','Eziness','Advanced']

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
    st.subheader("Upload Your Image")
    img_num = 0

    uploaded_file = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_file:
        for file in uploaded_file:
            img_num += 1

            if isinstance(file, BytesIO):
                bytes_data = file.getvalue()
                #st.text(bytes_data)
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(' ')

                with col2:
                    #st.image("https://static.streamlit.io/examples/dog.jpg")
                    st.image(bytes_data)  # , width=350
                with col3:
                    st.write(' '+ str(img_num))


    st.subheader("Upload Your Chart")
    uploaded_file2 = st.file_uploader("Upload Your Chart", type = ['csv'])
    if uploaded_file2:
        df = pd.read_csv(uploaded_file2, index_col=None)
        s = df.to_json(orient = 'columns')
        st.text(s)
        db.insert_chart(TODAY,s)
        df.to_csv('dataset.csv', index=None)
        st.dataframe(df)

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
        st.header("Notes Search")
        with st.form("saved_periods"):
            lst_file = db.list_files()
            lst_file.insert(0," ") #<----This way u can type the query!!
            chart = db.fetch_all_chart()
            wnote = db.fetch_all_wnote()
            #st.text(wnote)
            for i in range(len(chart)):
                lst_file.append("[chart]: "+chart[i]["key"])
            for k in range(len(wnote)):
                try:
                    lst_file.append("[wnote]: "+wnote[k]["title"])# + "- #{Content}" + str(wnote[k]["comment"]))
                except KeyError:
                    pass

            selected_file = st.selectbox("Select Results:", lst_file)
            submitted = st.form_submit_button("Load Notes")
            if submitted:
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
                    if len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]) != 0:
                        #st.text(len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]))
                        for i in range(len(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"])):
                            try:

                                # Get data from database
                                photos = db.fetch_notes("[Pic]: "+ w_srch+"---"+str(i+1))
                                content = photos.read()
                                st.image(content)
                                st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]["Comment"+str(i+1)+": "])
                            except AttributeError:
                                pass

                        try:
                            ct = db.fetch_chart({"key": w_srch})
                            # Get data from database
                            st.dataframe(ct)
                        except AttributeError:
                            pass

                    else:
                        st.success(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")})[0]["comment"]["Comment1"+ ": "])

                    st.json(db.fetch_wnote({"title": selected_file.replace("[wnote]: ", "")}))
                    st.dataframe(db.fetch_wnote(
                        {"title": selected_file.replace("[wnote]: ", "")}))  # selected_file.replace("wnote: ","")
                    # st.text(db.fetch_wnote("3ooonwy6z6f2"))
                elif "[chart]" in selected_file:
                    w_srch = selected_file.replace("[chart]: ", "")
                    ct = db.fetch_chart({"key": w_srch})
                    st.dataframe(ct)
                elif '[Pic]' in selected_file:
                    # w_srch = selected_file.replace("[Pic]: ", "")
                    # if "---" in w_srch:
                    #     w_srch = w_srch[:w_srch.find('---')]
                    # st.text(w_srch)
                    photos = db.fetch_notes(selected_file)
                    content = photos.read()
                    st.image(content)



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
            col1.selectbox("Select Month:", months, key="month")
            col2.selectbox("Select Year:", years, key="year")

            "---"
            with st.expander("Income"):
                for income in incomes:
                    st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
            with st.expander("Expenses"):
                for expense in expenses:
                    st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
            with st.expander("Comment"):
                comment = st.text_area("", placeholder="Enter a comment here ...")

            "---"
            submitted = st.form_submit_button("Save Data")
            if submitted:
                period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
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
                comment = period_data.get("comment")
                expenses = period_data.get("expenses")
                incomes = period_data.get("incomes")

                # Create metrics
                total_income = sum(incomes.values())
                total_expense = sum(expenses.values())
                remaining_budget = total_income - total_expense
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Income", f"{total_income} {currency}")
                col2.metric("Total Expense", f"{total_expense} {currency}")
                col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
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
            # st.write(result)
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

    p1 = px.pie(task_df, names='index', values='Status')
    st.plotly_chart(p1, use_container_width=True)





