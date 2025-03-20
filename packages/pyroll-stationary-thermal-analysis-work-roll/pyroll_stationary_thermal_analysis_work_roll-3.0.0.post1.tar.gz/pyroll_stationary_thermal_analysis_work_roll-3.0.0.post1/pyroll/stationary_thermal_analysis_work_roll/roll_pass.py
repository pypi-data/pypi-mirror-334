from pyroll.core import SymmetricRollPass, Hook, root_hooks


SymmetricRollPass.average_heat_flux = Hook[float]()
"""Heat Flux inside the RollPass from Profile to the Roll."""

@SymmetricRollPass.average_heat_flux
def average_heat_flux(self: SymmetricRollPass):
    mean_temperature = (self.in_profile.temperature + self.out_profile.temperature) / 2

    return self.roll.heat_transfer_coefficient * (mean_temperature - self.roll.temperature)


root_hooks.append(SymmetricRollPass.average_heat_flux)
