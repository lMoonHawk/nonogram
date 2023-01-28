import tkinter as tk
import tkinter.messagebox as messagebox

# Constants for validation
MIN_VALUE = 1
MAX_VALUE = 100


def on_label_click(event, label, var, labels):
    popup = tk.Toplevel()
    entry = tk.Entry(popup, textvariable=var, font=("Arial", 24), bg="white", bd=0)
    entry.pack()
    x = label.winfo_rootx()
    y = label.winfo_rooty()
    popup.geometry(f"+{x}+{y}")
    label_index = labels.index(label)

    def on_popup_validate():
        try:
            value = int(var.get())
            if MIN_VALUE <= value <= MAX_VALUE:
                label.config(text=var.get())
                popup.grab_release()
                popup.destroy()
                next_label = labels[(label_index + 1) % len(labels)]
                next_label.event_generate("<Button-1>")
            else:
                tk.messagebox.showerror("Error", f"Please enter a number between {MIN_VALUE} and {MAX_VALUE}")
                entry.focus_set()
                entry.select_range(0, tk.END)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid integer")
            entry.focus_set()
            entry.select_range(0, tk.END)

    enter_button = tk.Button(popup, text="Enter", command=on_popup_validate)
    enter_button.pack()
    popup.bind("<Return>", lambda _: on_popup_validate())
    popup.bind("<Tab>", lambda _: on_popup_validate())
    popup.focus_set()
    # popup.grab_set()
    entry.focus_set()
    entry.select_range(0, tk.END)  # Select all characters in the entry


root = tk.Tk()

# Create a 10x10 grid of labels
grid = [[tk.StringVar() for _ in range(10)] for _ in range(10)]
labels = []
for i in range(10):
    for j in range(10):
        grid[i][j].set(f"{i,j}")
        label = tk.Label(root, textvariable=grid[i][j], font=("Arial", 24))
        label.bind("<Button-1>", lambda event, l=label, v=grid[i][j]: on_label_click(event, l, v, labels))
        label.grid(row=i, column=j)
        labels.append(label)
root.mainloop()
