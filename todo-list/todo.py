from tkinter import *
import sqlite3

root = Tk()
root.title('Todo List')
root.geometry('450x500')

conn = sqlite3.connect('todo.db')

c = conn.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    """
)

conn.commit()

def compl(id):
    def _complete():
        todo=c.execute("SELECT * FROM todo WHERE id= ?", (id,)).fetchone()
        c.execute("UPDATE todo SET completed= ? WHERE id= ?", (not todo[3],id))
        conn.commit()
        render_todos()
    return _complete

def delete(id):
    def _del():
        c.execute("DELETE FROM todo WHERE id= ?", (id,))
        conn.commit()
        render_todos()
        
    return _del

def render_todos():
    todos = c.execute("SELECT * FROM todo").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for i in range(len(todos)):
        id = todos[i][0]
        completed = todos[i][3]
        description = todos[i][2]
        l = Checkbutton(frame,text=description,width=42,anchor='w',command=compl(id))
        l.grid(row=i,column=0,sticky='w')
        btn = Button(frame,text='Eliminar',command=delete(id))
        btn.grid(row=i,column=1)
        l.select() if completed else l.deselect()
        
        
def addTodo():
    todo = e.get()
    if todo:
        c.execute("INSERT INTO todo (description,completed) VALUES (?,?)", (todo,False))
        conn.commit()
        e.delete(0,END)
        render_todos()
    
l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command= addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas',padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe',padx=5)

e.focus()
render_todos()

root.bind('<Return>', lambda event: addTodo())


root.mainloop()


