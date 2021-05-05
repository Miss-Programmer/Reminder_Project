from colors import bcolors as color
import pandas as pd
import hash_password as hashing
import emoji
import csv
from task import Task
from tabulate import tabulate


class User:
    def __init__(self, username='', password='', log_in=False):
        self.username = username
        self.password = password
        self.log_in = log_in

    def signup(self):
        print(f"{color.OKBLUE}---------------------------signup---------------------------\n{color.ENDC}")
        df = pd.read_csv('user_pass.csv')
        while True:
            input_username = input(f"{color.PURPLE}please make a username: {color.ENDC}")
            if input_username in df.values:
                print(f"{color.RED}!!! This username is already exist. please select another username !!!{color.ENDC}")
            elif input_username == '':
                print(f"{color.RED}!!! INVALID USERNAME !!!{color.ENDC}")
            else:
                input_password = hashing.hash_password(input(f"{color.PURPLE}please create a password: {color.ENDC}"))
                self.username = input_username
                self.password = input_password
                df = df.append({'username': input_username, 'password': input_password}, ignore_index=True)
                df.to_csv('user_pass.csv', index=False)
                print(f"{color.YELLOW}*** Welcome {self.username} {emoji.emojize(':smiling_face_with_smiling_eyes:')}"
                      f" ***{color.ENDC}\n")

                # self.login()
                break

    def login(self):
        print(f"{color.OKBLUE}---------------------------login---------------------------\n{color.ENDC}")
        df = pd.read_csv('user_pass.csv')
        input_username = input(f'{color.PURPLE}username: {color.ENDC}')
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
                    print(f"{color.RED}!!! INPUT NOT VALID !!!{color.ENDC}")

            elif input_username == '':
                print(f"{color.RED}!!! INPUT NOT VALID !!!{color.ENDC}")

            elif input_username in df.values:
                with open('user_pass.csv', 'r') as userPass_file:
                    csv_reader = csv.DictReader(userPass_file)
                    for row in csv_reader:
                        if row['username'] == input_username:
                            input_password = input(f"{color.PURPLE}password: {color.ENDC}")
                            if hashing.verify_password(row['password'], input_password) is True:
                                self.username = row['username']
                                self.password = row['password']
                                print(f"{color.YELLOW}*** Welcome {self.username} "
                                      f"{emoji.emojize(':smiling_face_with_smiling_eyes:')} ***"
                                      f"{color.ENDC}\n")
                                self.log_in = True
                                allowed = 3

                            elif self.log_in is False:
                                if allowed < 2:
                                    print(
                                        f"{color.RED}!!! your password is wrong. please try again !!!\n{color.ENDC}")
                                    allowed += 1
                                    # login_func(self)
                                elif allowed == 2:
                                    allowed = 3
                                    print(
                                        f"{color.BOLD}{color.RED}"
                                        f"!!! You tried 3 times ... Please Try again later [action blocked] !!!\n"
                                        f"{color.ENDC}")
        # c = input("change password?")
        # if c == 'y':
        #     self.change_password()

    def change_password(self):
        print(f"{color.OKBLUE}-------------------------change password-------------------------\n{color.ENDC}")
        change = pd.read_csv('user_pass.csv')
        location = 0
        old_password = input(f"{color.PURPLE}Enter old password: ")
        with open('user_pass.csv', 'r') as my_file:
            csv_reader = csv.DictReader(my_file)
            for row in csv_reader:
                if row['username'] == self.username and hashing.verify_password(row['password'],
                                                                                old_password) is True:
                    new_password = input(f"Enter new password: {color.ENDC}")
                    hash_new_pass = hashing.hash_password(new_password)
                    self.password = hash_new_pass
                    print(f"{color.YELLOW}*** Your password is changed ***{color.ENDC}")
                    change.loc[location, 'password'] = hash_new_pass
                    change.to_csv('user_pass.csv', index=False)

            else:
                if self.log_in is False:
                    print(f'{color.RED}!!! WRONG PASSWORD !!!{color.ENDC}')

            location += 1

    def user__add_task(self):
        print(f"{color.OKBLUE}---------------------------Add Task---------------------------\n{color.ENDC}")
        task = Task(self.username)
        Task.create_task(task)

    def user__delete_task(self):
        """
        read tasks from pandas and show user list of her tasks. then user choose and delete one of them
        """
        print(f"{color.OKBLUE}---------------------------Delete Task---------------------------\n{color.ENDC}")
        # show tasks
        print(f"{color.YELLOW}Delete Which task? [enter the index]")
        tasks_data = pd.read_csv('tasks.csv')
        user_tasks = tasks_data[tasks_data['username'] == self.username]
        print(tabulate(user_tasks[['title']], headers='keys', tablefmt='fancy_grid'))

        # get input and call delete_task function to delete it
        location = int(input(f"{color.BOLD}Enter the number: {color.ENDC}"))
        print('\n')
        Task.delete_task(location)

    def user__edit_task(self):
        """
        user can edit task
        """
        print(f"{color.OKBLUE}---------------------------Edit Task---------------------------\n{color.ENDC}")
        # show tasks
        print(f"{color.YELLOW}For Which task? [enter the index]")
        tasks_data = pd.read_csv('tasks.csv')
        user_tasks = tasks_data[tasks_data['username'] == self.username]
        print(tabulate(user_tasks[['title']], headers='keys', tablefmt='fancy_grid'))

        # choose the task number and location and call edit_task()
        task = Task(self.username)
        location = int(input(f"{color.BOLD}Enter the number: {color.ENDC}"))
        print('\n')
        Task.edit_task(task, location)

    def user__show_everything(self):
        """
        user can see every information about the tasks like attributes and calender and eisenhower
        and followers and followings
        """
        print(f"{color.OKBLUE}-------------------------Show Tasks With Detail-------------------------\n{color.ENDC}")
        print(color.OKGREEN)
        tasks_data = pd.read_csv("tasks.csv")
        # filter on current user
        user_tasks = tasks_data[tasks_data['username'] == self.username]
        print(tabulate(user_tasks, headers='keys', tablefmt='fancy_grid'))
        print(f'\n{color.ENDC}')

    def user__tasks(self):
        """
        show tasks of the user to him/her
        """
        print(f"{color.OKBLUE}---------------------------Show Task names---------------------------\n{color.ENDC}")
        print(color.OKGREEN)
        tasks_data = pd.read_csv('tasks.csv')
        user_tasks = tasks_data[tasks_data['username'] == self.username]
        # task_titles = user_tasks.title.to_string(index=True)
        print(tabulate(user_tasks[['title']], headers='keys', tablefmt='fancy_grid'))
        print(f'\n{color.ENDC}')

    def user__progress(self):
        # show tasks
        print(f"{color.YELLOW}For Which task? [enter the index]")
        tasks_data = pd.read_csv('tasks.csv')
        user_tasks = tasks_data[tasks_data['username'] == self.username]
        print(tabulate(user_tasks[['title']], headers='keys', tablefmt='fancy_grid'))

        # choose the task number and location and call progress_in_task()
        task = Task(self.username)
        location = int(input(f"{color.BOLD}Enter the number: {color.ENDC}"))
        print('\n')
        Task.progress_in_task(task, location, self.username)

    @staticmethod
    def user__see_calender():
        """
        user can see all of tasks in calender
        """
