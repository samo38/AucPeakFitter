import numpy as np
import enum
import copy


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


class Exponential:

    def __init__(self):
        self.amplitude = Params()
        self.decay = Params()
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

    def set_xy(self, x: np.array, y: np.array):
        if self.type == Types.GAUSS:
            self.exp.x = None
            self.exp.y = None
            self.gauss.x = x
            self.gauss.y = y
        elif self.type == Types.EXP:
            self.exp.x = x
            self.exp.y = y
            self.gauss.x = None
            self.gauss.y = None

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
            model_out.append(gauss_model[i])
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

        self.name_list = name_list
        self.model = model_out

    def set_model(self, model: list):
        self.model = model
        self.sort_centers()

    def clear_modeled(self):
        self.data.y_model = None
        self.data.y_model = None
        self.data.residual = None
        for i in range(len(self.model)):
            self.model[i].clear_xy()


