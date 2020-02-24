#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from random import random
from math import sqrt
# from Vec2d import Vec2d // should be  sharded  to several files
from math import sqrt


class Vec2d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return type(self)(self.x * k, self.y * k)

    def int_pair(self):
        return (self.x, self.y)

    def __len__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return str(self.int_pair())

    def __repr__(self):
        return str(self.int_pair())


class Polyline(object):
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point):
        self.points.append(Vec2d(point[0], point[1]))
        self.speeds.append(Vec2d(random() * 2, random() * 2))



class Desc(object):
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

class Knot(Polyline):
    count = Desc()
    def __init__(self, count, Display, SCREEN_DIM):
        super().__init__()
        self.count = count
        self.gameDisplay = Display
        self.SCREEN_DIM = SCREEN_DIM

    def get_point(self, points, k, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * k + self.get_point(points, k, deg - 1) * (1 - k)

    def get_points(self, points):
        k = 1 / self.count
        result = []
        for it in range(self.count):
            result.append(self.get_point(points, it * k))
        return result

    def set_points(self):
        """recalculation of reference point coordinates"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > self.SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > self.SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """drawing points on the screen"""
        if style == "line":
            points = self.get_knot()

            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.gameDisplay, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(self.gameDisplay, color, (int(p.x), int(p.y)), width)

    def get_knot(self):
        if len(self.points) < 3:
            return []
        result = []
        for it in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[it] + self.points[it + 1]) * 0.5)
            ptn.append(self.points[it + 1])
            ptn.append((self.points[it + 1] + self.points[it + 2]) * 0.5)
            result.extend(self.get_points(ptn))
        return result


# main class
class Game(object):

    @classmethod
    def run(self, SCREEN_DIM):
        pygame.init()
        gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

        steps = 35
        working = True
        pause = True
        knot = Knot(steps, gameDisplay, SCREEN_DIM)

        hue = 0
        color = pygame.Color(0)

        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    if event.key == pygame.K_r:
                        knot = Knot(steps, gameDisplay, SCREEN_DIM)
                    if event.key == pygame.K_p:
                        pause = not pause
                    if event.key == pygame.K_KP_PLUS:
                        #knot.set_count(knot.get_count() + 1)
                        knot.count += 1
                    if event.key == pygame.K_KP_MINUS:
                        #steps = knot.get_count()
                        steps = knot.count
                        #knot.set_count(steps - 1 if steps > 1 else 0)
                        knot.count = (steps - 1 if steps > 1 else 0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    knot.add_point(event.pos)

            gameDisplay.fill((0, 0, 0))
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            knot.draw_points()
            knot.draw_points("line", 3, color)
            if not pause:
                knot.set_points()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


if __name__ == "__main__":
    Game.run((800, 600))