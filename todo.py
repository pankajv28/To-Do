from datetime import date

tasks = []

COMPLETED = 'COMPLETED'
ONGOING = 'ONGOING'
TOSTART = 'TOSTART'
TODO = True

class Task:

    def __init__(self,description,createdate):
        self.description = description
        self.createdate = createdate
        self.status = TOSTART

    def __str__(self):
        print (f'{self.description}')

def add_task(description):
    tasks.append(Task(description,date.today()))

def list_task():
    if tasks == []:
        print ('Empty List!')
    for task in tasks :
        print(f'{task.description}, {task.status}, {task.createdate}')

def change_status(index,current):
    if current.upper() in (COMPLETED,ONGOING,TOSTART):
        tasks[index-1].status = current.upper()
    else:
        print ('Incorrect Status')

def delete_task(index):
    if index <= len(tasks) :
        tasks.pop(index-1)
    else :
        print('To-do lists dont have these many tasks')

def quit_todo():
    print ('Goodbye!')
    return False

while TODO == True:
    command = input(' What to do > ')
    match(command.lower().strip()):
        case "add":
            add_task(input("Add task description : "))
        case "list":
            list_task()
        case "delete":
            delete_task(int(input("Which number task do you want to delete? ")))
        case "change":
            change_status(int(input('Which task number? ')),input('Updated Status is? '))
        case "quit":
            TODO = quit_todo()
        case _:
            print("Unknown command")