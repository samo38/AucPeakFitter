import numpy as np
import lmfit
import copy
import data_models as dms


def get_y_x(x_arr: np.array, y_arr: np.array, x):
    wh_1 = np.where(x_arr >= x)[0]
    wh_2 = np.where(x_arr <= x)[0]
    if len(wh_1) > 0:
        id_1 = wh_1[0]
    else:
        id_1 = None
    if len(wh_2) > 0:
        id_2 = wh_2[-1]
    else:
        id_2 = None
    if (id_1 is not None) and (id_2 is not None):
        if id_1 == id_2:
            return x_arr[id_1], y_arr[id_1]
        else:
            xx = 0.5 * (x_arr[id_1] + x_arr[id_2])
            yy = 0.5 * (y_arr[id_1] + y_arr[id_2])
            return xx, yy
    elif id_1 is not None:
        return x_arr[id_1], y_arr[id_1]
    elif id_2 is not None:
        return x_arr[id_2], y_arr[id_2]
    else:
        return None


class FitModel:

    def __init__(self, data_model: dms.DataModel):
        self.data_model = copy.deepcopy(data_model)

        self.parameters = lmfit.Parameters()
        self.prefix = []
        list_models = self._make_params()
        self.model = list_models[0]
        for i in range(1, len(list_models)):
            self.model = self.model + list_models[i]
        self.init = self.model.eval(self.parameters, x=self.data_model.data.x_trim)
        self.fit = self.model.fit(self.data_model.data.y_trim, self.parameters, x=self.data_model.data.x_trim)

    def _make_params(self):
        x = self.data_model.data.x_trim
        y = self.data_model.data.y_trim
        list_models = []
        sigma_bound_state = False
        sigma_bound_name = None
        for i in range(len(self.data_model.model)):
            func = self.data_model.model[i]
            # func = dms.Function(dms.Types.GAUSS)
            if not func.visible:
                continue
            if func.type == dms.Types.EXP:
                pref = 'exp_'
                self.prefix.append(pref)
                exp = lmfit.models.ExponentialModel(prefix=pref)
                self.parameters.update(exp.guess(y, x=x))
                list_models.append(exp)
            elif func.type == dms.Types.GAUSS:
                pref = f"gauss{i}_"
                self.prefix.append(pref)
                gauss = lmfit.models.GaussianModel(prefix=pref)
                self.parameters.update(gauss.make_params())
                cent_vary = not func.gauss.center.fixed
                sigma_vary = not func.gauss.sigma.fixed
                amplitude_vary = not func.gauss.amplitude.fixed

                expression = None
                if func.gauss.sigma.bound:
                    if sigma_bound_state:
                        expression = f"{sigma_bound_name}sigma"
                    else:
                        sigma_bound_state = True
                        sigma_bound_name = pref

                cent_val = func.gauss.center.value
                cent_min = func.gauss.center.min
                cent_max = func.gauss.center.max

                if sigma_vary:
                    sigma = np.std(x[np.logical_and(x >= cent_min, x <= cent_max)])
                else:
                    sigma = func.gauss.sigma.value
                if amplitude_vary:
                    interp = get_y_x(x, y, cent_val)
                    amplitude = 0.001
                    if interp is not None:
                        xx = interp[0]
                        yy = interp[1]
                        amplitude = (yy * sigma * np.sqrt(2 * np.pi)) / np.exp(-0.5 * ((xx - cent_val) / sigma) ** 2)
                else:
                    amplitude = func.gauss.amplitude.value

                self.parameters[pref + 'center'].set(value=cent_val, min=cent_min, max=cent_max, vary=cent_vary)
                if expression is None:
                    self.parameters[pref + 'sigma'].set(value=sigma, min=sigma / 100, vary=sigma_vary)
                else:
                    self.parameters[pref + 'sigma'].set(value=sigma, min=sigma / 100, vary=sigma_vary, expr=expression)
                self.parameters[pref + 'amplitude'].set(value=amplitude, min=1e-5, vary=amplitude_vary)
                list_models.append(gauss)
        return list_models

    def eval_components(self, n_points=500):
        x1 = self.data_model.data.x_trim[0]
        x2 = self.data_model.data.x_trim[-1]
        x_arr = np.linspace(x1, x2, n_points)
        self.data_model.data.x_model = x_arr
        components = self.fit.eval_components(x=x_arr)
        components_0 = self.fit.eval_components(x=self.data_model.data.x_trim)
        y_model = []
        yy = np.zeros(len(x_arr), dtype=np.float)
        yy_0 = np.zeros(len(self.data_model.data.x_trim), dtype=np.float)
        n = 0
        for i in range(len(self.data_model.model)):
            func = self.data_model.model[i]
            # func = dms.Function(dms.Types.GAUSS)
            if not func.visible:
                y_model.append(None)
            else:
                y_comp = components[self.prefix[n]]
                yy += y_comp
                yy_0 += components_0[self.prefix[n]]
                n += 1
                y_model.append(y_comp)
        y_model.append(yy)
        self.data_model.data.y_model = y_model
        self.data_model.data.residual = yy_0 - self.data_model.data.y_trim

    def get_data_model(self):
        return copy.deepcopy(self.data_model)


