import numpy as np


class Gaussian:

    def __init__(self, arr: np.array):
        self.amplitude = arr[0]
        self.center = arr[1]
        self.sigma = arr[2]


class Exponential:

    def __init__(self, arr: np.array):
        self.amplitude = arr[0]
        self.decay = arr[1]


class Model:

    def __init__(self):
        self.type = None
        self.coefficients = None

    def set_model(self, t: str, arr: np.array):
        if t == "GAUSS" and len(arr) == 3:
            self.type = t
            self.coefficients = Gaussian(arr)
        elif t == "EXP" and len(arr) == 2:
            self.type = t
            self.coefficients = Exponential(arr)


class DataModels:

    def __init__(self):
        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None
        self.has_models = False
        self.has_raw = False
        self.has_trim = False
        self.models = []

    def set_raw(self, x: np.array, y: np.array):
        self.x_raw = x
        self.y_raw = y
        self.has_raw = True

    def set_trim(self, x: np.array, y: np.array):
        self.x_trim = x
        self.y_trim = y
        self.has_trim = True

    def append_model(self, model: Model):
        if model.type is not None:
            self.models.append(model)
            self.has_models = True

    def clear(self):
        self.x_trim = None
        self.y_trim = None
        self.has_trim = False
        self.models = []
        self.has_models = False
