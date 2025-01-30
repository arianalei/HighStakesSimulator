def format_command(command):
    if not command:
        return "No command is currently executing."

    # Extract the command name and its parameters
    command_name, *params = command
    # Join the parameters with commas and convert them into a string
    params_text = ', '.join(str(param) for param in params)
    # Return the formatted string
    return f"{command_name}({params_text})"