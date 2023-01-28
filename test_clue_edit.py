import tkinter as tk
import tkinter.messagebox as messagebox

# Constants for validation
MIN_VALUE = 1
MAX_VALUE = 100


def on_label_click(event, label, var):
    popup = tk.Toplevel()
    entry = tk.Entry(popup, textvariable=var, font=("Arial", 24), bg="white", bd=0)
    entry.pack()
    entry.focus_set()
    entry.select_range(0, tk.END)

    def on_popup_validate():
        try:
            value = int(var.get())
            if MIN_VALUE <= value <= MAX_VALUE:
                label.config(text=var.get())
                popup.destroy()
            else:
                tk.messagebox.showerror("Error", f"Please enter a number between {MIN_VALUE} and {MAX_VALUE}")
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid integer")

    enter_button = tk.Button(popup, text="Enter", command=on_popup_validate)
    enter_button.pack()
    popup.bind("<Return>", lambda event: on_popup_validate())
    popup.grab_set()


root = tk.Tk()

# Create a 10x10 grid of labels
grid = [[tk.StringVar() for _ in range(10)] for _ in range(10)]
for i in range(10):
    for j in range(10):
        grid[i][j].set(f"{i,j}")
        label = tk.Label(root, textvariable=grid[i][j], font=("Arial", 24))
        label.bind("<Button-1>", lambda event, l=label, v=grid[i][j]: on_label_click(event, l, v))
        label.grid(row=i, column=j)

root.mainloop()
