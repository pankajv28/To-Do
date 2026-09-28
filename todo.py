from datetime import date
import json
import os

tasks = []
tostart = []
ongoing = []
completed = []

TODO = True

status_lists = {
    'tostart':tostart,
    'ongoing':ongoing,
    'completed':completed
}

class Task:
    def __init__(self,description,createdate):
        self.description = description
        self.createdate = createdate

    def __str__(self):
        print (f'{self.description}')

def add_task(description,list):
    list = status_lists[list]
    list.append(Task(description,date.today()))

def list_tasks():
    if tostart == [] and ongoing == [] and completed == []:
        print ('Empty List!')
    else :
        print(f'{"TO START":<25}{"ONGOING":<25}{"COMPLETED":<25}')
        max_length = max(len(tostart), len(ongoing), len(completed))
        for i in range(max_length):
            left = f'{i+1}. {tostart[i].description}' if i < len(tostart) else ''
            middle = f'{i+1}. {ongoing[i].description}' if i < len(ongoing) else ''
            right = f'{i+1}. {completed[i].description}' if i < len(completed) else ''
            print(f'{left:<25}{middle:<25}{right:<25}')

def change_status(current_status,index,new_status):
        task = status_lists[current_status][index-1]
        status_lists[new_status].append(task)
        status_lists[current_status].pop(index-1)

def delete_task(current_status,index):
    status = status_lists[current_status]
    if index <= len(status) :
        status.pop(index-1)
    else :
        print('List doesnt have these many tasks')

def quit_todo():
    print ('Goodbye!')
    return False

def error_status(status):
    if status in ('tostart','ongoing','completed'):
        return status
    else:
        raise NameError('Status name is invalid')

while TODO == True:
    command = input(' What to do > ')
    match(command.lower().strip()):
        case "add":
            add_task(input("Add task description : "),input("Status of the task : \n TOSTART\n ONGOING\n COMPLETED\n").strip().lower())
        case "list":
            list_tasks()
        case "delete":
            delete_task(error_status(input('Which list do you want to delete from?\n TOSTART\n ONGOING\n COMPLETED\n ')),int(input("Which number task do you want to delete? ")))
        case "change":
            change_status(error_status(input('Current Status is? \n TOSTART\n ONGOING\n COMPLETED\n ').strip().lower()),int(input('Which task number? ')),error_status(input('Updated Status is? \n TOSTART\n ONGOING\n COMPLETED\n ').strip().lower()))
        case "quit":
            TODO = quit_todo()
        case _:
            print("Unknown command")