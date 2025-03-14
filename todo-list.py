# THE BEST TO-DO LIST CODE IN THE WORLD - By Afshad Sidhwa and Azfar Ali (o.o)
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

def main():
    tasks = []
    taskcheck = []
    loaded_filename = None  # stores the currently loaded file name

# function addtask() makes use of the get methods to retrieve the user's input values for tasks and
# their priority. It records the input timestamp in a variable and appends all the data as a dictionary
# into the global tasks list. It then calls the sorttasks() and displaytasks() functions and clears
# the taskbar allowing for the user to enter another, with an error shown if no task is entered
    def addtask():
        task = taskentry.get()
        priority = priorityval.get()
        if task:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tasks.append({"task": task, "priority": priority, "timestamp": timestamp, "completed": False})
            sorttasks()
            displaytasks()
            taskentry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error!", "Task cannot be empty, please enter a valid task.")

# function sorttasks() receives the global list 'tasks' and sorts tasks based on the criteria of
# completion status and priority, using the sorted() function. The lambda function returns a tuple of
# values (x["completed"], x["priority"]) sorting them in that order, before assigning them back to the
# 'tasks' variable.   
    def sorttasks():
        nonlocal tasks
        tasks = sorted(tasks, key=lambda x: (x["completed"], x["priority"]))

# function displaytasks() updates the UI, displaying tasks in the 'taskframe'. It clears any existing
# widgets in the frame, then iterates through the 'tasks' list. It creates the labels and checkboxes for
# each task, depending on their Boolean Value. Then, the function displays their task name, priority and its timestamp.
# Checkboxes are set based on completion status of each task, and the checkbox variables are appended to the 'taskcheck' list
# for later reference.
    def displaytasks():
        for widget in taskframe.winfo_children():
            widget.destroy()

        nonlocal taskcheck
        taskcheck = [] #list for boolean check flags
        for index, task in enumerate(tasks):
            checkboxvar = tk.BooleanVar(value=task["completed"]) # checkbox boolean (T/F)
            checkbox = tk.Checkbutton(taskframe, variable=checkboxvar, bg="#6F2DA8", command=lambda i=index: updatecompletionstatus(i))
            checkbox.grid(row=index, column=0, padx=10, pady=5, sticky=tk.W)
            taskcheck.append(checkboxvar)
            displaylabel = tk.Label(taskframe, text=f"{task['task']} (Priority: {task['priority']},Timestamp: {task['timestamp']})", bg="#6F2DA8", fg="white")
            displaylabel.grid(row=index, column=1, columnspan=3, padx=10, pady=5, sticky=tk.W)

# function updatecompletionstatus(index) toggles the completion status of a task at the given index in
# the 'tasks' list, then calls the 'sorttasks' and 'displaytasks' functions to update the UI.    
    def updatecompletionstatus(index):
        tasks[index]["completed"] = not tasks[index]["completed"]
        sorttasks()
        displaytasks()

# function newlist() creates a new list. It takes 'tasks' as a nonlocal variable and creates a new
# empty list 'tasks' and then calls the 'displaytasks' function
    def newlist():
        nonlocal tasks
        tasks = []
        displaytasks()

# function deletechecked() deletes checked tasks. It takes 'tasks' as a non-local variable
# and makes a newtasks list. Then, it iterates over the index and task dictionary in 'tasks' 
# list and uses the get method to see if its not checked (FALSE). It then sets the original 
# 'tasks' list to newtasks and sorts and displays the items
    def deletechecked():
        nonlocal tasks
        newtasks = []
        for i, task in enumerate(tasks):
            if not taskcheck[i].get():
                newtasks.append(task)
        tasks = newtasks
        sorttasks()
        displaytasks()

# function saveasfile() prompts the user to choose the file path and name of where they want to
# store the list. The limitation is that the file type should be .txt. The funcitonmakes use of
# exception handling to deal with different scenarios. It opens filename for writing, and reads 
# the 'tasks' list and variable 'completionmarker' is made to store 'x' if the task is completed.
# The information is then written to the file on separate lines and a message box indicates changes 
# have been saved.
    def saveasfile():
        nonlocal loaded_filename
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'w') as file:
                    for task in tasks:
                        completionmarker = "x" if task["completed"] else " "
                        file.write(f"{completionmarker} {task['task']} (Priority: {task['priority']}, Timestamp: {task['timestamp']})\n")
                loaded_filename = filename
                messagebox.showinfo("Info", f"Saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error!", f"An error occurred: {str(e)}")
                
# function savetofile() saves current tasks to the specified file (currentfile). The function
# checks for the existence, the current file name, and provides appropriate messages for different scenarios
# should they arise.
    def savetofile():
        nonlocal loaded_filename
        if loaded_filename:
            if tasks:  # Check if there are tasks to save
                try:
                    with open(loaded_filename, 'w') as file:
                        for task in tasks:
                            completion_marker = "x" if task["completed"] else " "
                            file.write(f"{completion_marker} {task['task']} (Priority: {task['priority']}, Timestamp: {task['timestamp']})\n")
                    messagebox.showinfo("Info", f"Changes saved to {loaded_filename}")
                except Exception as e:
                    messagebox.showerror("Error!", f"An error occurred: {str(e)}")
            else:
                messagebox.showwarning("Warning!", "To-Do List is empty. Nothing to save.")
        else:
            messagebox.showwarning("Warning!", "Please use 'Save As' to create a new file or 'Load' to load an existing one.")

# function loadfromfile() loads tasks from specified files, updating the 'tasks' variable,
# and displaying the loaded tasks. Error handling is included here, incase of unexpected errors
# during the loading process.
    def loadfromfile(filename):
        try:
            with open(filename, 'r') as file:
                filelines = file.readlines()
                nonlocal tasks, loaded_filename
                tasks = []
                for line in filelines:
                    completion_marker, info = line.split(" ", 1)
                    taskname = info.split("(Priority:")[0].strip()
                    priority_timestamp = info.split("(Priority:")[1].split(", Timestamp: ")
                    priority = int(priority_timestamp[0])
                    timestamp = priority_timestamp[1].strip(")\n")
                    tasks.append({"task": taskname, "priority": priority, "timestamp": timestamp, "completed": completion_marker.strip() == "x"})
                sorttasks()
                displaytasks()
                loaded_filename = filename
            messagebox.showinfo("Info", f"List loaded from {filename}")
        except FileNotFoundError:
            messagebox.showerror("Sorry!", "File not found.")
        except Exception as e:
            messagebox.showerror("Error!", f"An error occurred: {str(e)}")

# function loadbutton() prompts the user to choose which file to load, and the nameis stored in 
# 'filename'. It must be a text file, and if valid, the 'loadfromfile' function is called with
# 'filename' as parameter.
    def loadbutton():
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            loadfromfile(filename)

# GUI code
    root = tk.Tk() # root is the orthodox name for the main window in tkinter
    root.title("To-Do List") # title of the project is "To-Do List"
    root.configure(bg="#6F2DA8") # sets the background color to purple in hexadecimal code
    buttoncolor = "white" # button color is set to white
    newlistbutton = tk.Button(root, text="New List", command=newlist, bg=buttoncolor) # creates a button to make a new list referencing function 'newlist'; colour is set to buttoncolor(white)
    newlistbutton.grid(row=0, column=0, padx=10, pady=10) # this line sets the button's parameters in the main window, padx and pady add padding to the button so it doesnt merge with other elements in the environment
    taskentry = tk.Entry(root, width=40) # allows users to enter tasks in the main window, max length is 40 
    taskentry.grid(row=0, column=1, padx=10, pady=10) # creates the button with padding
    priorityval = tk.IntVar() # priority variable created as an integer of the tkinter class
    priorityval.set(1) # default value is set to 1 
    prioritylabel = tk.Label(root, text="Priority:", bg="#6F2DA8", fg="white") # priority label is created in the main window that has the same background color and button is white
    prioritylabel.grid(row=0, column=2, padx=10, pady=10)# the button is created in the window with padding
    prioritymenu = tk.OptionMenu(root, priorityval, 1, 2, 3) # a dropdown menu is created that allows users to choose priority values from 1 to 3
    prioritymenu.grid(row=0, column=3, padx=10, pady=10)# dropdown menu is created in main window with padding
    addbutton = tk.Button(root, text="Add Task", command=addtask, bg=buttoncolor)# add button is formed in the main window its titled Add Task, referencing the addtask function, colour is set to white
    addbutton.grid(row=0, column=4, padx=10, pady=10)#button made with padding
    taskframe = tk.Frame(root, bg="#6F2DA8")# task frame window is created in the main window
    taskframe.grid(row=1, column=0, columnspan=5, padx=10, pady=10)# parameters are set and padding given
    deletebutton = tk.Button(root, text="Clear Checked Tasks", 
    command=deletechecked, bg=buttoncolor) # delete button is made called Clear Checked Tasks, referencing the deletechecked function, colour is set to white
    deletebutton.grid(row=2, column=0, columnspan=5, padx=10, pady=10) # padding and parameters given
    saveasbutton = tk.Button(root, text="Save As", command=saveasfile, 
    bg=buttoncolor) # saveas button is made allowing users to save to a file, as titled (Save As) and references the saveasfile function; colour is white
    saveasbutton.grid(row=3, column=0, padx=10, pady=10)
    savebutton = tk.Button(root, text="Save", command=savetofile, bg=buttoncolor) # save file button is made, referencing the savetofile function; colour is white
    savebutton.grid(row=3, column=1, padx=10, pady=10)
    loadbutton = tk.Button(root, text="Load", command=loadbutton, bg=buttoncolor)# load button is made, referencing the loadbutton function; colour is white
    loadbutton.grid(row=3, column=2, padx=10, pady=10)
    quitbutton = tk.Button(root, text="Quit", command=root.destroy, bg=buttoncolor) # quit button is created and it has the command root.destroy which closes the main window(root) 
    # its colour is also white :o
    quitbutton.grid(row=3, column=3, padx=10, pady=10)# button parameters and padding are provided
    displaytasks()# function call
    root.mainloop()# loop continues
if __name__ == "__main__":
    main()