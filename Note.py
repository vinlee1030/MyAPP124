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