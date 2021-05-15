import file
from colors import bcolors as color
from user import User
import emoji
from datetime import datetime
import time
import schedule
import logging
from win10toast import ToastNotifier
from task import Task
import hash_password as hashing

user = User()
task = Task(user.username)
now_time = time.time()

file.check_exist()

logging.basicConfig(level=logging.INFO, filename='log_data.log', filemode='a',
                    format=' %(asctime)s - %(name)s - %(levelname)s -%(message)s ')

print(f"{color.YELLOW}"
      f"------------------------ Hello {emoji.emojize(':smiling_face_with_heart-eyes:')} ------------------------\n"
      f"------------- Welcome to the reminder world -------------\n"
      f"............... Thanks for using this app ...............\n"
      f"{color.ENDC}")

while user.log_in is False:
    try:
        print(f"{color.PURPLE}************** MENU **************{color.ENDC}")
        print(f"{color.OKBLUE}")
        print("1- Login")
        print("2- Sign up")
        print(f'3- Exit\n{color.ENDC}')

        user_selection = int(input('>>>> ').strip().replace(" ", ""))
        if user_selection == 1:
            # ------------------------------login------------------------------
            user.login()

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
            raise Exception("you must inter 1 or 2 or 3")

    except ValueError as ve:
        print(f"Error: {ve}")
        logging.error("user inter wrong input")
    except Exception as e:
        print(f"Error: {e}")
        logging.error("wrong input entered")

# ------------------------------------- codes for reminder notification ---------------------------
try:
    user_tasks = file.user_row('tasks.csv', user.username)
    today = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
    today_str = today.strftime('%Y-%m-%d %H:%M')

    for user_task in user_tasks:
        schedule_postponed = True


        def print_remind_message():
            print(f"{color.OKCYAN}o0o0o0o0o0o0o0o Don't Forget {user_task['title']} o0o0o0o0o0o0o0o{color.ENDC}")

            toaster = ToastNotifier()
            toaster.show_toast("Reminder Notification", user_task["title"])
            postpone_selection = input(
                f"{color.YELLOW}Do you want to postponed task for 10 minutes? [y/n] >>>> {color.ENDC}").lower().strip()

            if postpone_selection == 'y':
                logging.info("user postponed task for 10 minute")
                global schedule_postponed
                schedule_postponed = False
                return schedule.cancel_job

            elif postpone_selection == 'n':
                pass

            change_due_input = input('Do you want to postpone due time? [y/n] ').lower().strip()

            if change_due_input == 'y':
                print('1-postponed one day')
                print('1-postponed one week')
                select_postpone = int(input(">>>> "))
                task.postpone(user_task['username'], user_task['due_time'], select_postpone)
            elif change_due_input == 'n':
                pass


        if user_task['importance_degree'] == '1' and user_task['progress'] != '100':
            if not schedule_postponed:
                schedule.every(10).seconds.do(print_remind_message)
            schedule.every(5).seconds.do(print_remind_message)

        elif user_task['importance_degree'] == '2' and user_task['progress'] != '100':
            due_day_datetime = datetime.strptime(user_task['due_time'], "%Y-%m-%d %H:%M:%S")
            due_day_str = due_day_datetime.strftime('%Y-%m-%d %H:%M')
            hour = due_day_datetime.strftime("%H:%M")
            if today_str == due_day_str:
                print_remind_message()

        elif user_task['importance_degree'] == '3' and user_task['progress'] != '100':
            if not schedule_postponed:
                schedule.every(interval=1).day.at('21:10').do(print_remind_message)
            schedule.every(interval=1).day.at('21:00').do(print_remind_message)

        elif user_task['importance_degree'] == '4' and user_task['progress'] != '100':
            if not schedule_postponed:
                schedule.every().friday.at('21:10').do(print_remind_message)
            schedule.every().friday.at('21:00').do(print_remind_message)

except Exception as e:
    print(f'Error: {e}')
    logging.error(f"Error Occurred. {e} ")

# ------------------------------------- codes for reminder notification ---------------------------


while user.log_in is True:
    print(f"{color.PURPLE}************** MENU **************{color.ENDC}")
    print(f'{color.OKBLUE}')
    print('1- Add Task')
    print('2- Delete Task')
    print('3- Edit Task')
    print("4- Task's progress")
    print('5- Share Task')
    print('6- Show Tasks')  # with or without details
    print(f'7- See tasks periodically')
    print(f'8- Categorize Task')
    print('9- change password')
    print(f'10- Logout')
    print(f'{color.ENDC}')

    # --------------------------- Reminder Turns On---------------------------
    schedule.run_pending()
    time.sleep(1)
    # --------------------------- Reminder Turns On---------------------------

    user_input = int(input(f'{color.OKBLUE}{color.BOLD}>>>> {color.ENDC}').strip().replace(" ", ""))
    try:

        if user_input == 1:
            # ------------------------------Add Task------------------------------
            print(f"{color.YELLOW}*** Please fill the following attributes for your task ***{color.ENDC}")
            title = input(f"{color.PURPLE}title: ").strip()
            description = input("description: ").strip()
            link = input("link: ").strip()
            location = input("location: ").strip()
            task_type = input("task type: ").lower().strip()
            due_time = input(f"When should you finish? [year-month-day hour:minute:second] {color.ENDC}")
            task.create_task(user.username, title, description, link, location, task_type, due_time)

        elif user_input == 2:
            # ------------------------------Delete Task------------------------------
            print(f"{color.OKBLUE}---------------------------Delete Task---------------------------\n{color.ENDC}")
            print(f'{color.YELLOW}')
            file.read_pandas('tasks.csv', user.username, 'title')
            print(f"Delete Which task? [enter the index]")
            location = int(input(f"{color.BOLD}Enter the number: {color.ENDC}").strip().replace(" ", ""))
            print('\n')
            task.delete_task(location)

        elif user_input == 3:
            # ------------------------------Edit Task------------------------------
            print(f"{color.OKBLUE}---------------------------Edit Task---------------------------\n{color.ENDC}")
            print(f"{color.YELLOW}For Which task? [enter the index]")
            file.read_pandas('tasks.csv', user.username, 'title')
            location = int(input(f"{color.BOLD}Enter the number: {color.ENDC}").strip().replace(" ", ""))
            print('\n')
            print(f"{color.YELLOW}--- What would you like to edit? ---{color.ENDC}")
            print(
                f"{color.OKCYAN}1- title\n2- description\n3- link\n4- location\n5- due time\n6- importance\n7- progress"
                f"{color.ENDC}")
            user_select = int(input('>>>> ').strip().replace(" ", ""))
            new_value = input(f"{color.BOLD}Please write the new value: {color.ENDC}").strip()
            task.edit_task(location, user_select, new_value)

        elif user_input == 4:
            # ------------------------------Task's progress------------------------------
            print(color.YELLOW)
            file.read_pandas('tasks.csv', user.username, 'title')
            location = int(input(f"{color.BOLD}Enter the number: {color.ENDC}").strip().replace(" ", ""))
            print('\n')
            task.progress_in_task(location, user.username)

        elif user_input == 5:
            # ------------------------------Share Task------------------------------
            print(f'{color.PURPLE}{color.BOLD}What Do You Want to Do?{color.ENDC}')
            print(f'{color.BLUE}')
            print('1- Send request')
            print(f'2- Check requests')
            print(f'3- back')
            print(f'{color.ENDC}')
            selection = int(input('>>>> ').strip().replace(" ", ""))

            if selection == 1:
                # send requests
                print(f"{color.OKBLUE}---------------------------Send Task---------------------------\n{color.ENDC}")

                print(f"{color.OKGREEN}Which Task?[enter the title]")
                print(color.OKGREEN)
                file.read_pandas('tasks.csv', user.username, 'title')
                task_title = input(f'>>>> {color.ENDC}').strip()

                print(f"{color.ORANGE}Send to which user?[enter the name]")
                file.read_pandas_not('user_pass.csv', user.username, 'username')
                user_name = input('>>>> ').strip()
                print(f'\n{color.ENDC}')

                user.share_task(selection=1, task_title=task_title, user_name=user_name)

            elif selection == 2:
                # check request
                user_data = file.read_all_pandas('requests.csv', user.username)
                if len(user_data.index.values) == 0:
                    print(f'{color.RED}You have no new request{color.ENDC}')
                else:
                    accept = (input(f'{color.BOLD}Do you want to add any task?[y/n] >>>> ')).lower().strip()
                    if accept == 'y':
                        task_title = input(f'{color.ORANGE}Which one? [inter the title]: ').strip()
                        user.share_task(selection=2, accept='y', task_title=task_title, user_name=user.username)
                        print(f"{color.YELLOW}*** Task Added ***{color.ENDC}\n")

                    elif accept == 'n':
                        print(f'{color.BOLD}{color.RED}Do you want to delete any request? [y/n]{color.ENDC}')
                        del_or_not = input(">>>> ").strip().replace(" ", "")
                        if del_or_not == 'y':
                            request_index = int(
                                input(f'{color.BOLD}Which one? [inter the index]: {color.ENDC}').strip())
                            file.delete_pandas('requests.csv', request_index)
                        elif del_or_not == 'n':
                            pass
            elif selection == 3:
                continue

        elif user_input == 6:
            # ------------------------------Show Tasks------------------------------
            print(f'{color.YELLOW}*** Please choose ***{color.ENDC}')
            print(f'{color.BLUE}1- Show tasks with detail')
            print(f'2- Show only the task names')
            print(f'3- back')

            selected = int(input('>>>> ').strip().replace(" ", ""))
            print('\n')
            if selected == 1:
                user.user__show_everything()
            elif selected == 2:
                user.user__tasks()
            elif selected == 3:
                continue
            else:
                print(f'{color.RED}!!! INVALID INPUT !!!{color.ENDC}')
                raise ValueError("input is not valid")

        elif user_input == 7:
            # ------------------------------See tasks periodically------------------------------
            # show her tasks
            print(f'{color.YELLOW}Select the period of time{color.ENDC}')
            print(f'{color.BLUE}1- Day')
            print('2- Week')
            print(f'3- Month{color.ENDC}')
            period_index = int(input(">>>> ").strip().replace(" ", ""))
            user.user__see_calender(period_index)

        elif user_input == 8:
            # ------------------------------Categorize Tasks------------------------------
            print(f"{color.YELLOW}Categorize based on: {color.ENDC}")
            print(f'{color.BLUE}1- Type')
            print('2- Importance')
            print(f'3- Done or Not{color.ENDC}')
            categorize_input = int(input('>>>> ').strip().replace(" ", ""))
            user.categorize_tasks(categorize_input)

        elif user_input == 9:
            print(f"{color.OKBLUE}-------------------------change password-------------------------\n{color.ENDC}")
            old_password = input(f"{color.PURPLE}Enter old password: ")
            row = file.user_row('user_pass.csv', user.username)
            if hashing.verify_password(row[0]['password'], old_password) is True:
                new_password = input(f"Enter new password: {color.ENDC}")
                user.change_password(user.username, new_password)

        elif user_input == 10:
            # ------------------------------Logout------------------------------
            print(
                f"{color.PURPLE}{color.BOLD}--- Have a nice Day {emoji.emojize(':smiling_face_with_smiling_eyes:')} ---"
                f"{color.ENDC}")
            user.log_in = False
        else:
            raise Exception("input is not valid")

    except NameError as ne:
        print(f'Error: {ne}')
        logging.error(f"Error Occurred! {ne}")

    except ValueError as ve:
        print(f'Error: {ve}')
        logging.error(f"Error Occurred! {ve}")

    except TypeError as te:
        print(f'Error: {te}')
        logging.error(f"Error Occurred! {te}")
