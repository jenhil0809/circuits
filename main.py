class Wire:
    def __init__(self, start, end, bars):
        self.start = start
        self.end = end
        bars[int(start[0])].add_wire(self)
        bars[int(end[0])].add_wire(self)


class Bar:
    def __init__(self, number):
        self.number = number
        self.wires = []
        self.power = [None, None]

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
            if int(wire.start[:-1]) not in checked and wire.end[-1] not in "+-" and bars[int(wire.start[:-1])].check_power(symbol, checked):
                return wire
            if int(wire.end[:-1]) not in checked and wire.end[-1] not in "+-" and bars[int(wire.end[:-1])].check_power(symbol, checked):
                return wire
        return None

bars = []
for i in range(30):
    bars.append(Bar(i))

Wire("3A", "2B", bars)
Wire("3B", "1+", bars)
Wire("2C", "5-", bars)
Wire("2D", "7A", bars)
Wire("8D", "7A", bars)
Wire("8D", "7B", bars)
Wire("6C", "5-", bars)
Wire("6C", "5+", bars)
for bar in bars:
    bar.change_power()
for bar in bars:
    if None not in bar.power:
        print(bar.number)
