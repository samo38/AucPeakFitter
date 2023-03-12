import numpy as np
import enum
import copy

N_POINTS = 2000


class Types(enum.Enum):
    EMPTY = 0
    GAUSS = 1
    EXP = 2


class Params:

    def __init__(self):
        self.fixed = False
        self.value = None
        self.min = None
        self.max = None
        self.bound = False


class Gaussian:

    def __init__(self):
        self.amplitude = Params()
        self.center = Params()
        self.sigma = Params()
        self.x = None
        self.y = None

    def reset_xy(self, x=None):
        if x is None:
            self.x = None
            self.y = None
        amp = self.amplitude.value
        cen = self.center.value
        sig = self.sigma.value
        b1 = amp is not None
        b2 = cen is not None
        b3 = sig is not None
        if b1 and b2 and b3:
            self.x = x
            y = (amp / (sig * np.sqrt(2 * np.pi)))
            y *= np.exp(-1 * (x - cen) ** 2 / (2 * sig ** 2))
            self.y = y
        else:
            self.x = None
            self.y = None


class Exponential:

    def __init__(self):
        self.amplitude = Params()
        self.decay = Params()
        self.x = None
        self.y = None

    def reset_xy(self, x=None):
        if x is None:
            self.x = None
            self.y = None
        amp = self.amplitude.value
        dec = self.decay.value
        b1 = amp is not None
        b2 = dec is not None
        if b1 and b2:
            self.x = x
            self.y = amp * np.exp(-1 * x / dec)
        else:
            self.x = None
            self.y = None


class Function:

    def __init__(self, t: enum.Enum):
        self.type = t
        self.name = ''
        self.visible = True
        self.gauss = Gaussian()
        self.exp = Exponential()

    def clear_xy(self):
        self.gauss.x = None
        self.gauss.y = None
        self.exp.x = None
        self.exp.y = None

    def reset_xy(self, x: np.array):
        if self.type == Types.GAUSS:
            self.exp.reset_xy()
            self.gauss.reset_xy(x)
        elif self.type == Types.EXP:
            self.exp.reset_xy(x)
            self.gauss.reset_xy()

    def get_xy(self):
        if self.type == Types.GAUSS:
            return self.gauss.x, self.gauss.y
        elif self.type == Types.EXP:
            return self.exp.x, self.exp.y


class Data:

    def __init__(self):
        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None
        self.x_model = None
        self.y_model = None
        self.residual = None

    def set_raw(self, x: np.array, y: np.array):
        self.x_raw = x
        self.y_raw = y

    def set_trim(self, x: np.array, y: np.array):
        self.x_trim = x
        self.y_trim = y
        self.x_model = np.linspace(x[0], x[-1], N_POINTS)
        self.y_model = np.zeros(N_POINTS, dtype=np.float)
        self.residual = None


class DataModel:

    def __init__(self):
        self.data = Data()
        self.model = []
        self.name_list = []
        self.next_index = 1

    def sort_centers(self):
        if len(self.model) == 0:
            return
        exp_model = None
        for i in range(len(self.model)):
            func = self.model[i]
            if func.type == Types.EXP:
                exp_model = copy.deepcopy(func)
                if exp_model.visible:
                    exp_model.name = "Buffer"
                else:
                    exp_model.name = "**Buffer**"
                break

        gauss_model = []
        cent_vals = []
        for i in range(len(self.model)):
            # func = dms.Function(dms.Types.GAUSS)
            func = self.model[i]
            if func.type == Types.GAUSS:
                tf = copy.deepcopy(func)
                cent_vals.append(tf.gauss.center.value)
                gauss_model.append(tf)

        cent_vals = np.array(cent_vals)
        arg_sort = np.argsort(cent_vals)
        model_out = []
        for i in arg_sort:
            func = copy.deepcopy(gauss_model[i])
            model_out.append(func)
        name_list = []
        for i in range(len(model_out)):
            if model_out[i].visible:
                name = f"Species {i + 1}"
                model_out[i].name = name
            else:
                name = f"**Species {i + 1}**"
                model_out[i].name = name
            if model_out[i].gauss.sigma.bound:
                name += " - bound"
            name_list.append(name)
        if exp_model is not None:
            if len(model_out) > 0:
                model_out = [exp_model] + model_out
                name_list = [exp_model.name] + name_list
            else:
                model_out = [exp_model]
                name_list = [exp_model.name]

        self.name_list.clear()
        self.name_list = name_list
        self.model.clear()
        self.model = model_out

    def set_model(self, model: list):
        self.model = copy.deepcopy(model)
        self.sort_centers()

    def clear_modeled(self):
        self.data.y_model = None
        self.data.y_model = None
        self.data.residual = None
        for i in range(len(self.model)):
            self.model[i].clear_xy()

    def reset_y_models(self):
        xx = self.data.x_model
        yy = np.zeros(len(xx), dtype=np.float)
        if xx is None:
            return
        for func in self.model:
            # func = Function()
            func.reset_xy(xx)
            xf, yf = func.get_xy()
            yy += yf
        self.data.y_model = yy

    def reset_residual(self, y=None):
        if y is None:
            self.data.residual = None
        else:
            self.data.residual = y - self.data.y_trim
