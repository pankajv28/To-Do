from datetime import date
import json
import os

statuses = (
    'TOSTART',
    'ONGOING',
    'COMPLETED'
)

filename = 'tasks.json'

def load_tasks():
    try:
        with open(filename,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print (f'{filename} was unreadable, starting from empty to-do list')
        return []

def save_tasks(tasks):
    temp = filename + '.tmp'
    with open(temp,'w') as file:
        json.dump(tasks,file,indent = 4)
    os.replace(temp,filename)

def in_status(tasks,status):
    return [t for t in tasks if t['status']==status]
        
def find_task(tasks, status, number):
    matches = in_status(tasks,status)
    if 1 <= number <= len(matches):
        return matches[number-1]
    else:
        raise ValueError('Task number is not valid')
    
def add_task(tasks,title,description,status):
    description = description.strip()
    if description :
        tasks.append({'title':title,'description':description, 'createdate': date.today().isoformat(), 'status':status})
    else : 
        raise ValueError('Description cannot be empty')

def list_tasks(tasks):
    for status in statuses:
        group = in_status(tasks,status)
        if group:
            print()
            for i, task in enumerate(group, 1):
                label = f"{i}. {task['title']} {task['description']}"
                print(f"{label:<25}{status.title()}")
            print()

def edit(tasks,current_status,number):
    match (input('What to edit? Title Or Description Or Status').strip().lower()):
        case 'title':
            edit_title(tasks,current_status,number)
        case 'description':
            edit_description(tasks,current_status,number)
        case 'status':
            new_status = ask_status('New Status')
            edit_status(tasks,current_status,number,new_status)
        case _:
            raise Exception('Invalid Edit Request')

def edit_title(tasks,current_status,number):
    title = input('New Title')
    find_task(tasks,current_status,number)['title'] = title

def edit_description(tasks,current_status,number):
    description = input('New Description')
    find_task(tasks,current_status,number)['description'] = description

def edit_status(tasks, current_status,index,new_status):
        if current_status != new_status:
            find_task(tasks,current_status,index)['status'] = new_status
        else :
            print ('Old and New task status are same')
            
def delete_task(tasks,current_status,index):
    tasks.remove(find_task(tasks,current_status,index))

def ask_status(prompt):
    input_status = input(f'{prompt} {"/".join(statuses)} ').strip().upper()
    if input_status not in statuses:
        raise ValueError('Status is invalid')
    else:
        return input_status
    
def ask_number(prompt):
    try: 
        return int(input(prompt))
    except:
        raise ValueError('Input has to be a whole number')
    
def main():
    tasks = load_tasks()
    while True:
        command = input(' What to do add/edit/delete/list/quit > ')
        try:
            match(command.lower().strip()):
                case "add":
                    add_task(tasks,input("Description : "),ask_status('Status : '))
                    save_tasks(tasks)
                case "list":
                    list_tasks(tasks)
                case "delete":
                    delete_task(tasks,ask_status('Delete from Status : '),ask_number('Task Number :'))
                    save_tasks(tasks)
                case "edit":
                    edit(tasks,ask_status('Current Status : '),ask_number('Task Number : '))
                    save_tasks(tasks)
                case "quit":
                    print('Goodbye!')
                    break
                case _:
                    print("Unknown command")
        except (ValueError) as e:
            print(f'Invalid input: {e}')

if __name__ == '__main__':
    main()