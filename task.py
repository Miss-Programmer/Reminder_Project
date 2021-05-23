import pandas as pd
from datetime import datetime, timedelta
from colors import bcolors as color
import logging
import file

logging.basicConfig(level=logging.INFO, filename='log_data.log', filemode='a',
                    format=' %(asctime)s - %(name)s - %(levelname)s -%(message)s ')


class Task:
    def __init__(self, username, title="", sender='', description="", link="", location="", task_type="",
                 created_time=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
                 due_time=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
                 importance="", progress=0, importance_degree=0, accepted=True):
        """
        username: username that task belongs to --> string
        title : name of the task --> string
        sender : another user who send the task for this user --> string
        description : description of the task --> string
        link : link of the task --> string
        location : location of the task --> location
        task_type : type of the task. task_types: [exam, hobby, study, personal] --> string
        created_time : the datetime that task created --> string
        due_time : the datetime that task should done --> string
        importance : the importance of task base on Eisenhower matrix(Do, Decide, Delegate, Delete) --> string
        progress : percentage of doing the task --> int
        importance_degree : importance of the task showing by number (1,2,3,4)--> int
        accepted: is True when user accept it. it's False when user don't accept it to be in her tasks
        """
        self.username = username
        self.title = title
        self.description = description
        self.link = link
        self.location = location
        self.task_type = task_type
        self.created_time = created_time
        self.due_time = due_time
        self.importance = importance
        self.progress = progress
        self.importance_degree = importance_degree
        self.sender = sender
        self.accepted = accepted

    def create_task(self, username, title, description, link, location, task_type, due_time):
        """
        user can create task here and initialize all task's attribute for it. it'll save in tasks.csv file
        :param username: username of who create task
        :param title: title of task
        :param description: description of task
        :param link: link of task
        :param location: location of task
        :param task_type: type of task *if task_type doesn't exist in ['personal', 'exam', 'hobby', 'study'], we log it
        :param due_time: due_time of task
        """
        self.created_time, self.title, self.description, self.link, self.location, self.task_type, self.due_time, \
        self.accepted, self.username = datetime.strftime(datetime.now(),
                                                         "%Y-%m-%d %H:%M:%S"), title, description, link, location, \
                                       task_type, datetime.strptime(due_time, "%Y-%m-%d %H:%M:%S"), True, username
        self.eisenhower_matrix()
        self.progress_in_task(user_name=self.username)

        file.store_pandas('tasks.csv', self.username, self.title, self.sender, self.description, self.link,
                          self.location,
                          self.task_type, self.created_time, self.due_time, self.importance, self.progress,
                          self.importance_degree, self.accepted)

        print(f"{color.YELLOW}*** '{self.title}' created! ***{color.ENDC}\n")

        logging.info(f"TASK ADDED! {self.username}'s task created with name {self.title}")

        tasks_type = ['personal', 'exam', 'hobby', 'study']
        if self.task_type not in tasks_type:
            logging.info(
                f"New task type! {self.username} define new task_type with name {self.task_type} for task {self.title}")

    def eisenhower_matrix(self, location=-1):
        """
        initialize importance attribute of task and create eisenhower matrix
        :param location: index of row that we may want to change eisenhower matrix's attributes for it --> int
        """
        try:
            print(f"{color.YELLOW}- Now please choose one of the items about your task -{color.ENDC}")
            print(f"{color.BLUE}1- immediate and important")
            print("2- immediate and NOT-important")
            print("3- NON-immediate and important")
            print(f"4- NON-immediate and NOT-important{color.ENDC}")
            user_selection = int(input('>>>> ').strip().replace(" ", ""))
            if user_selection == 1:
                # set reminder every 5 min
                self.importance = "Do!"
                self.importance_degree = 1
            elif user_selection == 2:
                # remind whenever user wants
                self.importance = "Decide!"
                self.importance_degree = 2
            elif user_selection == 3:
                # show in the end of the day
                self.importance = "Delegate"
                self.importance_degree = 3
            elif user_selection == 4:
                # show in the end of the week
                self.importance = "Delete"
                self.importance_degree = 4
            if location != -1:
                file.change_pandas('tasks.csv', 'importance', self.importance, self.username, location)
                file.change_pandas('tasks.csv', 'importance_degree', self.importance_degree, self.username, location)

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error Occurred. {e}")

    def edit_task(self, location, user_selection, new_value):
        """
        user can edit some attributes of task in this function
        :param location: index of row in tasks.csv that we want to change
        :param user_selection: edit for : 1:title,2:description,3:link,4:location,5:due time,6:importance,7:progress
        :param new_value: new value for change
        :return:
        """
        tasks_attribute = ['title', 'description', 'link', 'location', 'due_time']
        for i in range(len(tasks_attribute) - 1):
            if user_selection == i + 1:
                file.change_pandas('tasks.csv', tasks_attribute[i], new_value, self.username, location)

        if user_selection == 6:
            # edit importance
            self.eisenhower_matrix(location)
        elif user_selection == 7:
            # edit progress
            self.progress_in_task(location, self.username)
        print(f'{color.YELLOW}*** changed successfully ***{color.ENDC}\n')

    @staticmethod
    def delete_task(location):
        """
        delete task that user want
        :param location: index of row of tasks.csv for delete --> int
        """
        file.delete_pandas('tasks.csv', location)
        print(f'{color.YELLOW}*** task deleted successfully ***{color.ENDC}\n')

    def progress_in_task(self, location=-1, user_name=''):
        """
        update progress attribute base on percentage of doing the task
        :param location: index of task in tasks.csv that we want to update progress
        :param user_name: username of owner of task
        """
        print(f"{color.YELLOW}Any Progress?! [y/n]{color.ENDC}")
        new_progress = input('>>>> ').lower().strip().replace(" ", "")
        if new_progress == 'y':
            self.progress = int(
                input(f"{color.BOLD}Please write the new progress percentage: {color.ENDC}").strip().replace(" ", ""))
            file.change_pandas('tasks.csv', 'progress', self.progress, user_name, location)
            print(f"{color.YELLOW}*** Progress Updated ***")
            print('\n')

        elif new_progress == 'n':
            pass

        if self.progress == 0:
            print(f"{color.OKCYAN}task status : not started{color.ENDC}")
        elif 80 > self.progress > 0:
            print(f"{color.OKCYAN}task status : On The Way...{color.ENDC}")
        elif 100 > self.progress >= 80:
            print(f"{color.OKCYAN}task status : Almost Done...{color.ENDC}")
        elif self.progress == 100:
            print(f"{color.OKCYAN}task status : Done{color.ENDC}")
            logging.info(f"{self.username} completed task {self.title}")
        print('\n')

    @staticmethod
    def postpone(user_name, due_time, select_postpone):
        """
        postponed task for one day or one week. actually change due_time
        :param user_name: username of task's owner
        :param due_time: old due_time of task
        :param select_postpone: 1: one day, 2: one week
        """
        try:
            new_due_time = None
            if select_postpone == 1:
                # 1 day
                new_due_time = datetime.strptime(due_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
                logging.info(f"{user_name} postpone task for one day")

            elif select_postpone == 2:
                # 1 week
                new_due_time = datetime.strptime(due_time, "%Y-%m-%d %H:%M:%S") + timedelta(weeks=1)
                logging.info(f"{user_name} postpone task for one week")
            else:
                raise Exception("invalid input")

            location = file.get_index('tasks.csv', 'due_time', due_time, user_name=user_name)
            file.change_pandas('tasks.csv', 'due_time', new_due_time, location=location)
            print(f'{color.YELLOW}*** postponed successfully ***{color.ENDC}\n')

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error Occurred. {e}")


