from flujos_esenciales import *
import plotter


# flujo = Uniform(1, np.pi / 4) + Fuente(-5, (1, 1)) + VorticeIrrotacional(8, (-1, 1))
flujo = 25 * (Uniform(1) + Doblete(11 ** 2)) + (-15) * VorticeIrrotacional(1, escala_input=1 / 11)

flujo.set_initial_conditions(-10**10, 0, 1)


plotter.campo_de_velocidades((-5, 5), (-5, 5), flujo)
plotter.campo_de_velocidades((-10, 10), (-10, 10), flujo)
plotter.campo_de_velocidades((-20, 20), (-20, 20), flujo)
plotter.campo_de_presiones((-2, 2), (-2, 2), flujo)
plotter.lineas_de_corriente((-2, 2), (-2, 2), flujo)
plotter.lineas_de_potencial((-2, 2), (-2, 2), flujo)
