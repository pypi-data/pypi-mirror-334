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
        ax: plt.Axes = fig.subplots(subplot_kw={"projection": "polar"})

        ax.set_theta_zero_location("S")
        ax.set_theta_direction(1)

        heat_analysis = StationaryHeatAnalysis(unit.roll)
        polar_angles = heat_analysis.polar_angles

        max_temp = float(np.max(unit.roll.temperature_field)) + 25

        for cooling_section in unit.roll.cooling_sections:
            theta1 = np.radians(cooling_section[0])
            theta2 = np.radians(cooling_section[1])

            ax.plot([theta1, theta1], [0, max_temp], color="blue", alpha=0.15)
            ax.plot([theta2, theta2], [0, max_temp], color="blue", alpha=0.15)

            theta_fill = np.linspace(theta1, theta2, 100)
            r_fill_outer = np.full_like(theta_fill, max_temp)
            r_fill_inner = np.zeros_like(theta_fill)
            ax.fill_between(theta_fill, r_fill_inner, r_fill_outer, color='blue', alpha=0.15, label="Active Cooling")





        ax.plot([unit.roll.entry_angle, unit.roll.entry_angle], [0, max_temp], color="red", alpha=0.15)
        ax.plot([unit.roll.exit_angle, unit.roll.exit_angle], [0, max_temp], color="red", alpha=0.15)

        theta_fill = np.linspace(unit.roll.entry_angle, unit.roll.exit_angle, 100)
        r_fill_outer = np.full_like(theta_fill, max_temp)
        r_fill_inner = np.zeros_like(theta_fill)
        ax.fill_between(theta_fill, r_fill_inner, r_fill_outer, color='red', alpha=0.15, label="Roll - Profile Contact")



        for i, radius in enumerate(heat_analysis.normed_radial_coordinates):
            angles = np.array(list(polar_angles))
            temp = np.array(list(unit.roll.temperature_field[i, :]), dtype=np.float64)
            ax.plot(angles, temp, label=f"Radius:{radius * unit.roll.min_radius}")

        angle = np.deg2rad(67.5)
        ax.legend(
            loc="lower left", bbox_to_anchor=(0.5 + np.cos(angle) / 2, 0.5 + np.sin(angle) / 2)
        )

        return fig