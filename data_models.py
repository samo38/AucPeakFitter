import numpy as np
import enum


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


class Exponential:

    def __init__(self):
        self.amplitude = Params()
        self.decay = Params()


class Model:

    def __init__(self, t: enum.Enum):
        if t == Types.EMPTY:
            self.params = None
        elif t == Types.GAUSS:
            self.params = Gaussian()
        elif t == Types.EXP:
            self.params = Exponential()
        else:
            raise IOError("input value not exist!")
        self.type = t
        self.name = ''
        self.visible = True


class Data:

    def __init__(self):
        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None

    def set_raw(self, x: np.array, y: np.array):
        self.x_raw = x
        self.y_raw = y

    def set_trim(self, x: np.array, y: np.array):
        self.x_trim = x
        self.y_trim = y


class DataModels:

    def __init__(self):
        self.data = Data()
        self.models = []
        self.optimized = False

    def append_model(self, model: Model):
        if model.type != Types.EMPTY:
            self.models.append(model)

    def set_model(self, n: int, model: Model):
        if model.type != Types.EMPTY:
            self.models[n] = model

    def get_model(self, n: int):
        return self.models[n]

    def set_data(self, data: Data):
        self.data = data

    def get_data(self):
        return self.data

    def clear(self):
        self.data = Data()
        self.models = []
