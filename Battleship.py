import random
from random import random, randrange, randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за пределы поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Сюда уже стреляли"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, length, o):
        self.bow = bow
        self.length = length
        self.o = o
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.occupied = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.occupied:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.occupied.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.occupied:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.occupied.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.occupied:
            raise BoardUsedException()
            self.occupied.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль убит")
                    return False
                else:
                    print("Корабль ранен")
                    return True
        self.field[d.x][d.y] = "."
        print("Мимо")
        return False

    def begin(self):
        self.occupied = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ходит компьютер: {d.x+1} {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            coordinates = input("Ходит пользователь: ").split()
            if len(coordinates) != 2:
                print("Введите две координаты через пробел: ")
                continue
            x, y = coordinates
            x, y = int(x), int(y)
            return Dot(x-1, y-1)


def greet():
    print("-------------------")
    print("  Приветсвуем Вас  ")
    print("      в игре       ")
    print("    'Морской Бой'    ")
    print("-------------------")
    print(" формат ввода: x y (через пробел)")
    print(" x - номер строки  ")
    print(" y - номер столбца ")


class Game:
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for length in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def loop(self):
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя: ")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера: ")
            print(self.ai.board)
            if num % 2 == 0:
                print("-"*20)
                print("Ход пользователя")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ход компьютера")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл!")
                break
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        greet()
        self.loop()


g = Game()
g.start()