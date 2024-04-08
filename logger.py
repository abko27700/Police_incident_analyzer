def log_message(message):
    filename="logs.txt"
    """Simple function to log a message to a specified file."""
    with open(filename, 'a') as file:
        file.write(message + '\n')