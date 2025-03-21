"""
@author: original from Fernando Penaherrera and modified by Christoph Stucke, Malte Trauernicht, Kaja Petersen

"""
import pandas as pd
import numpy as np
import warnings



class WindTurbine(object):
    """
    Model of a simple wind turbine with a given power curve.
    """

    def __init__(self, rotor_area=None, max_power_mw=None, power_curve_file=None):
        """
        Model constructor

        rotor_area - swept area [m²]
        max_power_mw - max_power_mw [MW]
        power_curve_file - Power Curve CSV, see an example from: https://www.wind-turbine-models.com/turbines/550-enercon-e-82-e2-2.300 [accessed: 22.01.2025]
        """
        self.rotor_area = rotor_area
        self.max_power = max_power_mw
        self.power_curve = self.get_power_curve(power_curve_file)


    def get_power_curve(self, power_curve_file):
        """
        Get the data for the shape of the power curve.
        Normalizes the info and escalates to the rated power.
        """
        power_curve_data = pd.read_csv(power_curve_file)
        if "power_kw" in power_curve_data:
            power_curve_data["power"] = power_curve_data["power_kw"] * 0.001  # from kW to MW
        elif "power_mw" in power_curve_data:
            power_curve_data["power"] = power_curve_data["power_mw"]
        elif "power_factor" in power_curve_data:
            if self.rotor_area is not None:
                air_density = 1.19 # kg/m³ (25°C and ordinary atmospheric pressure)
                # basic formula for power output as a function of wind speed and turbine power-factor
                power_watt = 0.5 * power_curve_data["power_factor"] * air_density * self.rotor_area * power_curve_data["wind_speed"]**3
                power_curve_data["power"] = power_watt * 0.000001 # watt to MW
            elif self.max_power is not None:
                warnings.warn("Power-curve calculation based on power_factor and max_power_mw produces inaccurate results. Better results are achieved when rotor_area is used for calculation or when the power-curve is given with power-values.")
                max_rated_power = power_curve_data["power_factor"].max()
                power_curve_data["power"] = power_curve_data["power_factor"] / max_rated_power * self.max_power
            else:
                raise Exception("For power-curve calculation based on power_factor, either rotor_area or max_power_mw is required as input.")
        else:
            raise RuntimeError('No proper power curve data provided!')

        return power_curve_data


    def power_out(self, wind_speed):
        """
        Simple interpolation function to calculate the instant power using wind_speed [m/s]
        """
        x = self.power_curve["wind_speed"]
        y = self.power_curve["power"]
        return np.interp(wind_speed, x, y)


    def __repr__(self):
        """
        Print the turbine properties
        """
        max_rated_power = self.power_curve["power"].max()
        return f"Wind turbine:\n max_rated_power: {max_rated_power:.2f} MW\n rotor_area: {self.rotor_area} m²\n"



if __name__ == '__main__':
    wt = WindTurbine(rotor_area=5000)
    for i in range(0, 40):
        print(i, wt.power_out(i))
