import numpy as np


class Params:

    def __init__(self):
        self.fixed = None
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

    def __init__(self, t: str):
        if t == "GAUSS":
            self.type = t
            self.params = Gaussian()
        elif t == "EXP":
            self.type = t
            self.params = Exponential()
        self.name = ''


class DataModels:

    def __init__(self):
        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None
        self.models = []
        self.optimized = False

    def set_raw(self, x: np.array, y: np.array):
        self.x_raw = x
        self.y_raw = y

    def set_trim(self, x: np.array, y: np.array):
        self.x_trim = x
        self.y_trim = y

    def append_model(self, model: Model):
        if model.type is not None:
            self.models.append(model)

    def set_model(self, n: int, model: Model):
        if model.type is not None:
            self.models[n] = model

    def clear(self):
        self.x_trim = None
        self.y_trim = None
        self.models = []
