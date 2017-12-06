import itertools
import random
from collections import Counter
from enum import Enum, auto


class CellState(Enum):
    unknown = auto()
    dead = auto()
    miss = auto


class Game:
    def __init__(self, ships_config=None, xs=10, ys=10):
        if ships_config is None:
            ships_config = [(4, 1), (3, 2), (2, 3), (1, 4)]
        self.xs = xs
        self.ys = ys
        self.ships = []                         # список всех кораблей, которые могут стоять на поле. Из этого списка убираем по сигналу "промах".
        self.rest_ships = dict(ships_config)    # количество кораблей разного размера, которые где-то на поле.
        self.misses = []
        self.deads = []
        for size, count in ships_config:
            for y in range(self.ys):
                for x in range(self.xs - size + 1):
                    this_ship = []
                    for offset in range(size):
                        this_ship.append((x + offset, y))
                    self.ships.append(this_ship)
            if size > 1:
                for x in range(self.xs):
                    for y in range(self.ys - size + 1):
                        this_ship = []
                        for offset in range(size):
                            this_ship.append((x, y + offset))
                        self.ships.append(this_ship)
        self.misses = []  # тут отмечаем все промахи по чужому полю
        self.wounds = []  # тут отмечаем все раненые ячейки

    def show_field(self):
        c = Counter()
        for ship in self.ships:
            c.update(ship)
        ret = {}
        for xy in itertools.product(range(self.xs), range(self.ys)):
            if xy in self.misses:
                state = CellState.miss
            elif xy in self.deads:
                state = CellState.dead
            else:
                state = CellState.unknown
            ret[xy] = {
                'state': state,
                'count': c[xy]
            }
        return ret

    def choise_shot(self):
        ships_to_shot = []

        for ship in self.ships:
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
        cells_to_shot = [cell for cell, count in all_cells.items() if count == max_cell]
        return random.choice(cells_to_shot)

    def miss(self, xy):
        self.misses.append(xy)
        ships_to_remove = []
        for ship in self.ships:
            if xy in ship:
                ships_to_remove.append(ship)
        for ship in ships_to_remove:
            self.ships.remove(ship)

    def wound(self, xy):
        self.deads.append(xy)
        self.wounds.append(xy)

    def died(self, xy):
        self.wound(xy)
        sank_ship_size = len(self.wounds)
        self.rest_ships[sank_ship_size] -= 1

        ships_to_remove = []
        forbiden_cells = []
        for cell in self.wounds:
            forbiden_cells.append(cell)
            for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
                forbiden_cells.append((cell[0] + dx, cell[1] + dy))
        for ship in self.ships:
            if any(cell in forbiden_cells for cell in ship):
                ships_to_remove.append(ship)
            if self.rest_ships[sank_ship_size] == 0 and len(ship) == sank_ship_size:
                ships_to_remove.append(ship)
        for ship in ships_to_remove:
            if ship in self.ships:
                self.ships.remove(ship)
        self.wounds = []
