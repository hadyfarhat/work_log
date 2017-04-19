import datetime


class Entry:
    task_name = None
    minutes = None
    notes = None
    created_at = None

    def __init__(self):
        self.get_task_details()

    # get task name, num of minutes and notes if required
    def get_task_details(self):
        self.task_name = input("Enter the name of the task: ")
        self.minutes = self.get_minutes()
        self.notes = self.get_notes()
        self.created_at = datetime.datetime.now()

    # get num of minutes and verify it
    # the user should enter a valid input
    def get_minutes(self):
        while True:
            minutes = input("Enter the number of minutes spent on the task: ")
            try:
                minutes = int(minutes)
                return minutes
            except ValueError:
                print("Please Enter a valid num of minutes")

    # print task info
    def get_task_info(self):
        print("You created your task at")
        created_at_formatted = self.created_at.strftime("%m/%d/%Y %H:%M")
        print("{}".format(created_at_formatted))

    # get notes if the user wants to
    # else: leave it with a value of None
    def get_notes(self):
        answer = input("Do you want to write any note on this task ? N/y >>> ")
        if answer.lower() == "y":
            note = input("Enter your note >>> ")
            return note
        else:
            self.notes = None
            print("Alright. No notes are added")
