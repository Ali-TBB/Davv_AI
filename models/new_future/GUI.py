import tkinter as tk
import sys
import io

def run_command():
    input_text = input_text_area.get("1.0", "end-1c")  # Get text from the input Text widget
    
    # Redirect stdout to a StringIO object
    output_redirect = io.StringIO()
    sys.stdout = output_redirect
    
    # Here you can execute whatever command you want with the input_text
    print("Executing command with input:", input_text)
    
    # Get the output from the StringIO object
    output_text = output_redirect.getvalue()
    
    # Restore sys.stdout
    sys.stdout = sys.__stdout__
    
    # Display the output
    output_text_area.config(state='normal')
    output_text_area.insert("end", output_text + "\n")
    output_text_area.config(state='disabled')

# Create the main Tkinter window
root = tk.Tk()
root.title("Input Prompt")

# Create a label
label = tk.Label(root, text="Enter your input:")
label.pack()

# Create a Text widget for input
input_text_area = tk.Text(root, height=10, width=50)  # Set height and width as needed
input_text_area.pack()

# Create a "Run" button
run_button = tk.Button(root, text="Run", command=run_command)
run_button.pack()

# Create a label for output
output_label = tk.Label(root, text="Output:")
output_label.pack()

# Create a Text widget for output
output_text_area = tk.Text(root, height=10, width=50)  # Set height and width as needed
output_text_area.pack()

# Run the Tkinter event loop
root.mainloop()
