from datetime import datetime
import streamlit as st
import database as db
import pandas as pd
import ast
import random
TODAY = str(datetime.now()).split(":")[0].split(" ")[0]+" "+str(int(str(datetime.now()).split(":")[0].split(" ")[1])) +":"+ str(datetime.now()).split(":")[1]+" "+str(datetime.now()).split(":")[2]

class Note:

     i = f'Welcome to my Life Note! Today is {str(datetime.now().strftime("%Y-%m-%d"))}'
     def quizzing(wnote): #<----wnote = daily wnote
          coin_gain = 0
          coin_loss = 0
          with st.form("entry_form"):#, clear_on_submit=True):
               # submitted1 = st.form_submit_button("Shuffle")
               # if submitted1:
               #wnote = db.fetch_all_wnote()
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
                                   for i in range(len(db.fetch_dquiz())):
                                        st.write(db.fetch_dquiz()[i]["key"])
                                        db.delete_dquiz(db.fetch_dquiz()[i]["key"])

                              except IndexError:
                                   st.write("Deleted Cache")
                         if db.fetch_dquiz()[-1]["key"] == "[]" or db.fetch_dquiz()[-1]["Ans"] == [] or \
                                 db.fetch_dquiz()[-1]["Question"] == []:
                              db.delete_dquiz(db.fetch_quiz()[-1]["key"])
                              st.write("Delete []")
                              #st.text(f"Coin_Gain:{coin_gain}")
                              #st.text(f"Coin_Loss:{coin_loss}")
                              st.success("All Clear!")
                              try:
                                   for i in range(len(db.fetch_dquiz())):
                                        st.write(db.fetch_dquiz()[i]["key"])
                                        db.delete_dquiz(db.fetch_dquiz()[i]["key"])

                              except IndexError:
                                   st.write("Deleted Cache")
                              submit = st.form_submit_button("Restart")
                              if submit:
                                   st.write(db.fetch_dquiz())
                                   n_quiz = []  # Bug For  FUTURE FIX-->RESART WOULD TRIGGER SHUFFLING AFTER EVERY SUBMISSION
                                   n_ques = []
                                   n_ans = []
                                   # n_quiz = []            #Bug For  FUTURE FIX-->RESART WOULD TRIGGER SHUFFLING AFTER EVERY SUBMISSION
                                   # n_ques = []
                                   # n_ans = []
                                   # n_quiz = ast.literal_eval(db.fetch_quiz()[0]["key"])
                                   # n_ques = db.fetch_quiz()[0]["Question"]
                                   # n_ans = db.fetch_quiz()[0]["Ans"]
                                   try:
                                        for i in range(len(db.fetch_dquiz())):
                                             st.write(db.fetch_dquiz()[i]["key"])
                                             db.delete_dquiz(db.fetch_dquiz()[i]["key"])

                                   except IndexError:
                                        st.write("Deleted Cache")
                         else:
                              try:
                                   # n_quiz = []
                                   n_quiz = ast.literal_eval(db.fetch_dquiz()[-1]["key"])
                                   # st.write("quiz")
                                   # st.write(quiz)
                                   n_ques = db.fetch_dquiz()[-1]["Question"]
                                   n_ans = db.fetch_dquiz()[-1]["Ans"]
                                   # st.write("NL")
                                   # st.write(db.fetch_quiz()[-1])
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
                         n_quiz = ast.literal_eval(db.fetch_dquiz()[-1]["key"])
                         # st.write("quiz")
                         # st.write(quiz)
                         n_ques = db.fetch_dquiz()[-1]["Question"]
                         n_ans = db.fetch_dquiz()[-1]["Ans"]
                         # st.write("NL")
                         st.write(db.fetch_dquiz()[-1])
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
                              rand = random.randint(0, len(ans) - 1)
                              temp = ans_shuffle[k]
                              ans_shuffle[k] = ans_shuffle[rand]
                              ans_shuffle[rand] = temp

                         for k in range(len(ans)):
                              rand = random.randint(0, len(question) - 1)
                              temp = question_shuffle[k]
                              question_shuffle[k] = question_shuffle[rand]
                              question_shuffle[rand] = temp
                              # checkbox_val = st.checkbox("Form checkbox")
                         # db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), False)
                         # n_quiz = question_shuffle
                         # n_ans = ans_shuffle
                    else:
                         st.write("NOT SHUF")
                         question = []
                         ans = []
                         for i in range(len(quiz)):
                              question.append(quiz[i][:-1])
                              ans.append(quiz[i][-1])
                         # db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
                         question_shuffle = n_ques
                         ans_shuffle = n_ans
                    col1, col2 = st.columns(2)
                    sq = col1.selectbox("Select Question:", question_shuffle)  # , key="month"
                    sa = col2.selectbox("Select Ans:", ans_shuffle)  # , key="year"
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
                              # if quiz != []:
                              db.insert_dquiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)

                         else:
                              st.write("Correct=False1")
                              correct = False

                              db.insert_dquiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)
                    except ValueError:
                         st.write("VALUEＥＲＲＯＲ1")
                         pass

                    submitted2 = st.form_submit_button("Submit Answer")
                    n_correct = db.fetch_dquiz()[-1]["Correct"]
                    if submitted2:
                         try:
                              # n_quiz = []
                              n_quiz = ast.literal_eval(db.fetch_dquiz()[-1]["key"])
                              # st.write("quiz")
                              # st.write(quiz)
                              n_ques = db.fetch_dquiz()[-1]["Question"]
                              n_ans = db.fetch_dquiz()[-1]["Ans"]
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

                              try:
                                   if question.index(sq) == ans.index(sa):
                                        st.write("Correct=True")
                                        n_correct = True
                                        # db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)
                                   else:
                                        st.write("Correct=False")
                                        n_correct = False
                                        # db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), correct)
                              except ValueError:
                                   st.write("VALUEＥＲＲＯＲ")
                                   pass
                              # st.write("n_correct")
                              # st.write((n_correct))
                              # st.write(quiz)
                              st.write(sq)
                              st.write(sa)
                              if n_correct:
                                   # st.write("question_shuffle")
                                   db.save_coin("1", TODAY)
                                   coin_gain += 1
                                   st.success(str(sq) + '-->' + str(sa) + "       [AC]")
                                   for i in range(len(quiz)):
                                        try:
                                             if quiz[i][:-1] == sq:
                                                  quiz.remove(quiz[i])
                                                  db.insert_dquiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle),
                                                                 n_correct)
                                        except IndexError:
                                             pass
                                        try:
                                             if question_shuffle[i] == sq:
                                                  # st.write(question_shuffle)
                                                  question_shuffle.remove(question_shuffle[i])
                                                  db.insert_dquiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle),
                                                                 n_correct)
                                        except IndexError:
                                             pass

                                        try:
                                             if ans_shuffle[i] == sa:
                                                  ans_shuffle.remove(ans_shuffle[i])
                                                  db.insert_dquiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle),
                                                                 n_correct)
                                        except IndexError:
                                             pass
                                   submitted3 = st.form_submit_button("Continue")
                              else:
                                   submitted3 = st.form_submit_button("Continue")
                                   st.warning("[WA]")
                                   db.save_coin("-2",TODAY)
                                   coin_loss -= 2
                                   db.insert_dquiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)

                         except ValueError:
                              st.text(f"Coin_Gain:{coin_gain}")
                              st.text(f"Coin_Loss:{coin_loss}")
                              st.write("ALL CLEAR")

               except NameError:
                    pass


#-----------Memory Quiz------------------------------------------------------------
     def Mem_quiz(wnote):
          st.title("Memory Quiz")
          wnote = db.fetch_all_wnote()
          quiz = []
          for i in range(len(wnote)):
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
                              if len(n_split) > 1:
                                   quiz.append(n_split)
          ques = []
          ans = []
          for i in range(len(quiz)):
               ques.append(quiz[i][:-1])
               ans.append(quiz[i][-1])
          # st.write(quiz)
          # st.write(ques)
          # st.write(ans)
          if len(quiz) < 8:
               st.write(f':orange[{8 - len(quiz)} note(s) away from playing Memory Game!!]')
          if len(quiz) >= 8:        #8 <=len(quiz) <= 18:
               # with st.form("Entry_form1", clear_on_submit=True):
               #      size1 = st.form_submit_button("4*4")
               # if size1:
               with st.form("Entry_form", clear_on_submit=True):
                    # ques = ['1','2','3','4','5','6','7','8']
                    # ans = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
                    #st.write(db.fetch_memquiz())
                    if db.fetch_memquiz() == [] or len(db.fetch_memquiz()[-1]['RandQuiz'])!=16 or len(db.fetch_memquiz()[-1]['RandNote'])!=16:
                         ran_lst = []
                         while len(ran_lst) < 16:
                              ran = random.randint(0, 15)#(0, 15) len(quiz)-1
                              if ran not in ran_lst:
                                   ran_lst.append(ran)
                              #st.write(ran_lst)
                         ran_note = []
                         while len(ran_note) < len(quiz):#16:
                              ran = random.randint(0, len(quiz)-1)  # (0, 15) len(quiz)-1
                              if ran not in ran_note:
                                   ran_note.append(ran)
                         db.insert_memquiz(TODAY,ran_lst,ran_note)
                    else:
                         try:
                              ran_lst = db.fetch_memquiz()[-1]['RandQuiz']
                              ran_note = db.fetch_memquiz()[-1]['RandNote']
                         except IndexError:
                              st.write("IndexERROR")

                    wnote = db.fetch_all_wnote()
                    quiz = []
                    for i in range(len(wnote)):
                         num = wnote[i]['title'].find('{Content}')
                         dic_comment = eval(wnote[i]['title'][num + 9:])
                         for k in dic_comment:
                              b_split = dic_comment[k].split("//")
                              for b in b_split:
                                   n_split = b.split("::")
                                   if n_split[0] != '':
                                        if len(n_split) > 1:                              
                                             quiz.append(n_split)
                    note = []
                    for ran in ran_note:
                         note.append(quiz[ran])
                    quiz = note
                    ques = []
                    ans = []
                    for i in range(len(quiz)):
                         ques.append(quiz[i][:-1])
                         ans.append(quiz[i][-1])
                    # st.write(ans)
                    # st.write(ques)
                    lst = []
                    for k in ran_lst:
                         if k == 'Empty':
                              lst.append('Empty')
                         elif k <= k<=7: #(len(quiz)-1)
                              lst.append(ques[k])
                         else:
                              lst.append(ans[k-8]) #(ans[k-len(quiz])
                         # lst.append(ques[k])
                         # lst.append(ans[k])
                    #st.write(lst[0])
                    box_lst = []
                    true_ct = 0
                    for i in range(4):
                         col1, col2,col3,col4 = st.columns(4)

                         f = col1.checkbox(f'1{i}')
                         if f == True:
                              true_ct += 1
                              if lst[0 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append('')
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                              elif true_ct <= 2:
                                   empty = [lst[0 + i * 4]]
                                   empty.append('')
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[0 + i * 4])
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                         else:
                              if lst[0 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append(lst[0 + i * 4])
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[0 + i * 4])
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                         box_lst.append([a,f])

                         f = col2.checkbox(f'2{i}')
                         if f == True:
                              true_ct += 1
                              if lst[1 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append('')
                                   b = col2.selectbox(f"Select 2{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[1 + i * 4]]
                                   empty.append('')
                                   b = col2.selectbox(f"Select 2{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[1 + i * 4])
                                   b = col2.selectbox(f"Select 2{i}:", empty)
                         else:
                              if lst[1 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append(lst[1 + i * 4])
                                   b = col2.selectbox(f"Select 2{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[1 + i * 4])
                                   b = col2.selectbox(f"Select 2{i}:", empty)
                         box_lst.append([b, f])

                         f = col3.checkbox(f'3{i}')
                         if f == True:
                              true_ct += 1
                              if lst[2 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append('')
                                   c = col3.selectbox(f"Select 3{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[2 + i * 4]]
                                   empty.append('')
                                   c = col3.selectbox(f"Select 3{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[2 + i * 4])
                                   c = col3.selectbox(f"Select 3{i}:", empty)
                         else:
                              if lst[2 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append(lst[2 + i * 4])
                                   c = col3.selectbox(f"Select 3{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[2 + i * 4])
                                   c = col3.selectbox(f"Select 3{i}:", empty)
                         box_lst.append([c, f])

                         f = col4.checkbox(f'4{i}')
                         if f == True:
                              true_ct += 1
                              if lst[3 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append('')
                                   d = col4.selectbox(f"Select 4{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[3 + i * 4]]
                                   empty.append('')
                                   d = col4.selectbox(f"Select 4{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[3 + i * 4])
                                   d = col4.selectbox(f"Select 4{i}:", empty)
                         else:
                              if lst[3 + i * 4] == "Empty":
                                   empty = []
                                   #empty.append(lst[3 + i * 4])
                                   d = col4.selectbox(f"Select 4{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[3 + i * 4])
                                   d = col4.selectbox(f"Select 4{i}:", empty)
                         box_lst.append([d, f])
                    #st.write(box_lst)
                    ct = 0

                    check = []
                    for j in (box_lst):
                         if True in j:
                              st.write(str(ct) +'--->'+str(lst[ct]))
                              if '' in j:
                                   j[0] = lst[ct]
                         ct += 1
                         if "" not in j and None not in j:
                              check.append(j[0])
                    st.write((check))
                    # st.markdown('Streamlit is **_really_ cool**.')
                    # st.markdown('This text is: red[colored], and this is **:blue[colored] ** and bold.')
                    # st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
                    if check == []:
                         st.markdown(":red[$Pick Two Cards!$] :warning:")
                    if len(check) > 2:
                         st.markdown("**_:red[Two Cards Only!]_** :warning:")
                    if len(check) >= 2:
                         if check[0] in ques:
                              if check[1] in ans:
                                   if ques.index(check[0]) == ans.index(check[1]):
                                        # ran_lst.remove(ran_lst(ques.index(check[0])))
                                        # ran_lst.remove(ran_lst(ans.index(check[1])+7))
                                        st.write(ran_lst.index(ques.index(check[0])))
                                        st.write(ran_lst.index(ans.index(check[1])+8))#+8 +len(quiz)
                                        ran_lst[ran_lst.index(ques.index(check[0]))] = 'Empty'
                                        ran_lst[ran_lst.index(ans.index(check[1])+8)] = 'Empty'#+8 +len(quiz)
                                        db.insert_memquiz(TODAY, ran_lst,ran_note)
                                        st.success("Correct!:ok_hand:")
                                        st.markdown(':trophy::trophy:')
                                        db.save_coin("3", TODAY)
                                   else:
                                        st.warning("WA:shit:")
                                        db.save_coin("-2", TODAY)
                              else:
                                   st.warning("WA:persevere:")
                                   db.save_coin("-2", TODAY)
                         elif check[1] in ques:
                              if check[0] in ans:
                                   if ques.index(check[1]) == ans.index(check[0]):
                                        st.write((ques.index(check[1])))
                                        st.write((ans.index(check[0])+8))#+8+len(quiz)
                                        ran_lst[ran_lst.index(ques.index(check[1]))] = 'Empty'
                                        ran_lst[ran_lst.index(ans.index(check[0])+8)] = 'Empty'#+8+len(quiz)
                                        db.insert_memquiz(TODAY, ran_lst,ran_note)
                                        st.success("Correct!:thumbsup:")
                                        st.markdown(':mahjong::mahjong:')
                                        db.save_coin("3", TODAY)
                                   else:
                                        st.warning("WA:anguished:")
                                        st.markdown(':space_invader:')
                                        db.save_coin("-2", TODAY)
                              else:
                                   st.warning("WA:confused:")
                                   db.save_coin("-2", TODAY)
                         else:
                              st.warning("WA:sweat:")
                              db.save_coin("-2", TODAY)
                    empty_ct = 0
                    for i in (ran_lst):
                         if i == "Empty":
                              empty_ct += 1
                    if empty_ct == len(ran_lst):
                         st.success("Well Done!:punch:")
                         sub2 = st.form_submit_button("Restart:recycle:")
                         if sub2:
                              st.write("StartOver")
                              ran_lst = []
                              while len(ran_lst) < 16:
                                   ran = random.randint(0, 15)
                                   if ran not in ran_lst:
                                        ran_lst.append(ran)
                                   # st.write(ran_lst)
                              ran_note = []
                              while len(ran_note) < 16:
                                   ran = random.randint(0, len(quiz) - 1)  # (0, 15) len(quiz)-1
                                   if ran not in ran_note:
                                        ran_note.append(ran)
                              db.insert_memquiz(TODAY, ran_lst, ran_note)


                    else:
                         sub = st.form_submit_button("SUB")

#-----------------6 By 6 Game----------------------------------------------------------------
          if len(quiz) >= 1800000: #18
               # with st.form("Entry_form22", clear_on_submit=True):
               #      size2 = st.form_submit_button("6*6")
               # if size2:
               with st.form("Entry_form2", clear_on_submit=True):
                    # ques = ['1','2','3','4','5','6','7','8']
                    # ans = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']
                    # st.write(db.fetch_memquiz())
                    if db.fetch_memquiz() == [] or len(db.fetch_memquiz()[-1]['RandQuiz'])!=36:
                         ran_lst = []
                         while len(ran_lst) < 36:
                              ran = random.randint(0, 35)
                              if ran not in ran_lst:
                                   ran_lst.append(ran)
                              # st.write(ran_lst)
                         db.insert_memquiz(TODAY, ran_lst)
                    else:
                         try:
                              ran_lst = db.fetch_memquiz()[-1]['RandQuiz']
                         except IndexError:
                              st.write("IndexERROR")
                    lst = []
                    for k in ran_lst:
                         if k == 'Empty':
                              lst.append('Empty')
                         elif k <= 17:
                              lst.append(ques[k])
                         else:
                              lst.append(ans[k - 18])
                    #st.write(ques)
                    #st.write(ans)
                    #st.write(lst)
                    box_lst = []
                    true_ct = 0
                    for i in range(6):
                         col1, col2, col3, col4, col5, col6 = st.columns(6)

                         f = col1.checkbox(f'1{i}')
                         if f == True:
                              true_ct += 1
                              if lst[0 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append('')
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                              elif true_ct <= 2:
                                   empty = [lst[0 + i * 6]]
                                   empty.append('')
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[0 + i * 6])
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                         else:
                              if lst[0 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append(lst[0 + i * 4])
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[0 + i * 6])
                                   a = col1.selectbox(f"Select 1{i}:", empty)
                         box_lst.append([a, f])

                         f = col2.checkbox(f'2{i}')
                         if f == True:
                              true_ct += 1
                              if lst[1 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append('')
                                   b = col2.selectbox(f"Select 2{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[1 + i * 6]]
                                   empty.append('')
                                   b = col2.selectbox(f"Select 2{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[1 + i * 6])
                                   b = col2.selectbox(f"Select 2{i}:", empty)
                         else:
                              if lst[1 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append(lst[1 + i * 4])
                                   b = col2.selectbox(f"Select 2{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[1 + i * 6])
                                   b = col2.selectbox(f"Select 2{i}:", empty)
                         box_lst.append([b, f])

                         f = col3.checkbox(f'3{i}')
                         if f == True:
                              true_ct += 1
                              if lst[2 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append('')
                                   c = col3.selectbox(f"Select 3{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[2 + i * 6]]
                                   empty.append('')
                                   c = col3.selectbox(f"Select 3{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[2 + i * 6])
                                   c = col3.selectbox(f"Select 3{i}:", empty)
                         else:
                              if lst[2 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append(lst[2 + i * 4])
                                   c = col3.selectbox(f"Select 3{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[2 + i * 6])
                                   c = col3.selectbox(f"Select 3{i}:", empty)
                         box_lst.append([c, f])

                         f = col4.checkbox(f'4{i}')
                         if f == True:
                              true_ct += 1
                              if lst[3 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append('')
                                   d = col4.selectbox(f"Select 4{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[3 + i * 6]]
                                   empty.append('')
                                   d = col4.selectbox(f"Select 4{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[3 + i * 6])
                                   d = col4.selectbox(f"Select 4{i}:", empty)
                         else:
                              if lst[3 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append(lst[3 + i * 4])
                                   d = col4.selectbox(f"Select 4{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[3 + i * 6])
                                   d = col4.selectbox(f"Select 4{i}:", empty)
                         box_lst.append([d, f])

                         f = col5.checkbox(f'5{i}')
                         if f == True:
                              true_ct += 1
                              if lst[4 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append('')
                                   d = col5.selectbox(f"Select 5{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[4 + i * 6]]
                                   empty.append('')
                                   d = col5.selectbox(f"Select 5{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[4 + i * 6])
                                   d = col5.selectbox(f"Select 5{i}:", empty)
                         else:
                              if lst[4 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append(lst[3 + i * 4])
                                   d = col5.selectbox(f"Select 5{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[4 + i * 6])
                                   d = col5.selectbox(f"Select 5{i}:", empty)
                         box_lst.append([d, f])

                         f = col6.checkbox(f'6{i}')
                         if f == True:
                              true_ct += 1
                              if lst[5 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append('')
                                   d = col6.selectbox(f"Select 6{i}:", empty)  # , key="month"
                              elif true_ct <= 2:
                                   empty = [lst[5 + i * 6]]
                                   empty.append('')
                                   d = col6.selectbox(f"Select 6{i}:", empty)  # , key="month"
                              else:
                                   empty = ['']
                                   empty.append(lst[5 + i * 6])
                                   d = col6.selectbox(f"Select 6{i}:", empty)
                         else:
                              if lst[5 + i * 6] == "Empty":
                                   empty = []
                                   # empty.append(lst[3 + i * 4])
                                   d = col6.selectbox(f"Select 6{i}:", empty)
                              else:
                                   empty = ['']
                                   empty.append(lst[5 + i * 6])
                                   d = col6.selectbox(f"Select 6{i}:", empty)
                         box_lst.append([d, f])

                    #st.write(box_lst)
                    ct = 0

                    check = []
                    for j in (box_lst):
                         if True in j:
                              st.write(str(ct) + '--->' + str(lst[ct]))
                              if '' in j:
                                   j[0] = lst[ct]
                         ct += 1
                         if "" not in j and None not in j:
                              check.append(j[0])
                    #st.write((check))
                    # st.markdown('Streamlit is **_really_ cool**.')
                    # st.markdown('This text is: red[colored], and this is **:blue[colored] ** and bold.')
                    # st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
                    if check == []:
                         st.markdown(":red[$Pick Two Cards!$] :warning:")
                    if len(check) > 2:
                         st.markdown("**_:red[Two Cards Only!]_** :warning:")
                    if len(check) >= 2:
                         if check[0] in ques:
                              if check[1] in ans:
                                   if ques.index(check[0]) == ans.index(check[1]):
                                        # ran_lst.remove(ran_lst(ques.index(check[0])))
                                        # ran_lst.remove(ran_lst(ans.index(check[1])+7))
                                        st.write(ran_lst.index(ques.index(check[0])))
                                        st.write(ran_lst.index(ans.index(check[1]) + 18))
                                        ran_lst[ran_lst.index(ques.index(check[0]))] = 'Empty'
                                        ran_lst[ran_lst.index(ans.index(check[1]) + 18)] = 'Empty'
                                        db.insert_memquiz(TODAY, ran_lst)
                                        st.success("Correct!:ok_hand:")
                                        st.markdown(':trophy::trophy:')
                                        db.save_coin("3", TODAY)
                                   else:
                                        st.warning("WA:shit:")
                                        db.save_coin("-2", TODAY)
                              else:
                                   st.warning("WA:persevere:")
                                   db.save_coin("-2", TODAY)
                         elif check[1] in ques:
                              if check[0] in ans:
                                   if ques.index(check[1]) == ans.index(check[0]):
                                        st.write((ques.index(check[1])))
                                        st.write((ans.index(check[0]) + 18))
                                        ran_lst[ran_lst.index(ques.index(check[1]))] = 'Empty'
                                        ran_lst[ran_lst.index(ans.index(check[0]) + 18)] = 'Empty'
                                        db.insert_memquiz(TODAY, ran_lst)
                                        st.success("Correct!:thumbsup:")
                                        st.markdown(':mahjong::mahjong:')
                                        db.save_coin("3", TODAY)
                                   else:
                                        st.warning("WA:anguished:")
                                        st.markdown(':space_invader:')
                                        db.save_coin("-2", TODAY)
                              else:
                                   st.warning("WA:confused:")
                                   db.save_coin("-2", TODAY)
                         else:
                              st.warning("WA:sweat:")
                              db.save_coin("-2", TODAY)
                    empty_ct = 0
                    for i in (ran_lst):
                         if i == "Empty":
                              empty_ct += 1
                    if empty_ct == len(ran_lst):
                         st.success("Well Done!:punch:")
                         sub2 = st.form_submit_button("Restart:recycle:")
                         if sub2:
                              st.write("StartOver")
                              ran_lst = []
                              while len(ran_lst) < 36:
                                   ran = random.randint(0, 35)
                                   if ran not in ran_lst:
                                        ran_lst.append(ran)
                                   # st.write(ran_lst)
                              db.insert_memquiz(TODAY, ran_lst)


                    else:
                         sub = st.form_submit_button("SUB")

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

#---------seems like csv files with mandarin cannot be retrieved and formed into dataframe with correct characters
     # st.text(type(ct))
     # def Convert(lst):
     #     res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
     #     return res_dct

#----------------Date Order Chaos-------------------------
# st.write('data',data['Date'][i])dates1 = ''
                #             dates2 = ''
                #             dates_ct = 1
                # st.write('clean',clean_data['Tasks'][j])
                # if clean_data['Tasks'][j] == data['Date'][i]:
                #
                #     data['Date'][i] = '0'
                #
                #     st.write("YYYYYYYYY")
                # if len(data[key]) == 1:
                #     clean_data['Date'].append(data['Date'][0])
                #     clean_data['Tasks'].append(1)
                # else:
                #     try:
                #         if i == 1:
                #             clean_data['Date'].append(data['Date'][0])
                #         dates1 = data['Date'][i]
                #         ct = i + 1
                #         while ct <= len(data['Date']):
                #             st.write(data['Date'])
                #             dates2 = data['Date'][ct]
                #             if dates1 == dates2 and dates1 != '0' and dates2 != '0':
                #                 dates_ct += 1
                #                 data['Date'][ct] = '0'
                #
                #             else:
                #                 if dates2 != '0' and dates1 != '0' and dates2!=dates1:
                #                     clean_data['Date'].append(dates2)
                #                 clean_data['Tasks'].append(dates_ct)
                #                 dates_ct = 1
                #             ct += 1
                #     except IndexError:
                #         #clean_data['Tasks'].append(dates_ct)
                #         pass


# st.write(data)
# elif result[i] != 'Status':
#     data[key].append(result[i][count])
#     count += 1
# st.write(data)

    # for stat in range(len(data['Status'])):
    #     st.write(data['Status'][stat])
    #     if data['Status'][stat] != 'ToDo' and stat < len(data['Status']):
    #         data['Task'] = data['Task'][:stat].append(data['Task'][stat+1:])
    #         data['Status'] = data['Status'][:stat].append(data['Task'][stat + 1:])
    #         data['Date'] = data['Date'][:stat].append(data['Date'][stat + 1:])
    #         st.write(data)
    #     if data['Status'][stat] != 'ToDo' and stat == len(data['Status']):
    #         data['Task'] = data['Task'][:stat]
    #         data['Status'] = data['Status'][:stat]
    #         data['Date'] = data['Date'][:stat]
    #         st.write(data)

# st.text(f"Comment: {comment}") #                 # st.text(value)
# st.text(incomes)st.text(label)
#                 # st.text(source)# st.text(expenses)
#                 #                 # st.text(list(range(len(incomes))))
#                 # st.text(target)
#

#random.shuffle(ans)
        # ans_shuffle.append(ans)
        #st.write(ans_shuffle)
        # st.write(ans)
        # ans_shuffle = list(random.shuffle(ans))
        # ans_shuffle.append(ans)
        # st.write(ans_shuffle)

# n_correct = db.fetch_quiz()[-1]["Correct"]
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
# st.write((sa))
# st.write(question)
# st.write(ans)

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
                              # db.insert_quiz(quiz, TODAY)
                              # submitted = st.form_submit_button("Restart")
                              # if submitted:
                              # db.insert_quiz([],TODAY)
                              # pass
                    # elif submitted2 and n_correct==False:
                    #     st.warning("WA")

# db.insert_quiz(str(quiz), TODAY, (question_shuffle), (ans_shuffle), n_correct)
# ans_shuffle = [n for n in ans]
# question_shuffle = [q for q in question]
# col1, col2 = st.columns(2)
# sq = col1.selectbox("Select Question:", question_shuffle)  # , key="month"
# sa = col2.selectbox("Select Ans:", ans_shuffle)  # , key="year"
# submitted3 = st.form_submit_button("Continue")
# if submitted3:
