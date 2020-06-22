from flujos_esenciales import *
import plotter


flujo = Uniform(1, np.pi / 4) + Fuente(1, (1, 1)) + Fuente(1, (-1, 1))
flujo.set_initial_conditions(-100, -100, 1)


plotter.campo_de_velocidades((-5, 5), (-5, 5), flujo)
plotter.campo_de_presiones((-5, 5), (-5, 5), flujo)
plotter.lineas_de_corriente((-5, 5), (-5, 5), flujo)
plotter.lineas_de_potencial((-5, 5), (-5, 5), flujo)
