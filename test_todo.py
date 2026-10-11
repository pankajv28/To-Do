import pytest
import todo

def make_tasks():
    return [
        {'title': '1', 'description': 'Get library subscription', 'status':'COMPLETED'},
        {'title': '2', 'description': 'Complete Coding', 'status':'ONGOING'},
        {'title': '3', 'description': 'Lunch', 'status':'TOSTART'},
        {'title': '4', 'description': 'Boiled Eggs', 'status':'TOSTART'},
    ]

def test_instatus_correct():
    tasks = make_tasks()
    tostart =  todo.in_status(tasks,'TOSTART')
    assert len(tostart) == 2

def test_findtask_correct():
    tasks = make_tasks()
    task = todo.find_task(tasks,'TOSTART',2)
    assert task['description'] == 'Boiled Eggs'

def test_findtask_number_too_big():
    tasks = make_tasks()
    with pytest.raises(ValueError):
        todo.find_task(tasks, 'TOSTART', 5)

def test_addtask():
    tasks = make_tasks()
    todo.add_task(tasks,'5','Check Funds','TOSTART')
    assert len(tasks) == 5
    assert tasks[-1]['description'] == 'Check Funds'
    assert tasks[-1]['status'] == 'TOSTART'

def test_changetask_moves_task():
    tasks = make_tasks()
    todo.edit_status(tasks,'TOSTART',2,'ONGOING')
    assert tasks[3]['status'] == 'ONGOING'

def test_changetask_leaves_other_tasks():
    tasks = make_tasks()
    todo.edit_status(tasks,'TOSTART',2,'ONGOING')
    assert tasks[2]['status'] == 'TOSTART'

def test_changetask_bad_number():
    tasks = make_tasks()
    with pytest.raises(ValueError):
        todo.edit_status(tasks, 'ONGOING', 5, 'COMPLETED')

def test_deletetask():
    tasks = make_tasks()
    todo.delete_task(tasks,'COMPLETED',1)
    assert len(tasks) == 3
    assert tasks[0]['description'] == 'Complete Coding'

def test_deletetask_badnumber():
    tasks = make_tasks()
    with pytest.raises(ValueError):
        todo.delete_task(tasks,'COMPLETED',5)
    assert len(tasks) == 4

def test_load_missing_file_gives_empty_list(tmp_path,monkeypatch):
    monkeypatch.setattr(todo,'filename',str(tmp_path/'tasks.json'))
    assert todo.load_tasks() == []

def test_save_then_load_gives_same_tasks(tmp_path,monkeypatch):
    monkeypatch.setattr(todo,'filename',str(tmp_path/'tasks.json'))
    tasks = make_tasks()
    todo.save_tasks(tasks)
    assert todo.load_tasks() == tasks

def test_save_leaves_no_temp_file(tmp_path,monkeypatch):
    monkeypatch.setattr(todo,'filename',str(tmp_path/'tasks.json'))
    todo.save_tasks(make_tasks())
    assert not (tmp_path/ 'tasks.json.tmp').exists()

def test_load_corrupted_file_gives_empty_list(tmp_path,monkeypatch):
    fake_file = tmp_path/'tasks.json'
    fake_file.write_text('this is not json')
    monkeypatch.setattr(todo,'filename',str(fake_file))
    assert todo.load_tasks() == []