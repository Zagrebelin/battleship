import random
from collections import Counter

import itertools
from PIL import Image, ImageDraw
import heatmap

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

    def show_field(self, scheme_name):
        colors = {
            1: (255, 0, 0, 30),
            2: (0, 255, 0, 50),
            3: (0, 255, 255, 30),
            4: (0, 0, 255, 30),
        }
        size = 50
        i = Image.new('RGB', (20 + size * len(self.xs), 20 + size * len(self.ys)))
        d = ImageDraw.Draw(i, 'RGB')
        d.rectangle([(0, 0), i.size], fill='gray')
        c = Counter()
        for ship in self.alive_ships:
            c.update(ship)
        lo, high = min(c.values()), max(c.values())
        for x, _ in enumerate(self.xs):
            for y, _ in enumerate(self.ys):
                this_cell_count = c[x,y]
                xy0 = (10 + x * size, 10 + y * size)
                xy1 = (10 + x * size + size, 10 + y * size + size)
                color = heatmap.get_color(scheme_name, lo, high, this_cell_count)
                d.rectangle([xy0, xy1], fill=color, outline='black')
                d.text((xy0[0]+size/2, xy0[1]+size/2), f'{this_cell_count}     ')
        i.show()
        i.close()

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

        random.choices(list(all_cells.keys()), weights=list(all_cells.values()))
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

    def wound(self, xy):
        self.wounds.append(xy)

    def died(self, xy):
        self.wounds.append(xy)
        ships_to_remove = []
        forbiden_cells = []
        for cell in self.wounds:
            forbiden_cells.append(cell)
            for dx, dy in itertools.product([-1,0,1], [-1,0,1]):
                forbiden_cells.append((cell[0]+dx, cell[1]+dy))
        for ship in self.alive_ships:
            if any(cell in forbiden_cells for cell in ship):
                ships_to_remove.append(ship)
        for ship in ships_to_remove:
            self.alive_ships.remove(ship)
        self.wounds = []


if __name__ == '__main__':
    g = Game()
    while True:
        cell = g.choise_shot()
        print(cell, g.xs[cell[0]], g.ys[cell[1]])
        result = None
        while not result or result not in '123sq':
            result = input('Промах/ранен/убит [123]? [S]how field? [Q]uit?')
        if result == '1': # miss
            g.miss(cell)
            continue
        elif result == '2': # ранен
            g.wound(cell)
            continue
        elif result == '3':
            g.died(cell)
            continue
        elif result == 'q':
            break
        elif result == 's':
            g.show_field('fire')

