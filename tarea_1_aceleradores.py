import matplotlib.pyplot as plt
from pyfiglet import Figlet
import numpy as np
import re
import sys
import random

def main():
    figlet = Figlet()
    output_title = figlet.setFont(font = 'big')
    output_title = figlet.renderText("Particle Movement Simulator")
    print(f"{output_title}\n")
    print("\nAuthor: Juan Sebastián Caicedo\n")
    print("Este programa simula el movimiento de\nuna partícula en un sincrotón bajo diferentes\ncondiciones de campo magnético.\n")
    print("MENÚ PRINCIPAL\n")
    print("1. Monocromador")
    print("2. Movimiento de partícula positiva en campo magnético de sincrotrón")
    print("3. Salir del programa")
    option = input("\nSeleccione una de las opciones: ")
    option = option.strip()
    match option:
        case "1" | "1.":
            x0, v0 = initial_data()
            monocromador(x0, v0)
            main()
        case "2" | "2.":
            main_2()
        case "3" | "3.":
            sys.exit()
        case _:
            print("\nOpción inválida, inténtelo nuevamente\n")
            main()

def main_2():
    print("\nCuál de las siguientes opciones desea visualizar? \n")
    print("1. Sincrotrón con campo magnético uniforme")
    print("2. Sincrotrón con campo magnético perturbado")
    print("3. Gradiente alterno")
    print("4. Regresar al menú principal")
    print("5. Salir del programa")
    option_2 = input("\nSeleccione una de las opciones: ")
    option_2 = option_2.strip()
    match option_2:
        case "1" | "1.":
            x0, v0 = initial_data()
            sincrotron(x0, v0)
            main_2()
        case "2" | "2.":
            x0, v0 = initial_data()
            sincrotron_perturbated_b(x0, v0)
            main_2()
        case "3" | "3.":
            x0, v0 = initial_data()
            gradiente_alterno(x0, v0)
            main_2()
        case "4" | "4.":
            main()
        case "5" | "5.":
            sys.exit()
        case _:
            print("\nOpción inválida, inténtelo nuevamente\n")
            main_2()

def animation_approval():
    while True:
        animation = input("\nDesea realizar una simulación del desplazamiento de la carga? (y/n): ")
        animation = animation.strip().lower()
        if re.search("^y$", animation):
            print("\nADVERTENCIA, este proceso puede tomar un par de minutos\nSi desea terminar el proceso, presione las teclas Ctrl + C\n")
            animation = True
            break
        elif re.search("^n$", animation):
            animation = False
            break
        else:
            print("\nOpción inválida, inténtelo nuevamente")
            continue
    return animation

def initial_data():
    print("A continuación, ingresará los datos iniciales de la partícula: \n")
    while True:
        try:
            x0 = input("Ingrese la posición inicial x0 de la partícula (m): ")
            x0 = int(x0.strip())
            break
        except ValueError:
            print("\nPosición inicial inválida, inténtelo nuevamente\n")
            continue
    while True:
        try:
            v0 = input("\nIngrese la velocidad inicial v0 de la partícula (m/s): ")
            v0 = int(v0.strip())
            break
        except ValueError:
            print("\nVelocidad inicial inválida, inténtelo nuevamente\n")
            continue
    return x0, v0

def monocromador(x0, v0):
    particle = Particle(x0, v0)
    while True:
        animation = input("\nDesea realizar una simulación del desplazamiento de la carga? (y/n): ")
        animation = animation.strip().lower()
        if re.search("^y$", animation):
            print("\nADVERTENCIA, este proceso puede tomar un par de minutos\nSi desea terminar el proceso, presione las teclas Ctrl + C")
            animation = True
            break
        elif re.search("^n$", animation):
            animation = False
            break
        else:
            print("\nOpción inválida, inténtelo nuevamente")
            continue
    particle.simulate(0.01, animation)
    particle.plot_trajectory()
    particle.plot_radius_vs_time()

def sincrotron(x0, v0):
    """
    Sección 2.1
    """
    particle = Particle(x0, v0)
    animation = animation_approval()
    particle.simulate(0.01, animation, angle = 2*np.pi)
    particle.plot_trajectory()
    particle.plot_radius_vs_time()



def sincrotron_perturbated_b(x0, v0):
    """
    Sección 2.2
    """
    particle = Particle(x0, v0)
    while True:
            try:
                delta_radius = input("\nIngrese un valor de Delta R menor al radio de la trayectoria: ")
                delta_radius = int(delta_radius.strip())
                if delta_radius >= particle.radius[0]:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("\nValor inválido, inténtelo nuevamente")
                continue
    animation = animation_approval()
    particle.simulate(0.01, animation, angle = 2*np.pi, perturbation = True, delta_radius = delta_radius)
    particle.plot_trajectory()
    particle.plot_radius_vs_time()

def gradiente_alterno(x0, v0):
    """
    Sección 2.3
    """
    particle = Particle(x0, v0)
    while True:
            try:
                delta_radius = input("\nIngrese un valor de Delta R menor al radio de la trayectoria: ")
                delta_radius = int(delta_radius.strip())
                if delta_radius >= particle.radius[0]:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("\nValor inválido, inténtelo nuevamente")
                continue
    animation = animation_approval()
    particle.simulate(0.01, animation, angle = 2*np.pi, perturbation = True, delta_radius = delta_radius, alternador = True)
    particle.plot_trajectory()
    particle.plot_radius_vs_time()
    


class Particle:
    def __init__(self, x0, v0, y0 = 0, q = 1.60217663e-19, m = 9.1093837015e-31):
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = v0
        self.q = q
        self.m = m
        self.B = m*v0/(q*x0)
        self.trajectory_x = [x0]
        self.trajectory_y = [y0]
        self.radius = [np.sqrt(x0**2+y0**2)]
        self.time = [0]
        
        
    def displacement(self, dt, delta_radius, perturbation = False, alternador = False):

        self.v = np.sqrt(self.vx**2 + self.vy**2)
        self.R = np.sqrt(self.x**2 + self.y**2)

        #Fuerzas magnéticas
        if perturbation:
            if not alternador:
                self.perturbation_displacement(delta_radius)
                Fx = -self.q * self.v * self.perturbated_B * self.x/self.perturbated_radius
                Fy = -self.q * self.v * self.perturbated_B * self.y/self.perturbated_radius
            else:
                self.perturbation_displacement(delta_radius, alternador = alternador)
                Fx = -self.q * self.v * self.perturbated_B * self.x/self.perturbated_radius
                Fy = -self.q * self.v * self.perturbated_B * self.y/self.perturbated_radius


        else:
            Fx = -self.q * self.v * self.B * self.x/self.R
            Fy = -self.q * self.v * self.B * self.y/self.R

        #Aceleraciones
        ax = Fx/self.m
        ay = Fy/self.m

        #Cambio de velocidad
        self.vx += ax*dt
        self.vy += ay*dt

        #Cambio de posición
        self.x += self.vx*dt
        self.y += self.vy*dt
        
        #Almacenar posiciones
        self.trajectory_x.append(self.x)
        self.trajectory_y.append(self.y)
        self.radius.append(self.R)
        self.time.append(self.time[-1] + dt)

    def perturbation_displacement(self, delta_radius, alternador = False):
        current_angle = np.arctan2(self.y, self.x)
        if current_angle < 0:
            current_angle += 2*np.pi
        random_number = random.choice([0, 0.5, 1])
        self.perturbated_radius = self.R + (2*random_number-1)*delta_radius
        self.p = self.m * self.v
        reference_B = self.p / (self.perturbated_radius * self.q)
        if self.perturbated_radius - self.R == 0:
            m = 0
        else: 
            m = (reference_B -  self.B)/(self.perturbated_radius - self.R)
        if alternador:
            if (0 <= current_angle and current_angle <= np.pi/3) or (2/3*np.pi <= current_angle and current_angle <= np.pi) or (4/3*np.pi <= current_angle and current_angle <= 5/3*np.pi):
                m = abs(m)
            else:
                m *= -1
        self.perturbated_B = m*(self.perturbated_radius - self.R) + self.B

    def simulate(self, dt, animation = True, angle = np.pi, perturbation = False, delta_radius = 0, alternador = False):
        title_options = ['uniforme', 'perturbado']
        angle_travelled = 0
        if animation:
            plt.ion()
            fig, ax = plt.subplots()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Trayectoria de la partícula en un campo magnético uniforme')
            while  angle_travelled < angle:
                last_x, last_y = self.x, self.y
                if not perturbation:
                    title = title_options[0]
                    self.displacement(dt, delta_radius)
                else:
                    title = title_options[1]
                    if not alternador:
                        self.displacement(dt, delta_radius, perturbation = True)
                    else:
                        self.displacement(dt, delta_radius, perturbation = True, alternador = alternador)


                current_angle = np.arctan2(self.y, self.x)
                delta_angle = current_angle - np.arctan2(last_y, last_x)
                if delta_angle > np.pi:
                    delta_angle -= 2 * np.pi
                elif delta_angle < -np.pi:
                    delta_angle += 2 * np.pi
                angle_travelled += abs(delta_angle)

                ax.clear()  
                ax.plot(self.trajectory_x, self.trajectory_y, marker='o')
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title(f'Trayectoria de la partícula en un campo magnético {title}')
                ax.axis('equal')
                plt.draw() 
                plt.pause(0.01)

            plt.ioff()
            plt.show()

        else:
            while  angle_travelled < angle:
                last_x, last_y = self.x, self.y
                if not perturbation:
                    title = title_options[0]
                    self.displacement(dt, delta_radius)
                else:
                    title = title_options[1]
                    if not alternador:
                        self.displacement(dt, delta_radius, perturbation = True)
                    else:
                        self.displacement(dt, delta_radius, perturbation = True, alternador = alternador)

                current_angle = np.arctan2(self.y, self.x)
                delta_angle = current_angle - np.arctan2(last_y, last_x)
                if delta_angle > np.pi:
                    delta_angle -= 2 * np.pi
                elif delta_angle < -np.pi:
                    delta_angle += 2 * np.pi
                angle_travelled += abs(delta_angle)

    def plot_trajectory(self, perturbation = False):
        plt.plot(self.trajectory_x, self.trajectory_y, marker='o')
        plt.xlabel('X')
        plt.ylabel('Y')
        if not perturbation:
            plt.title(f'Trayectoria de la partícula en un campo magnético uniforme')
        else:
            plt.title(f'Trayectoria de la partícula en un campo magnético perturbado')
        plt.axis('equal')
        plt.grid(True)
        plt.show()

    def plot_radius_vs_time(self):
        plt.plot(self.time, self.radius, marker='o')
        plt.xlabel('Time (s)')
        plt.ylabel('Radius (m)')
        plt.title('Cambio del radio contral el tiempo')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()