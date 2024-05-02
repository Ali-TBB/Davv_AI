#!/usr/bin/python3
'''module Run_pross'''
import uuid
from BaseModel import BaseModel
from FixError import FixError
import subprocess

class Run_pross(BaseModel):
    def __init__(self, value, *args, **kwargs):
        super().__init__("dataset/Run_pross.json", value, *args, **kwargs)
        self.number = kwargs.get("number", 1)
        self.is_problem = kwargs.get("is_problem", False)
        self.issue_name = kwargs.get("issue_name", None)
        self.operation_detail = kwargs.get("operation_detail", None)
        self.id = str(uuid.uuid4())
        self.operation_name = "this is first setup"

    def Error(self, issue):
        issue = f"#error {issue}"
        Fixer = FixError(issue)
        #re run the command
        self.Run()

    def Run(self):
        try:
            # Read the command from the specified file
            with open("command.py", "r") as file:
                command_content = file.read().strip()
            # Execute the command using subprocess
            subprocess.run(["python", "command.py"])
        except Exception as e:
            print(f"An error occurred while running the command: {e}")
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


while True:
    prompt = input(">>")
    if prompt == "exit":
        break
    elif prompt == "clear":
        print("\033c")
    elif prompt == "":
        print()
    else:
        op = Run_pross(prompt, "command.py")
        op.Start()
        op.Run()