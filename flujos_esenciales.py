import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod


class Flujo:
    def __init__(self, rho):
        self.initial_condition = None
        self.rho = rho

    def set_initial_conditions(self, x0, y0, P0):
        vx0, vy0 = self.velocidad(np.array([[x0]]), np.array([[y0]]))
        self.initial_condition = ((vx0[0, 0], vy0[0, 0]), P0)

    @abstractmethod
    def funcion(self, x, y):
        pass

    def corriente(self, x, y):
        return np.imag(self.funcion(x, y))

    def potencial(self, x, y):
        return np.real(self.funcion(x, y))

    def presion(self, x, y):
        if self.initial_condition is None:
            raise Exception('Initial conditions must be set')

        (v0_x, v0_y), P0 = self.initial_condition
        v_x, v_y = self.velocidad(x, y)

        return P0 + (self.rho / 2) * (np.hypot(v0_x, v0_y) ** 2 - np.hypot(v_x, v_y) ** 2)

    @abstractmethod
    def velocidad(self, x, y):
        pass

    @staticmethod
    def cartesian_to_polar(x, y):
        return np.abs(x + y * 1j), np.angle(x + y * 1j)

    @staticmethod
    def polar_to_cartesian(r, theta):
        z = r * np.exp(theta * 1j)
        return np.real(z), np.imag(z)

    def __add__(self, other):
        return Composite([self, other])


class Composite(Flujo):
    def __init__(self, flujos, rho=1):
        super().__init__(rho)
        self.flujos = flujos

    def funcion(self, x, y):
        res = np.full(x.shape, 0j)
        for flujo in self.flujos:
            res += flujo.funcion(x, y)
        return res

    def velocidad(self, x, y):
        v_x = np.zeros(x.shape)
        v_y = np.zeros(y.shape)
        for flujo in self.flujos:
            v_x_i, v_y_i = flujo.velocidad(x, y)
            v_x += v_x_i
            v_y += v_y_i
        return v_x, v_y


class Uniform(Flujo):
    def __init__(self, A, direction='x', rho=1):
        super().__init__(rho)
        self.A = A
        if direction == 'x':
            self.alpha = 0
        elif direction == 'y':
            self.alpha = np.pi / 2
        elif isinstance(direction, (int, float, complex)):
            self.alpha = complex(direction)

    def funcion(self, x, y):
        return self.A * (x + y * 1j) * np.exp(self.alpha * 1j)

    def flujo(self, x, y):
        return np.real(self.funcion(x, y))

    def potencial(self, x, y):
        return np.imag(self.funcion(x, y))

    def velocidad(self, x, y):
        shape = len(x), len(y)
        return np.full(shape, np.real(self.A * np.cos(self.alpha))), np.full(shape, np.real(self.A * np.sin(self.alpha)))


class Fuente(Flujo):
    def __init__(self, A, x0=(0, 0), rho=1):
        super().__init__(rho)
        self.A = A
        self.z0 = complex(*x0)

    def funcion(self, x, y):
        return self.A * np.log(x + y * 1j - self.z0)

    def velocidad(self, x, y):
        r, theta = self.cartesian_to_polar(x - np.real(self.z0), y - np.imag(self.z0))
        v = self.A / r
        return np.real(v * np.cos(theta)), np.real(v * np.sin(theta))


class VorticeIrrotacional(Flujo):
    def __init__(self, A, x0=(0, 0), rho=1):
        super().__init__(rho)
        self.A = A
        self.z0 = complex(*x0)

    def funcion(self, x, y):
        return -1j * self.A * np.log(x + y * 1j - self.z0)

    def velocidad(self, x, y):
        r, theta = self.cartesian_to_polar(x - np.real(self.z0), y - np.imag(self.z0))
        v = self.A / r
        return np.real(v * -np.sin(theta)), np.real(v * np.cos(theta))
