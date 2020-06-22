import numpy as np
import matplotlib.pyplot as plt
from flujos_esenciales import Flujo


def campo_de_velocidades(x_lim, y_lim, flujo: Flujo):
    nx = 5 * (x_lim[1] - x_lim[0])
    ny = 5 * (y_lim[1] - y_lim[0])
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    f_x, f_y = flujo.velocidad(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = 2 * np.log(np.sqrt(f_x ** 2 + f_y ** 2))

    ax.streamplot(x, y, f_x, f_y, linewidth=1, color=colors, density=1, arrowstyle='->', cmap='jet')

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_aspect('equal')
    ax.set_title('Campo de Velocidades')
    plt.show()


def contour(x, y, z, title='', units=None):
    levels = np.linspace(np.min(z), np.max(z), 20)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    cp = ax.contourf(x, y, z, levels=levels)
    clb = fig.colorbar(cp)  # Add a colorbar to a plot
    if units is not None:
        clb.ax.set_title(units)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_aspect('equal')
    ax.set_title(title)
    plt.show()


def lineas_de_corriente(x_lim, y_lim, flujo: Flujo):
    nx = 5 * (x_lim[1] - x_lim[0])
    ny = 5 * (y_lim[1] - y_lim[0])
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    z = flujo.corriente(X, Y)

    contour(X, Y, z, 'Lineas de Corriente')


def lineas_de_potencial(x_lim, y_lim, flujo: Flujo):
    nx = 5 * (x_lim[1] - x_lim[0])
    ny = 5 * (y_lim[1] - y_lim[0])
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    z = flujo.potencial(X, Y)

    contour(X, Y, z, 'Lineas de Potencial')


def campo_de_presiones(x_lim, y_lim, flujo: Flujo):
    nx = 5 * (x_lim[1] - x_lim[0])
    ny = 5 * (y_lim[1] - y_lim[0])
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    z = flujo.presion(X, Y)

    contour(X, Y, z, 'Campo de Presiones', units='Presión (Pa)')
