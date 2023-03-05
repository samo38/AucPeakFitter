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


class Function:

    def __init__(self, t: enum.Enum):
        self.type = t
        self.name = ''
        self.visible = True
        self.gauss = Gaussian()
        self.exp = Exponential()


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
        self.next_index = 1
        self.optimized = False

    def append_model(self, model: Function):
        if model.type != Types.EMPTY:
            self.model.append(model)

    def set_model(self, n: int, model: Function):
        if model.type != Types.EMPTY:
            self.model[n] = model

    def get_model(self, n: int):
        return self.model[n]

    def set_data(self, data: Data):
        self.data = data

    def get_data(self):
        return self.data

    def clear(self):
        self.data = Data()
        self.model = []
