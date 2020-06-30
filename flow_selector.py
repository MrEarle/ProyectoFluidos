from tkinter import *
from tkinter import messagebox


class FlowSelector:
    def __init__(self, window, options, row=1, first=True):
        self.window = window
        self.options = options

        # Frame
        flowFrame = Frame(window)
        flowFrame.grid(column=0, row=row, sticky=(N, W, E, S))
        flowFrame.columnconfigure(0, weight=1)
        flowFrame.rowconfigure(0, weight=1)

        self.frame = flowFrame

        self.props = {
            'out_scale': 1,
            'flow': 'Uniforme',
            'in_scale': 1,
            'x0': 0,
            'y0': 0,
            'A': 1,
        }

        Label(self.frame, text="f(z)=" if first else "+").grid(column=0, row=0)
        self._scale = self.out_scale()
        Label(self.frame, text="*").grid(column=2, row=0)
        self._selector = self.selector()
        Label(self.frame, text="(").grid(column=4, row=0)
        self.in_scale()
        Label(self.frame, text="  *  z").grid(column=6, row=0)
        self.z0()
        Label(self.frame, text=",    A = ").grid(column=8, row=0)
        self.A()
        Label(self.frame, text=")").grid(column=10, row=0)

    def selector(self):
        # Flow select
        selectedFlow = StringVar(self.frame)

        selectedFlow.set(self.props['flow'])

        popupMenu = OptionMenu(self.frame, selectedFlow, *self.options)
        popupMenu.grid(column=3, row=0)

        def changeFlow(*args):
            self.props['flow'] = selectedFlow.get()

        selectedFlow.trace('w', changeFlow)

        return selectedFlow

    def out_scale(self):
        value = StringVar(self.frame)

        value.set(str(self.props['out_scale']))

        valEntry = Entry(self.frame, width=10, textvariable=value)

        valEntry.grid(column=1, row=0)

        def onChange(*args):
            try:
                val = value.get()
                if val != '':
                    self.props['out_scale'] = float(val)
            except Exception:
                messagebox.showerror('Valor incorrecto', 'El valor que multiplica al flujo debe ser un numero')
                value.set(str(self.props['out_scale']))

        value.trace('w', onChange)
        return value

    def in_scale(self):
        value = StringVar(self.frame)

        value.set(str(self.props['in_scale']))

        valEntry = Entry(self.frame, width=10, textvariable=value)

        valEntry.grid(column=5, row=0)

        def onChange(*args):
            try:
                val = value.get()
                if val != '':
                    self.props['in_scale'] = float(val)
            except Exception:
                messagebox.showerror('Valor incorrecto', 'El valor que multiplica al flujo debe ser un numero')
                value.set(str(self.props['in_scale']))

        value.trace('w', onChange)
        return value

    def z0(self):
        frame = Frame(self.frame)

        x0 = StringVar(frame)
        y0 = StringVar(frame)
        x0.set(str(self.props['x0']))
        y0.set(str(self.props['y0']))

        x0Entry = Entry(frame, width=10, textvariable=x0)
        y0Entry = Entry(frame, width=10, textvariable=y0)

        def onX0Change(*args):
            try:
                val = x0.get()
                if val != '':
                    self.props['x0'] = float(val)
            except Exception:
                messagebox.showerror('Valor incorrecto', 'El valor de x0 debe ser un numero')
                x0.set(str(self.props['x0']))

        def onY0Change(*args):
            try:
                val = y0.get()
                if val != '':
                    self.props['y0'] = float(val)
            except Exception:
                messagebox.showerror('Valor incorrecto', 'El valor de y0 debe ser un numero')
                y0.set(str(self.props['y0']))

        x0.trace('w', onX0Change)
        y0.trace('w', onY0Change)

        Label(frame, text="  +  (").grid(column=0, row=0)
        x0Entry.grid(column=1, row=0)
        Label(frame, text="  +  ").grid(column=2, row=0)
        y0Entry.grid(column=3, row=0)
        Label(frame, text=" * i)").grid(column=4, row=0)

        frame.grid(column=7, row=0)

    def A(self):
        value = StringVar(self.frame)

        value.set(str(self.props['in_scale']))

        valEntry = Entry(self.frame, width=10, textvariable=value)

        valEntry.grid(column=9, row=0)

        def onChange(*args):
            try:
                val = value.get()
                if val != '':
                    self.props['A'] = float(val)
            except Exception:
                messagebox.showerror('Valor incorrecto', 'El valor de la amplitud debe ser un numero')
                value.set(str(self.props['A']))

        value.trace('w', onChange)
        return value
