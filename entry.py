import datetime


class Entry:
    task_name = None
    minutes = None
    notes = None
    created_at = None

    def __init__(self, task_name=None, minutes=None,
                 created_at=None, notes=None):
        if task_name:
            self.task_name = task_name
            self.minutes = int(minutes)
            self.created_at = datetime.datetime.strptime(
                                                    created_at,
                                                    "%Y-%m-%d %H:%M:%S.%f")
            self.notes = notes
        else:
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
            if minutes:
                try:
                    minutes = int(minutes)
                    return minutes
                except ValueError:
                    print("Please Enter a valid num of minutes")
            else:
                print("Please enter a valid input. ex 12")

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

    def __str__(self):
        return """
        Task Name: {}
        Created At: {}
        Minutes Spend: {}
        Notes: {}
        """.format(self.task_name, self.created_at, self.minutes, self.notes)
