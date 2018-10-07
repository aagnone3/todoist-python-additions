#!/usr/bin/env python
import os
import todoist
import pickle
from os import path
from argparse import ArgumentParser

from todoist_python_additions.lib.state import Todoist


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-p', '--project', required=True, help='Project to get descendant tasks of.')
    return parser


def main():
    args = build_parser().parse_args()

    with Todoist(sync=True) as api:
        tasks = api.get_subtasks(args.project)

        if len(tasks) > 0:
            for task in tasks:
                print("({}) {}".format(task['project'], task['content']))
        else:
            print("No tasks under {}".format(args.project))


if __name__ == '__main__':
    main()
