from flujos_esenciales import *
import plotter


U = 25
a = 11
K = 15
# flujo = U * (Uniform(1) + Doblete(a ** 2)) + (-K) * VorticeIrrotacional(1, escala_input=1 / a)
flujo = Doblete(1) + Fuente(-1)

flujo.set_initial_conditions(-10**10, 0, 101300)


plotter.campo_de_velocidades((-1, 1), (-1, 1), flujo)
plotter.campo_de_velocidades((-5, 5), (-5, 5), flujo)
plotter.campo_de_velocidades((-10, 10), (-10, 10), flujo)
plotter.campo_de_velocidades((-20, 20), (-20, 20), flujo)
plotter.campo_de_presiones((-2, 2), (-2, 2), flujo)
plotter.lineas_de_corriente((-1, 1), (-1, 1), flujo)
plotter.lineas_de_potencial((-1, 1), (-1, 1), flujo)
