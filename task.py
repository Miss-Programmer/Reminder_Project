import pandas as pd
from datetime import datetime, timedelta
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import csv
from colors import bcolors as color
import time
import schedule


class Task:
    def __init__(self, username, title="", description="", link="", location="", task_type="",
                 date_remind="", time_remind="", created_time=JalaliDateTime.today(), due_time=JalaliDateTime.today(),
                 importance="", progress=0, importance_degree=0, sender=''):
        """
        title : name of the task --> string
        description : description of the task --> string
        link : link of the task --> string
        location : location of the task --> location
        task_type : type of the task. for example: sport, education, diet, habits, ... --> string
        date_remind : the date that the task should remind to user --> string
        time_remind : the time that the task should remind to user --> string
        created_time : the datetime that task created --> string
        due_time : the datetime that task should done --> string
        importance : the importance of task base on Eisenhower matrix(Do, Decide, Delegate, Delete) --> string
        progress : percentage of doing the task --> int
        importance_degree : importance of the task showing by number (1,2,3,4)--> int
        followers : the other users that add the user tasks to their profile --> ...
        following : the other users that the user add their tasks to her/his profile
        """
        self.username = username
        self.title = title
        self.description = description
        self.link = link
        self.location = location
        self.task_type = task_type
        self.date_remind = date_remind
        self.time_remind = time_remind
        self.created_time = created_time
        self.due_time = due_time
        self.importance = importance
        self.progress = progress
        self.importance_degree = importance_degree
        self.sender = sender
        # self.followers = followers
        # self.following = following

    def create_task(self):
        """
        user can create task here and initialize some attributes for it
        """
        print(f"{color.YELLOW}*** Please fill the following attributes for your task ***{color.ENDC}")
        time_format = '%Y-%m-%d %H:%M:%S'
        self.created_time = datetime.strptime(JalaliDateTime.today().strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")
        self.title = input(f"{color.PURPLE}title: ")
        self.description = input("description: ")
        self.link = input("link: ")
        self.location = input("location: ")
        self.task_type = input("task type: ")
        self.due_time = datetime.strptime(
            input(f"When should you finish? [year/month/day hour:minute:second] {color.ENDC}"), "%Y/%m/%d %H:%M:%S")
        # self.due_time = JalaliDateTime(due_time, "%A -- %Y/%m/%d")
        # remind time specified base on eisenhower_matrix
        # I should convert the string into time with strptime ****
        # maybe we can store the task here
        self.eisenhower_matrix()
        self.progress_in_task()

        # store tasks with pandas
        task_data = pd.DataFrame({'username': [self.username], 'title': [self.title], 'description': [self.description],
                                  'link': [self.link], 'location': [self.location], 'task_type': [self.task_type],
                                  'date_remind': [self.date_remind],
                                  'time_remind': [self.time_remind], 'created_time': [self.created_time],
                                  'due_time': [self.due_time], 'importance': [self.importance],
                                  'progress': [self.progress], 'importance_degree': [self.importance_degree],
                                  'sender': [self.sender]},
                                 columns=['username', 'title', 'description', 'link', 'location', 'task_type',
                                          'date_remind', 'time_remind', 'created_time', 'due_time',
                                          'importance', 'progress', 'importance_degree', 'sender'])
        task_data.to_csv("tasks.csv", index=False, mode='a', header=False)

        print(f"{color.YELLOW}*** '{self.title}' created! ***{color.ENDC}\n")

    # @staticmethod
    def task_reminder(self, importance_degree):
        """
        print notification for every task base on the importance attribute
        it is staticmethod because we should do it for all of user's tasks
        """
        self.importance_degree = importance_degree
        if self.importance_degree == 1:
            schedule.every(5).seconds.do(self.print_remind_message())
        elif self.importance_degree == 2:
            today = datetime.strptime(JalaliDateTime.today().strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")
            due_day = self.due_time.strftime("%Y/%m/%d %H:%M:%S")
            hour = self.due_time.strftime("%H")
            if today == due_day:
                schedule.every().day.at(hour).do(self.print_remind_message())
        elif self.importance_degree == 3:
            schedule.every().day.at("21:00:00").do(self.print_remind_message())
        elif self.importance_degree == 4:
            schedule.every().friday.at('21:00:00').do(self.print_remind_message())

    def print_remind_message(self):
        print(f"o0o0o0o0o0o0o0o Don't Forget {self.title} o0o0o0o0o0o0o0o")

    def eisenhower_matrix(self):
        """
        initialize importance attribute of task and create eisenhower matrix
        """
        print(f"{color.YELLOW}- Now please choose one of the items about your task -{color.ENDC}")
        print(f"{color.BLUE}1- immediate and important")
        print("2- immediate and NOT-important")
        print("3- NON-immediate and important")
        print(f"4- NON-immediate and NOT-important{color.ENDC}")
        user_selection = int(input('>>>> '))
        if user_selection == 1:
            # set reminder every 5 min
            self.importance = "Do!"
            self.importance_degree = 1
            # self.task_reminder(1)
        elif user_selection == 2:
            # remind whenever user wants
            self.importance = "Decide!"
            self.importance_degree = 2
            # self.task_reminder(2)
        elif user_selection == 3:
            # show in the end of the day
            self.importance = "Delegate"
            self.importance_degree = 3
            # self.task_reminder(3)
        elif user_selection == 4:
            # show in the end of the week
            self.importance = "Delete"
            self.importance_degree = 4
            # self.task_reminder(4)
        else:
            print("Invalid input")

    def edit_task(self, location):
        """
        user can edit some attributes of task in this function
        """
        print(f"{color.YELLOW}--- What would you like to edit? ---{color.ENDC}")
        print(f"{color.OKCYAN}1- title")
        print("2- description")
        print("3- link")
        print("4- location")
        print("5- date of reminder")
        print("6- time of reminder")
        print("7- due time")
        print("8- importance")
        print(f"9- progress{color.ENDC}")
        user_selection = int(input())
        user_tasks = pd.read_csv('tasks.csv')
        if user_selection == 1:
            # edit title
            self.title = input(f"{color.BOLD}Please write the new title: {color.ENDC}")
            # user_tasks.replace({'title': self.title}, inplace=True)
            user_tasks.loc[[location], ['title']] = self.title
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 2:
            # edit description
            self.description = input(f"{color.BOLD}Please write the new description: {color.ENDC}")
            user_tasks.loc[[location], ['description']] = self.description
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 3:
            # edit link
            self.link = input(f"{color.BOLD}Please write the new link: {color.ENDC}")
            user_tasks.loc[[location], ['link']] = self.link
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 4:
            # edit location
            self.location = input(f"{color.BOLD}Please write the new location: {color.ENDC}")
            user_tasks.loc[[location], ['location']] = self.location
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 5:
            # edit date of reminder
            self.date_remind = input(f"{color.BOLD}Please write the new date to remind: {color.ENDC}")
            user_tasks.loc[[location], ['date_remind']] = self.date_remind
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 6:
            # edit time of reminder
            self.time_remind = input(f"{color.BOLD}Please write the new time to remind: {color.ENDC}")
            user_tasks.loc[[location], ['time_remind']] = self.time_remind
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 7:
            # edit due time
            self.due_time = input(f"{color.BOLD}Please write the new due time: {color.ENDC}")
            user_tasks.loc[[location], ['due_time']] = self.due_time
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 8:
            # edit importance
            # self.eisenhower_matrix()
            print(f"{color.YELLOW}- Now please choose one of the items about your task -{color.ENDC}")
            print(f"{color.BLUE}1- immediate and important")
            print("2- immediate and NOT-important")
            print("3- NON-immediate and important")
            print(f"4- NON-immediate and NOT-important{color.ENDC}")
            user_selection = int(input('>>>> '))
            if user_selection == 1:
                # set reminder every 5 min
                self.importance = "Do!"
                user_tasks.loc[[location], ['importance']] = self.importance
                # self.task_reminder(1)
            elif user_selection == 2:
                # remind whenever user wants
                self.importance = "Decide!"
                user_tasks.loc[[location], ['importance']] = self.importance
                # self.task_reminder(2)
            elif user_selection == 3:
                # show in the end of the day
                self.importance = "Delegate"
                user_tasks.loc[[location], ['importance']] = self.importance
                # self.task_reminder(3)
            elif user_selection == 4:
                # show in the end of the week
                self.importance = "Delete"
                user_tasks.loc[[location], ['importance']] = self.importance
                # self.task_reminder(4)
            else:
                print("Invalid input")
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        elif user_selection == 9:
            # edit progress
            self.progress = input(f"{color.BOLD}Please write the new progress percentage: {color.ENDC}")
            user_tasks.loc[[location], ['progress']] = self.progress
            print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')
        else:
            print("invalid input")

        # update the file
        user_tasks.to_csv('tasks.csv', index=False)

    @staticmethod
    def delete_task(location):
        """
        a task can be deleted by user
        """
        tasks_data = pd.read_csv('tasks.csv')
        # tasks_data=tasks_data.drop(location)
        tasks_data.drop([location], axis=0, inplace=True)
        print(f'{color.YELLOW}*** task deleted successfully ***{color.ENDC}')
        tasks_data.to_csv('tasks.csv', index=False)

    def progress_in_task(self, location=0, user_name=''):
        """
        initialize progress attribute base on percentage of doing the task
        """
        user_tasks = pd.read_csv('tasks.csv')
        print(f"{color.YELLOW}Any Progress?! [y/n]{color.ENDC}")
        new_progress = input('>>>> ').lower()
        if new_progress == 'y':
            self.progress = int(input(f"{color.BOLD}Please write the new progress percentage: {color.ENDC}"))
            user_tasks.loc[[location], ['progress']] = self.progress
            user_tasks.to_csv('tasks.csv', index=False)
            print(f"{color.YELLOW}*** Progress Updated ***")
            print('\n')
        elif new_progress == 'n':
            pass
        user_progress = user_tasks.iloc[location]['progress']
        self.progress = user_progress

        if self.progress == 0:
            print(f"{color.OKCYAN}task status : not started{color.ENDC}")
            user_tasks.to_csv('tasks.csv', index=False)
        elif 80 > self.progress > 0:
            print(f"{color.OKCYAN}task status : On The Way...{color.ENDC}")
        elif 100 > self.progress >= 80:
            print(f"{color.OKCYAN}task status : Almost Done...{color.ENDC}")
        elif self.progress == 100:
            print(f"{color.OKCYAN}task status : Done{color.ENDC}")
        print('\n')

    def categorize_tasks(self):
        """
        store every task in list base on progress
        * not started
        * started
        * almost done
        * done
        user can categorize them base on day, week, or month
        """
        print("categorize_tasks")

    def show_task_in_calender(self):
        """
        user can show created time and due time of task in calender
        """
        print("show_task_in_calender")

    def share_task(self):
        """
        first, user should follow other user --> following += 1
        then watch her/his tasks, choose them
        then, chose tasks add to users tasks
        """
        print("share_task")

    @staticmethod
    def calender():
        """
        show all of the tasks in calender
        """
        print("calender")

# while True:
#     schedule.run_pending()
#     time.sleep(1)
# task = Task('negin')
# task.delete_task(2)
