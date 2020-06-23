import numpy as np
import matplotlib.pyplot as plt
from flujos_esenciales import Flujo


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def campo_de_velocidades(x_lim, y_lim, flujo: Flujo):
    nx = 64
    ny = 64
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    f_x, f_y = flujo.velocidad(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = sigmoid(np.hypot(f_x, f_y) / 50)

    # ax.quiver(x, y, f_x, f_y, colors, scale=64, linewidth=1, cmap='jet', pivot='mid')
    ax.streamplot(x, y, f_x, f_y, color=colors, cmap='jet', density=2, linewidth=0.5, arrowstyle='->')

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_aspect('equal')
    ax.set_title('Campo de Velocidades')
    plt.show()


def contour(x, y, z, title='', units=None):
    z[z < -1000000] = -1000000
    levels = np.linspace(np.min(z), np.max(z), 20)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    cp = ax.contourf(x, y, z, cmap='jet', levels=levels)
    try:
        clb = fig.colorbar(cp)  # Add a colorbar to a plot
        if units is not None:
            clb.ax.set_title(units)
    except Exception:
        pass

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_aspect('equal')
    ax.set_title(title)
    plt.show()


def lineas_de_corriente(x_lim, y_lim, flujo: Flujo):
    nx = 100
    ny = 100
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    z = flujo.corriente(X, Y)

    contour(X, Y, z, 'Lineas de Corriente')


def lineas_de_potencial(x_lim, y_lim, flujo: Flujo):
    nx = 100
    ny = 100
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    z = flujo.potencial(X, Y)

    contour(X, Y, z, 'Lineas de Potencial')


def campo_de_presiones(x_lim, y_lim, flujo: Flujo):
    nx = 100
    ny = 100
    x = np.linspace(*x_lim, nx)
    y = np.linspace(*y_lim, ny)

    X, Y = np.meshgrid(x, y)

    z = flujo.presion(X, Y)

    contour(X, Y, z, 'Campo de Presiones', units='Presión (Pa)')
