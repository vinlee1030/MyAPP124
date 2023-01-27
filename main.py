import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import calendar
from datetime import datetime
import database as db
import Note as nt
import pandas as pd
import os
from io import BytesIO, StringIO

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 1

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
        options=["Home","My Notes","Income&Expense Tracker"], #Contact
        icons=["house","book","coin"], #envelope
        menu_icon="cast",
        default_index=0,
        orientation="vertical" #optional

    )
#st.title("My App")

if selected == "Home":
    st.title(f"*{selected}")
    st.text(nt.Note.i)
if selected == "My Notes":
    st.title(f"*{selected}")
if selected == "Income&Expense Tracker":
    st.title(f"*{selected}")
#-----------My Notes Tab------------------------
subjects = ['Macroeconomics','Engineering Math','Mandarin']
categories = ['HW','Exam','Quiz']
importance = ['Memorization','Concept','Ez','Advanced']

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
    uploaded_file = st.file_uploader("Upload Your Image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_file:
        for file in uploaded_file:
            if isinstance(file, BytesIO):
                bytes_data = file.getvalue()
                st.image(bytes_data, width=250)

    st.subheader("Upload Your Chart")
    uploaded_file = st.file_uploader("Upload Your Chart", type = ['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, index_col=None)
        df.to_csv('dataset.csv', index=None)
        st.dataframe(df)

    selected2 = option_menu(
        menu_title=None,
        options=["Notes Entry", "Notes Search", "Review Notes"],
        icons=["pencil-fill", "search",'controller'],  # https://icons.getbootstrap.com/  bar-chart-fill
        orientation="horizontal",
    )

    if selected2 == "Notes Entry":
        st.header('+ Create Notes +')
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            col1.selectbox("Select Subject:", subjects)
            col2.selectbox("Select Categories:", categories)

            "---"
            with st.expander("Importance"):
                for i in importance:
                    st.number_input(f"{i}", min_value=0, format="%i", step=1)
            with st.expander("Comment"):
                comment = st.text_area("", placeholder="Enter a comment here ...")

            add_comment = st.form_submit_button("Add Comment")
            if add_comment:
                with st.expander("Comment"):
                    comment = st.text_area("1", placeholder="Enter a comment here ...")

            "---"
            submitted = st.form_submit_button("Save Data")
            if submitted:
                period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
                incomes = {income: st.session_state[income] for income in incomes}
                expenses = {expense: st.session_state[expense] for expense in expenses}
                db.insert_period(period, incomes, expenses, comment)
                st.success("Data saved!")

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










