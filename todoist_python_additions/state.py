import os
import todoist
from os import path
import pickle
from tabulate import tabulate
from datetime import datetime, timedelta

STATE_FN = "/tmp/todoist_state.pkl"
SYNC_INTERVAL = timedelta(minutes=15)
STATE_FN = "/tmp/todoist_state.pkl"
DATE_FORMAT = "%a %d %b %Y %H:%M:%S"
DT_NOW = datetime.now()


def parse_datetime(date_str):
    if date_str is None:
        return None
    return datetime.strptime(date_str[:date_str.find('+')-1], DATE_FORMAT)


def is_overdue(task):
    due_time = parse_datetime(task['due_date_utc'])
    if due_time is None:
        return False

    return task['checked'] != 1 and due_time < DT_NOW


class Todoist(object):

    def __init__(self, sync=False):
        self.sync = sync

    def __enter__(self):
        self.get_state(force_sync=self.sync)
        return self

    def __exit__(self, *args):
        self.persist(self.state)

    def _synced_state(self):
        API_KEY = os.environ["TODOIST_API_TOKEN"]
        api = todoist.TodoistAPI(API_KEY)
        api.sync()

        # @aagnone state additions
        project_map = {project['id']: project for project in api.state['projects']}
        item_map = {item['id']: item for item in api.state['items']}
        for _id, item in item_map.items():
            item_map[_id]['project'] = project_map[item['project_id']]['name']

        self.api = api
        self.state = api.state
        self.item_map = item_map
        self.project_map = project_map
        self.sync_time = datetime.now()

    def get_state(self, force_sync=False):
        if path.exists(STATE_FN):
            with open(STATE_FN, 'rb') as fp:
                state = pickle.load(fp)

            if force_sync or datetime.now() - state["sync_time"] > SYNC_INTERVAL:
                self._synced_state()
        else:
            self._synced_state()

    def get_overdue_tasks(self):
        return list(filter(is_overdue, self.state['items']))

    def has_project_ancestor(self, probe_id, target_name):
        project = self.project_map[probe_id]
        parent_project_id = project['parent_id']
        if parent_project_id:
            return self.has_project_ancestor(parent_project_id, target_name)
        return project['name'] == target_name

    def get_subtasks(self, project_root):
        data = []
        for item in self.state['items']:
            if self.has_project_ancestor(item['project_id'], project_root):
                data.append(item)
        return data

    def persist(self, state):
        with open(STATE_FN, 'wb') as fp:
            state = pickle.dump(state, fp)
