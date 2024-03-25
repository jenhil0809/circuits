import tkinter as tk
import main


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.row1 = tk.IntVar()
        self.col1 = tk.IntVar()
        self.row2 = tk.IntVar()
        self.col2 = tk.IntVar()
        self.background_image=tk.PhotoImage(file="breadboard.png")
        self.game = Game(self)
        self.game.pack()
        self.inputs = Inputs(self)
        self.inputs.pack()

class Game(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master: GameApp = master
        self.sim = main.Sim(30)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=master.background_image)
    def draw_line(self, x1, x2, y1, y2):
        if y1 < 0 and y2 < 0:
            print("Error:only one end may be +/-")
            y1, y2 = "-", "+"
        elif y1 == -1:
            line = self.canvas.create_line(x1*10+20, y1*10+30, x2*10+20, y2*10+60, fill="red", width=2)
            y1 = "-"
        elif y2 == -1:
            line = self.canvas.create_line(x1*10+20, y1*10+60, x2*10+20, y2*10+30, fill="red", width=2)
            y2 = "-"
        elif y1 == -2:
            line = self.canvas.create_line(x1*10+20, y1*10+50, x2*10+20, y2*10+60, fill="red", width=2)
            y1 = "+"
        elif y2 == -2:
            line = self.canvas.create_line(x1*10+20, y1*10+60, x2*10+20, y2*10+50, fill="red", width=2)
            y2 = "+"
        else:
            line = self.canvas.create_line(x1*10+20, y1*10+60, x2*10+20, y2*10+60, fill="red", width=2)
        if (y1, y2) != ("-", "+"):
            if type(y1) == int:
                y1 =chr(74-y1)
            if type(y2) == int:
                y2 =chr(74-y2)
            self.sim.add_wire(str(x1)+y1, str(x2)+y2)
            print(self.sim.powered_bars())


class Inputs(tk.Frame):
    def __init__(self, master: GameApp):
        super().__init__()
        self.master: GameApp = master
        SCALE_LABELS = {
            -2: "+",
            -1: "-",
            0: "j",
            1: "i",
            2: "h",
            3: "g",
            4: "f"
        }
        def scale_labels(value, slider):
            slider.config(label=SCALE_LABELS[int(value)])

        self.row1_input = tk.Scale(self, from_=-2, to=4, orient="horizontal", variable=master.row1, showvalue=False, command=lambda slider:scale_labels(master.row1.get(), self.row1_input))
        self.row2_input = tk.Scale(self, from_=-2, to=4, orient="horizontal", variable=master.row2, showvalue=False, command=lambda slider:scale_labels(master.row2.get(), self.row2_input))
        self.col1_input = tk.Scale(self, from_=1, to=30, orient="horizontal", variable=master.col1)
        self.col2_input = tk.Scale(self, from_=1, to=30, orient="horizontal", variable=master.col2)
        self.submit_button = tk.Button(self, text="Add wire", command=lambda: self.master.game.draw_line(
            master.col1.get(),master.col2.get(), master.row1.get(), master.row2.get()))
        self.place_widgets()

    def place_widgets(self):
        tk.Label(self, text="Coords 1:").grid(row=0, column=0)
        tk.Label(self, text="Coords 2:").grid(row=2, column=0)
        self.row1_input.grid(row=1, column=1)
        self.row2_input.grid(row=3, column=1)
        self.col1_input.grid(row=1, column=0)
        self.col2_input.grid(row=3, column=0)
        self.submit_button.grid(row=4, column=11)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()