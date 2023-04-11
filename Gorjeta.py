import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 9, 2), 'Comida (1000kcal)')
altura = ctrl.Antecedent(np.arange(120, 200, 5), 'Altura (cm)')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 11, 2), 'Peso (10kg)' )

# automf -> Atribuição de categorias automaticamente
comer["Pouco"] = fuzz.trapmf(comer.universe,[0,0,2,4])
comer["Razoável"] = fuzz.trapmf(comer.universe,[2,4,6,8])
comer["Bastante"] = fuzz.trapmf(comer.universe,[4,6,10,10])

altura["Baixo"] = fuzz.trapmf(altura.universe,[0,0,150,160])
altura["Médio"] = fuzz.trapmf(altura.universe,[150,160,170,175])
altura["Alto"] = fuzz.trapmf(altura.universe,[165,175,200,250])

peso["Peso_Leve"] = fuzz.trapmf(peso.universe,[0,0,4,6])
peso["Peso_Médio"] = fuzz.trapmf(peso.universe,[4,6,8,10])
peso["Pesado"] = fuzz.trapmf(peso.universe,[8,10,12,12])

#Visualizando as variáveis
comer.view()
altura.view()
peso.view()


# #Criando as regras

regra_1 = ctrl.Rule(comer['Bastante'] & altura['Baixo'], peso['Pesado'])
regra_2 = ctrl.Rule(comer['Bastante'] & altura['Médio'], peso['Pesado'])
regra_3 = ctrl.Rule(comer['Bastante'] & altura['Alto'], peso['Peso_Médio'])
regra_4 = ctrl.Rule(comer['Razoável'] & altura['Alto'], peso['Peso_Leve'])
regra_5 = ctrl.Rule(comer['Razoável'] & altura['Médio'], peso['Peso_Médio'])
regra_6 = ctrl.Rule(comer['Razoável'] & altura['Baixo'], peso['Peso_Médio'])
regra_7 = ctrl.Rule(comer['Pouco'] & altura['Alto'], peso['Peso_Leve'])
regra_8= ctrl.Rule(comer['Pouco'] & altura['Médio'], peso['Peso_Leve'])
regra_9 = ctrl.Rule(comer['Pouco'] & altura['Baixo'], peso['Peso_Médio'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3,regra_4,regra_5,regra_6,regra_7,regra_8,regra_9])
# #Simulando
CalculoPeso = ctrl.ControlSystemSimulation(controlador)

notacomer = int(input('Número de calorias (1000kcal): '))
notaaltura = int(input('Altura (cm): '))
CalculoPeso.input['Comida (1000kcal)'] = notacomer
CalculoPeso.input['Altura (cm)'] = notaaltura
CalculoPeso.compute()

valorPeso = CalculoPeso.output['Peso (10kg)']

print(f"\nQuantidade de calorias: {notacomer*1000}kcal\nAltura da pessoa: {notaaltura}cm\n Peso: {valorPeso*10}kg")

comer.view(sim=CalculoPeso)
altura.view(sim=CalculoPeso)
peso.view(sim=CalculoPeso)

plt.show()