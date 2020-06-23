from flujos_esenciales import *
import plotter


# flujo = Uniform(1, np.pi / 4) + Fuente(1, (1, 1)) + Fuente(1, (-1, 1))
flujo = 2 * (Uniform(1) + Doblete(4)) + 1.5 * VorticeIrrotacional(1)
flujo.set_initial_conditions(-100, -100, 1)


plotter.campo_de_velocidades((-2, 2), (-2, 2), flujo)
plotter.campo_de_presiones((-2, 2), (-2, 2), flujo)
plotter.lineas_de_corriente((-2, 2), (-2, 2), flujo)
plotter.lineas_de_potencial((-2, 2), (-2, 2), flujo)
