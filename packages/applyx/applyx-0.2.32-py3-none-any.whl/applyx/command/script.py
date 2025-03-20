# coding=utf-8

import os
import sys
from importlib import import_module

from applyx.command.base import BaseCommand


class Command(BaseCommand):
    def register(self, subparser):
        parser = subparser.add_parser('script', help='run script')
        parser.add_argument(
            '-s',
            '--script',
            type=str,
            dest='script',
            default='',
            help='specify script module',
        )
        parser.add_argument(
            '-v',
            '--vars',
            type=str,
            dest='extra_vars',
            action='append',
            default=[],
            help='specify extra arguments',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='enable debug mode',
        )

    def invoke(self, args):
        if not args.script:
            print('should specify script module')
            return

        script_module_name = f'{self.project.__package__}.scripts.{args.script}'
        script_module = import_module(script_module_name)

        variables = {}
        for item in args.extra_vars:
            segs = item.split('=')
            if len(segs) != 2:
                print(f'Invalid extra variables {item}')
                sys.exit()
            variables[segs[0]] = segs[1]

        script_class = getattr(script_module, 'Script', None)
        if script_class is None:
            print(f'{args.script}.Script not found')
            return

        script_instance = script_class(variables=variables, debug=args.debug)
        script_instance.run()
