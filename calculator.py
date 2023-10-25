import tkinter as tk

def button_click(number):
    current = display_var.get()
    display_var.set(current + str(number))

def clear():
    display_var.set("")

def evaluate():
    try:
        expression = display_var.get()
        result = str(eval(expression))
        display_var.set(result)
    except:
        display_var.set("Error")

# Create the main window
window = tk.Tk()
window.title("Calculator")

# Create and configure the display
display_var = tk.StringVar()
display = tk.Entry(window, textvariable=display_var, font=('Arial', 24))
display.grid(row=0, column=0, columnspan=4)
display_var.set("")

# Create buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

row_val, col_val = 1, 0

for button in buttons:
    tk.Button(window, text=button, padx=20, pady=20, font=('Arial', 18),
              command=lambda b=button: button_click(b) if b.isnumeric() or b in ('+', '-', '*', '/') else clear() if b == 'C' else evaluate()).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Start the GUI event loop
window.mainloop()