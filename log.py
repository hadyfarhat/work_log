import datetime
import sys

from entry import Entry


# clear screen funciton
def clear():
    print("\033c", end="")


# prints a new line
def new_line():
    print("\n")


class Log():
    entries = []

    # menu message
    menu = """
    1- Add new entry
    2- Lookup previous entries
    3- Delete entry
    4- Edit entry
    5- Quit
    """

    previous_entries_menu = """
    1- Find by Date
    2- Find by Time Spent
    3- Find by Exact Search
    4- Find by Pattern
    5- Find by Date Range
    """

    def __init__(self):
        test = input("[t]esting or [r]unning >>> ")
        if test == "r":
            while True:
                self.game_menu()
                input("Press Enter to continue")
                clear()
        else:
            # testing
            self.game_menu()

    def game_menu(self):
        print(self.menu)
        user_option = self.get_main_menu_option()
        # run the command the user entered
        self.run(int(user_option))

    # user should enter either 1 or 2
    def get_main_menu_option(self):
        while True:
            user_option = input("Enter an option >>> ")
            if user_option:
                if user_option in ["1", "2", "3", "4", "5"]:
                    print("Good option")
                    return user_option
                else:
                    print("Please enter either of these [1,2,3,4,5]")
            else:
                print("Please enter an input")

    # run a menu command
    def run(self, command):
        if command == 1:
            # create an entry and append it to entries
            self.e = Entry()
            self.entries.append(self.e)
        elif command == 2:
            self.search_entries()
        elif command == 3:
            self.delete_entry()
        elif command == 4:
            self.edit_entry()
        elif command == 5:
            sys.exit()

    # search for previous entries
    def search_entries(self):
        # display a menu and get an option
        menu_option = self.get_previous_entries_menu_option()
        if menu_option == 1:
            self.find_by_date()
        elif menu_option == 2:
            self.find_by_time_spent()
        elif menu_option == 3:
            self.find_by_exact_search()
        elif menu_option == 4:
            pass
        elif menu_option == 5:
            self.find_by_date_range()

    # user should enter a valid menu option
    def get_previous_entries_menu_option(self):
        while True:
            print(self.previous_entries_menu)
            # user should enter a valid option
            while True:
                menu_option = input("Enter a valid option >>> ")
                try:
                    menu_option = int(menu_option)
                    break
                except ValueError:
                    print("Please Enter a valid option [1,2,3,4,5]")

            if menu_option in [1, 2, 3, 4, 5]:
                return menu_option
            else:
                print("Please Enter a valid menu option [1,2,3,4]")

    # find entry by date
    def find_by_date(self):
        # keep looping till user enters a valid date
        while True:
            date_search_format = input("Enter a date mm/dd/yyyy >>> ")
            try:
                date_search = datetime.datetime.strptime(date_search_format,
                                                         "%m/%d/%Y")
                break
            except ValueError:
                print("Please enter a valid date")

        entries_found = []
        for entry in self.entries:
            if entry.created_at.year == date_search.year:
                if entry.created_at.month == date_search.month:
                    if entry.created_at.day == date_search.day:
                        entries_found.append(entry)

        if entries_found:
            self.print_entries_found(entries_found, "date")
        else:
            print("No entries were found based"
                  "on your date search {}".format(date_search_format))

    # find entry by time spent
    def find_by_time_spent(self):
        # keep looping till user enters a valid time
        while True:
            time_search = input("Enter a number of minutes >>> ")
            try:
                time_search = int(time_search)
                break
            except ValueError:
                print("Please Enter a valid number of minutes. ex: 13")

        entries_found = []
        for entry in self.entries:
            if entry.minutes == time_search:
                entries_found.append(entry)

        if entries_found:
            self.print_entries_found(entries_found, "time")
        else:
            print("No entries were found based on your "
                  "time search {}".format(time_search))

    # find entry by exact search
    def find_by_exact_search(self):
        entry_search = input("Enter an exact entry task name or note >>> ")
        entries_found = []
        if entry_search:
            for entry in self.entries:
                if (entry.task_name == entry_search or
                        entry.notes == entry_search):
                        entries_found.append(entry)

        if entries_found:
            self.print_entries_found(entries_found, "exact entry")
        else:
            print("No entries were found based on your "
                  "exact entry search {}".format(entry_search))

        # find by date range For example between 01/01/2016 and 12/31/2016.
    def find_by_date_range(self):
        # user should enter a valid date
        # first date
        while True:
            first_date_format = input("Enter the first date mm/dd/yyyy >>> ")
            try:
                first_date = datetime.datetime.strptime(first_date_format,
                                                        "%m/%d/%Y")
                break
            except ValueError:
                print("Please enter a valid date")
                print("Press Enter to continue")
                clear()

        # second date
        while True:
            second_date_format = input("Enter the second date mm/dd/yyyy >>> ")
            try:
                second_date = datetime.datetime.strptime(second_date_format,
                                                        "%m/%d/%Y")
                break
            except ValueError:
                print("Please enter a valid date")
                print("Press Enter to continue")
                clear()

        # calculate number of dates between first and second dates
        days = (second_date - first_date).days
        # array of all dates between the first and second dates
        dates = []
        for i in range(1, days+1):
            dates.append(first_date + datetime.timedelta(days=i))

        entries_found = []
        for date in dates:
            for entry in self.entries:
                if entry.created_at.year == date.year:
                    if entry.created_at.month == date.month:
                        if entry.created_at.day == date.day:
                            entries_found.append(entry)

        if entries_found:
            for entry in entries_found:
                self.display_entry(entry)
        else:
            print("No entries were found")

    # printes all entries that match the user's input
    def print_entries_found(self, entries_found, search_type):
        new_line()
        print("These entries were found based on your {} search ".format(
                                                                search_type
                                                                ))
        print("Note the time displayed is in a 24 hour clock format")
        print(30*"=")
        new_line()
        for entry_found in entries_found:
            self.display_entry(entry_found)

    # delete an entry
    # def 

    # enable the user to change date, task_name, time_spent, notes
    def edit_entry(self):
        if self.entries:
            while True:
                entry_found = False
                entry_search = input("Enter an entry's task name: ")
                count = 0
                for entry in self.entries:
                    if entry.task_name == entry_search:
                        entry_found = True
                        entry_search = entry
                        if entry_found:
                            break
                        count+=1
                        
                if not entry_found:
                    print("No entries were found basded on that search")
                    answer = input("[S]earch again | [B]ack to menu: ")
                    if answer.lower() == "b":
                        break
                else:
                    clear()
                    self.display_entry(entry_search)
                    # keep looping till user enters valid option
                    while True:
                        print("1- Change date")
                        print("2- Change task name")
                        print("3- Change time spent")
                        print("4- Change notes (if the entry has one)")
                        print("5- Return back to menu")
                        option = input("Enter an option: ")
                        if option in ["1", "2", "3", "4", "5"]:
                            if option == "1":
                                self.edit_entry_date(count)
                            elif option == "2":
                                self.edit_entry_task_name(count)
                            elif option == "3":
                                self.edit_entry_time_spent(count)
                            elif option == "4":
                                self.edit_entry_notes(count)
                            elif option == "5":
                                return None
                        else:
                            print("Please enter a valid option")
                            input("Press Enter to continue ")
                            clear()
                        input("Press Enter to continue... ")
                        clear()
        else:
            print("No entries were found")

    # change date; helper function for edit_entry()
    def edit_entry_date(self, count):
        # user should enter a valid date
        while True:
            user_date_format = input("Enter date mm/dd/yyyy >>> ")
            try:
                user_date = datetime.datetime.strptime(user_date_format,
                                                       "%m/%d/%Y")
                break
            except ValueError:
                print("Please enter a valid date")

        print("Replacing your entry's date ....")
        self.entries[count].created_at =self.entries[count].created_at.replace(
                                               year=user_date.year,
                                               month=user_date.month,
                                               day=user_date.day)
        print("Entry date was changed successfully to {}".format(
                                            self.entries[count].created_at))

    # change entry task name; helper function for edit_entry()
    def edit_entry_task_name(self, count):
        new_name = input("Enter a new name for your entry >>> ")
        print("Changing your entry's name")
        self.entries[count].task_name = new_name
        print("Your entry's name was successfully changed to {}".format(
                                                self.entries[count].task_name))

    # change entry time spent; helper function for edit_entry()
    def edit_entry_time_spent(self, count):
        # user should enter a number
        while True:
            new_time = input("Enter the # of minutes spent on the entry >>> ")
            try:
                new_time = int(new_time)
                break
            except ValueError:
                print("Please enter a number")
                input("Press Enter to continue... ")
                clear()
        print("Changing your entry's time spent ...")
        self.entries[count].minutes = new_time
        print("Your entry's time spent was successfully changed to {}".format(
                                                self.entries[count].minutes))

    # change entry notes; helper function for edit_entry()
    def edit_entry_notes(self, count):
            new_note = input("Enter your new note: ")
            self.entries[count].notes = new_note

    # display entry with date, task name, time spent, and notes information.
    def display_entry(self, entry):
        new_line()
        print("Entry name: {}".format(entry.task_name,))
        print("\t- created at {}".format(entry.created_at.strftime(
                                                        "%m/%d/%Y %H:%M")))
        print("\t- Time Spent: {}".format(entry.minutes))
        if entry.notes:
            print("\t- Additional Notes: {}".format(entry.notes))
        else:
            print("\t- Additional Notes: No notes were "
                  "added to this entry")
        print(20*"-")




