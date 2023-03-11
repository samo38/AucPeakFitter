import numpy as np
import scipy as sp
import lmfit
import copy
import data_models as dms


def get_exponential(x_arr, amplitude, decay):
    return amplitude * np.exp(-1 * x_arr / decay)


def get_gaussian(x_arr, amplitude, sigma, center):
    return (amplitude / (sigma * np.sqrt(2 * np.pi))) * np.exp(-1 * (x_arr - center) ** 2 / (2 * sigma ** 2))


class FitModel:

    def __init__(self, data_model: dms.DataModel):
        self.data_model = copy.deepcopy(data_model)
        self.fit = None
        self.prefix = []

    def _guess_init(self):
        yy = copy.deepcopy(self.data_model.data.y_trim)
        xx = copy.deepcopy(self.data_model.data.x_trim)
        for i in range(len(self.data_model.model)):
            func = self.data_model.model[i]
            # func = dms.Function(dms.Types.GAUSS)
            if not func.visible:
                continue
            if func.type == dms.Types.EXP:
                if func.exp.amplitude.value is None or func.exp.decay.value is None:
                    pref = 'exp_'
                    self.prefix.append(pref)
                    exp = lmfit.models.ExponentialModel(prefix=pref)
                    params = exp.guess(yy, x=xx)
                    decay_i = params.get('exp_decay').value
                    amplitude_i = params.get('exp_amplitude').value
                    y_exp = amplitude_i * np.exp(-1 * xx / decay_i)
                    yy -= y_exp
                    func.exp.amplitude.value = amplitude_i
                    func.exp.decay.value = decay_i
            elif func.type == dms.Types.GAUSS:
                cent_val = func.gauss.center.value
                cent_min = func.gauss.center.min
                cent_max = func.gauss.center.max
                if func.gauss.sigma.value is None:
                    sigma_i = np.std(xx[np.logical_and(xx >= cent_min, xx <= cent_max)])
                    func.gauss.sigma.value = sigma_i
                if func.gauss.amplitude.value is None:
                    sigma_i = func.gauss.sigma.value
                    f = sp.interpolate.interp1d(xx, yy)
                    y_cent_val = f(cent_val)
                    amplitude_i = (y_cent_val * sigma_i * np.sqrt(2 * np.pi))
                    func.gauss.amplitude.value = amplitude_i
                    y_gauss = (amplitude_i / (sigma_i * np.sqrt(2 * np.pi)))
                    y_gauss *= np.exp(-1 * (xx - cent_val) ** 2 / (2 * sigma_i ** 2))
                    yy -= y_gauss

    def _build_model(self, params):
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
                # params.update(exp.guess(y, x=x))
                params.update(exp.make_params())
                list_models.append(exp)
                amplitude = func.exp.amplitude.value
                amplitude_vary = not func.exp.amplitude.fixed
                decay = func.exp.decay.value
                decay_vary = not func.exp.decay.fixed
                params[pref + 'amplitude'].set(value=amplitude, vary=amplitude_vary)
                params[pref + 'decay'].set(value=decay, vary=decay_vary)
            elif func.type == dms.Types.GAUSS:
                pref = f"gauss{i}_"
                self.prefix.append(pref)
                gauss = lmfit.models.GaussianModel(prefix=pref)
                params.update(gauss.make_params())
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
                sigma = func.gauss.sigma.value
                amplitude = func.gauss.amplitude.value

                params[pref + 'center'].set(value=cent_val, min=cent_min, max=cent_max, vary=cent_vary)
                if expression is None:
                    params[pref + 'sigma'].set(value=sigma, min=sigma / 100, vary=sigma_vary)
                else:
                    params[pref + 'sigma'].set(value=sigma, min=sigma / 100, vary=sigma_vary, expr=expression)
                params[pref + 'amplitude'].set(value=amplitude, min=1e-6, vary=amplitude_vary)
                list_models.append(gauss)
        return list_models

    def _final_values(self):
        x1 = self.data_model.data.x_trim[0]
        x2 = self.data_model.data.x_trim[-1]
        x_trim = self.data_model.data.x_trim
        xx = np.linspace(x1, x2, 1500)
        yy_mod = np.zeros(len(xx), dtype=np.float)
        yy_err = np.zeros(len(x_trim), dtype=np.float)
        params = self.fit.params
        new_model = []
        for i in range(len(self.data_model.model)):
            func = copy.deepcopy(self.data_model.model[i])
            # func = dms.Function(dms.Types.GAUSS)
            if func.type == dms.Types.EXP:
                if func.visible:
                    pref = 'exp_'
                    amplitude = params.get(pref + "amplitude")
                    decay = params.get(pref + "decay")
                    func.exp.amplitude.value = amplitude.value
                    func.exp.decay.value = decay.value
                    yy = get_exponential(xx, amplitude.value, decay.value)
                    func.set_xy(xx, yy)
                    yy_mod += yy
                    yy_err += get_exponential(x_trim, amplitude.value, decay.value)
                else:
                    func.clear_xy()
            elif func.type == dms.Types.GAUSS:
                if func.visible:
                    pref = f"gauss{i}_"
                    amplitude = params.get(pref + "amplitude")
                    center = params.get(pref + "center")
                    sigma = params.get(pref + "sigma")
                    func.gauss.amplitude.value = amplitude.value
                    func.gauss.center.value = center.value
                    func.gauss.sigma.value = sigma.value
                    yy = get_gaussian(xx, amplitude.value, sigma.value, center.value)
                    func.set_xy(xx, yy)
                    yy_mod += yy
                    yy_err += get_gaussian(x_trim, amplitude.value, sigma.value, center.value)
                else:
                    func.clear_xy()
            new_model.append(func)
        self.data_model.set_model(new_model)
        self.data_model.data.y_model = yy_mod
        self.data_model.data.x_model = xx
        self.data_model.data.residual = yy_err - self.data_model.data.y_trim

    def init_fit(self):
        self._guess_init()
        parameters = lmfit.Parameters()
        list_models = self._build_model(parameters)
        if len(list_models) == 0:
            return
        tot_models = list_models[0]
        for i in range(1, len(list_models)):
            tot_models += list_models[i]
        self.fit = tot_models.fit(self.data_model.data.y_trim, parameters, x=self.data_model.data.x_trim)
        self._final_values()

    def get_data_model(self):
        return copy.deepcopy(self.data_model)


