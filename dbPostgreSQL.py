import psycopg2
from psycopg2 import Error


class DataBase:
    def __init__(self):
        self.connection = psycopg2.connect(host="ec2-18-204-162-101.compute-1.amazonaws.com",
                                dbname="*********",
                                user="*********",
                                password="*********",
                                port=5432)
        
        
    def __enter__(self):
        try:
            self.cursor = self.connection.cursor()
            return self

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    

    


    def getVersion(self):
        self.cursor.execute("SELECT version();")
        record = self.cursor.fetchone()
        print("You are connected to - ", record, "\n")






    def getQuestionsBySubject(self, subject_id):
        self.cursor.execute('SELECT * FROM ping_questions WHERE subject = (%s);', (subject_id,))
        result = self.cursor.fetchall()

        return result
    

    def addMultiQuestion(self, question, options, correctAnswer, subject, user_id):
        self.cursor.execute('INSERT INTO ping_questions (questions, options, correctAnswer, subject, author_id) VALUES(%s, %s, %s, %s, %s);', (question, options, correctAnswer, subject, user_id,))


    def addQuestion(self, question, subject, user_id):
        self.cursor.execute('INSERT INTO ping_questions (questions, subject, author_id) VALUES(%s, %s, %s);', (question, subject, user_id,))


    def deleteQuestionById(self, question_id):
        self.cursor.execute('DELETE FROM ping_questions WHERE question_id = (%s)', (question_id,))


    def createQuizID(self, quiz_id, user_id):
        self.cursor.execute('INSERT INTO ping_quiz (quiz_id, user_id) VALUES (%s, %s);', (quiz_id, user_id,))

    
    def getQuizID(self, user_id):
        self.cursor.execute('SELECT quiz_id FROM ping_quiz WHERE user_id = (%s);', (user_id,))
        result = self.cursor.fetchall() #fetchone()

        return result
    

    def getCurrentQuestion(self, quiz_id):
        self.cursor.execute('''SELECT ping_questions.*, ping_qq_relations.answer_id
                                FROM ping_questions 
                                JOIN ping_qq_relations ON ping_qq_relations.question_id = ping_questions.question_id
                                WHERE (ping_qq_relations.quiz_id = (%s) AND ping_qq_relations.current = 1);''', (quiz_id,))
        return self.cursor.fetchall()

    

    def resetCurrent(self, quiz_id):
        self.cursor.execute("UPDATE ping_qq_relations SET current = 0 WHERE quiz_id = (%s)", (quiz_id,))


    def setCurrent(self, quiz_id, q_id):
        self.cursor.execute("INSERT INTO ping_qq_relations (quiz_id, question_id) VALUES (%s, %s);", (quiz_id, q_id,))
        self.cursor.execute("UPDATE ping_qq_relations SET current = 1 WHERE (quiz_id = (%s) AND question_id = (%s));", (quiz_id, q_id,))


    def getAnswersById(self, quiz_id):
        self.cursor.execute('''SELECT answers_id FROM ping_answers 
                                JOIN ping_qq_relations ON ping_qq_relations.answer_id = ping_answers.answers_id 
                                WHERE ping_qq_relations.quiz_id = (%s);''', (quiz_id,))
        return self.cursor.fetchall()


    def deleteAnswers(self, answer_id):
        self.cursor.execute("DELETE FROM ping_answers WHERE answers_id = (%s);", (answer_id,))

        



    def getSubjects(self, parent_id):
        self.cursor.execute("SELECT * FROM ping_subjects WHERE parent_id = (%s);", (parent_id,))
        result = self.cursor.fetchall()

        return result
    

    def createSubject(self, subject_name, parent_id):
        self.cursor.execute('INSERT INTO ping_subjects (subject_name, parent_id) VALUES(%s, %s);', (subject_name, parent_id))


    def deleteSubject(self, subject_id):
        self.cursor.execute("DELETE FROM ping_subjects WHERE subject_id = (%s)", (subject_id,)) #Trenger trigger for å slette undermapper og innhold

    

    


    def addAnswer(self, answer_id, answer):
        self.cursor.execute('INSERT INTO ping_answers (answers_id, answer) VALUES(%s, %s);', (answer_id, answer))


    def getAnswers(self, quiz_id):
        self.cursor.execute("""SELECT ping_answers.*
                                FROM ping_answers 
                                JOIN ping_qq_relations ON ping_qq_relations.answer_id = ping_answers.answers_id
                                WHERE (ping_qq_relations.quiz_id = (%s) AND ping_qq_relations.current = 1);""", (quiz_id,))
        result = self.cursor.fetchall()

        return result

    

    


    def getUserById(self, user_id):    
        self.cursor.execute("SELECT * FROM ping_users WHERE user_id = (%s);", (user_id,))
        result = self.cursor.fetchall()

        return result
    

    def getUser(self, email):   
        self.cursor.execute("SELECT * FROM ping_users WHERE e_mail = (%s);", (email,))
        result = self.cursor.fetchall()

        return result


    def createUser(self, user):
        self.cursor.execute('''INSERT INTO ping_users(e_mail, password, firstname, lastname, uuid, verified)
                VALUES(%s, %s, %s, %s, %s, 1)''', user)



