
class Question:
    def __init__(self, id, question, subject, options, correctAnswer, author_id):
        self.id = id
        self.question = question
        self.subject = subject

        if options != None:
            self.options = options.split(",")
        else:
            self.options = None

        self.correctAnswer = correctAnswer
        self.author_id = author_id
        