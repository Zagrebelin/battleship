import tkinter

from logic import Game



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
        x = self.game.xs[self.cell[0]]
        y = self.game.ys[self.cell[1]]
        self.cell_as_text.set('%s %s' % (x,y))

    def cmd_reset(self):
        self.game = Game()
        self.next_cell()

    def cmd_show(self):
        self.game.show_field('fire')


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
