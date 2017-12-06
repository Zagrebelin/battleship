import tkinter

from logic import Game, CellState

"""

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
                this_cell_count = c[x, y]
                xy0 = (10 + x * size, 10 + y * size)
                xy1 = (10 + x * size + size, 10 + y * size + size)
                color = heatmap.get_color(scheme_name, lo, high, this_cell_count)
                d.rectangle([xy0, xy1], fill=color, outline='black')
                d.text((xy0[0] + size / 2, xy0[1] + size / 2), f'{this_cell_count}     ')
        i.show()
from PIL import Image, ImageDraw
import heatmap

"""

class ViewModel:
    def __init__(self, root):
        self.game = Game()
        self.cell_as_text = tkinter.StringVar(root)
        self.next_cell()

    def cmd_miss(self):
        self.game.miss(self.cell)
        self.next_cell()

    def cmd_wound(self):
        self.game.wound(self.cell)
        self.next_cell()

    def cmd_died(self):
        self.game.died(self.cell)
        self.next_cell()

    def next_cell(self):
        self.cell = self.game.choise_shot()
        x = 'абвгдежзик'[self.cell[0]]
        y = self.cell[1]+1
        self.cell_as_text.set('%s %s' % (x,y))

    def cmd_reset(self):
        self.game = Game()
        self.next_cell()

    def cmd_show(self):
        stat = self.game.show_field()
        for y in range(self.game.ys):
            for x in range(self.game.xs):
                cell = stat[x,y]
                if cell['state'] == CellState.miss:
                    ch = '.'
                elif cell['state'] == CellState.dead:
                    ch = 'X'
                else:
                    ch = str(cell['count'])
                print('%3s' % ch, end='   ')
            print()
        print()



if __name__ == '__main__':
    root = tkinter.Tk()
    vm = ViewModel(root)
    tkinter.Label(root, textvariable=vm.cell_as_text).pack()
    tkinter.Button(root, text='Промах', command=vm.cmd_miss).pack()
    tkinter.Button(root, text='Ранен', command=vm.cmd_wound).pack()
    tkinter.Button(root, text='Убит', command=vm.cmd_died).pack()
    tkinter.Button(root, text='Всё сначала', command=vm.cmd_reset).pack()
    tkinter.Button(root, text='Поле', command=vm.cmd_show).pack()

    root.mainloop()
