import subprocess
import csv
from tkinter.filedialog import askopenfilename
from os import getcwd, listdir, path, mkdir
import components.configHandler as configHandler
from components.colors import colors

filepath = path.dirname(path.realpath(__file__))
commandfiles = [x.replace(".txt", "") for x in listdir(f'{filepath}/commands')]
config, indexes = configHandler.loadConfig(filepath)

# Make directories if they don't exist
mkdir(f'{filepath}/commands') if path.isdir(f'{filepath}/commands') == False else None
mkdir(f'{filepath}/files') if path.isdir(f'{filepath}/files') == False else None


def autoComplete(text, state):
    possibles = [str(x) for x in commandfiles if x.startswith(text)]
    if state < len(possibles):
        return possibles[state]
    else:
        return None

try:
    import readline
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autoComplete)
except:
    pass

def menu():
    while True:
        try:
            option = int(input(f'''
{colors.WARNING}1. {colors.INPUT}Run commands
{colors.WARNING}2. {colors.INPUT}Remove rows from CSV
{colors.WARNING}3. {colors.INPUT}New Config
{colors.WARNING}4. {colors.INPUT}Quit{colors.ENDC}

Whats u wants to dos: '''))
            match option:
                case 1:
                    commandFile()
                case 2:
                    stripRows()
                case 3:
                    configHandler.addConfig(filepath)
                case 4:
                    quit()
        except ValueError:
            print(f"{colors.ECHO}Bruh{colors.ENDC}")

# Function for handling command files


def commandFile():
    while True:
        try:
            filename = input(
                f'\n{colors.INPUT}Input name of command file{colors.ENDC}: ')
            commands = []
            with open(f"./commands/{filename}.txt") as file:
                for line in file:
                    commands.append(line.strip('\n'))
            for command in commands:
                checked_command = checkInserts(command)
                runCommand(checked_command) if checked_command else None
            break
        except Exception as e:
            print(e)


# Function for checking possible inserts in command strings
def checkInserts(command: str):
    inserts = {
        "INSERTVAR": lambda a, b: a.replace(b, input(f'\n{colors.WARNING}COMMAND {colors.COMMAND}{a} {colors.WARNING}REQUIRES USER INPUT IN PLACE OF {colors.INPUT}{b}{colors.ENDC}: ')),
        "FILENAME": lambda a, b: a.replace(b, askopenfilename(initialdir="./files")),
        "echo": lambda a, b: (a.replace(b, f'{b} {colors.ECHO}')+colors.ENDC) if (a[0:4] == "echo") else a
        # "FILENAME": lambda a, b: a.replace(b, print(f'\n{colors.WARNING}COMMAND {colors.COMMAND}{a} {colors.WARNING}REQUIRES FILE FOR {colors.INPUT}{b}{colors.WARNING} - SELECT FILE FROM DIRECTORY{colors.ENDC}{askopenfilename(initialdir="./files")}')),
    }
    if checkConditions(command):
        return False
    for insert in inserts.keys():
        if insert in command:
            return inserts[insert](command, insert)
    return command


def checkConditions(command: str):
    conditionWasMet = False

    for cmd in indexes.keys():
        if cmd in command:
            configObject = config[indexes[cmd]]
            print(f'''
{colors.WARNING}Condition was present for command {colors.COMMAND}{command}{colors.WARNING}... 
Checking for conditions({colors.COMMAND}{configObject["condition"]}{colors.WARNING}) from{colors.COMMAND} {configObject["depends"]}{colors.ENDC}:''')
            try:
                commandrun = subprocess.run(
                    [configObject["depends"]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout = commandrun.stdout.decode('utf-8').split("\n")
                print(
                    f'{colors.INPUT}{commandrun.stdout.decode("utf-8")}{colors.ENDC}')
                for line in stdout:
                    for i in range(len(configObject["condition"])):
                        # print(i+1, configObject["condition"]
                        #       [i], len(configObject["condition"]))
                        if configObject["condition"][i] in line:
                            conditionWasMet = True
                        else:
                            conditionWasMet = False
                            break
                    if conditionWasMet:
                        print(
                            f'{colors.OK}Condition(s) were met. Skipping {colors.COMMAND}{command}{colors.OK}!{colors.ENDC}')
                        return conditionWasMet
                print(
                    f'{colors.ECHO}Condition(s) were not met. Continuing with {colors.COMMAND}{command}{colors.ENDC}')
                return conditionWasMet
            except subprocess.CalledProcessError as e:
                print(e)


# Functio for running commands in shell
def runCommand(command: str):
    try:
        if command[0:4] != "echo":
            print(
                f'\n{colors.INPUT}Running command {colors.COMMAND}{command}{colors.ENDC}')
        commandrun = subprocess.run(
            [command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(commandrun.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(e)

# Function for stripping rows from csv


def stripRows():
    try:
        # print(f'\n{colors.WARNING}FILES IN FOLDER:')
        # for x in listdir("./files"):
        #     print(f'{colors.INPUT}{x}')
        file = askopenfilename(initialdir='./files')
        filename = path.basename(file.replace(".csv", ""))
#         file = input(f'''
# {colors.WARNING}File has to be in /files folder{colors.ENDC}
# Input just the name of the file to remove rows from (Ex: thisfile):
# ''')
        while True:
            try:
                start = int(
                    input(f'\n{colors.INPUT}Keep rows starting from{colors.ENDC}: '))-1
                end = int(
                    input(f'{colors.INPUT}Keep rows ending to{colors.ENDC}: '))-1
                break
            except ValueError:
                print(f"{colors.ECHO}Bruh{colors.ENDC}")

        with open(file) as inp, open(f'{getcwd()}/files/{filename}_clean.csv', 'w') as out:
            tbw = csv.writer(out)
            for i, row in enumerate(csv.reader(inp)):
                if i >= start and i <= end or i == 0:
                    print(row)
                    tbw.writerow(row)
            print(
                f'{colors.OK}All done - changed file saved as {filename}_clean.csv{colors.ENDC}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    menu()
