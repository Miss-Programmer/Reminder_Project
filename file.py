import csv
import logging
import os
from tabulate import tabulate
import pandas as pd

try:
    def read_pandas(file, user_name, attribute):
        """
        read from file and print rows of attribute, that belongs to user_name
        """
        tasks_data = pd.read_csv(file)
        user_tasks = tasks_data[tasks_data['username'] == user_name]
        print(tabulate(user_tasks[[attribute]], headers='keys', tablefmt='fancy_grid'))


    def read_pandas_not(file, user_name, attribute):
        """
        read from file and print rows of attribute, that don't belongs to user_name
        """
        tasks_data = pd.read_csv(file)
        user_tasks = tasks_data[tasks_data['username'] != user_name]
        print(tabulate(user_tasks[[attribute]], headers='keys', tablefmt='fancy_grid'))


    def read_all_pandas(file, user_name):
        """
        read from file and print rows belongs to user_name
        :return: dataframe of all rows belong to username
        """
        data = pd.read_csv(file)
        user_data = data[data['username'] == user_name]
        print(tabulate(user_data, headers='keys', tablefmt='fancy_grid'))
        return user_data


    def delete_pandas(file, location):
        """
        delete specific row of file
        """
        tasks_data = pd.read_csv(file)
        tasks_data.drop([location], axis=0, inplace=True)
        tasks_data.to_csv(file, index=False)


    def change_pandas(file, attribute, new_value, user_name='', location=-1):
        """
        change and update file
        :param file: file user want to change
        :param attribute: attribute that user want to change
        :param new_value: new value for replace
        :param user_name: owner of row
        :param location: index of row for change
        """
        data = pd.read_csv(file)
        if location == -1:
            location = data[data['username'] == user_name].index.values
        data.loc[location, [attribute]] = new_value
        data.to_csv(file, index=False)


    def store_pandas(file, user_name, title, sender, description, link, location, task_type, created_time, due_time,
                     importance, progress, importance_degree, accepted):
        """
        store a new row to file
        """
        new_data = pd.DataFrame(
            [{'username': user_name, 'title': title, 'sender': sender, 'description': description, 'link': link,
              'location': location, 'task_type': task_type, 'created_time': created_time, 'due_time': due_time,
              'importance': importance, 'progress': progress, 'importance_degree': importance_degree,
              'accepted': accepted}],
            columns=['username', 'title', 'sender', 'description', 'link', 'location', 'task_type',
                     'created_time', 'due_time', 'importance', 'progress', 'importance_degree', 'accepted'])
        new_data.to_csv(file, index=False, mode='a', header=False)


    def user_row(file, user_name):
        """
        read file and find rows belongs to user_name
        :return: list of user tasks
        """
        user_tasks = []
        with open(file) as open_file:
            file_reader = csv.DictReader(open_file)
            for row in file_reader:
                if row['username'] == user_name:
                    user_tasks.append(row)
        return user_tasks


    def get_index(file, attribute, value, user_name):
        """
        get index of user row with specific value
        :param file: file for search
        :param attribute: attribute for search
        :param value: specific value that should be in row
        :param user_name: name of user in row
        :return: index of specific row --> int
        """
        file_data = pd.read_csv(file)
        user_file = file_data[file_data['username'] == user_name]
        index = user_file[user_file[attribute] == value].index.values
        return index


except FileNotFoundError as fnf_error:
    print("Error. File not found")
    logging.error(fnf_error)


def check_exist():
    """
    for all files in this project, check if that file doesn't exist, create it and write header for it
    """
    if os.path.exists('tasks.csv'):
        pass
    else:
        with open('tasks.csv', 'w') as tasks:
            fields = ['username', 'title', 'sender', 'description', 'link', 'location', 'task_type', 'created_time',
                      'due_time', 'importance', 'progress', 'importance_degree', 'accepted']
            task_writer = csv.DictWriter(tasks, fieldnames=fields)
            task_writer.writeheader()
    if os.path.exists('user_pass.csv'):
        pass
    else:
        with open('user_pass.csv', 'w') as user_pass:
            fields = ['username', 'password', 'user_status']
            user_pass_writer = csv.DictWriter(user_pass, fieldnames=fields)
            user_pass_writer.writeheader()

    if os.path.exists('requests.csv'):
        pass
    else:
        with open('requests.csv', 'w') as requests:
            fields = ['username', 'title', 'sender', 'description', 'link', 'location', 'task_type', 'created_time',
                      'due_time', 'importance', 'progress', 'importance_degree', 'accepted']
            request_writer = csv.DictWriter(requests, fieldnames=fields)
            request_writer.writeheader()


if __name__ == '__main__':
    # data = read_all_pandas('requests.csv', 'ali')
    pass
