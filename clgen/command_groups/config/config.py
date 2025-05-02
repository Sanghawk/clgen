from click import Group

from .openai import openai_group

config_group = Group("config", help="Manage settings.")

config_group.add_command(openai_group)
