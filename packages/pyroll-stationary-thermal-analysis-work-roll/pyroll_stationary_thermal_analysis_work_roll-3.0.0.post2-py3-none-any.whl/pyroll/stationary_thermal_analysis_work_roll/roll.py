from typing import List

from pyroll.core import Roll, Hook, root_hooks
from .stationary_heat_analysis import StationaryHeatAnalysis

Roll.peclet_number = Hook[float]()
"""Peclet number of the roll."""

Roll.cooling_sections = Hook[List[float]]()
"""Cooling sections of the roll."""

Roll.coolant_heat_transfer_coefficient = Hook[float]()
"""Heat Transfer coefficient of the coolant."""

Roll.free_surface_heat_transfer_coefficient = Hook[float]()
"""Heat Transfer coefficient of the coolant."""

Roll.heat_transfer_coefficient = Hook[float]()
"""Heat Transfer coefficient between roll and profile."""

Roll.coolant_temperature = Hook[float]()
"""Temperature of the coolant."""

Roll.temperature_field = Hook[float]()
"""Temperature field inside the roll."""


@Roll.peclet_number
def peclet_number(self: Roll):
    return (self.surface_velocity * self.min_radius ** 2) / self.thermal_diffusivity

@Roll.coolant_heat_transfer_coefficient
def default_water(self: Roll):
    return 15000

@Roll.heat_transfer_coefficient
def default_steel_steel(self: Roll):
    return 6000

@Roll.free_surface_heat_transfer_coefficient
def default_air(self: Roll):
    return 15

@Roll.coolant_temperature
def default_water(self: Roll):
    return 35 + 273.15

@Roll.temperature_field
def temperature_field(self: Roll):
    heat_analysis = StationaryHeatAnalysis(self)
    temperature_field = heat_analysis.solve()
    return temperature_field

root_hooks.append(Roll.peclet_number)