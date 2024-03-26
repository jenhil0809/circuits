class Wire:
    def __init__(self, start, end, bars):
        self.start = start
        self.end = end
        bars[int(start[0])].add_wire(self)
        bars[int(end[0])].add_wire(self)

class Bulb(Wire):
    def __init__(self, start, end, bars):
        super().__init__(start, end, bars)
        self.bars = bars
        self.on = False
        self.check_status()

    def check_status(self):
        if None not in self.bars[int(self.start[0])].power and None not in self.bars[int(self.start[0])].power:
            self.on = True
        else:
            self.on = False
        return self.on


class Bar:
    def __init__(self, number):
        self.number = number
        self.wires = []
        self.power = [None, None]
        self.bars = []

    def add_wire(self, wire):
        self.wires.append(wire)
        self.change_power()

    def change_power(self):
        if self.check_power("+", []) not in self.power:
            self.power[0] = self.check_power("+", [])
        if self.check_power("-", []) not in self.power:
            self.power[1] = self.check_power("-", [])

    def check_power(self, symbol, checked):
        checked.append(self.number)
        for wire in self.wires:
            if wire.start[-1] == symbol and int(wire.end[:-1]) == self.number:
                return wire
            if wire.end[-1] == symbol and int(wire.start[:-1]) == self.number:
                return wire
            if int(wire.start[:-1]) not in checked and wire.end[-1] not in "+-" and self.bars[
                int(wire.start[:-1])].check_power(symbol, checked):
                return wire
            if int(wire.end[:-1]) not in checked and wire.end[-1] not in "+-" and self.bars[
                int(wire.end[:-1])].check_power(symbol, checked):
                return wire
        return None


class Sim:
    def __init__(self, num_bars):
        self.bars = [Bar(i) for i in range(num_bars)]
        self.components = []
        for bar in self.bars:
            bar.bars = self.bars

    def add_wire(self, start, end):
        self.components.append(Wire(start, end, self.bars))

    def add_bulb(self, start, end):
        self.components.append(Bulb(start, end, self.bars))

    def powered_bars(self):
        for bar in self.bars:
            bar.change_power()
        return [bar.number for bar in self.bars if None not in bar.power]


if __name__ == "__main__":
    sim = Sim(30)
    sim.add_wire("3A", "2B")
    sim.add_bulb("3B", "1+")
    sim.add_wire("2C", "5-")
    #sim.add_wire("2D", "7A")
    #sim.add_wire("8D", "7B")
    #sim.add_wire("6C", "5+")
    #sim.add_wire("6C", "5-")
    print(sim.powered_bars())
