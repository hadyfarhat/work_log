import csv

from log import Log

l = Log()

print("Program has ended")

with open('entries.csv', 'w', newline='') as csvfile:
    fieldnames = ['task_name', 'time_spent', 'created_at', 'notes']
    entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    entry_writer.writeheader()
    for entry in l.entries:
        entry_writer.writerow({
            'task_name': '{}'.format(entry.task_name),
            'created_at': '{}'.format(entry.created_at),
            'time_spent': '{}'.format(entry.minutes),
            'notes': '{}'.format(entry.notes)
            })
