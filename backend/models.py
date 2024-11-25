from datetime import datetime

class Profile:
    def __init__(self, user_id, name, surname, email, password, user_type='P', last_logged_in=None):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.user_type = user_type
        self.last_logged_in = last_logged_in or datetime.now()

class Test:
    def __init__(self, test_id, title, description, subject, datetime=None, sequence=False, max_time=None, user=None):
        self.test_id = test_id
        self.title = title
        self.description = description
        self.subject = subject
        self.datetime = datetime or datetime.now()
        self.sequence = sequence
        self.max_time = max_time
        self.user = user

class Question:
    def __init__(self, question_id, title, task, help_text=None, test=None):
        self.question_id = question_id
        self.title = title
        self.task = task
        self.help = help_text
        self.test = test

class FilledTest:
    def __init__(self, filled_test_id, test=None, user=None, date_time_beginning=None):
        self.filled_test_id = filled_test_id
        self.test = test
        self.user = user
        self.date_time_beginning = date_time_beginning or datetime.now()

class FilledQuestion:
    def __init__(self, question=None, solution="Test", is_correct=False, filled_test=None):
        self.question = question
        self.solution = solution
        self.is_correct = is_correct
        self.filled_test = filled_test

class CorrectSolution:
    def __init__(self, correct_solution_id, correct_solution_text, case_sensitive=False, question=None):
        self.correct_solution_id = correct_solution_id
        self.correct_solution_text = correct_solution_text
        self.case_sensitive = case_sensitive
        self.question = question

class Token:
    def __init__(self, id, user_id, token, created=None):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.created = created or datetime.now()