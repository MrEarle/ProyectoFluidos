import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod


class Flujo(ABC):
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

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError('Cannot multiply by something thats not a number')

        return Composite([self], escala_output=other)

    def __rmul__(self, other):
        return self.__mul__(other)


class Composite(Flujo):
    def __init__(self, flujos, escala_input=1, escala_output=1, rho=1):
        super().__init__(rho)
        self.flujos = flujos
        self.escala_output = escala_output
        self.escala_input = escala_input

    def funcion(self, x, y):
        res = np.full(x.shape, 0j)
        for flujo in self.flujos:
            res += flujo.funcion(self.escala_input * x, self.escala_input * y)
        return self.escala_output * res

    def velocidad(self, x, y):
        v_x = np.zeros(x.shape)
        v_y = np.zeros(y.shape)
        for flujo in self.flujos:
            v_x_i, v_y_i = flujo.velocidad(self.escala_input * x, self.escala_input * y)
            v_x += v_x_i
            v_y += v_y_i
        return self.escala_output * v_x, self.escala_output * v_y


class Uniform(Flujo):
    def __init__(self, A, escala_input=1, direction='x', rho=1):
        super().__init__(rho)
        self.A = A
        self.escala_input = escala_input

        if direction == 'x':
            self.alpha = 0
        elif direction == 'y':
            self.alpha = np.pi / 2
        elif isinstance(direction, (int, float, complex)):
            self.alpha = complex(direction)

    def funcion(self, x, y):
        z = self.escala_input * (x + y * 1j)
        return self.A * z * np.exp(self.alpha * 1j)

    def flujo(self, x, y):
        return np.real(self.funcion(x, y))

    def potencial(self, x, y):
        return np.imag(self.funcion(x, y))

    def velocidad(self, x, y):
        shape = len(x), len(y)
        vx = np.real(self.escala_input * self.A * np.cos(self.alpha))
        vy = np.real(self.escala_input * self.A * np.sin(self.alpha))
        return np.full(shape, vx), np.full(shape, vy)


class Fuente(Flujo):
    def __init__(self, A, x0=(0, 0), escala_input=1, rho=1):
        super().__init__(rho)
        self.A = A
        self.z0 = complex(*x0)
        self.escala_input = escala_input

    def funcion(self, x, y):
        z = self.escala_input * (x + y * 1j)
        return self.A * np.log(z - self.z0)

    def velocidad(self, x, y):
        x = self.escala_input * x
        y = self.escala_input * y
        r, theta = self.cartesian_to_polar(x - np.real(self.z0), y - np.imag(self.z0))
        vr = self.escala_input * self.A / r
        vt = 0

        vx = vr * np.cos(theta) - vt * np.sin(theta)
        vy = vr * np.sin(theta) + vt * np.cos(theta)
        return np.real(vx), np.real(vy)


class VorticeIrrotacional(Flujo):
    def __init__(self, A, x0=(0, 0), escala_input=1, rho=1):
        super().__init__(rho)
        self.A = A
        self.z0 = complex(*x0)
        self.escala_input = escala_input

    def funcion(self, x, y):
        z = self.escala_input * (x + y * 1j)
        return -1j * self.A * np.log(z - self.z0)

    def velocidad(self, x, y):
        x = self.escala_input * x
        y = self.escala_input * y
        r, theta = self.cartesian_to_polar(x - np.real(self.z0), y - np.imag(self.z0))
        v = self.escala_input * self.A / r
        return np.real(v * -np.sin(theta)), np.real(v * np.cos(theta))


class Doblete(Flujo):
    def __init__(self, A, x0=(0, 0), escala_input=1, rho=1):
        super().__init__(rho)
        self.A = A
        self.z0 = complex(*x0)
        self.escala_input = escala_input

    def funcion(self, x, y):
        z = self.escala_input * (x + y * 1j)
        return self.A / (z - self.z0)

    def velocidad(self, x, y):
        r, theta = self.cartesian_to_polar(x - np.real(self.z0), y - np.imag(self.z0))
        vr = -self.A / (r ** 2) * np.cos(theta) * (1 / self.escala_input)
        vt = -self.A / (r ** 2) * np.sin(theta) * (1 / self.escala_input)

        vx = vr * np.cos(theta) - vt * np.sin(theta)
        vy = vr * np.sin(theta) + vt * np.cos(theta)
        return np.real(vx), np.real(vy)


class Custom(Flujo):
    def __init__(self, funcion, velocidad, rho=1):
        super().__init__(rho)
        self._funcion = funcion
        self._velocidad = velocidad

    def funcion(self, x, y):
        return self._funcion(x, y)

    def velocidad(self, x, y):
        return self._velocidad(x, y)
