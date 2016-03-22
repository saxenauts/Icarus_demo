from matplotlib import pyplot
from matplotlib import rc

import numpy as np
from scipy.integrate import quad

np.seterr(all = 'ignore')

#rc('font', **{'family': 'sans-serif', 'sans-serif':['Helvetica']})
#rc('text', usetex = True)

h = 6.626e-34
c = 3.0e+8
k = 1.38e-23
sol_rad = 6.957e+8
pars = 3.086e+16

def generate_fluxes(wavelengths, temperature):
    lam = (h*c)/(k*temperature)
    cons = 2*(np.pi)*h*(c**2)
    fluxes = [cons/((wav**5)*((np.exp(lam/wav))-1)) for wav in wavelengths]
    return fluxes
    
def generate_observed_fluxes(wavelength, temperature, rad, dis):
    fluxes = generate_fluxes(wavelength, temperature)
    obs_fluxes = [(flux)*(((sol_rad*rad)/(dis*pars))**2)  for flux in fluxes]
    return obs_fluxes
    
    


wavelengths = np.arange(1e-9, 3e-6, 1e-9)

temperatures = [5000, 6000, 7000, 8000]

flux_list = [generate_fluxes(wavelengths, temp) for temp in temperatures]

#pyplot.hold(True) 

cols = ['r-', 'g-', 'b-', 'k-']

for i in range(4):
    
    pyplot.plot(wavelengths*1e9, flux_list[i], cols[i])

def integrand(wavelength):
    obs_flux = generate_observed_flux(wavelength, 7000,1,2)
    return obs_flux
    
#return absolute value using integration, parameters: wavelengths only
#def magnitude_abs(wavelength):
 #   return (-2.5)*(np.log10((quad(integrand, 507e-9, 595e-9))/(wavelength*(generate_observed_flux(wavelength, 7000, 2.26, 7.70)))))

wavelength_centre_filter = [365e-9, 445e-9, 551e-9, 658e-9]
      
#return approximated value using, parameters: wavelength only
def magnitude_app(wavelength):
    magnitudes = [ ((-2.5)*(np.log10((generate_observed_fluxes([wave], 7000, 1, 2)[0])/(generate_observed_fluxes([wave], 7000, 2.818, 7.70)[0])))) for wave in wavelength]
    return magnitudes

   
magnitudes = magnitude_app(wavelength_centre_filter)
pyplot.text(1500, 2.5e+14, "Respective to star Vega\n\n" + "Radius = 2.818 (Solar Radius) \nDistance: 7.68 parsecs" + "\n" + "U: " + str(magnitudes[0]) + '\n' + "B: "  + str(magnitudes[1]) + '\n' + "V: " + str(magnitudes[2]) + '\n'  + "R: " + str(magnitudes[3]))

pyplot.ylabel("Flux")
pyplot.xlabel("Wavelength")
pyplot.show()     
#pyplot.ylabel(r'\textbf{Flux} (J/s.m^{2}.$\Delta$$\lambda\$.sr', fontsize = 16)
#pyplot.xlabel(r'\textbf{Wavelength}', fontsize = 16)    

