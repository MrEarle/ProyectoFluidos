from tkinter import *
import tkinter
import flow_selector
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from flujos_esenciales import *

flujos = {
    'Uniforme': Uniform,
    'Fuente': Fuente,
    'Vortice Irrotacional': VorticeIrrotacional,
    'Doblete': Doblete,
}


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class MainScreen:
    def __init__(self):
        self.window = Tk()

        self.window.title('Flujos Esenciales')
        self.window.geometry('1000x500')

        Label(self.window, text="Flow Toolz 5000", font=("Arial", 25)).grid(column=0, row=0)

        self.choices = {'Uniforme', 'Fuente', 'Vortice Irrotacional', 'Doblete'}

        self.flowFrame = Frame(self.window)
        self.flowFrame.grid(row=2, column=0)

        self.flows = [flow_selector.FlowSelector(self.flowFrame, self.choices, row=1, first=True)]

        self.plt = None

        self.plot_type = StringVar(self.window)
        self.plot_type.set('velocidad')

        self.buttonFrame = Frame(self.window)
        self.buttonFrame.grid(row=0, column=1)

        self.add()
        self.remove()
        self.enterButton()

        self.plotType()

    def plotType(self):
        typeFrame = Frame(self.window)
        typeFrame.grid(column=0, row=1)
        Label(typeFrame, text='Tipo de grafico:').grid(column=0, row=1)
        popupMenu = OptionMenu(typeFrame, self.plot_type, *['velocidad', 'corriente', 'potencial'])
        popupMenu.grid(column=1, row=1)

    def add(self):
        def onClick(*args):
            self.flows.append(flow_selector.FlowSelector(self.flowFrame, self.choices, row=len(self.flows) + 1, first=False))

        btn = Button(self.buttonFrame, text="Add flow", command=onClick)

        btn.grid(column=1, row=0)

    def remove(self):
        def onClick(*args):
            f = self.flows.pop()
            f.frame.destroy()

        btn = Button(self.buttonFrame, text="Remove flow", command=onClick)

        btn.grid(column=2, row=0)

    def enterButton(self):
        def onClick(*args):
            print([i.props for i in self.flows])
            plot_type = self.plot_type.get()
            if plot_type == 'velocidad':
                self.plotSpeed()
            else:
                self.plotLevel(plot_type)

        btn = Button(self.buttonFrame, text="Generate Flow", command=onClick)

        btn.grid(column=3, row=0)

    @staticmethod
    def getFlow(props):
        z0 = (props['x0'], props['y0'])
        return props['out_scale'] * flujos[props['flow']](props['A'], escala_input=props['in_scale'], x0=z0)

    def plotSpeed(self):
        if self.plt is not None:
            self.plt.destroy()

        flujo = self.getFlow(self.flows[0].props)
        if len(self.flows) > 1:
            for f in self.flows[1:]:
                flujo += self.getFlow(f.props)

        frame = Frame(self.window)

        fig = Figure(figsize=(5, 4), dpi=100)

        nx = 64
        ny = 64
        x = np.linspace(-10, 10, nx)
        y = np.linspace(-10, 10, ny)

        X, Y = np.meshgrid(x, y)

        f_x, f_y = flujo.velocidad(X, Y)

        ax = fig.add_subplot(111)

        colors = sigmoid(np.hypot(f_x, f_y) / 50)

        # ax.quiver(x, y, f_x, f_y, colors, scale=64, linewidth=1, cmap='jet', pivot='mid')
        ax.streamplot(x, y, f_x, f_y, color=colors, cmap='jet', density=2, linewidth=0.5, arrowstyle='->')

        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_aspect('equal')
        ax.set_title('Campo de Velocidades')
        ax.set_xlim((-5, 5))
        ax.set_ylim((-5, 5))

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            self.window.quit()     # stops mainloop
            self.window.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(master=frame, text="Quit", command=_quit)
        button.pack(side=tkinter.BOTTOM)

        frame.grid(row=3, column=0)

        self.plt = frame

    def plotLevel(self, f_type):
        if self.plt is not None:
            self.plt.destroy()

        flujo = self.getFlow(self.flows[0].props)
        if len(self.flows) > 1:
            for f in self.flows[1:]:
                flujo += self.getFlow(f.props)

        frame = Frame(self.window)

        fig = Figure(figsize=(5, 4), dpi=100)

        nx = 100
        ny = 100
        x = np.linspace(-10, 10, nx)
        y = np.linspace(-10, 10, ny)

        X, Y = np.meshgrid(x, y)

        if f_type == 'potencial':
            z = flujo.potencial(X, Y)
        elif f_type == 'corriente':
            z = flujo.corriente(X, Y)
        else:
            z = flujo.presion(X, Y)

        ax = fig.add_subplot(111)

        z[z < -1000000] = -1000000
        levels = np.linspace(np.min(z), np.max(z), 20)

        cp = ax.contour(x, y, z, cmap='jet', levels=levels)

        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_aspect('equal')
        ax.set_title(f_type)
        ax.set_xlim((-5, 5))
        ax.set_ylim((-5, 5))

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            self.window.quit()     # stops mainloop
            self.window.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(master=frame, text="Quit", command=_quit)
        button.pack(side=tkinter.BOTTOM)

        frame.grid(row=3, column=0)

        self.plt = frame


window = MainScreen()
window.window.mainloop()
