===========
mosaik-wind
===========

This package is a *mosaik* simulator for wind turbines. It uses wind speed data to calculate the power output of a wind turbine given a power curve.

Attributes:

* P[MW] - output attribute, generated active power [MW] (note that it was named *P_gen* in the old version)
* wind_speed - input attribute, wind speed [m/s]

Parameters:

* power_curve_file - a power curve file in .csv format that must be sutable for *pd.read_csv*, see CSV formatting section below. For an example of a power curve, see at: https://www.wind-turbine-models.com/turbines/550-enercon-e-82-e2-2.300
* rotor_area - swept area [m²]
* max_power_mw -  maximum rated power [MW]

The simulator entities can be configured using these parameters in two ways:

1. Calculating power using the power curve that is given as the instant power in kW or MW (*power_kw* or *power_mw*). In this case the power is interpolated based on given wind speed, see CSV formatting section below.
2. Calculating power using the wind turbine power formula and so called *power_factor* (*cp* or the coefficient of performance, see `also <https://x-engineer.org/wind-turbine-energy/>`_). In this case either the *rotor_area* or the *max_power_mw* of the turbine must be specified.    


Installation
============
* To use this project, you have to install at least version 3.4.0 of `mosaik <https://mosaik.offis.de/>`_
* It is recommended, to use the `mosaik_csv <https://gitlab.com/mosaik/components/data/mosaik-csv>`_ library to import wind data.

You can install this project through pip with the following command::

    pip install mosaik-wind


How to Use
==========
Note that one working example can be found in tests folder.

Specify simulators configurations within your scenario script::

    sim_config = {
        'CSV': {
            'python': 'mosaik_csv:CSV',
        },
        'Wind': {
            'python': 'mosaik_components.wind:Simulator'
        },
        ...
    }

Initialize the wind- and csv-simulator::

    wind_data = world.start("CSV",
                       sim_start='YYYY-MM-DD HH:mm:ss',
                       datafile='path/to/wind_speed/data.csv')

    wind_sim = world.start('Wind',
                        power_curve_file='path/to/power_curve/data.csv',
                        step_size=3600
                        gen_neg=True)

Instantiate model entities::

    wind_speed = wind_data.Wind()
    wind_model = wind_sim.WT()

Connect wind- with csv-simulator::

    world.connect(wind_speed, wind_model, 'wind_speed')


CSV-Formatting
==============

For the simulator to work correctly, both .csv files have to be specifically formatted!

wind-data
---------
Each row in the .csv needs a DateTime entry in the YYYY-MM-DD HH:mm:ss format and a *wind_speed* value, measured in meters per second.
The wind_data.csv is formatted accordingly to the conventions of the `mosaik_csv <https://gitlab.com/mosaik/components/data/mosaik-csv>`_ simulator::

    Wind
    Time,wind_speed
    YYYY-MM-DD HH:mm:ss,v1
    YYYY-MM-DD HH:mm:ss,v2
    ...


power-curve
-----------
Note that the entries for each data point require the *wind_speed* [m/s], as well as a corresponding *power_factor* or related power values *power_kw* [kW] or *power_mw* [MW].
The power-curve .csv does not need the *mosaik_csv* formatting::

    wind_speed,power_factor
    0,0
    1,0
    2,0.12
    3,0.29
    ...

    wind_speed,power_kw
    0,0
    3.5,100
    4.0,205
    4.5,355
    ...

    wind_speed,power_mw
    0,0
    3.5,0.1
    4.0,0.205
    4.5,0.355
    ...

