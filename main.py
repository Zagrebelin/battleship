import random
from collections import Counter

import itertools
from PIL import Image, ImageDraw


class Game:
    def __init__(self, ships_config=None, xs=None, ys=None):
        if ships_config is None:
            ships_config = [(4, 1), (3, 2), (2, 3), (1, 4)]
        if xs is None:
            self.xs = list('абвгдежзик')
        if ys is None:
            self.ys = list(range(1, 11))
        self.all_ships = []
        for size, count in ships_config:
            for y, _ in enumerate(self.ys):
                for x in range(len(self.xs) - size + 1):
                    this_ship = []
                    for offset in range(size):
                        if x + offset <= len(self.xs):
                            this_ship.append((x + offset, y))

                    self.all_ships.append(this_ship)
            if size > 1:
                for x, _ in enumerate(self.xs):
                    for y in range(len(self.ys) - size + 1):
                        this_ship = []
                        for offset in range(size):
                            this_ship.append((x, y + offset))
                        self.all_ships.append(this_ship)
        self.alive_ships = self.all_ships.copy()
        self.misses = []  # тут отмечаем все промахи по чужому полю
        self.wounds = []  # тут отмечаем все раненые ячейки

    def show_field(self):
        colors = {
            1: (255, 0, 0, 30),
            2: (0, 255, 0, 50),
            3: (0, 255, 255, 30),
            4: (0, 0, 255, 30),
        }
        size = 50
        i = Image.new('RGB', (20 + size * len(self.xs), 20 + size * len(self.ys)))
        d = ImageDraw.Draw(i, 'RGBA')
        d.rectangle([(0, 0), i.size], fill='gray')
        for x, _ in enumerate(self.xs):
            for y, _ in enumerate(self.ys):
                xy0 = (10 + x * size, 10 + y * size)
                xy1 = (10 + x * size + size, 10 + y * size + size)
                d.rectangle([xy0, xy1], fill='#ffffff10', outline='black')
        for ship in self.all_ships:
            if len(ship) != 2:
                continue
            start = ship[0]
            end = ship[-1]
            x0 = 10 + start[0] * size + 5
            y0 = 10 + start[1] * size + 5
            x1 = 10 + end[0] * size + size - 10
            y1 = 10 + end[1] * size + size - 10
            d.rectangle([(x0, y0), (x1, y1)], fill=colors[len(ship)], outline='gray')

        i.show()

    def choise_shot(self):
        ships_to_shot = []

        for ship in self.alive_ships:
            if self.wounds:
                if all(cell in ship for cell in self.wounds):
                    ships_to_shot.append(ship)
            else:
                ships_to_shot.append(ship)
        all_cells = Counter()
        for ship in ships_to_shot:
            all_cells.update(cell for cell in ship if cell not in self.wounds)
        max_cell = all_cells.most_common()[0][1]
        cells_to_shot = [cell for cell, count in all_cells.items() if count==max_cell]
        return random.choice(cells_to_shot)

    def miss(self, xy):
        ships_to_remove = []
        for ship in self.alive_ships:
            if xy in ship:
                ships_to_remove.append(ship)
        for ship in ships_to_remove:
            self.alive_ships.remove(ship)

g = Game()
print(g.choise_shot())