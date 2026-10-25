
import tkinter as tk
import ast
import operator

# ---------- Window ----------
root = tk.Tk()
root.title("PYTHON GUI CALCULATOR")
root.geometry("420x560")
root.resizable(False, False)
root.configure(bg="#222222")

# ---------- Calculator state ----------
expression = tk.StringVar(value="0")
just_calculated = False

# ---------- Safe arithmetic evaluator ----------
def evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp):
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
        }

        operation = operations.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported operation")

        return operation(evaluate(node.left), evaluate(node.right))

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -evaluate(node.operand)
        if isinstance(node.op, ast.UAdd):
            return evaluate(node.operand)

    raise ValueError("Invalid expression")


def calculate():
    global just_calculated

    try:
        text = expression.get()
        tree = ast.parse(text, mode="eval")
        result = evaluate(tree.body)

        if isinstance(result, float) and not result.is_integer():
            result = round(result, 10)
        elif isinstance(result, float):
            result = int(result)

        expression.set(str(result))
        just_calculated = True

    except ZeroDivisionError:
        expression.set("Cannot divide by zero")
        just_calculated = True
    except (ValueError, SyntaxError, OverflowError):
        expression.set("Error")
        just_calculated = True


# ---------- Button logic ----------
def press(value):
    global just_calculated

    current = expression.get()

    if value == "AC":
        expression.set("0")
        just_calculated = False
        return

    if value == "C":
        if current in ("Error", "Cannot divide by zero"):
            expression.set("0")
        else:
            expression.set(current[:-1] or "0")
        just_calculated = False
        return

    if value == "=":
        calculate()
        return

    if current in ("Error", "Cannot divide by zero"):
        expression.set("0")
        current = "0"

    if just_calculated:
        if value in ("+", "-", "x", "/", "%"):
            just_calculated = False
        else:
            expression.set("0")
            current = "0"
            just_calculated = False

    if value in ("+", "-", "x", "/", "%"):
        if current == "0" and value != "-":
            return

        if current[-1] in "+-x/%":
            expression.set(current[:-1] + value)
        else:
            expression.set(current + value)

    else:
        if value == ".":
            # Prevent multiple decimal points in the current number.
            number = current.replace("x", "+").replace("/", "+")
            number = number.replace("%", "+")
            number = number.split("+")[-1].split("-")[-1]

            if "." in number:
                return

        if value == "00" and current == "0":
            return

        if current == "0" and value != ".":
            expression.set(value)
        else:
            expression.set(current + value)


# Convert the visible multiplication sign to Python's operator.
def calculate():
    global just_calculated

    try:
        text = expression.get().replace("x", "*")
        tree = ast.parse(text, mode="eval")
        result = evaluate(tree.body)

        if isinstance(result, float) and not result.is_integer():
            result = round(result, 10)
        elif isinstance(result, float):
            result = int(result)

        expression.set(str(result))
        just_calculated = True

    except ZeroDivisionError:
        expression.set("Cannot divide by zero")
        just_calculated = True
    except (ValueError, SyntaxError, OverflowError):
        expression.set("Error")
        just_calculated = True


# ---------- Display ----------
display = tk.Label(
    root,
    textvariable=expression,
    font=("Arial", 28),
    bg="#222222",
    fg="white",
    anchor="e",
    padx=15,
    pady=20,
)
display.pack(fill="x", padx=12, pady=(15, 10))

# ---------- Buttons ----------
buttons = [
    ["AC", "%", "C", "/"],
    ["7", "8", "9", "x"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["00", "0", ".", "="],
]

button_frame = tk.Frame(root, bg="#222222")
button_frame.pack(fill="both", expand=True, padx=5, pady=5)

for row_index, row in enumerate(buttons):
    button_frame.grid_rowconfigure(row_index, weight=1)

    for col_index, value in enumerate(row):
        button_frame.grid_columnconfigure(col_index, weight=1)

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 20),
            bg="#eeeeee",
            fg="black",
            activebackground="#cccccc",
            relief="raised",
            bd=1,
            command=lambda v=value: press(v),
        )
        button.grid(
            row=row_index,
            column=col_index,
            sticky="nsew",
            padx=4,
            pady=4,
        )

root.mainloop()
