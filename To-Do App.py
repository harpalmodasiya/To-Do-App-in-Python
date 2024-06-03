#-------------------------------------------------------------------------------
# Name:        To-Do App
# Purpose:     My first Task as a Python Programming Intern at CodSoft.
#
# Author:      Harpal Modasiya
#
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# Function to add a task to the list and database
def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

# Function to update the task listbox
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

# Function to complete (delete) a selected task from the list and database
def complete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Complete.')

# Function to complete (delete) all tasks from the list and database
def complete_all_tasks():
    message_box = messagebox.askyesno('Completed All', 'Are you sure?')
    if message_box == True:
        while len(tasks) != 0:
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

# Function to clear the task listbox
def clear_list():
    task_listbox.delete(0, 'end')

# Function to close the application
def close():
    print(tasks)
    guiWindow.destroy()

# Function to retrieve tasks from the database
def retrieve_database():
    while len(tasks) != 0:
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    # Creating the main GUI window
    guiWindow = Tk()
    guiWindow.title("To-Do App")
    guiWindow.geometry("900x400+200+100")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="black")

    # Connecting to SQLite database
    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    # Creating a frame for function buttons
    functions_frame = Frame(guiWindow, bg="black")
    functions_frame.pack(side="left", fill="y")

    # Label for task entry
    task_label = Label(functions_frame, text="Enter the Task:", font=("Arial", 20, "bold"), bg="black", fg="#7865F8")
    task_label.pack(pady=20)

    # Entry field for task input
    task_field = Entry(functions_frame, font=("Arial", 14, "bold"), width=22, bg="white", fg="black")
    task_field.pack(pady=12)

    # Button to add a task
    add_button = Button(functions_frame, text="Add Task", width=20, font=("Arial", 14, "bold"), bg="#7865F8", command=add_task)
    add_button.pack(pady=12)

    # Button to complete a selected task
    complete_button = Button(functions_frame, text="Complete Task", width=20, font=("Arial", 14, "bold"), bg="#7865F8", command=complete_task)
    complete_button.pack(pady=12)

    # Button to complete all tasks
    complete_all_button = Button(functions_frame, text="Complete All Tasks", width=20, font=("Arial", 14, "bold"), bg="#7865F8", command=complete_all_tasks)
    complete_all_button.pack(pady=12)

    # Button to exit the application
    exit_button = Button(functions_frame, text="Exit", width=20, font=("Arial", 14, "bold"), bg="#7865F8", command=close)
    exit_button.pack(pady=12, padx=30)

    # Listbox to display tasks
    task_listbox = Listbox(guiWindow, width=50, height=18, font="bold", selectmode='SINGLE', bg="white", fg="black", selectbackground="#7865F8", selectforeground="black")
    task_listbox.pack(side="right", fill="y", padx=20, pady=20)

    # Retrieve and display tasks from the database on startup
    retrieve_database()
    list_update()

    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
