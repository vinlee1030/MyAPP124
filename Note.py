from datetime import datetime
class Note:

     i = f'Welcome to my Life Note! Today is {str(datetime.now().strftime("%Y-%m-%d"))}'
     #--------------Upload Image Chaos--------------
     # from pathlib import Path
     # from PIL import Image
     #
     # def load_image(image_file):
     #      img = Image.open(image_file)
     #      return img

     # if selected == 'My Notes':
     #      # st.subheader("Image")
     #      # image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
     #      #
     #      # if image_file is not None:
     #      #     # To See details
     #      #     file_details = {"filename": image_file.name, "filetype": image_file.type,
     #      #                     "filesize": image_file.size}
     #      #     st.write(file_details)
     #      #     ui = image_file.getvalue()
     #      #     st.text(ui)
     #      #     # To View Uploaded Image
     #      #     st.image(image_file, width=250) #load_image(ui)
     #      st.title("Upload Your Dataset")
     #      uploaded_file = st.file_uploader("Upload Your Dataset")
     #      if uploaded_file:
     #           # st.text(file.name)
     #           # fn = os.path.basename(file.name)
     #           # path = os.path.abspath(fn)
     #           # st.text(fn)
     #           # st.text(path)
     #           # #st.write(bytes_data)
     #           bytes_data = uploaded_file.getvalue()
     #
     #           st.image(bytes_data)

     # try:
     #      bytes_data = uploaded_file.getvalue()
     #      st.write("YYYYY")
     #      bytes_data = uploaded_file.getvalue()
     #      st.image(bytes_data)
     # except st.error:
     #      df = pd.read_csv(uploaded_file, index_col=None)
     #      df.to_csv('dataset.csv', index=None)
     #      st.dataframe(df)
     #      pass

     # if uploaded_file:
     #
     #      if isinstance(uploaded_file, BytesIO):
     #           st.write("YYYYY")
     #           bytes_data = uploaded_file.getvalue()
     #           st.image(bytes_data)
     #      elif isinstance(uploaded_file, StringIO): #else:
     #           df = pd.read_csv(uploaded_file, index_col=None)
     #           df.to_csv('dataset.csv', index=None)
     #           st.dataframe(df)

     # img = Image.open(content, mode="r")
     # photos = io.BytesIO()
     # photos = photos.getvalue()
     # st.text(img)
     # with open("photos", "rb") as f:
     #     for chunk in photos.iter_chunks(4096):
     #         st.text(chunk)
     #         f.write(chunk)
     #     photos.close()
     # img = Image.open(photos)
     # st.image(img)

     # st.image(photos)

     # comment = period_data.get("comment")
     # expenses = period_data.get("expenses")
     # incomes = period_data.get("incomes")

#--------------------Search Chaos----------------------------------------
# def search(srch, query, lst_file):
#
#     #selected_file = st.selectbox("Select Results:", lst_file)
#     if srch and len(query) != 0 and query != None:
#         n_lst = ['or']
#         st.text("Search for: " + query)
#         for s in range(len(lst_file)):
#             if query in lst_file[s]:
#                 n_lst.append(lst_file[s])
#         # if len(n_lst) == 0:
#         #     st.text("No result found")
#         #     selected_file = st.selectbox("Select Results:", lst_file)  # lst_file
#         #
#         # else:
#         selected_file = st.selectbox("Select Results:", n_lst)
#         lst_file = []
#         lst_file.append(n_lst)
#         # db.insert_cache(selected_file, TODAY)
#         st.text(n_lst)
#         st.text(selected_file)
#             # st.text(np.savetxt(n_lst))
#             # st.text(dict(n_lst))
#     # else:
#     #     selected_file = st.selectbox("Select Results:", n_lst)
#     return n_lst
#      search_method = ["ByDate", "By Name"]
#      selected_search = st.selectbox("Select Search Method:", search_method)
#      # with st.expander("Query"):
#      #     query = st.text_area("", placeholder="Enter a query here ...")
#      sub = st.form_submit_button("Enter")
#      if selected_search == "By Name" and sub:
#           st.text("Search " + selected_search)
#      with st.expander("Query"):
#           query = st.text_area("", placeholder="Enter a query here ...")
#
#      srch = st.form_submit_button("Search")
#
#
# if srch and len(query) != 0 and query != None:
#      n_lst = ['or']
#      st.text("Search for: " + query)
#      for s in range(len(lst_file)):
#           if query in lst_file[s]:
#                n_lst.append(lst_file[s])
#      # if len(n_lst) == 0:
#      #     st.text("No result found")
#      #     selected_file = st.selectbox("Select Results:", lst_file)  # lst_file
#      #
#      # else:
#      selected_file = st.selectbox("Select Results:", n_lst)
#      lst_file = []
#      lst_file.append(n_lst)
#      # db.insert_cache(selected_file, TODAY)
#      st.text(n_lst)
#      st.text(selected_file)
# else:
#      selected_file = st.selectbox("Select Results:", lst_file)
#      # final = db.search(srch, query, lst_file)
#      # st.text(final)
#      # enter = st.form_submit_button("Enter!")
#      # if enter:
#      #     try:
#      #         st.text(final)
#      #     except NameError:
#      #         st.text("error")
#      # final = st.selectbox("Select Results:", lst_file)
#
#      # final = st.selectbox("Select Results:", db.fetch_cache())

#---------Add comment chaos
#add_comment = [a ,b ,c,d]
            # ac = st.form_submit_button("Add Comment" + str(img_num))
            # if ac:
            # add_comment[ct] = st.form_submit_button("Add Comment" + str(img_num))
            # if add_comment[ct]:
            #
            #     with st.expander("Comment" + str(ct)):
            #         ct -= 1
            #         comment = st.text_area(str(ct), placeholder="Enter a comment here ...")
            #         add_comment[ct] = st.form_submit_button("Add Comment" + str(img_num))
            # if img_num > 1:
            #     add_comment[img_num - 1] = st.form_submit_button("Add Comment"+str(img_num))
            #     if add_comment[img_num - 1]:
            #         with st.expander("Comment"+str(img_num)):
            #             add_comment[img_num - 1] = False
            #             img_num -= 1
            #             add_comment[img_num - 1] = st.form_submit_button("Add Comment" + str(img_num))
            #             comment = st.text_area(str(img_num), placeholder="Enter a comment here ...")