import matplotlib.pyplot as plt
from pyfiglet import Figlet
import numpy as np
import re
import sys
import random

def main():
    figlet = Figlet()
    output_title = figlet.setFont(font = 'big')
    output_title = figlet.renderText("Particle Movement in synchrotron")
    print(f"{output_title}\n")
    print("\nAuthor: Juan Sebastián Caicedo\n")
    print("Este programa simula el movimiento de\nuna partícula en un sincrotón bajo diferentes\ncondiciones de campo magnético.\n")
    print("MENÚ PRINCIPAL\n")
    print("1. Anillos de almacenamiento ideal")
    print("2. Partícula en sincrotrón con momento no ideal de diseño de la máquina")
    print("3. Acelerador Sincrotrón Booster")
    print("4. Salir del programa")
    option = input("\nSeleccione una de las opciones: ")
    option = option.strip()
    match option:
        case "1" | "1.":
            dP, dB, kwargs = validate_data(option)
            particle = Particle(dP = dP, dB = dB, **kwargs)
            P, R, DeltaT, T = particle.displacement()
            particle.show_graphics(P, R, DeltaT, T)
            main()
        case "2" | "2.":
            dP, dB, kwargs  = validate_data(option)
            particle = Particle(dP = dP, dB = dB, **kwargs)
            P, R, DeltaT, T = particle.displacement()
            particle.show_graphics(P, R, DeltaT, T)
            main()
        case "3" | "3.":
            dP, dB, kwargs  = validate_data(option)
            particle = Particle(dP = dP, dB = dB, **kwargs)
            P, R, DeltaT, T = particle.displacement()
            particle.show_graphics(P, R, DeltaT, T)
            main()
        case "4" | "4.":
            sys.exit()
        case _:
            print("\nOpción inválida, inténtelo nuevamente\n")
            main()

def validate_data(option):
    while True:
        try: 
            data = input("Ingrese los valores de campo magnético (T) y campo eléctrico (V)\ny longitud de las cavidades (m) separados por coma (,)\nSi desea los valores por defecto (1 T, 1 V, 2 m) oprima ENTER: ")
            data = data.strip()
            matches = re.search(r"^(.+), *(.+), *(.+)$", data)
            if re.search(r"^$", data):
                fields = {}
                break
            elif matches:
                B, E0, Lcavidad = float(matches.group(1)), float(matches.group(2)), float(matches.group(3))
                if (B > 0) and (E0 > 0) and (Lcavidad > 0):
                    fields = {"B": B, "E0": E0, "Lcavidad": Lcavidad}
                    break
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            print("Los datos ingresados son inválidos, inténtelo nuevamente")
            continue
        except AttributeError:
            continue
    dP, dB = 0, 0
    if option == "2" or option == "2.":
        while True:
            try:
                dP = input("Ingrese el valor del cambio de momento (dP): ")
                dP = float(dP.strip())
                if dP < 0:
                    raise ValueError
                break
            except ValueError:
                print("\nCambio de momento inválido, inténtelo nuevamente\n")
                continue
    elif option == "3" or option == "3.":
        while True:
            try:
                dB = input("\nIngrese el valor del cambio del campo magnético (dB): ")
                dB = float(dB.strip())
                break
            except ValueError:
                print("\nCambio de campo magnético inválido, inténtelo nuevamente\n")
                continue
    return dP, dB, fields    


class Particle:
    def __init__(self, dP = 0, dB = 0, B = 1, E0 = 1, Lcavidad = 2, q = 1.60217663e-19, m = 9.1093837015e-31):
        self.v = 3e8 #m//s
        self.q = q
        self.m = m
        self.B = B
        self.E0 = E0
        self.Lcavidad = Lcavidad
        self.dP = dP
        self.dB = dB
        random_number = random.choice([0, 0.5, 1])
        """ Momento inicial de la partícula"""
        self.p0 = self.m*self.v
        """Radio de trayectoria circular de partícula ideal"""
        self.r0 = self.p0/(self.q*self.B)
        """Frecuencia del campo eléctrico en cavidad RF"""
        self.w = self.v/self.r0
        """Momento inicial según OPCIÓN elegida"""
        self.p = self.p0 + (2*random_number-1)*self.dP
        """Radio de trayectoria circular de partícula real según opción"""
        self.radius = [self.p/(self.q/self.B)]
        """Instante de primera llegada a cavidad RF"""
        self.T0 = 2*np.pi*self.radius[0]/self.v
        self.time = [self.T0]
        """Número n de vuelta"""
        self.n = 1
        """Momento inicial"""
        self.P = [self.p + self.dP]
        """Inicio de DeltaT"""
        self.DeltaT = [0]
        
    def displacement(self):
        while self.n <= 100:
            i = self.n
            """Campo eléctrico en cavidad de RF"""
            E = self.E0*np.cos(self.w*self.time[i-1] + np.pi/2)
            """Fuerza sobre la partícula en cavidad RF"""
            F = self.q*E
            """Tiempo actuando la fuerza en cavidad de longitud Lcavidad"""
            dT = self.Lcavidad/self.v
            """Cambio de momento por paso en cavidad RF"""
            self.dP = F*dT
            """Momento antes del paso por la cavidad RF"""
            Pant = self.p
            """Nuevo momento de la partícula"""
            self.P += [Pant + self.dP]
            """Nuevo radio de la trayectoria circular"""
            self.B += self.dB
            self.radius += [self.P[i]/(self.q*self.B)]
            """Nueva circunferencia a recorrer"""
            L = 2*np.pi*self.radius[i]
            """Tiempo de recorrido de nueva circunferencia"""
            Tnew = L/self.v
            """Nuevo instante de llegada a cavidad de RF"""
            self.time += [self.time[i-1]+Tnew]
            """Adelnato o atraso con respecto a tiempo ideal"""
            self.DeltaT += [Tnew - (2*np.pi*self.r0/self.v)]
            self.n += 1
        return self.P, self.radius, self.DeltaT, self.time
    

    def show_graphics(self, P, R, DeltaT, T):
    
        n = np.arange(0,101)
        fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize = (15,4))

        #Momento P de la partícula en función del número de la vuelta
        axs[0, 0].plot(n, P, 'tab:blue')
        axs[0, 0].set_title('Momento P de la partícula en\nfunción del número de la vuelta')
        axs[0, 0].set_xlabel('Número de vuelta (n)')
        axs[0, 0].set_ylabel('Momento de la partícula\n$kg\cdot m/s$')

        #Radio de la trayectoria R en función del número de la vuelta:
        axs[0, 1].plot(n, R, 'tab:orange')
        axs[0, 1].set_title('Radio de la trayectoria R en\nfunción del número de la vuelta:')
        axs[0, 1].set_xlabel('Número de vuelta (n)')
        axs[0, 1].set_ylabel('Radio de trayetoria (m)')

        #Adelanto o atraso de llegada a cavidad de RF en función del número de la vuelta
        axs[1, 0].plot(n, DeltaT, 'tab:green')
        axs[1, 0].set_title('Adelanto o atraso de llegada a\ncavidad de RF en función\ndel número de la vuelta')
        axs[1, 0].set_xlabel('Número de vuelta (n)')
        axs[1, 0].set_ylabel('$\Delta T$ (s)')

        # Tiempo acumulado a la llegada a la cavidad de RF en función del número de la vuelta:
        axs[1, 1].plot(n, T, 'tab:red')
        axs[1, 1].set_title('Tiempo acumulado a la llegada a la\ncavidad de RF en función del\nnúmero de la vuelta:')
        axs[1, 1].set_xlabel('Número de vuelta (n)')
        axs[1, 1].set_ylabel('Tiempo (s)')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()