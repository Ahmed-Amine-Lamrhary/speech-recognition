from executors.command_executor import command_map

def execute_command(command_name, text):
    executor = command_map.get(command_name)
    executor.execute(text)
