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
        self.main = False
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
            self.y = Gaussian.get_fx(x, amp, sig, cen)
        else:
            self.x = None
            self.y = None

    @staticmethod
    def get_fx(x, amplitude, sigma, center):
        y = (amplitude / (sigma * np.sqrt(2 * np.pi)))
        y *= np.exp(-1 * (x - center) ** 2 / (2 * sigma ** 2))
        return y


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
            self.y = Exponential.get_fx(x, amp, dec)
        else:
            self.x = None
            self.y = None

    @staticmethod
    def get_fx(x, amplitude, decay):
        return amplitude * np.exp(-1 * x / decay)


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
            if self.visible:
                self.gauss.reset_xy(x)
            else:
                self.gauss.reset_xy()
        elif self.type == Types.EXP:
            if self.visible:
                self.exp.reset_xy(x)
            else:
                self.exp.reset_xy()
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
        self.y_model = None
        self.residual = None

    def set_raw(self, x: np.array, y: np.array):
        self.x_raw = x
        self.y_raw = y

    def set_trim(self, x: np.array, y: np.array):
        self.x_trim = x
        self.y_trim = y
        self.y_model = None
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
        self.next_index = 1
        for i in range(len(self.model)):
            # func = dms.Function(dms.Types.GAUSS)
            func = self.model[i]
            if func.type == Types.GAUSS:
                tf = copy.deepcopy(func)
                cent_vals.append(tf.gauss.center.value)
                gauss_model.append(tf)
                self.next_index += 1

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
        x1 = self.data.x_trim[0]
        x2 = self.data.x_trim[-1]
        x = self.data.x_trim
        xx = np.linspace(x1, x2, N_POINTS)
        y = np.zeros(len(x), dtype=np.float)
        model = False
        for func in self.model:
            # func = Function()
            func.reset_xy(xx)
            if not func.visible:
                continue
            if func.type == Types.GAUSS:
                amp = func.gauss.amplitude.value
                sig = func.gauss.sigma.value
                cen = func.gauss.center.value
                y += Gaussian.get_fx(x, amp, sig, cen)
                model = True
            elif func.type == Types.EXP:
                amp = func.exp.amplitude.value
                dec = func.exp.decay.value
                y += Exponential.get_fx(x, amp, dec)
                model = True
        if model:
            self.data.y_model = y
            self.data.residual = y - self.data.y_trim
        else:
            self.data.y_model = None
            self.data.residual = None
