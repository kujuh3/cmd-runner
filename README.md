## Runner

Meant to be run on linux - probably hangs on windows due to tkinter.
Designed for WSL

### Installation
Install tkinter via apt
```bash
sudo apt-get install python3-tk
```

### Usage
#### Running the program
```bash
python main.py
```

#### Commands to be run go into /commands folder as .txt files.
 - INSERTVAR is a string to be inserted in a command where you would want user input - this input will be asked from the user when the command runs
 - FILENAME is a string to be inserted in a command where you would want to choose a file - this will be asked via a window prompt
 - Echo's are configured to be usen as instructive prompts when running commands.

A commands .txt file should include commands to be run line by line </br>
##### Example run of example.txt commands file
![image](https://github.com/kujuh3/cmd-runner/assets/66220187/850c3873-3e34-4f85-84a1-9192dee9b4d2)

##### Example run of insert_example.txt commands file
![image](https://github.com/kujuh3/cmd-runner/assets/66220187/3d739ce7-3ba7-4c4d-936a-8f179bd921be)
