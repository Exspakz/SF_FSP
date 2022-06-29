from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "You're trying to shoot outside!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "You have already shot this cell"


class BoardWrongShipException(BoardException):
    pass


class Dot:  
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    

class Ship:
    def __init__(self, bow, length, orient):
        self.bow = bow
        self.length = length
        self.orient = orient
        self.lives = length
    
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            
            if self.orient == 0:
                cur_x += i
            
            elif self.orient == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots

    
class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        
        self.field = [['0' for _ in range(size)] for _ in range(size)]
        self.count_destr = 0
        self.busy = []
        self.ships = []
        
    def __str__(self):
        skin = ''
        skin += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, j in enumerate(self.field):
            skin += f"\n{i + 1} | {' | '.join(j)} |"
          
        if self.hid:
            skin = skin.replace('■', '0')
        return skin
                  
    def out_field(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))
        
    def contour(self, ship, verb=False):
        near = [
            (1, 1), (1, 0), (0, 1),
            (0, 0), (0, -1), (-1, 0),
            (1, -1), (-1, 1), (-1, -1)
        ]
        
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out_field(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)
        
    def add_ship(self, ship):
        
        for d in ship.dots:
            if self.out_field(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
            
        self.ships.append(ship)
        self.contour(ship)
                        
    def shot(self, d):
        if self.out_field(d):
            raise BoardOutException()
    
        if d in self.busy:
            raise BoardUsedException()
                        
        self.busy.append(d)
            
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count_destr += 1
                    self.contour(ship, verb=True)
                    print('Ship destroyed!')
                    return True
                else:
                    print('Hit!')
                    return True
                        
        self.field[d.x][d.y] = '.'
        print('Missed!')
        return False
                        
    def begin(self):
        self.busy = []
        
        
class Player:
    def __init__(self, user_board, enemy_board):
        self.user_board = user_board
        self.enemy_board = enemy_board
        
    def ask(self):
        raise NotImplementedError()
        
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Coordinates: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input('Coordinates: ').split()
            
            if len(cords) != 2:
                print('Enter 2 coordinates!')
                continue

            x, y = cords
            
            if not (x.isdigit()) or not (y.isdigit()):
                print('Enter only numbers!')
                continue
                
            x, y = int(x), int(y)
            
            return Dot(x - 1, y - 1)
        
        
class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.us = User(pl, co)
        self.ai = AI(co, pl)

    def gen_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = (Ship(Dot(randint(0, self.size), 
                                 randint(0, self.size)), i, randint(0, 1)))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.gen_board()
        return board

    def show_board(self):
        print('User board:' + ' ' * 24 + 'AI board:')
        us = str(self.us.user_board).split('\n')
        ai = str(self.ai.user_board).split('\n')
        for k, j in zip(us, ai):
            print(f'{k}   :   {j}')
          
    def loop(self):
        num = 0
        while True:
            self.show_board()
            if num % 2 == 0:
                print('User move!')
                repeat = self.us.move()
            else:
                print('AI move!')
                repeat = self.ai.move()
            if repeat:
                num -= 1
                  
            if self.ai.user_board.count_destr == 7:
                print('User won!')
                self.show_board()
                break
                  
            if self.us.user_board.count_destr == 7:
                print('AI won!')
                self.show_board()
                break
            num += 1
                  
    def start(self):
        self.loop()
        
        
g = Game()
g.start()
