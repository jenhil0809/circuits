import tkinter as tk
import main


class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.row1 = tk.IntVar()
        self.col1 = tk.IntVar()
        self.row2 = tk.IntVar()
        self.col2 = tk.IntVar()
        self.typ = tk.StringVar()
        self.bulbs = []
        self.sim_obj = []
        self.background_image = tk.PhotoImage(file="breadboard.png")
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

    def add_line(self, x1, x2, y1, y2, type):
        valid = True
        if type == "wire":
            col = "black"
        elif type == "bulb":
            col = "DarkRed"
        else:
            valid = False
            print("Error: select a component type")
        if y1 < 0 and y2 < 0:
            valid = False
            print("Error:only one end may be +/-")
            y1, y2 = "-", "+"
        if valid:
            self.master.bulbs.append([x1, y1, x2, y2, col, type])
            if y1 >= 0:
                y1 = chr(74 - y1)
            if y2 >= 0:
                y2 = chr(74 - y2)
            if y1 == -2:
                y1 = "+"
            elif y1 == -1:
                y1 = "-"
            if y2 == -2:
                y2 = "+"
            elif y2 == -1:
                y2 = "-"
            if type == "wire":
                self.sim.add_wire(str(x1) + str(y1), str(x2) + str(y2))
            elif type == "bulb":
                self.sim.add_bulb(str(x1) + str(y1), str(x2) + str(y2))
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.master.background_image)
        for i in range(len(self.sim.components)):
            if self.master.bulbs[i][-1] == "bulb" and self.sim.components[i].check_status():
                self.master.bulbs[i][4] = "red"
            elif self.master.bulbs[i][-1] == "bulb":
                self.master.bulbs[i][4] = "DarkRed"
            self.draw_line(*self.master.bulbs[i][:-1])

    def draw_line(self, x1, y1, x2, y2, col):
        if y1 == -1:
            self.canvas.create_line(x1 * 10 + 20, y1 * 10 + 30, x2 * 10 + 20, y2 * 10 + 60, fill=col, width=2)
        elif y2 == -1:
            self.canvas.create_line(x1 * 10 + 20, y1 * 10 + 60, x2 * 10 + 20, y2 * 10 + 30, fill=col, width=2)
        elif y1 == -2:
            self.canvas.create_line(x1 * 10 + 20, y1 * 10 + 50, x2 * 10 + 20, y2 * 10 + 60, fill=col, width=2)
        elif y2 == -2:
            self.canvas.create_line(x1 * 10 + 20, y1 * 10 + 60, x2 * 10 + 20, y2 * 10 + 50, fill=col, width=2)
        else:
            self.canvas.create_line(x1 * 10 + 20, y1 * 10 + 60, x2 * 10 + 20, y2 * 10 + 60, fill=col, width=2)


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

        self.row1_input = tk.Scale(self, from_=-2, to=4, orient="horizontal", variable=master.row1, showvalue=False,
                                   command=lambda slider: scale_labels(master.row1.get(), self.row1_input))
        self.row2_input = tk.Scale(self, from_=-2, to=4, orient="horizontal", variable=master.row2, showvalue=False,
                                   command=lambda slider: scale_labels(master.row2.get(), self.row2_input))
        self.col1_input = tk.Scale(self, from_=1, to=30, orient="horizontal", variable=master.col1)
        self.col2_input = tk.Scale(self, from_=1, to=30, orient="horizontal", variable=master.col2)
        self.type_input = tk.OptionMenu(self, master.typ, "wire", "bulb")
        self.submit_button = tk.Button(self, text="Add wire", command=lambda: self.master.game.add_line(
            master.col1.get(), master.col2.get(), master.row1.get(), master.row2.get(), master.typ.get()))
        self.place_widgets()

    def place_widgets(self):
        tk.Label(self, text="Coords 1:").grid(row=0, column=0)
        tk.Label(self, text="Coords 2:").grid(row=2, column=0)
        self.row1_input.grid(row=1, column=1)
        self.row2_input.grid(row=3, column=1)
        self.col1_input.grid(row=1, column=0)
        self.col2_input.grid(row=3, column=0)
        self.submit_button.grid(row=4, column=1)
        self.type_input.grid(row=4, column=0)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
