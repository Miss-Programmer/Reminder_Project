from colors import bcolors as color
from user import User
import emoji
import pandas as pd
from datetime import timedelta, datetime
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import csv
import sched, time
import schedule
from tabulate import tabulate

# from time import time, sleep

user = User()
now_time = time.time()

print(f"{color.YELLOW}"
      f"------------------------ Hello {emoji.emojize(':smiling_face_with_heart-eyes:')} ------------------------\n"
      f"------------- Welcome to the reminder world -------------\n"
      f"............... Thanks for using this app ...............\n"
      f"{color.ENDC}")

while user.log_in is False:
    print(f"{color.PURPLE}************** MENU **************{color.ENDC}")
    print(f"{color.OKBLUE}")
    print("1- Login")
    print("2- Sign up")
    print(f'3- Exit\n{color.ENDC}')

    user_selection = int(input('>>>> '))
    if user_selection == 1:
        # ------------------------------login------------------------------
        user.login()
        now_time = datetime.strptime(JalaliDateTime.today().strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")

    elif user_selection == 2:
        # ------------------------------signup------------------------------
        user.signup()

    elif user_selection == 3:
        # ------------------------------Exit------------------------------
        print(
            f"{color.PURPLE}{color.BOLD}--- Have a nice Day {emoji.emojize(':smiling_face_with_smiling_eyes:')} ---"
            f"{color.ENDC}")
        break
    else:
        print(f'{color.RED}!!! INVALID INPUT !!!{color.ENDC}')

# ------------------------------------- codes for reminder notification ---------------------------

with open('tasks.csv') as task_file:
    task_reader = csv.DictReader(task_file)
    for task in task_reader:
        if task['username'] == user.username:

            def print_remind_message():
                print(f"{color.OKCYAN}o0o0o0o0o0o0o0o Don't Forget {task['title']} o0o0o0o0o0o0o0o{color.ENDC}")


            if task['importance_degree'] == '1':
                schedule.every(5).seconds.do(print_remind_message)
            elif task['importance_degree'] == '2':
                today = datetime.strptime(JalaliDateTime.today().strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")
                due_day = datetime.strptime(task['due_time'], "%Y/%m/%d %H:%M:%S")
                hour = due_day.strftime("%H")
                if today == due_day:
                    schedule.every().day.at(hour).do(print_remind_message)
            elif task['importance_degree'] == '3':
                schedule.every().day.at("21:00:00").do(print_remind_message)
            elif task['importance_degree'] == '4':
                schedule.every().friday.at('21:00:00').do(print_remind_message)

# ------------------------------------- codes for reminder notification ---------------------------


while user.log_in is True:
    print(f"{color.PURPLE}************** MENU **************{color.ENDC}")
    print(f'{color.BLUE}1- Add Task')
    print('2- Delete Task')
    print('3- Edit Task')
    print("4- Task's progress")
    print('5- Share Task')
    print('6- Show Tasks')  # with or without details
    print(f'7- See Calender')
    print(f'8- Logout{color.ENDC}')

    # print(f"{color.OKCYAN}--------------------------- Reminder Turns On---------------------------\n{color.ENDC}")
    schedule.run_pending()
    time.sleep(1)
    # all_jobs = schedule.get_jobs()
    # print(all_jobs)

    user_input = int(input('>>>> '))
    if user_input == 1:
        # ------------------------------Add Task------------------------------
        user.user__add_task()
    elif user_input == 2:
        # ------------------------------Delete Task------------------------------
        user.user__delete_task()
    elif user_input == 3:
        # ------------------------------Edit Task------------------------------
        user.user__edit_task()
    elif user_input == 4:
        # ------------------------------Task's progress------------------------------
        user.user__progress()

    elif user_input == 5:
        # ------------------------------Share Task------------------------------
        print('What Do You Want to Do?')
        print('1- Send Task')
        print('2- Check requests')
        selection = int(input('>>>> '))
        if selection == 1:
            print(f"{color.OKBLUE}---------------------------Send Task---------------------------\n{color.ENDC}")
            # tasks data
            print("Which Task?[enter the title]")
            print(color.OKGREEN)
            tasks_data = pd.read_csv('tasks.csv')
            user_tasks = tasks_data[tasks_data['username'] == user.username]
            print(tabulate(user_tasks[['title']], headers='keys', tablefmt='fancy_grid'))
            task_title = input('>>>> ')

            # users data
            print("Send to which user?[enter the name]")
            users_data = pd.read_csv('user_pass.csv')
            users_data = users_data[users_data['username'] != user.username]
            print(tabulate(users_data[['username']], headers='keys', tablefmt='fancy_grid'))
            print(f'\n{color.ENDC}')
            user_name = input('>>>> ')
            print(f'\n{color.ENDC}')

            request_data = pd.DataFrame(
                {'username': [user_name], 'title': [task_title], 'description': '', 'link': '', 'location': '',
                 'task_type': '', 'date_remind': '', 'time_remind': '', 'created_time': '',
                 'due_time': '', 'importance': '', 'progress': '', 'importance_degree': '', 'sender': [user.username]})
            request_data.to_csv("requests.csv", index=False, mode='a', header=False)
            print("*** Task Sent ***")

        elif selection == 2:
            request_data = pd.read_csv('requests.csv')
            user_request_data = request_data[request_data['username'] == user.username]
            print(tabulate(user_request_data['username'], headers='keys', tablefmt='fancy_grid'))
            # print(request_data)
            accept = (input('Do you want to add any task?[y/n] ')).lower()
            if accept == 'y':
                accepted_index = int(input('Which one? [inter the index]: '))
                accept_row = pd.DataFrame({'username': request_data['username'], 'title': request_data['title'],
                                           'description': '', 'link': '', 'location': '', 'task_type': '',
                                           'date_remind': '', 'time_remind': '', 'created_time': '',
                                           'due_time': '', 'importance': '',
                                           'progress': '', 'importance_degree': '', 'sender': request_data['sender']})
                accept_row.to_csv("tasks.csv", index=False, mode='a', header=False, line_terminator='\n')
                request_data = request_data.drop(request_data.index[[accepted_index]])
                request_data.to_csv('requests.csv', index=False, mode='a', header=False)
                print("*** Task Added ***")
            elif accept == 'n':
                print('Do you want to delete any request? [y/n]')
                del_or_not = input(">>>> ")
                if del_or_not == 'y':
                    request_index = int(input('Which one? [inter the index]: '))
                    request_data.drop(request_index + 1, axis=0, inplace=True)
                    request_data.to_csv('requests.csv', index=False, header=False)
                elif del_or_not == 'n':
                    pass

    elif user_input == 6:
        # ------------------------------Show Tasks------------------------------
        print(f'{color.YELLOW}*** Please choose ***{color.ENDC}')
        print(f'{color.BLUE}1- Show tasks with detail')
        print(f'2- Show only the task names')
        print(f'3- Show tasks with the specific value{color.ENDC}')  # !!!!!!!!!!!!!!!!!!!!!!!
        selected = int(input('>>>> '))
        print('\n')
        if selected == 1:
            user.user__show_everything()
        elif selected == 2:
            user.user__tasks()
        else:
            print(f'{color.RED}!!! INVALID INPUT !!!{color.ENDC}')

    elif user_input == 7:
        # ------------------------------See Calender------------------------------
        pass


    elif user_input == 8:
        # ------------------------------Logout------------------------------
        print(f"{color.PURPLE}{color.BOLD}--- Have a nice Day {emoji.emojize(':smiling_face_with_smiling_eyes:')} ---"
              f"{color.ENDC}")
        user.log_in = False
