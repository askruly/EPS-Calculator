import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import time
import math
from termcolor import colored

# Function to calculate the output data
def calculate():
    # Get input data from the user
    Nmax = float(Nmax_entry.get())
    Nmin = float(Nmin_entry.get())
    Tcirc_per = float(Tcirc_per_entry.get())
    tT = float(tT_entry.get())
    Delta_t = float(Delta_t_entry.get())

    # Get the selected accumulator battery or input the efficiency
    if ηab_var.get() == 1:
        ηab = 0.9 # Li-Ion
    elif ηab_var.get() == 2:
        ηab = 0.85 # Ni-Cd
    elif ηab_var.get() == 3:
        ηab = 0.8 # Ni-H2
    elif ηab_var.get() == 4:
        ηab = 0.75 # Ni-MH
    else:
        try:
            ηab = float(ηab_var.get())
        except ValueError:
            result_label.config(text="Error: Please enter a valid value for efficiency.")
            return
    
    # Calculate output data using the given formulas
    Tsol = Tcirc_per - tT
    Navp_eps = (Nmin * Tsol + Delta_t * (Nmax - Nmin)) / Tcirc_per
    Nsb = ((Nmin * tT) + Nmax * Delta_t) / (Tsol * ηab) + Nmin

    # Display input and output data in the GUI window
    """
    input_data = f"Input Data:\nNmax = {Nmax} W\nNmin = {Nmin} W\nTpr_obr = {Tcirc_per} min\n"
    input_data += f"tT = {tT} min\nDelta_t = {Delta_t} min\nη = {ηab}\n\n"
    output_data = f"Output Data:\n\nTime spent by the spacecraft on the side of solar activity, \nTsol = {Tsol} min\n"
    output_data += f"\nAverage power of the spacecraft EPS, \nNavp_eps = {Navp_eps} W\n"
    output_data += f"\nSolar battery power, \nNsb = {Nsb} W\n"
    """

    # Display output values
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Результат:" + "\n", "blue")
    output_text.insert(tk.END, f"\nВремя нахождения КА на стороне солнечной активности, ")
    output_text.insert(tk.END, f"\nTсолн = {Tsol} мин\n", "red")
    output_text.insert(tk.END, f"\nСредняя мощность СЭС КА, ")
    output_text.insert(tk.END, f"\nNср.сэс = {Navp_eps} Вт\n", "red")
    output_text.insert(tk.END, f"\nМощность солнечных батарей, ")
    output_text.insert(tk.END, f"\nNсб = {Nsb} ВТ\n", "red")
    
    # Configure the "red" tag to make text red
    output_text.tag_config("red", foreground="red")
    output_text.tag_config("blue", foreground="blue")
    
    # Display animation
    """
    formula1 = "\nTsol = Tcirc_per - tT"
    formula2 = "Navp_eps = (Nmin * Tsoln + Dt * (Nmax - Nmin)) / Tcirc_per"
    formula3 = "Nsb = ((Nmin * tT) + Nmax * Dt) / Tsol * ηab + Nmin"

    for formula in [formula1, formula2, formula3]:
        for char in formula:
            formula_label.config(text=formula_label.cget("text") + char)
            formula_label.update()
            time.sleep(0.005)
        formula_label.config(text=formula_label.cget("text") + "\n")

    result_label.config(text=input_data + output_data)
    """

def clear():
    Nmax_entry.delete(0, tk.END)
    Nmin_entry.delete(0, tk.END)
    Tcirc_per_entry.delete(0, tk.END)
    tT_entry.delete(0, tk.END)
    Delta_t_entry.delete(0, tk.END)
    output_text.delete('1.0', tk.END) 
        
# Create GUI window
root = tk.Tk()
root.title("EPS Calculator/Расчет СЭС")

# Create tabs
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Расчет мощности КА')
tab_control.add(tab2, text='Расчет проектной мощности СБ')
tab_control.add(tab3, text='Расчет параметров СБ')
tab_control.add(tab4, text='Расчет параметров АБ')
tab_control.pack(expand=1, fill='both')

# Open the image
image = Image.open("C:/Users/User/OneDrive/Рабочий стол/Дипломная Работа/PocketQube/EPS.png")

# Resize the image
new_size = (400, 300)  # Specify the new size
resized_image = image.resize(new_size)

# Convert the resized image to a PhotoImage object
photo_image = ImageTk.PhotoImage(resized_image)

# Create a Label widget to display the image
img_label = tk.Label(tab1, image=photo_image)
img_label.grid(rowspan=5, column=2, padx=5, pady=5)

# Create input fields for Calculation 1
Nmax_label = tk.Label(tab1, text="Мощность в режиме работы БЦК (Nmax, Вт): ", font=("Times New Roman", 11))
Nmax_label.grid(row=0, column=0, padx=5, pady=5)
Nmax_entry = tk.Entry(tab1)
Nmax_entry.grid(row=0, column=1, padx=5, pady=5)

Nmin_label = tk.Label(tab1, text="Мощность в дежурном режиме (Nmin, Вт): ", font=("Times New Roman", 11))
Nmin_label.grid(row=1, column=0, padx=5, pady=5)
Nmin_entry = tk.Entry(tab1)
Nmin_entry.grid(row=1, column=1, padx=5, pady=5)

Tcirc_per_label = tk.Label(tab1, text="Период обращения (Tпер.обр, мин): ", font=("Times New Roman", 11))
Tcirc_per_label.grid(row=2, column=0, padx=5, pady=5)
Tcirc_per_entry = tk.Entry(tab1)
Tcirc_per_entry.grid(row=2, column=1, padx=5, pady=5)

tT_label = tk.Label(tab1, text="Время нахождения в тени (tT, мин): ", font=("Times New Roman", 11))
tT_label.grid(row=3, column=0, padx=5, pady=5)
tT_entry = tk.Entry(tab1)
tT_entry.grid(row=3, column=1, padx=5, pady=5)

Delta_t_label = tk.Label(tab1, text="Время работы БЦК (Δt, мин): ", font=("Times New Roman", 11))
Delta_t_label.grid(row=4, column=0, padx=5, pady=5)
Delta_t_entry = tk.Entry(tab1)
Delta_t_entry.grid(row=4, column=1, padx=5, pady=5)

ηab_label = tk.Label(tab1, text="Выберите тип АБ \n(или введите значение эффективности (η)): ", font=("Times New Roman", 11))
ηab_label.grid(row=5, column=0, padx=5, pady=5)
ηab_options = {1: "0.9 (Li-Ion)", 2: "0.85 (Ni-Cd)", 3: "0.8 (Ni-H2)", 4: "0.75 (Ni-MH)"}
ηab_var = tk.IntVar()
ηab_radiobutton1 = tk.Radiobutton(tab1, text="Li-Ion", variable=ηab_var, value=1, font=("Times New Roman", 11))
ηab_radiobutton2 = tk.Radiobutton(tab1, text="Ni-Cd", variable=ηab_var, value=2, font=("Times New Roman", 11))
ηab_radiobutton3 = tk.Radiobutton(tab1, text="Ni-H2", variable=ηab_var, value=3, font=("Times New Roman", 11) )
ηab_radiobutton4 = tk.Radiobutton(tab1, text="Ni-MH", variable=ηab_var, value=4, font=("Times New Roman", 11))
ηab_radiobutton5 = tk.Radiobutton(tab1, text="Другие (Введите значение)", variable=ηab_var, value=5, font=("Times New Roman", 11))
ηab_radiobutton1.grid(row=5, column=1, padx=5, pady=5, sticky="w")
ηab_radiobutton2.grid(row=6, column=1, padx=5, pady=5, sticky="w")
ηab_radiobutton3.grid(row=7, column=1, padx=5, pady=5, sticky="w")
ηab_radiobutton4.grid(row=8, column=1, padx=5, pady=5, sticky="w")
ηab_radiobutton5.grid(row=9, column=1, padx=5, pady=5, sticky="w")
ηab_entry = tk.Entry(tab1)
ηab_entry.grid(row=10, column=1, padx=5, pady=5)

# Create a label widget to display the formulas
formula_label = tk.Label(tab1, font=("Times New Roman", 11))
formula_label.grid(row=0, column=4, rowspan=3, columnspan=4, padx=5, pady=5)

calculate_button = tk.Button(tab1, text="Расчет", command=calculate, font=("Times New Roman", 11))
calculate_button.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

result_label = tk.Label(tab1, text="", font=("Times New Roman", 11))
result_label.grid(row=3, column=4, rowspan=3, columnspan=4, padx=5, pady=5)

# Output text area
output_text = tk.Text(tab1, width=50, height=10)
output_text.grid(row=5, column=2, rowspan=5, columnspan=5, padx=5, pady=5)

clear_button = tk.Button(tab1, text="Очистить", command=clear, width=10) 
clear_button.grid(row=9, column=2, rowspan=5, columnspan=5, padx=10)

#-------------------------------------------------------------------------------------------------------------------------------------

# Function to calculate degradation coefficient and design capacity of solar battery
def calculate1():
    # Get user input values
    h = float(orbit_height_entry.get())
    t = float(operation_time_entry.get())
    φ1 = float(disorientation_angle1_entry.get())
    φ2 = float(disorientation_angle2_entry.get())
    Nsb = float(solar_battery_power_entry.get())

    # Calculate degradation coefficient based on orbit height
    if h >= 200 and h < 500:
        kd = 0.08
    elif h >= 500 and h < 3000:
        kd = 0.08 + 0.22*(h-500)/2500
    elif h >= 3001 and h <= 36000:
        kd = 0.3 - 0.1*(h-3000)/17000
    else:
        kd = 0.1

    # Calculate design capacity of SB
    Nc_sb = (Nsb * (1 + kd * t)) / (math.cos(math.radians(φ1)) * math.cos(math.radians(φ2)))

    # Update output labels with calculated values
    """
    degradation_coefficient_label.config(text=f"Degradation coefficient, \nkd = {kd}")
    design_capacity_label.config(text=f"\nDesign capacity of SB, \nNc_sb = {Nc_sb} W")
    """

    # Display output values
    output_text1.delete('1.0', tk.END)
    output_text1.insert(tk.END, f"Результат:" + "\n", "blue")
    output_text1.insert(tk.END, f"\nКоэффициент деградации СБ, ")
    output_text1.insert(tk.END, f"\nkd = {kd}\n", "red")
    output_text1.insert(tk.END, f"\nПроектная мощность СБ, ")
    output_text1.insert(tk.END, f"\nNпр.сб = {Nc_sb} Вт", "red")

    # Display animation
    formula1 = "Nпр.сб = (Nсб * (1 + kd * t)) / (math.cos(math.radians(φ1)) * math.cos(math.radians(φ2)))"

    for formula in [formula1]:
        for char in formula:
            formula_label3.config(text=formula_label3.cget("text") + char)
            formula_label3.update()
            time.sleep(0.005)
        formula_label3.config(text=formula_label3.cget("text") + "\n")

    # Configure the "red" tag to make text red
    output_text1.tag_config("red", foreground="red")
    output_text1.tag_config("blue", foreground="blue")

def clear1():
    orbit_height_entry.delete(0, tk.END)
    operation_time_entry.delete(0, tk.END)
    disorientation_angle1_entry.delete(0, tk.END)
    disorientation_angle2_entry.delete(0, tk.END)
    solar_battery_power_entry.delete(0, tk.END)
    output_text1.delete('1.0', tk.END) 

# Create input labels and entry fields
orbit_height_label = tk.Label(tab2, text="Высота орбиты (км), h: ", font=("Times New Roman", 11))
orbit_height_label.grid(row=0, column=0, padx=5, pady=5)
orbit_height_entry = tk.Entry(tab2)
orbit_height_entry.grid(row=0, column=1, padx=5, pady=5)

operation_time_label = tk.Label(tab2, text="Время летной эксплуатации КА (год), t: ", font=("Times New Roman", 11))
operation_time_label.grid(row=1, column=0, padx=5, pady=5)
operation_time_entry = tk.Entry(tab2)
operation_time_entry.grid(row=1, column=1, padx=5, pady=5)

disorientation_angle1_label = tk.Label(tab2, text="Угол дезориентации СБ1 (град), φ1: ", font=("Times New Roman", 11))
disorientation_angle1_label.grid(row=2, column=0, padx=5, pady=5)
disorientation_angle1_entry = tk.Entry(tab2)
disorientation_angle1_entry.grid(row=2, column=1, padx=5, pady=5)

disorientation_angle2_label = tk.Label(tab2, text="Угол дезориентации СБ2 (град), φ2: ", font=("Times New Roman", 11))
disorientation_angle2_label.grid(row=3, column=0, padx=5, pady=5)
disorientation_angle2_entry = tk.Entry(tab2)
disorientation_angle2_entry.grid(row=3, column=1, padx=5, pady=5)

solar_battery_power_label = tk.Label(tab2, text="Мощность СБ (Вт), Nсб: ", font=("Times New Roman", 11))
solar_battery_power_label.grid(row=4, column=0, padx=5, pady=5)
solar_battery_power_entry = tk.Entry(tab2)
solar_battery_power_entry.grid(row=4, column=1, padx=5, pady=5)

calculate_button = tk.Button(tab2, text="Расчет", command=calculate1, font=("Times New Roman", 11))
calculate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

formula_label3 = tk.Label(tab2, font=("Times New Roman", 11))
formula_label3.grid(row=0, column=2, rowspan=3, columnspan=4, padx=5, pady=5)

degradation_coefficient_label = tk.Label(tab2, text="", font=("Times New Roman", 11))
degradation_coefficient_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

design_capacity_label = tk.Label(tab2, text="", font=("Times New Roman", 11))
design_capacity_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Output text area
output_text1 = tk.Text(tab2, width=50, height=10)
output_text1.grid(row=5, column=2, rowspan=5, columnspan=5, padx=5, pady=5)

clear_button1 = tk.Button(tab2, text="Очистить", command=clear1, width=10) 
clear_button1.grid(row=10, column=2, rowspan=5, columnspan=5, padx=10)

#------------------------------------------------------------------------------------------------------------------

def calculate2():
    # Get user input values
    Nc_sb = float(Nc_sb_entry.get())
    q = 1396  # solar constant in Earth orbits (W/m^2)
    k = float(kf_entry.get())
    
    # Get the selected solar battery or input the efficiency
    if nsb_var.get() == 1:
        ηsb = 0.18 # Si
    elif nsb_var.get() == 2:
        ηsb = 0.265 # GaAs
    elif nsb_var.get() == 3:
        ηsb = 0.19 # InP
    else:
        try:
            ηsb = float(nsb_entry.get())
        except ValueError:
            result_label.config(text="Error: Please enter a valid value for efficiency.")
            return
        
    # Get the selected accumulator battery
    γ_options = {"2": 2, "3": 3, "4": 4}
    γ = γ_options[γ_var.get()]

    # calculated dependencies
    S = Nc_sb / (q * k * ηsb)  # SB area (m^2)
    Sl = S * 1.03  # the area of the SB taking into account losses (m^2)
    M = S * γ  # weight SB (kg)

    # Display input and output data in the GUI window
    """
    input_data = f"Input Data:\n\nη = {ηsb} %\nNc_sb = {Nc_sb} W\nq = {q} W/m^2\n"
    input_data += f"k = {k} \nγ = {γ} kg/m^2\n\n"
    output_data = f"Output Data:\n\nSB area (S): {S} m^2\n"
    output_data += f"\nArea of the SB taking into account losses (Sl): {Sl} m^2\n"
    output_data += f"\nWeight of SB (M): {M} kg\n"
    """
    
    # Display output values
    output_text2.delete('1.0', tk.END)
    output_text2.insert(tk.END, f"Вводные данные:\n\nη = {ηsb} %\nNпр.сб = {Nc_sb} Вт\nqс = {q} Вт/м^2\n")
    output_text2.insert(tk.END, f"k = {k} \nγ = {γ} кг/м^2\n\n")
    output_text2.insert(tk.END, f"Результат:" + "\n", "blue")
    output_text2.insert(tk.END, f"\nПлощадь СБ (S): ")
    output_text2.insert(tk.END, f"\nS = {S} м^2\n", "red")
    output_text2.insert(tk.END, f"\nПлощаль СБ с учетом потерь (Sпсб): ")
    output_text2.insert(tk.END, f"\nSпсб = {Sl} м^2\n", "red")    
    output_text2.insert(tk.END, f"\nМасса СБ (Mсб): ")    
    output_text2.insert(tk.END, f"\nMсб = {M} кг\n", "red")

    # Configure the "red" tag to make text red
    output_text2.tag_config("red", foreground="red")
    output_text2.tag_config("blue", foreground="blue")

    # Display animation
    formula1 = "\nSсб = Nпр.сб / (qс * k * ηсб)"
    formula2 = "\nSпсб = Sсб * 1.03"
    formula3 = "\nMсб = Sсб * γ"

    for formula in [formula1, formula2, formula3]:
        for char in formula:
            formula_label1.config(text=formula_label1.cget("text") + char)
            formula_label1.update()
            time.sleep(0.005)
        formula_label1.config(text=formula_label1.cget("text") + "\n")

    # result_label1.config(text=input_data + output_data)

def clear2():
    nsb_entry.delete(0, tk.END)
    Nc_sb_entry.delete(0, tk.END)
    kf_entry.delete(0, tk.END)
    disorientation_angle2_entry.delete(0, tk.END)
    solar_battery_power_entry.delete(0, tk.END)
    output_text2.delete('1.0', tk.END) 

# Create input fields for Calculation 1
nsb_label = tk.Label(tab3, text="Выберите тип СБ \n(или введите значение эффективности (η)): ", font=("Times New Roman", 11))
nsb_label.grid(row=0, column=0, padx=5, pady=5)
nsb_options = {1: "0.18 (Si)", 2: "0.265 (GaAs)", 3: "0.19 (InP)"}
nsb_var = tk.IntVar()
nsb_radiobutton1 = tk.Radiobutton(tab3, text="Si", variable=nsb_var, value=1, font=("Times New Roman", 11))
nsb_radiobutton2 = tk.Radiobutton(tab3, text="GaAs", variable=nsb_var, value=2, font=("Times New Roman", 11))
nsb_radiobutton3 = tk.Radiobutton(tab3, text="InP", variable=nsb_var, value=3, font=("Times New Roman", 11) )
nsb_radiobutton5 = tk.Radiobutton(tab3, text="Другие (введите значение)", variable=nsb_var, value=5, font=("Times New Roman", 11))
nsb_radiobutton1.grid(row=0, column=1, padx=5, pady=5, sticky="w")
nsb_radiobutton2.grid(row=1, column=1, padx=5, pady=5, sticky="w")
nsb_radiobutton3.grid(row=2, column=1, padx=5, pady=5, sticky="w")
nsb_radiobutton5.grid(row=3, column=1, padx=5, pady=5, sticky="w")
nsb_entry = tk.Entry(tab3)
nsb_entry.grid(row=4, column=1, padx=5, pady=5)

Nc_sb_label = tk.Label(tab3, text="Проектная мощность СБ (Nпр.сб, Вт): ", font=("Times New Roman", 11))
Nc_sb_label.grid(row=6, column=0, padx=5, pady=5)
Nc_sb_entry = tk.Entry(tab3)
Nc_sb_entry.grid(row=6, column=1, padx=5, pady=5)

q_label = tk.Label(tab3, text="Солнечная постоянная (Вт/м^2): q = 1396 Вт/м^2", font=("Times New Roman", 11))
q_label.grid(row=7, column=0, padx=5, pady=5)

kf_label = tk.Label(tab3, text="Коэффициент заполнения, k: ", font=("Times New Roman", 11))
kf_label.grid(row=8, column=0, padx=5, pady=5)
kf_entry = tk.Entry(tab3)
kf_entry.grid(row=8, column=1, padx=5, pady=5)

γ_label = tk.Label(tab3, text="Удельная масса СБ (2, 3 or 4) (γ кг/м^2): ", font=("Times New Roman", 11))
γ_label.grid(row=9, column=0, padx=5, pady=5)
γ_var = tk.StringVar(value="2")
γ_dropdown = tk.OptionMenu(tab3, γ_var, "2", "3", "4")
γ_dropdown.grid(row=9, column=1, padx=5, pady=5)

# Create a label widget to display the formulas
formula_label1 = tk.Label(tab3, font=("Times New Roman", 11))
formula_label1.grid(row=0, column=2, padx=5, pady=5)

calculate_button = tk.Button(tab3, text="Расчет", command=calculate2, font=("Times New Roman", 11))
calculate_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

result_label1 = tk.Label(tab3, text="", font=("Times New Roman", 11))
result_label1.grid(row=1, column=2, rowspan=9, padx=5, pady=5)

# Output text area
output_text2 = tk.Text(tab3, width=50, height=20)
output_text2.grid(row=5, column=2, columnspan=2, rowspan=9, padx=5, pady=5)

clear_button2 = tk.Button(tab3, text="Очистить", command=clear2, width=10) 
clear_button2.grid(row=13, column=0, rowspan=5, columnspan=2, padx=10)

#--------------------------------------------------------------------------------------------------------------------------------

# function to calculate output parameters
def calculate3():
    # get input values from entry widgets
    Nc_sb = float(N_entry.get())
    Nmin = float(Nmin_entry3.get())
    tT = float(tT_entry2.get())
    φ = float(φ_entry.get())
    U = float(U_entry.get())

    # Get the selected accumulator battery
    k_options = {"3": 3, "4": 4, "5": 5}
    k = k_options[k_var.get()]

    # Calculating output parameters
    E = (Nc_sb - Nmin) * tT * k
    Eraz = E / (1 - φ)
    Cpr = Eraz
    C = E / U

    # Display input and output data in the GUI window
    """
    input_data = f"Input Data:\n\nNc_sb = {Nc_sb} W\nNmin = {Nmin} W/m^2\ntT = {tT} min\n"
    input_data += f"k = {k} \nφ = {φ}\nU = {U} V\n\n"
    output_data = f"Output Data:\n\nDesign capacity of AB (E): {E} Wh\n"
    output_data += f"\nPermissible depth of discharge (Eraz): {Eraz} Wh\n"
    output_data += f"\nAB capacity (Cpr): {Cpr} Wh\n"
    output_data += f"\nCapacity AB (C): {C} Ah\n"
    """

    # Display output values
    output_text3.delete('1.0', tk.END)
    output_text3.insert(tk.END, f"Входные данные:\n\nNпр.сб = {Nc_sb} Вт\nNmin = {Nmin} Вт\ntT = {tT} мин\n")
    output_text3.insert(tk.END, f"kрез = {k} \nφ = {φ}\nU = {U} В\n\n")
    output_text3.insert(tk.END, f"Результат:" + "\n", "blue")
    output_text3.insert(tk.END, f"\nПроектная емкость АБ (Eпр.аб): ")
    output_text3.insert(tk.END, f"\nEпр.аб = {E} Втч\n", "red")
    output_text3.insert(tk.END, f"\nДопустимая глубина разряда (Eраз.аб): ")
    output_text3.insert(tk.END, f"\nEраз.аб = {Eraz} Втч\n", "red")
    output_text3.insert(tk.END, f"\nЕмкость АБ (Cпр.аб): ")
    output_text3.insert(tk.END, f"\nCпр.аб = {Cpr} Втч\n", "red")
    output_text3.insert(tk.END, f"\nЕмкость АБ (C): ")
    output_text3.insert(tk.END, f"\nC = {C} Втч\n", "red")

    # Configure the "red" tag to make text red
    output_text3.tag_config("red", foreground="red")
    output_text3.tag_config("blue", foreground="blue")

    # Display animation
    formula1 = "\nEпр.аб = (Nпр.сб - Nmin) * tT * kрез"
    formula2 = "\nEраз.аб = Eпр.аб / (1 - φ)"
    formula3 = "\nCпр.аб = Eраз.аб"
    formula4 = "\nC = Eпр.аб / U"

    for formula in [formula1, formula2, formula3, formula4]:
        for char in formula:
            formula_label2.config(text=formula_label2.cget("text") + char)
            formula_label2.update()
            time.sleep(0.005)
        formula_label2.config(text=formula_label2.cget("text") + "\n")

    # result_label2.config(text=input_data + output_data)

def clear3():
    N_entry.delete(0, tk.END)
    Nmin_entry3.delete(0, tk.END)
    tT_entry2.delete(0, tk.END)
    φ_entry.delete(0, tk.END)
    U_entry.delete(0, tk.END)
    output_text3.delete('1.0', tk.END) 

# create input parameter labels and entry widgets
k_label = tk.Label(tab4, text="Коэффициент резерва (k) (3, 4, или 5): ", font=("Times New Roman", 11))
k_label.grid(row=0, column=0, padx=5, pady=5)
k_var = tk.StringVar(value="3")
k_dropdown = tk.OptionMenu(tab4, k_var, "3", "4", "5")
k_dropdown.grid(row=0, column=1, padx=5, pady=5)

N_label = tk.Label(tab4, text="Проектная мощность СБ (Nпр.сб, Вт): ", font=("Times New Roman", 11))
N_label.grid(row=1, column=0, padx=5, pady=5)
N_entry = tk.Entry(tab4)
N_entry.grid(row=1, column=1, padx=5, pady=5)

Nmin_label3 = tk.Label(tab4, text="Мощность в дежурном режиме (Nmin, Вт): ", font=("Times New Roman", 11))
Nmin_label3.grid(row=2, column=0, padx=5, pady=5)
Nmin_entry3 = tk.Entry(tab4)
Nmin_entry3.grid(row=2, column=1, padx=5, pady=5)

tT_label2 = tk.Label(tab4, text="Время нахождения в тени (tT, мин): ", font=("Times New Roman", 11))
tT_label2.grid(row=3, column=0, padx=5, pady=5)
tT_entry2 = tk.Entry(tab4)
tT_entry2.grid(row=3, column=1, padx=5, pady=5)

φ_label = tk.Label(tab4, text="Допустимая глубина разряда АБ (φ): ", font=("Times New Roman", 11))
φ_label.grid(row=4, column=0, padx=5, pady=5)
φ_entry = tk.Entry(tab4)
φ_entry.grid(row=4, column=1, padx=5, pady=5)

U_label = tk.Label(tab4, text="Номинальное напряжение (U, В): ", font=("Times New Roman", 11))
U_label.grid(row=5, column=0, padx=5, pady=5)
U_entry = tk.Entry(tab4)
U_entry.grid(row=5, column=1, padx=5, pady=5)

# Create a label widget to display the formulas
formula_label2 = tk.Label(tab4, font=("Times New Roman", 11))
formula_label2.grid(row=0, column=2, padx=5, pady=5)

calculate_button = tk.Button(tab4, text="Расчет", command=calculate3, font=("Times New Roman", 11))
calculate_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

result_label2 = tk.Label(tab4, text="", font=("Times New Roman", 11))
result_label2.grid(row=0, column=2, rowspan=7, padx=5, pady=5)

# Output text area
output_text3 = tk.Text(tab4, width=50, height=10)
output_text3.grid(row=8, columnspan=2, padx=5, pady=5)

clear_button3 = tk.Button(tab4, text="Очистить", command=clear3, width=10) 
clear_button3.grid(row=13, column=0, rowspan=5, columnspan=2, padx=10)

root.mainloop()