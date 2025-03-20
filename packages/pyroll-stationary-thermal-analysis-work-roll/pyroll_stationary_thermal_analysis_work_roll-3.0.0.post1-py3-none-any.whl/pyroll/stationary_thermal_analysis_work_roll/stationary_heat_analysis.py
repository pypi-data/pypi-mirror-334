import numpy as np
import mpmath as mp
import pyroll.core as pr

from scipy.integrate import trapezoid

mp.dps = 50


class StationaryHeatAnalysis:
    def __init__(self, roll: pr.RollPass.Roll):
        self.roll = roll
        self.roll_pass = self.roll.roll_pass
        self.number_of_fourier_terms = 141
        self.angular_discretization = 360
        self.radial_discretization = 2
        self.reference_temperature = 1 + 273.15
        self.polar_angles = mp.linspace(0, 2 * np.pi, self.angular_discretization, endpoint=True)
        self.fourier_orders = mp.linspace((-self.number_of_fourier_terms + 1) / 2,
                                          (self.number_of_fourier_terms + 1) / 2,
                                          self.number_of_fourier_terms,
                                          endpoint=False)
        self.radial_coordinates = mp.linspace(0.985 * self.roll.min_radius, self.roll.min_radius, self.radial_discretization)
        self.normed_radial_coordinates = [radial_coordinate / self.roll.min_radius for radial_coordinate in self.radial_coordinates]
        self.normed_cooling_array = mp.zeros(self.angular_discretization, 1)
        self.normed_heating_array = mp.zeros(self.angular_discretization, 1)

    def create_diagonal_matrix(self):
        fourier_coefficients = mp.zeros(self.number_of_fourier_terms, 1)
        diag_matrix = mp.matrix(self.number_of_fourier_terms, self.number_of_fourier_terms)
        reciprocate_peclet = 1 / self.roll.peclet_number

        for i, fourier_order in enumerate(self.fourier_orders):
            bessel_function_argument_at_surface = (
                    mp.sqrt(-mp.j * fourier_order) * 1 / mp.sqrt(reciprocate_peclet)
            )

            numerator = mp.besselj(
                fourier_order, bessel_function_argument_at_surface, derivative=1
            )
            denominator = mp.besselj(fourier_order, bessel_function_argument_at_surface)

            fourier_coefficients[i] = (
                    bessel_function_argument_at_surface * numerator / denominator
            )

        for i in range(self.number_of_fourier_terms):
            diag_matrix[i, i] = fourier_coefficients[i]

        return diag_matrix

    def create_hermitian_matrix_from_cooling_array(self, cooling_fourier_coefficients):
        middle_index = self.number_of_fourier_terms // 2
        hermitian_matrix = mp.matrix(self.number_of_fourier_terms, self.number_of_fourier_terms)

        for i in range(self.number_of_fourier_terms):
            for j in range(self.number_of_fourier_terms):
                index = middle_index + (j - i)
                if 0 <= index < self.number_of_fourier_terms:
                    hermitian_matrix[i, j] = cooling_fourier_coefficients[index]
                else:
                    hermitian_matrix[i, j] = mp.conj(hermitian_matrix[j, i])

        return hermitian_matrix

    def complex_fourier_analysis(self, array):
        fourier_coefficients = mp.zeros(self.number_of_fourier_terms, 1)

        integrand = mp.zeros(self.number_of_fourier_terms, self.angular_discretization)

        for i, order in enumerate(self.fourier_orders):
            for j, angle in enumerate(self.polar_angles):
                integrand[i, j] = array[j] * mp.exp(-mp.j * order * angle)

        integrand_array = np.array(integrand.tolist(), dtype=complex)

        for i, order in enumerate(self.fourier_orders):
            fourier_coefficients[i, 0] = (
                    1 / (2 * mp.pi) * trapezoid(y=integrand_array[i], x=self.polar_angles, dx=1)
            )
        return fourier_coefficients

    def temperature_fourier_analysis(self):
        coefficients = mp.matrix(self.radial_discretization, self.number_of_fourier_terms)
        reciprocate_peclet = 1 / self.roll.peclet_number

        for i, radius in enumerate(self.normed_radial_coordinates):
            for j, order in enumerate(self.fourier_orders):
                bessel_function_argument_at_radius = (
                        mp.sqrt(-mp.j * order) * radius / mp.sqrt(reciprocate_peclet)
                )
                bessel_function_argument_at_surface = (
                        mp.sqrt(-mp.j * order) * 1 / mp.sqrt(reciprocate_peclet)
                )

                numerator = mp.besselj(order, bessel_function_argument_at_radius)
                denominator = mp.besselj(order, bessel_function_argument_at_surface)

                coefficients[i, j] = numerator / denominator

        return coefficients

    def set_normed_cooling_values(self):

        for cooling_section_angles in self.roll.cooling_sections:
            self.normed_cooling_array[cooling_section_angles[0]: cooling_section_angles[
                1]] = self.roll.min_radius * self.roll.coolant_heat_transfer_coefficient / self.roll.thermal_conductivity

        for i in range(self.normed_cooling_array.rows):
            if self.normed_cooling_array[i] == 0:
                self.normed_cooling_array[i] = self.roll.min_radius * self.roll.free_surface_heat_transfer_coefficient / self.roll.thermal_conductivity

    def set_normed_heating_values(self):
        bite_angle = int(np.ceil(np.abs(mp.degrees(self.roll.entry_angle))))
        lower_boundary = (self.angular_discretization - bite_angle)

        self.normed_heating_array[
        lower_boundary: self.angular_discretization] = self.roll.min_radius * self.roll_pass.average_heat_flux / (
                self.roll.thermal_conductivity * self.reference_temperature)

    def solve(self):
        self.set_normed_cooling_values()
        self.set_normed_heating_values()

        normed_temperature = mp.matrix(self.radial_discretization, self.angular_discretization)

        cooling_fourier_coefficients = self.complex_fourier_analysis(self.normed_cooling_array)
        heating_fourier_coefficients = self.complex_fourier_analysis(self.normed_heating_array)
        temperature_fourier_coefficients = self.temperature_fourier_analysis()
        diagonal_matrix = self.create_diagonal_matrix()
        cooling_hermitian_matrix = self.create_hermitian_matrix_from_cooling_array(cooling_fourier_coefficients)
        invers_matrix = mp.inverse((diagonal_matrix + cooling_hermitian_matrix))
        temperature_equation_fourier_constants = invers_matrix * heating_fourier_coefficients

        for r, radius in enumerate(self.normed_radial_coordinates):
            for j, angle in enumerate(self.polar_angles):
                terms = [
                    mp.re(
                        temperature_equation_fourier_constants[i]
                        * temperature_fourier_coefficients[r, i]
                        * mp.exp(mp.j * order * angle)
                    )
                    for i, order in enumerate(self.fourier_orders)
                ]
                normed_temperature[r, j] = mp.fsum(terms)

        temperature_field = mp.matrix(self.radial_discretization, self.angular_discretization)
        for r, radius in enumerate(self.normed_radial_coordinates):
            for j, angle in enumerate(self.polar_angles):
                temperature_field[r, j] = (
                        normed_temperature[r, j] * self.reference_temperature + self.roll.coolant_temperature
                )

        return temperature_field
