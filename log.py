import datetime

from entry import Entry

class Log():
	entries = []

	# menu message
	menu = """
	1- Add new entry
	2- Lookup previous entries
	"""

	previous_entries_menu = """
	1- Find by Date
	2- Find by Time Spent
	3- Find by Exact Search
	4- Find by Pattern
	"""

	def __init__(self):
		self.game_menu()

	def game_menu(self):
		# while True:
		print(self.menu)
		user_option = self.get_main_menu_option()
		# run the command the user entered
		self.run(int(user_option))


	# user should enter either 1 or 2
	def get_main_menu_option(self):
		while True:
			user_option = input("Enter 1 or 2 >>> ")
			if user_option:
				if user_option == "1" or user_option == "2":
					print("Good option")
					return user_option
				else:
					print("Please enter either 1 or 2")
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

	# search for previous entries
	def search_entries(self):
		menu_option = self.get_previous_entries_menu_option()
		if menu_option == 1:
			self.find_by_date()
		elif menu_option == 2:
			self.find_by_time_spent()
		elif menu_option == 3:
			self.find_by_exact_search()
		elif menu_option == 4:
			pass

	# user should enter a valid menu option
	def get_previous_entries_menu_option(self):
		while True:
			print(self.previous_entries_menu)
			menu_option = int(input("Enter 1,2,3 or 4 >>> "))
			if menu_option in [1,2,3,4]:
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

	# printes all entries that match the user's input
	def print_entries_found(self, entries_found, search_type):
		print("These entries were found based on your {} search ".format(
																search_type
																))
		print("Note the time displayed is in a 24 hour clock format")
		for entry_found in entries_found:
			print("	{} created at {}".format(
											entry_found.task_name,
											entry_found.created_at.strftime(
												"%m/%d/%Y %H:%M")
											))



















