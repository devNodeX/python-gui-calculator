import tkinter as tk 

root = tk.Tk()
root.title("PYTHON GUI CALCULATOR")
root.geometry("400x600")

display = tk.Label( root , 
                    text = "0" ,
                    font = ("Arial" , 28),
                    bg = "#222222" ,
                    fg = "white" ,
                    anchor = "e" , 
                    padx = 15,
                    pady = 20 
                   )
display.pack(fill = "x" , padx = 15  , pady = 15)



# Create a frame to hold calculator buttons
button_frame = tk.Frame(root)
button_frame.pack()

buttons = ["AC", "%", "C" ,"/" ,"7", "8", "9", "x","4", "5", "6", "-", "1", "2", "3", "+", "00" , "0" ,"." ,"=" ]

for i, text in enumerate(buttons):
    button = tk.Button(
        button_frame,
        text=text,
        font=("Arial", 20),
        width=5,
        height=2
    )

    button.grid(row=i // 4, column=i % 4, padx=5, pady=5)

root.mainloop()