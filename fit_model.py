import numpy as np
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

    def _build_model(self, params):
        x = self.data_model.data.x_trim
        y = self.data_model.data.y_trim
        main_peak = None
        for i in range(len(self.data_model.model)):
            func = self.data_model.model[i]
            if func.type == dms.Types.GAUSS and func.visible and func.gauss.main:
                main_peak = f"gauss{i}_sigma"
                break

        list_models = []
        for i in range(len(self.data_model.model)):
            func = self.data_model.model[i]
            if not func.visible:
                continue
            if func.type == dms.Types.EXP:
                pref = 'exp_'
                self.prefix.append(pref)
                exp = lmfit.models.ExponentialModel(prefix=pref)
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
                cent_val = func.gauss.center.value
                cent_min = func.gauss.center.min
                cent_max = func.gauss.center.max
                sigma = func.gauss.sigma.value
                amplitude = func.gauss.amplitude.value

                params[pref + 'center'].set(value=cent_val, min=cent_min, max=cent_max, vary=cent_vary)
                if func.gauss.sigma.bound:
                    params[pref + 'sigma'].set(vary=False, expr=main_peak)
                else:
                    params[pref + 'sigma'].set(value=sigma, min=sigma / 100, vary=sigma_vary)
                params[pref + 'amplitude'].set(value=amplitude, min=1e-4, vary=amplitude_vary)
                list_models.append(gauss)
        return list_models

    def _final_values(self):
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
                else:
                    func.clear_xy()
            new_model.append(func)
        self.data_model.set_model(new_model)
        self.data_model.reset_y_models()

    def init_fit(self):
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


