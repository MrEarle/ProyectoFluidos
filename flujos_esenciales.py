import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

from abc import ABC, abstractmethod

sym.init_printing()


class Flujo(ABC):
    def __init__(self, rho):
        self.initial_condition = None
        self._rho = rho

    @property
    def symbolic(self):
        return sym.Rational(0, 1)

    @property
    def corriente_symbolic(self):
        return sym.im(self.symbolic)

    @property
    def potencial_symbolic(self):
        return sym.re(self.symbolic)

    @property
    def velocidad_symbolic(self):
        v_x = sym.diff(self.potencial_symbolic, sym.Symbol('x', real=True))
        v_y = sym.diff(self.potencial_symbolic, sym.Symbol('y', real=True))
        return v_x, v_y

    @property
    def presion_symbolic(self):
        if self.initial_condition is None:
            raise Exception('Initial conditions must be set')

        (v0_x, v0_y), P0 = self.initial_condition
        v_x, v_y = self.velocidad_symbolic

        return P0 + (self.rho / 2) * (v0_x ** 2 + v0_y ** 2 - (v_x ** 2 + v_y ** 2))

    @property
    def rho(self):
        return self._rho

    def set_rho(self, rho):
        self._rho = rho

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

        return P0 + (self.rho / 2) * (v0_x ** 2 + v0_y ** 2 - (v_x ** 2 + v_y ** 2))

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

    @property
    def rho(self):
        return self._rho

    @property
    def symbolic(self):
        s = sym.Rational(0, 1)
        for flujo in self.flujos:
            s += flujo.symbolic
        return self.escala_output * s

    def set_rho(self, value):
        self._rho = value

        for flujo in self.flujos:
            flujo.set_rho(value)

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
    def __init__(self, A, escala_input=1, direction='x', rho=1, x0=None):
        super().__init__(rho)
        self.A = A
        self.escala_input = escala_input

        if direction == 'x':
            self.alpha = 0
        elif direction == 'y':
            self.alpha = np.pi / 2
        elif isinstance(direction, (int, float, complex)):
            self.alpha = complex(direction)

    @property
    def symbolic(self):
        z = sym.Symbol('x', real=True) + sym.I * sym.Symbol('y', real=True)
        return self.A * self.escala_input * z * sym.exp(-self.alpha * sym.I)

    def funcion(self, x, y):
        z = self.escala_input * (x + y * 1j)
        return self.A * z * np.exp(-self.alpha * 1j)

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

    @property
    def symbolic(self):
        z = sym.Symbol('x', real=True) + sym.I * sym.Symbol('y', real=True)
        z *= self.escala_input
        return self.A * sym.log(z - self.z0)

    def funcion(self, x, y):
        z = self.escala_input * (x + y * 1j)
        result = self.A * np.log(z - self.z0)
        result[z - self.z0 == 0 + 0j] = -10**10 + 0j
        return result

    def velocidad(self, x, y):
        x = self.escala_input * x
        y = self.escala_input * y
        r, theta = self.cartesian_to_polar(x - np.real(self.z0), y - np.imag(self.z0))
        vr = self.escala_input * self.A / r
        vr[r == 0] = 0
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

    @property
    def symbolic(self):
        z = sym.Symbol('x', real=True) + sym.I * sym.Symbol('y', real=True)
        z *= self.escala_input
        return -1j * self.A * sym.log(z - self.z0)

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

    @property
    def symbolic(self):
        z = sym.Symbol('x', real=True) + sym.I * sym.Symbol('y', real=True)
        z *= self.escala_input
        return self.A / (z - self.z0)

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
    def __init__(self, funcion, velocidad, symbolic=None, rho=1):
        super().__init__(rho)
        self._funcion = funcion
        self._velocidad = velocidad
        self._symbolic = symbolic

    @property
    def symbolic(self):
        return self._symbolic

    def funcion(self, x, y):
        return self._funcion(x, y)

    def velocidad(self, x, y):
        return self._velocidad(x, y)
