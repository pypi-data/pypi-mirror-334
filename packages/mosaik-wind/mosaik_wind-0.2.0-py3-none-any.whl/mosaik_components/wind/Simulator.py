"""
@author: original from Fernando Penaherrera,
modified by Christoph Stucke, Malte Trauernicht, Kaja Petersen and Danila Valko

"""
import mosaik_api_v3 as mosaik_api
import mosaik_components.wind.WindTurbine as WindTurbine
import itertools

meta = {
    'models': {
        'WT': {
            'public': True,
            'params': [  # Define the parameters of the related class
                'rotor_area',  # swept area [m²]
                'max_power_mw',  # max rated power [MW]
                'power_curve_file', # power curve CSV file, see an example from: https://www.wind-turbine-models.com/turbines/550-enercon-e-82-e2-2.300 [accessed: 22.01.2025]
            ],
            'attrs': ['P[MW]',  # generated instant power [MW]
                      'wind_speed',  # instant wind speed [m/s]
            ]
        }
    }
}


class Simulator(mosaik_api.Simulator):
    """
    Simulator for the wind turbine
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__(meta)  # Initialise the inherited simulator
        self.sid = None
        self.gen_neg = False
        self.step_size = None
        self.cache = {}
        self._entities = {}
        self.eid_counters = {'WT': itertools.count()}
        self.power_curve_file = None
        

    def init(self, sid, time_resolution=1., power_curve_file=None, step_size=None, gen_neg=False):
        self.sid = sid
        self.power_curve_file = power_curve_file
        self.step_size = step_size
        self.gen_neg = gen_neg
        return self.meta


    def create(self, num, model, **model_params):
        entities = []
        model_params.setdefault('rotor_area', None)
        model_params.setdefault('max_power_mw', None)
        model_params.setdefault('power_curve_file', self.power_curve_file)

        if model_params['power_curve_file'] is None:
            raise RuntimeError('No power curve data provided! Consider defining the power_curve_file parameter in init() or create().')

        for i in range(num):
            eid = '%s-%s' % (model, next(self.eid_counters.get('WT')))
            self._entities[eid] = WindTurbine.WindTurbine(**model_params)
            entities.append({'eid': eid, 'type': model, 'rel': []})
        return entities


    def step(self, time, inputs, max_advance):
        self.cache = {}
        for eid, attrs in inputs.items():
            for attr, vals in attrs.items():
                if attr == "wind_speed":
                    self.cache[eid] = self._entities[eid].power_out(sum(vals.values()))
                    if self.gen_neg:
                        self.cache[eid] *= -1
        return time + self.step_size


    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            if eid not in self._entities.keys():
                raise ValueError(f"Unknown entity ID {eid}")

            data[eid] = {}
            for attr in attrs:
                if attr != "P[MW]":
                    raise ValueError(f"Unknown output attribute {attr}")
                data[eid][attr] = self.cache[eid]
        return data


def main():
    mosaik_api.start_simulation(Simulator(), "Simulator")


if __name__ == '__main__':
    main()
