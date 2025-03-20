import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

from pyroll.report import hookimpl
from pyroll.core import Unit
from pyroll.core import RollPass



from .stationary_heat_analysis import StationaryHeatAnalysis

@hookimpl(specname="unit_plot")
def roll_temperature_field_plot(unit: Unit):
    if isinstance(unit, RollPass):
        fig: plt.Figure = plt.figure()
        axl: plt.Axes
        ax, axl = fig.subplots(nrows=2, subplot_kw={"projection": "polar"}, height_ratios=[1, 0.15])
        ax.set_theta_zero_location("S")

        heat_analysis = StationaryHeatAnalysis(unit.roll)
        polar_angles = heat_analysis.polar_angles

        max_temp = float(np.max(unit.roll.temperature_field)) + 25

        for cooling_section in unit.roll.cooling_sections:
            theta1 = np.radians(cooling_section[0])
            theta2 = np.radians(cooling_section[1])

            cooling_1 = ax.plot([theta1, theta1], [0, max_temp], color="blue", alpha=0.15, label="Active Cooling")
            cooling_2 = ax.plot([theta2, theta2], [0, max_temp], color="blue", alpha=0.15, label="Active Cooling")

            theta_fill = np.linspace(theta1, theta2, 100)
            r_fill_outer = np.full_like(theta_fill, max_temp)
            r_fill_inner = np.zeros_like(theta_fill)
            cooling_fill = ax.fill_between(theta_fill, r_fill_inner, r_fill_outer, color='blue', alpha=0.15, label="Active Cooling")





        heating_1 = ax.plot([unit.roll.entry_angle, unit.roll.entry_angle], [0, max_temp], color="red", alpha=0.15, label="Roll - Profile Contact")
        heating_2 = ax.plot([unit.roll.exit_angle, unit.roll.exit_angle], [0, max_temp], color="red", alpha=0.15, label="Roll - Profile Contact")

        theta_fill = np.linspace(unit.roll.entry_angle, unit.roll.exit_angle, 100)
        r_fill_outer = np.full_like(theta_fill, max_temp)
        r_fill_inner = np.zeros_like(theta_fill)
        heat_fill = ax.fill_between(theta_fill, r_fill_inner, r_fill_outer, color='red', alpha=0.15, label="Roll - Profile Contact")


        plots= []
        for i, radius in enumerate(heat_analysis.normed_radial_coordinates):
            angles = np.array(list(polar_angles))
            temp = np.array(list(unit.roll.temperature_field[i, :]), dtype=np.float64)
            temp_plot = ax.plot(angles, temp, label=f"Radius:{radius * unit.roll.min_radius}")
            plots.append(temp_plot)

        axl.axis("off")
        axl.legend(handles=plots[0] + plots[1] + cooling_1 + heating_1, ncols=2, loc="lower center")

        return fig