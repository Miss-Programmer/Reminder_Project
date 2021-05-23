from colors import bcolors as color
import pandas as pd
import hash_password as hashing
import emoji
import csv
from tabulate import tabulate
from datetime import datetime
import logging
import file

logging.basicConfig(level=logging.INFO, filename='log_data.log', filemode='a',
                    format=' %(asctime)s - %(name)s - %(levelname)s -%(message)s ')


class User:
    def __init__(self, username='', password='', log_in=False, user_status='acrive'):
        """
        :param username: username of user
        :param password: password of user
        :param log_in: if log_in=true, user login successfully, if log_in=False, user can't login
        :param user_status active but if user inter wrong password 3 times, it will be blocked
        """
        self.username = username
        self.password = password
        self.log_in = log_in
        self.user_status = user_status

    def signup(self):
        """
        get username and if it does not exist, get password and create a user with that information
        """
        print(f"{color.OKBLUE}---------------------------signup---------------------------\n{color.ENDC}")
        df = pd.read_csv('user_pass.csv')
        while True:
            input_username = input(f"{color.PURPLE}please make a username: {color.ENDC}")

            if input_username in df.values:
                print(f"{color.RED}!!! This username is already exist. please select another username !!!{color.ENDC}")
                raise Exception('This username is already exist.')

            elif input_username == '':
                print(f"{color.RED}!!! INVALID USERNAME !!!{color.ENDC}")
                raise Exception("user can't input empty value as username")

            else:
                input_password = hashing.hash_password(input(f"{color.PURPLE}please create a password: {color.ENDC}"))
                self.username = input_username
                self.password = input_password
                self.user_status = 'active'
                df = df.append(
                    {'username': input_username, 'password': input_password, 'user_status': self.user_status},
                    ignore_index=True)
                df.to_csv('user_pass.csv', index=False)
                print(f"{color.YELLOW}*** Welcome {self.username} {emoji.emojize(':smiling_face_with_smiling_eyes:')}"
                      f" ***{color.ENDC}\n")
                break

    def login(self):
        """
        get username and if it exists, get password and check if it's true or not. if it was true, allow user to
        login and show her/him the menu.
        if user input wrong password for 3 times, he/she will be blocked and can't login anymore
        """
        print(f"{color.OKBLUE}---------------------------login---------------------------\n{color.ENDC}")
        try:
            df = pd.read_csv('user_pass.csv')
            input_username = input(f'{color.PURPLE}username: {color.ENDC}')
            assert input_username != '', 'username cant be empty'
            allowed = 0
            while allowed != 3:
                if input_username not in df.values and self.log_in is False:
                    selection = input(
                        f"{color.OKCYAN}username not exist. Do you want to signup?[y/n] {color.ENDC}\n").lower()

                    if selection == 'y':
                        self.signup()
                        break

                    elif selection == 'n':
                        break

                    else:
                        print(f"{color.RED}!!! Input not valid !!!{color.ENDC}")
                        raise Exception("wrong input")

                elif input_username == '':
                    print(f"{color.RED}!!! Input not valid !!!{color.ENDC}")
                    raise Exception("user can't input empty value as username")

                elif input_username in df.values:
                    with open('user_pass.csv', 'r') as userPass_file:
                        csv_reader = csv.DictReader(userPass_file)
                        for row in csv_reader:
                            if row['username'] == input_username:
                                if row['user_status'] == 'blocked':
                                    print(f"{color.RED}--- you can't login ---{color.ENDC}")
                                    allowed = 3
                                    break
                                input_password = input(f"{color.PURPLE}password: {color.ENDC}")

                                if hashing.verify_password(row['password'], input_password) is True:
                                    self.username = row['username']
                                    self.password = row['password']
                                    print(f"{color.YELLOW}*** Welcome {self.username} "
                                          f"{emoji.emojize(':smiling_face_with_smiling_eyes:')} ***"
                                          f"{color.ENDC}\n")
                                    self.log_in = True
                                    logging.info(
                                        f"{self.username} logged in with password {self.password}")
                                    allowed = 3
                                    break

                                elif self.log_in is False:
                                    if allowed < 2:
                                        print(
                                            f"{color.RED}!!! your password is wrong. please try again !!!\n{color.ENDC}")
                                        allowed += 1
                                        # login_func(self)

                                    elif allowed == 2:
                                        allowed = 3
                                        row['user_status'] = 'blocked'
                                        file.change_pandas('user_pass.csv', 'user_status', 'blocked', self.username)
                                        print(
                                            f"{color.BOLD}{color.RED}"
                                            f"!!! You tried 3 times ... Please Try again later [action blocked] !!!\n"
                                            f"{color.ENDC}")

                                        # sleep(60)
                                        raise Exception(f"{self.username} tried 3 times for login.")

        except Exception as exception:
            logging.warning(f"Warning: {exception}")
            print(exception)

        except FileNotFoundError as fnf_error:
            logging.error(f"Error: {fnf_error}")
            print(fnf_error)

    def change_password(self, user_name, new_password):
        """
        get old password of user and if the old password be true, get new password and replace the old password
        :param user_name: username of user
        :param new_password: new password of user --> not hash
        """
        new_hash_pass = hashing.hash_password(new_password)
        self.password = new_hash_pass
        file.change_pandas('user_pass.csv', 'password', new_hash_pass, user_name)
        print(f"{color.YELLOW}*** Your password is changed ***{color.ENDC}\n")

    def user__show_everything(self):
        """
        user can see every information about her/his tasks
        """
        print(f"{color.OKBLUE}-------------------------Show Tasks With Detail-------------------------\n{color.ENDC}")
        print(color.BOLD)
        file.read_all_pandas('tasks.csv', self.username)
        print(f'\n{color.ENDC}')

    def user__tasks(self):
        """
        show all task titles of the user to him/her
        """
        print(f"{color.OKBLUE}---------------------------Show Task names---------------------------\n{color.ENDC}")
        print(color.BOLD)
        file.read_pandas('tasks.csv', self.username, 'title')
        print(f'\n{color.ENDC}')

    def user__see_calender(self, period_index):
        """
        user can see all of tasks in day, week and month
        :param period_index: 1 for day, 2 for week, 3 for month --> int
        """
        with open('tasks.csv') as task_file:
            task_reader = csv.DictReader(task_file)
            today = datetime.strftime(datetime.now(), '%d')  # str
            today_week = datetime.strftime(datetime.now(), '%W')  # str
            today_month = datetime.now().month
            today_year = datetime.now().year
            today_tasks_done = []
            today_tasks_remain = []
            week_tasks_done = []
            week_tasks_remain = []
            month_tasks_done = []
            month_tasks_remain = []
            for row in task_reader:
                if row['username'] == self.username:
                    due_day = datetime.strptime(row['due_time'], "%Y-%m-%d %H:%M:%S").day  # int
                    due_week = datetime.strftime(datetime.strptime(row['due_time'], "%Y-%m-%d %H:%M:%S"), '%W')  # str
                    due_month = datetime.strptime(row['due_time'], "%Y-%m-%d %H:%M:%S").month
                    due_year = datetime.strptime(row['due_time'], "%Y-%m-%d %H:%M:%S").year
                    if int(today) == int(due_day) and int(today_month) == int(due_month) and int(today_year) == int(
                            due_year):
                        # today tasks
                        if row['progress'] == '100':
                            today_tasks_done.append(row)
                        elif row['progress'] != '100':
                            today_tasks_remain.append(row)

                    if int(today_year) == int(due_year) and int(today_week) == int(due_week):
                        # this week tasks
                        if row['progress'] == '100':
                            week_tasks_done.append(row)
                        elif row['progress'] != '100':
                            week_tasks_remain.append(row)

                    if today_year == due_year and today_month == due_month:
                        # this month tasks
                        if row['progress'] == '100':
                            month_tasks_done.append(row)
                        elif row['progress'] != '100':
                            month_tasks_remain.append(row)

                    else:
                        continue

            if period_index == 1:
                # Day
                print(f'{color.RED}{color.BOLD}today tasks\n{color.ENDC}')
                print(f'{color.OKGREEN}****************** Done Tasks *******************')
                print(tabulate(today_tasks_done, headers='keys', tablefmt='fancy_grid'), f'{color.ENDC}')
                print(f'{color.ORANGE}**************** Remaining Tasks ****************')
                print(tabulate(today_tasks_remain, headers='keys', tablefmt='fancy_grid'), f'{color.ENDC}')

            elif period_index == 2:
                # Week
                print(f'{color.RED}{color.BOLD}This Week tasks\n{color.ENDC}')
                print(f'{color.OKGREEN}****************** Done Tasks *******************')
                print(tabulate(week_tasks_done, headers='keys', tablefmt='fancy_grid'), f'{color.ENDC}')
                print(f'{color.ORANGE}**************** Remaining Tasks ****************')
                print(tabulate(week_tasks_remain, headers='keys', tablefmt='fancy_grid'), f'{color.ENDC}')

            elif period_index == 3:
                # Month
                print(f'{color.RED}{color.BOLD}This Month tasks\n{color.ENDC}')
                print(f'{color.OKGREEN}****************** Done Tasks *******************')
                print(tabulate(month_tasks_done, headers='keys', tablefmt='fancy_grid'), f'{color.ENDC}')
                print(f'{color.ORANGE}**************** Remaining Tasks ****************')
                print(tabulate(month_tasks_remain, headers='keys', tablefmt='fancy_grid'), f'{color.ENDC}')

    def categorize_tasks(self, categorize_input, due_time=''):
        """
        show tasks base of 1:type, 2:importance, 3:done or not
        types: 'exam', 'personal', 'hobby', 'study'
        importance: 'Do!', 'Decide!', 'Delegate', 'Delete'
        done: 'not started', 'on the way', 'almost done', 'done'
        :param categorize_input: 1 for type, 2 for importance, 3 for done or not
        :param due_time: due_time of task
        """
        tasks_data = pd.read_csv('tasks.csv')
        user_tasks = tasks_data.loc[tasks_data['username'] == self.username]
        if int(categorize_input) == 1:
            # categorize base on type
            task_types = ['exam', 'personal', 'hobby', 'study']
            for type in task_types:
                print(f'{color.YELLOW}*   *   *   *   *   {type}   *   *   *   *   *{color.ENDC}')
                print(color.OKGREEN)
                user_task_types = user_tasks.loc[lambda user_tasks: user_tasks['task_type'] == type]
                print(tabulate(user_task_types, headers='keys', tablefmt='fancy_grid'))
                print(f"\n{color.ENDC}")
        elif int(categorize_input) == 2:
            # categorize base on importance
            importance_list = ['Do!', 'Decide!', 'Delegate', 'Delete']
            for imp in importance_list:
                print(f'{color.YELLOW}*   *   *   *   *   {imp}   *   *   *   *   *{color.ENDC}')
                print(color.OKGREEN)
                user_task_types = user_tasks.loc[lambda user_tasks: user_tasks['importance'] == imp]
                print(tabulate(user_task_types, headers='keys', tablefmt='fancy_grid'))
                print(f"\n{color.ENDC}")
        elif int(categorize_input) == 3:
            # categorize base on done or not
            progress_list = ['not started', 'on the way', 'almost done', 'done']
            print(f'{color.YELLOW}*   *   *   *   *   not started   *   *   *   *   *{color.ENDC}')
            print(color.OKGREEN)
            task_progress = user_tasks.loc[lambda user_tasks: user_tasks['progress'].astype(int) == 0]
            if due_time == 'day':
                today = datetime.strftime(datetime.now(), '%Y-%m-%d')
                task_progress = user_tasks.loc[user_tasks['due_time'].isin([today])]
            print(tabulate(task_progress, headers='keys', tablefmt='fancy_grid'))
            print(f"\n{color.ENDC}")
            # ---
            print(f'{color.YELLOW}*   *   *   *   *   on the way   *   *   *   *   *{color.ENDC}')
            print(color.OKGREEN)
            task_progress = user_tasks.loc[
                (user_tasks['progress'].astype(int) > 0) & (user_tasks['progress'].astype(int) < 80)]
            print(tabulate(task_progress, headers='keys', tablefmt='fancy_grid'))
            print(f"\n{color.ENDC}")
            # ---
            print(f'{color.YELLOW}*   *   *   *   *   almost done   *   *   *   *   *{color.ENDC}')
            print(color.OKGREEN)
            task_progress = user_tasks.loc[
                (user_tasks['progress'].astype(int) >= 80) & (user_tasks['progress'].astype(int) < 100)]
            print(tabulate(task_progress, headers='keys', tablefmt='fancy_grid'))
            print(f"\n{color.ENDC}")
            # ---
            print(f'{color.YELLOW}*   *   *   *   *   done   *   *   *   *   *{color.ENDC}')
            print(color.OKGREEN)
            task_progress = user_tasks.loc[lambda user_tasks: user_tasks['progress'].astype(int) == 100]
            print(tabulate(task_progress, headers='keys', tablefmt='fancy_grid'))
            print(f"\n{color.ENDC}")

    def share_task(self, selection, accept='', task_title='', user_name=''):
        """
        send request for other users or check requests for her/himself and decide to add them to her/his tasks or not
        :param selection: 1 for send task, 2 for chech request
        :param accept: accept to add the task to her tasks or not --> [y/n]
        :param task_title: title of task that share
        :param user_name: name of user that she want to send task for
        """
        if selection == 1:
            # send task
            user_tasks = file.user_row('tasks.csv', self.username)
            for task in user_tasks:
                if task['title'] == task_title:
                    file.store_pandas('requests.csv', user_name, task['title'], self.username,
                                      task['description'], task['link'],
                                      task['location'], task['task_type'],
                                      '', task['due_time'],
                                      task['importance'], task['progress'],
                                      task['importance_degree'], False)
                    print(f"{color.YELLOW}*** Task sent ***{color.ENDC}\n")

        if selection == 2 and accept == 'y':
            request_data = file.user_row('requests.csv', user_name)
            for request in request_data:
                if request['title'] == task_title:
                    file.store_pandas('tasks.csv', request['username'], request['title'],
                                      request['sender'], request['description'], request["link"],
                                      request["location"], request["task_type"],
                                      datetime.strftime(datetime.now(),
                                                        "%Y-%m-%d %H:%M:%S"),
                                      request["due_time"], request["importance"], request["progress"],
                                      request["importance_degree"], True)
                    accepted_index = file.get_index('requests.csv', 'title', task_title, user_name=user_name)
                    file.delete_pandas('requests.csv', int(accepted_index))


if __name__ == "__main__":
    user = User(username='kosar')
    # user.share_task(selection=2, accepted_index=0, user_name='ali')
