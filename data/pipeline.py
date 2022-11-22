from enquiries import choose
from re import match
from datetime import datetime


def input_prompt(message, end=":\t"):
    print(message, end=end)
    return input()

def get_name(DATA):
    name = input_prompt("NOMBRE")
    DATA["name"] = name

def get_age(DATA):
    age = input_prompt("EDAD")
    DATA["age"] = int(age)

def get_sex(DATA):
    choice = choose("SEXO:", ["Masculino", "Femenino"])
    if match("^M", choice):
        DATA["sex"] = "M"
    else:
        DATA["sex"] = "F"
    
    print("SEXO:", choice)

def get_diabetes(DATA):
    choice = choose("TIPO DE DIABETES:", ["Tipo I", "Tipo II", "No diabetes"])
    DATA["diabetes_type"] = choice
    print("TIPO DE DIABETES:", choice)

def get_dfu_type(DATA):
    choice = choose("TIPO DE ÚLCERA:", ["Neuroinfecciosa", "Isquémica", "Flebolinfática", "Combinada"])
    DATA["dfu_type"] = choice
    print("TIPO DE ÚLCERA:", choice)

def get_dfu_loc(DATA):
    foot = choose("LOCALIZACIÓN DE LA ÚLCERA:\nPIE:", ["Derecho", "Izquierdo"])
    
    choice = choose("LOCALIZACIÓN DE LA ÚLCERA:\nREGIÓN DE LOCALIZACIÓN:", ["Dedos del pie", "Plantar", "Dorsal", "Calcánea", "Anterior del tobillo", "Posterior del tobillo", "Retromaleolar lateral", "Retromaleolar medial", "Anterior de la pierna", "Posterior de la pierna", "Sural"])    
    DATA["dfu_loc"] = f"Región {choice} del pie {foot}"
    print("LOCALIZACIÓN DE LA ÚLCERA:", DATA["dfu_loc"])
    
def data_pipeline():
    now = datetime.now()
    DATA = {
        "name": "-",
        "age": "-",
        "sex": "-",
        "diabetes_type": "-",
        "dfu_type": "-",
        "dfu_loc": "-",
        "datetime": f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}"
    }
    print("====================================")
    print("DATOS DEL PACIENTE")
    print("====================================")
    
    get_name(DATA)
    get_age(DATA)
    get_sex(DATA)
    get_diabetes(DATA)
    get_dfu_type(DATA)
    get_dfu_loc(DATA)
    print("====================================")
    print(DATA)
    return DATA