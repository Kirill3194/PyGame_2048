import pygame
import random
import sqlite3


class Field:
    def __init__(self, login, password):
        self.field = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.score = 0
        self.random_cube()
        self.random_cube()
        self.login = login
        self.password = password

    def random_cube(self):
        cubes = []
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                if self.field[y][x] == 0:
                    cubes.append(y * len(self.field) + x)
        randomcube = random.choice(cubes)
        self.field[randomcube // 4][randomcube % 4] = 2

    def left_move(self):
        summ = 0
        for y in range(len(self.field)):
            for x in range(len(self.field)):
                for cord_x in range(len(self.field)):
                    change_x = cord_x - 1
                    if self.field[y][cord_x] == 0:
                        continue
                    while change_x >= 0:
                        if self.field[y][change_x] == 0:
                            self.field[y][change_x] = self.field[y][change_x + 1]
                            self.field[y][change_x + 1] = 0
                            summ += 1
                        else:
                            break
                        change_x -= 1
                if x + 1 < len(self.field) and self.field[y][x] == self.field[y][x + 1] and self.field[y][x] != 0:
                    self.field[y][x] = self.field[y][x] * 2
                    self.score += self.field[y][x]
                    self.field[y][x + 1] = 0
                    summ += 1
        if summ > 0:
            self.random_cube()

    def right_move(self):
        summ = 0
        for y in range(len(self.field)):
            for x in range(len(self.field) - 1, -1, -1):
                for cord_x in range(len(self.field) - 1, -1, -1):
                    change_x = cord_x + 1
                    if self.field[y][cord_x] == 0:
                        continue
                    while change_x < len(self.field):
                        if self.field[y][change_x] == 0:
                            self.field[y][change_x] = self.field[y][change_x - 1]
                            self.field[y][change_x - 1] = 0
                            summ += 1
                        else:
                            break
                        change_x += 1
                if x - 1 >= 0 and self.field[y][x] == self.field[y][x - 1] and self.field[y][x] != 0:
                    self.field[y][x] = self.field[y][x] * 2
                    self.score += self.field[y][x]
                    self.field[y][x - 1] = 0
                    summ += 1
        if summ > 0:
            self.random_cube()

    def down_move(self):
        summ = 0
        for x in range(len(self.field)):
            for y in range(len(self.field) - 1, -1, -1):
                for cord_y in range(len(self.field) - 1, -1, -1):
                    change_y = cord_y + 1
                    if self.field[cord_y][x] == 0:
                        continue
                    while change_y < len(self.field):
                        if self.field[change_y][x] == 0:
                            self.field[change_y][x] = self.field[change_y - 1][x]
                            self.field[change_y - 1][x] = 0
                            summ += 1
                        else:
                            break
                        change_y += 1
                if y - 1 >= 0 and self.field[y][x] == self.field[y - 1][x] and self.field[y][x] != 0:
                    self.field[y][x] = self.field[y][x] * 2
                    self.field[y - 1][x] = 0
                    summ += 1
                    self.score += self.field[y][x]
        if summ > 0:
            self.random_cube()

    def top_move(self):
        summ = 0
        for x in range(len(self.field)):
            for y in range(len(self.field)):
                for cord_y in range(len(self.field)):
                    change_y = cord_y - 1
                    if self.field[cord_y][x] == 0:
                        continue
                    while change_y >= 0:
                        if self.field[change_y][x] == 0:
                            self.field[change_y][x] = self.field[change_y + 1][x]
                            self.field[change_y + 1][x] = 0
                            summ += 1
                        else:
                            break
                        change_y -= 1
                if y + 1 < len(self.field) and self.field[y][x] == self.field[y + 1][x] and self.field[y][x] != 0:
                    self.field[y][x] = self.field[y][x] * 2
                    self.field[y + 1][x] = 0
                    summ += 1
                    self.score += self.field[y][x]
        if summ > 0:
            self.random_cube()

    def __str__(self):
        for y in range(len(self.field)):
            print(self.field[y])
        return '------------------'

    def move(self, side):
        if side == 'l':
            self.left_move()
        if side == 'r':
            self.right_move()
        if side == 'd':
            self.down_move()
        if side == 't':
            self.top_move()
        if side == 'new':
            self.new_game()

    def new_game(self):
        self.field = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.score = 0
        self.random_cube()
        self.random_cube()


class Registration:
    def __init__(self):
        self.login = 0
        self.password = 0

    def check(self, login, password):
        con = sqlite3.connect("2048_accounts.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM player""").fetchall()
        registration_is_confirmed = True
        for player in result:
            if player == login:
                print('Пользователь под таким логином уже есть!')
                registration_is_confirmed = False
        if len(login) <= 3 and registration_is_confirmed:
            registration_is_confirmed = False
            print('login слишком маленький, он должен состоять как минимум из 4 символов')
        elif len(password) <= 5 and registration_is_confirmed:
            registration_is_confirmed = False
            print('password слишком маленький, он должен состоять как минимум из 6 символов')
        return registration_is_confirmed

    def registration_player(self):
        self.login = 0
        self.password = 0
        if self.check(self.login, self.password):
            pass
        else:
            pass


class Entrance:
    def __init__(self):
        pass

    def check(self):
        pass

    def entrance_player(self):
        pass


Field1 = Field('aaaaa', 'aaaaa')
print(Field1)
a = input()
while a != '0':
    Field1.move(a)
    print(Field1)
    a = input()
