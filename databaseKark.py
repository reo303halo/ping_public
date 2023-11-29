import mysql.connector
from mysql.connector import errorcode


class DataBase:
    def __init__(self):
        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v22_olsenroy',
                    'password': '********', #Password is ** for privacy reasons. 
                    'database': 'stud_v22_olsenroy'}

        self.configuration = dbconfig


    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared = True)
        return self


    def __exit__(self, exc_type, exc_val, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    




    def getQuestionsBySubject(self, subject_id):
        try:   
            self.cursor.execute('SELECT * FROM ping_questions WHERE subject = (%s);', (subject_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    

    def addMultiQuestion(self, question, options, correctAnswer, subject, user_id):
        try:
            self.cursor.execute('INSERT INTO ping_questions (questions, options, correctAnswer, subject, author_id) VALUES(%s, %s, %s, %s, %s);', (question, options, correctAnswer, subject, user_id,))
        except mysql.connector.Error as err:
                print(err)


    def addQuestion(self, question, subject, user_id):
        try:
            self.cursor.execute('INSERT INTO ping_questions (questions, subject, author_id) VALUES(%s, %s, %s);', (question, subject, user_id,))
        except mysql.connector.Error as err:
                print(err)


    def deleteQuestionById(self, question_id):
        try:
            self.cursor.execute('DELETE FROM ping_questions WHERE question_id = (%s)', (question_id,))
        except mysql.connector.Error as err:
                print(err)

        
    def createQuizID(self, quiz_id, user_id):
        try:
            self.cursor.execute('INSERT INTO ping_quiz (quiz_id, user_id) VALUES (%s, %s);', (quiz_id, user_id,))
        except mysql.connector.Error as err:
                print(err)

    
    def getQuizID(self, user_id):
        try:
            self.cursor.execute('SELECT quiz_id FROM ping_quiz WHERE user_id = (%s);', (user_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    

    def getCurrentQuestion(self, quiz_id):
        try:
            self.cursor.execute('''SELECT ping_questions.*, ping_qq_relations.answer_id
                                    FROM ping_questions 
                                    JOIN ping_qq_relations ON ping_qq_relations.question_id = ping_questions.question_id
                                    WHERE (ping_qq_relations.quiz_id = (%s) AND ping_qq_relations.current = 1);''', (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    

    def resetCurrent(self, quiz_id):
        try:
            self.cursor.execute("UPDATE ping_qq_relations SET current = 0 WHERE quiz_id = (%s)", (quiz_id,))
        except mysql.connector.Error as err:
                print(err)


    def setCurrent(self, quiz_id, q_id):
        try:
            self.cursor.execute("INSERT IGNORE INTO ping_qq_relations (quiz_id, question_id) VALUES (%s, %s);", (quiz_id, q_id,))
            self.cursor.execute("UPDATE ping_qq_relations SET current = 1 WHERE (quiz_id = (%s) AND question_id = (%s));", (quiz_id, q_id,))
        except mysql.connector.Error as err:
                print(err)


    def deleteAnswers(self):
        try:
            self.cursor.execute("DELETE FROM ping_answers;")
        except mysql.connector.Error as err:
                print(err)

        # WHERE answer_id = (%s);", (answer_id,)
        # Only delete answers related to the session for the teacher who is exciquting the quit.




    def getSubjects(self, parent_id):
        try:
            self.cursor.execute("SELECT * FROM ping_subjects WHERE parent_id = (%s);", (parent_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    

    def createSubject(self, subject_name, parent_id):
        try:
            self.cursor.execute("INSERT INTO ping_subjects (subject_name, parent_id) VALUES(%s, %s);", (subject_name, parent_id,))
        except mysql.connector.Error as err:
                print(err)
    

    def deleteSubject(self, subject_id):
        try:
            self.cursor.execute("DELETE FROM ping_subjects WHERE subject_id = (%s)", (subject_id,)) #Trenger trigger for å slette undermapper og innhold
        except mysql.connector.Error as err:
                print(err)






    def addAnswer(self, answer_id, answer):
        try:
            self.cursor.execute('INSERT INTO ping_answers (answers_id, answer) VALUES(%s, %s);', (answer_id, answer,))
        except mysql.connector.Error as err:
                print(err) 
    

    def getAnswers(self, quiz_id):
        try:
            self.cursor.execute("""SELECT ping_answers.*
                                    FROM ping_answers 
                                    JOIN ping_qq_relations ON ping_qq_relations.answer_id = ping_answers.answers_id
                                    WHERE (ping_qq_relations.quiz_id = (%s) AND ping_qq_relations.current = 1);""", (quiz_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err) 
        return result

    

    


    def getUserById(self, user_id):    
        try:
            self.cursor.execute("SELECT * FROM ping_users WHERE user_id = (%s);", (user_id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err) 
        return result
    

    def getUser(self, email):   
        try:
            self.cursor.execute("SELECT * FROM ping_users WHERE e_mail = (%s);", (email,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err) 
        return result


    def createUser(self, user):
        try:
            self.cursor.execute('''INSERT INTO ping_users(e_mail, password, firstname, lastname, uuid)
                    VALUES(%s, %s, %s, %s, %s)''', user)
        except mysql.connector.Error as err:
                print(err) 
