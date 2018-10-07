#!/usr/bin/env python
import os
import todoist
import pickle
from os import path
from tabulate import tabulate
from datetime import datetime, timedelta

from todoist_python_additions.lib.state import Todoist
from todoist_python_additions.lib.notify import send_text
from todoist_python_additions.lib.self_email import send_mail


def main():
    with Todoist(sync=True) as api:
        tasks = api.get_overdue_tasks()

        if len(tasks) > 0:
            msg = "Overdue Tasks"
            for d in tasks:
                msg += "\n({}) {}".format(d['project'], d['content'])
            send_mail(msg, subject="OVERDUE TASKS")

if __name__ == '__main__':
    main()
