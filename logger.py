def log_message(message):
    filename="logs.txt"
    with open(filename, 'a') as file:
        file.write(message + '\n')