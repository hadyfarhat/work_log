import re
import datetime
import os.path
import csv
import sre_constants

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
        self.load_entries()
        while True:
            if self.game_menu() == "quit":
                break
            input("Press Enter to continue")
            clear()

    def load_entries(self):
        """load entries if they exist from csv file"""
        if os.path.exists("./entries.csv"):
            with open("entries.csv", "r") as csv_file:
                entry_reader = csv.reader(csv_file, delimiter=',')
                for row in entry_reader:
                    if row[0] == "task_name":
                        continue
                    else:
                        self.e = Entry(row[0], row[1], row[2], row[3])
                        self.entries.append(self.e)

        else:
            # just continue the program
            print("We found no history of any csv file. "
                  "We will create a new one.")

    def game_menu(self):
        print(self.menu)
        user_option = self.get_main_menu_option()
        # run the command the user entered
        if user_option == "5":
            return "quit"
        self.run(int(user_option))

    def get_main_menu_option(self):
        """user should enter either 1 or 2"""
        while True:
            user_option = input("Enter an option >>> ")
            if user_option:
                if user_option in ["1", "2", "3", "4", "5"]:
                    return user_option
                else:
                    print("Please enter either of these [1,2,3,4,5]")
            else:
                print("Please enter an input")

    def run(self, command):
        """run a menu command"""
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
            print("you quit")

    def search_entries(self):
        """search for previous entries"""
        # display a menu and get an option
        menu_option = self.get_previous_entries_menu_option()
        if menu_option == 1:
            self.find_by_date()
        elif menu_option == 2:
            self.find_by_time_spent()
        elif menu_option == 3:
            self.find_by_exact_search()
        elif menu_option == 4:
            self.find_by_pattern()
        elif menu_option == 5:
            self.find_by_date_range()

    def get_previous_entries_menu_option(self):
        """user should enter a valid menu option"""
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

    def find_by_date(self):
        """find entry by date"""
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
            entries = {}
            for i in range(len(entries_found)):
                entries[i] = entries_found[i]

            # user should enter a valid option
            while True:
                self.print_entries_found(entries, "date")
                option = self.get_option(entries)
                self.edit_entry(entries[option])
                break
        else:
            print("No entries were found based"
                  "on your date search {}".format(date_search_format))

    def find_by_time_spent(self):
        """find entry by time spent"""
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
            entries = {}
            for i in range(len(entries_found)):
                entries[i] = entries_found[i]
            # user should enter a valid option
            while True:
                self.print_entries_found(entries, "date")
                option = self.get_option(entries)
                self.edit_entry(entries[option])
                break
        else:
            print("No entries were found based on your "
                  "time search {}".format(time_search))

    def find_by_exact_search(self):
        """find entry by exact search"""
        entry_search = input("Enter an exact entry task name or note >>> ")
        entries_found = []
        if entry_search:
            for entry in self.entries:
                if (entry.task_name == entry_search or
                        entry.notes == entry_search):
                        entries_found.append(entry)

        if entries_found:
            entries = {}
            for i in range(len(entries_found)):
                entries[i] = entries_found[i]
            # user should enter a valid option
            while True:
                self.print_entries_found(entries, "date")
                option = self.get_option(entries)
                self.edit_entry(entries[option])
                break
        else:
            print("No entries were found based on your "
                  "exact entry search {}".format(entry_search))

    def find_by_pattern(self):
        """find by regex patter"""
        regex = input("Enter your regex >>> ")
        entries_found = []
        # check if the user entered a regex
        if regex:
            for entry in self.entries:
                try:
                    if (re.findall(r'{}'.format(regex), entry.task_name) or
                            re.findall(r"{}".format(regex), entry.notes)):
                            entries_found.append(entry)
                except sre_constants.error:
                    pass
        else:
            print("Please enter a regex")

        if entries_found:
            if entries_found:
                entries = {}
                for i in range(len(entries_found)):
                    entries[i] = entries_found[i]
                # user should enter a valid option
                while True:
                    self.print_entries_found(entries, "date")
                    option = self.get_option(entries)
                    self.edit_entry(entries[option])
                    break
            else:
                print("No entries were found based on your "
                      "exact entry search {}".format(regex))
        else:
            print("No entries were found based on your pattern")

    def find_by_date_range(self):
        """find by date range For example between 01/01/2016 and 12/31/2016."""
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
            entries = {}
            for i in range(len(entries_found)):
                entries[i] = entries_found[i]
            # user should enter a valid option
            while True:
                self.print_entries_found(entries, "date")
                option = self.get_option(entries)
                self.edit_entry(entries[option])
                break
        else:
            print("No entries were found")

    def print_entries_found(self, entries, search_type=None, delete=False):
        """printes all entries that match the user's input"""
        if not delete:
            new_line()
            if search_type:
                print("These entries were found based "
                      "on your {} search ".format(search_type))
            else:
                print("These entries were found: ")
            print("Note the time displayed is in a 24 hour clock format")
        print(30*"=")
        new_line()
        for key, value in entries.items():

            print("{}: {}".format(key, value))

    def delete_entry(self):
        """delete an entry"""
        entries = {}
        for i in range(len(self.entries)):
            entries[i] = self.entries[i]

        if entries:
            # user should enter a valid option
            while True:
                print("Which entry you wish to delelte ?")
                self.print_entries_found(entries, delete=True)
                option = self.get_option(entries)
                del self.entries[option]
                break
        else:
            print("No entries were found")

    def edit_entry(self, entry_search=None):
        """enable the user to change date, task_name, time_spent, notes"""
        if self.entries:
            while True:
                # if no entry is passed to the function
                # => get an entry
                if not entry_search:
                    entry_found = False
                    entries = {}
                    for i in range(len(self.entries)):
                        entries[i] = self.entries[i]

                    if entries:
                        # user should enter a valid option
                        while True:
                            print("Which entry you wish to edit ?")
                            self.print_entries_found(entries, search_type=None)
                            option = self.get_option(entries)
                            entry_search = self.entries[option]
                            break
                    else:
                        print("No entries were found")
                # if an entry is passed to the function
                # set entry_found to True
                else:
                    entry_found = True

                if entry_found:
                    clear()
                    # keep looping till user enters valid option
                    while True:
                        self.display_entry(entry_search)
                        print("1- Change date")
                        print("2- Change task name")
                        print("3- Change time spent")
                        print("4- Change notes")
                        print("5- Return back to menu")
                        option = input("Enter an option: ")
                        if option in ["1", "2", "3", "4", "5"]:
                            if option == "1":
                                self.edit_entry_date(entry_search)
                            elif option == "2":
                                self.edit_entry_task_name(entry_search)
                            elif option == "3":
                                self.edit_entry_time_spent(entry_search)
                            elif option == "4":
                                self.edit_entry_notes(entry_search)
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

    def edit_entry_date(self, entry_search):
        """change date; helper function for edit_entry()"""
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
        count = self.get_index(entry_search)
        self.entries[count].created_at = self.entries[
                                               count].created_at.replace(
                                               year=user_date.year,
                                               month=user_date.month,
                                               day=user_date.day)
        print("Entry date was changed successfully to {}".format(
                                            self.entries[count].created_at))

    def edit_entry_task_name(self, entry_search):
        """change entry task name; helper function for edit_entry()"""
        new_name = input("Enter a new name for your entry >>> ")
        print("Changing your entry's name")
        count = self.get_index(entry_search)
        self.entries[count].task_name = new_name
        print("Your entry's name was successfully changed to {}".format(
                                                self.entries[count].task_name))

    def edit_entry_time_spent(self, entry_search):
        """change entry time spent; helper function for edit_entry()"""
        # user should enter a number
        while True:
            new_time = input("Enter the # of minutes spent on the entry >>> ")
            try:
                new_time = int(new_time)
                break
            except ValueError:
                print("Please enter a number")
                input("Press Enter to continue... ")
        print("Changing your entry's time spent ...")
        count = self.get_index(entry_search)
        self.entries[count].minutes = new_time
        print("Your entry's time spent was successfully changed to {}".format(
                                                self.entries[count].minutes))

    def edit_entry_notes(self, entry_search):
        """change entry notes; helper function for edit_entry()"""
        new_note = input("Enter your new note: ")
        count = self.get_index(entry_search)
        self.entries[count].notes = new_note

    def display_entry(self, entry):
        """display entry with date, task name,
           time spent, and notes information."""
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

    def get_index(self, entry_search):
        """get index position of an entry from self.entries"""
        count = 0
        for entry in self.entries:
            if entry == entry_search:
                return count
            count += 1

    def get_option(self, entries):
        """get option from menu"""
        while True:
            option = input("Choose one of the above >>> ")
            try:
                option = int(option)
                if option in range(len(entries)):
                    return option
                else:
                    print("Please enter a valid entry")
            except ValueError:
                print("Please enter a valid option")
