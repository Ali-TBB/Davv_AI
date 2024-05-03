#!/usr/bin/python3
'''module Run_process'''
import uuid
from BaseModel import BaseModel
from FixError import FixError
import subprocess

class Run_process(BaseModel):
    def __init__(self, value, *args, **kwargs):
        super().__init__("dataset/data.json", value, *args, **kwargs)
        self.number = kwargs.get("number", 1)
        self.is_problem = kwargs.get("is_problem", False)
        self.issue_name = kwargs.get("issue_name", None)
        self.operation_detail = kwargs.get("operation_detail", None)
        self.id = str(uuid.uuid4())
        self.operation_name = "this is first setup"

    def Error(self, issue):
        issue = f"#error {issue}"
        Fixer = FixError(issue)
        Fixer.Start()
        Fixer.Run()
        #re run the command
        self.Run()

    def Run(self):
        print("Operation is runing ...")
        try:
            # Execute the command using subprocess
            result = subprocess.run(["python", "command.py"], capture_output=True)
            # Check the return code of the subprocess
            if result.returncode != 0:
                print(f"Command execution failed with return code {result.returncode}")
                # If there is an error, pass it to the Error method
                self.Error(result.stderr.decode("utf-8"))
            else:
                # Print the output of the executed script
                RED = '\033[91m'
                RESET = '\033[0m'
                print("Output:\n", RED + result.stdout.decode("utf-8") + RESET)
        except Exception as e:
            print(f"on run An error occurred while running the command: {e}")
            # Pass the error to the Error method
            self.Error(str(e))


    def TestCode(self):
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.number}"

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict


"""
while True:
    prompt = input(">>")
    if prompt == "exit":
        break
    elif prompt == "clear":
        print("\033c")
    elif prompt == "":
        print()
    else:
        op = Run_process(prompt, "command.py")
        op.Start()
        op.Run()
"""