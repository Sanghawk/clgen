from click import Group

from .openai import openai_command_group

config_command_group = Group("config", help="Manage settings.")

config_command_group.add_command(openai_command_group)
