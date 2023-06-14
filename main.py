import subprocess
import csv
from tkinter.filedialog import askopenfilename
from os import getcwd, listdir, path

class colors:
    COMMAND = '\033[94m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    INPUT = '\033[96m'
    ECHO = '\033[31m'
    OK = '\033[92m'


def menu():
    while True:
        try:
            option = int(input('''
What u wants to dos:
    1. Run commands
    2. Remove rows from CSV
    3. Quit
'''))
            match option:
                case 1:
                    main()
                case 2:
                    stripLines()
                case 3:
                    quit()
        except ValueError:
            print(f"{colors.ECHO}Bruh{colors.ENDC}")


def main():
    filename = input(
        f'\n{colors.INPUT}Input name of command file{colors.ENDC}: ')
    commands = []
    try:
        with open(f"./commands/{filename}.txt") as file:
            for line in file:
                commands.append(line.strip('\n'))
        for command in commands:
            checked_command = checkInserts(command)
            runCommand(checked_command)
    except Exception as e:
        print(e)


def checkInserts(command: str):
    inserts = {
        "INSERTVAR": lambda a, b: a.replace(b, input(f'\n{colors.WARNING}COMMAND {colors.COMMAND}{a} {colors.WARNING}REQUIRES USER INPUT IN PLACE OF {colors.INPUT}{b}{colors.ENDC}: ')),
        "FILENAME": lambda a, b: a.replace(b, askopenfilename(initialdir="./files")),
        "echo": lambda a, b: (a.replace(b,f'{b} {colors.ECHO}')+colors.ENDC) if (a[0:4] == "echo") else a,
        #"FILENAME": lambda a, b: a.replace(b, print(f'\n{colors.WARNING}COMMAND {colors.COMMAND}{a} {colors.WARNING}REQUIRES FILE FOR {colors.INPUT}{b}{colors.WARNING} - SELECT FILE FROM DIRECTORY{colors.ENDC}{askopenfilename(initialdir="./files")}')),
    }
    for insert in inserts.keys():
        if insert in command:
            return inserts[insert](command, insert)
    return command


def runCommand(command: str):
    try:
        if command[0:4] != "echo":
            print(f'\n{colors.INPUT}Running command {colors.COMMAND}{command}{colors.ENDC}')
        subprocess.run([command], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e)


def stripLines():
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
                start = int(input(f'\n{colors.INPUT}Keep rows starting from{colors.ENDC}: '))-1
                end = int(input(f'{colors.INPUT}Keep rows ending to{colors.ENDC}: '))-1
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
