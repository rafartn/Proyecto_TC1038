'''Repositorio de GitHub: https://github.com/rafartn/Proyecto_TC1038
En este código no se implementan listas de listas
Sin embargo, se utiliza un dataframe de pandas, que resulta mucho más conveniente,
ya que permite implementar de mejor manera el almacenamiento de datos por medio de un csv'''

import pandas as pd
from datetime import datetime

AHORA=datetime.now()
MAPAS=("Abyss", "Ascent", "Bind", "Breeze", "Corrode", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset", "Fracture")
AGENTES=("Brimstone", "Viper", "Omen", "Sova", "Sage", "Phoenix", "Raze", "Cypher", "Jett", "Reyna", "Killjoy", "Breach", "Fade", "Chamber", "Neon", "Kay/o", "Yoru", "Astra", "Harbor", "Gekko", "Deadlock", "Iso", "Clove", "Vyse", "Waylay", "Tejo", "Miks", "Hush")
columnas=['fecha','mapa', 'agente', 'bajas', 'muertes', 'asistencias', 'rondas', 'resultado']

def verificar_fecha(fecha, lista):
    '''Esta función verifica que la fecha sea de un formato adecuado
    Le adjunta la fecha a la lista si es de formato adecuado e indica si no lo es
    Regresa si la fecha es válida y la lista a adjuntar al csv
    Esta es una nueva funcionalidad con respecto al avance 2,
    incluye el uso de funciones de manejo de cadenas vistas en clase como join(), split() o replace()'''
    espacios=False
    flag=True
    #Primero se quitan los espacios de la fecha
    fecha=fecha.replace(" ", "")
    #Luego se verifica que hayan números o divisores en la fecha
    for c in fecha:
        if c not in ("1234567890/"):
            flag=False
    #Se divide después según el divisor
    fecha=fecha.split("/")
    #Se verifican varios lineamientos
    try:
        if len(fecha) != 3:
            flag=False
        # Permitiremos registrar años de partidas pasadas, pero no antes de la sálida del juego Valorant, que fue en 2020
        elif int(fecha[0]) not in range(1, 32) or int(fecha[1]) not in range (1, 13) or int(fecha[2]) not in range(2020, AHORA.year+1):
            flag=False
    except:
        flag=False
    if flag:
        fecha="/".join(fecha)
        lista.append(fecha)
    else:
        print("La fecha ingresada no es válida")
    return flag, lista

'''Función que verifica que exista el archivo csv y lo crea en caso de que no
El programa se desarrolla en un csv para que sea posible guardar los datos incluso cuando el código se termina'''
def verificar_csv():
    try:
        datos=pd.read_csv(r"datos_proyecto.csv")
    except:
        datos=pd.DataFrame(columns=columnas)
        datos.to_csv(r"datos_proyecto.csv", index=False )
        print("no existe el archivo")
    return datos

#Función que verifica que el número de rondas sea válido (mayor o igual a 13) y lo agrega a la lista en caso de serlo
def verificar_rondas(num, lista):
    if num>=13:
        lista.append(num)
        return True, lista
    else:
        print("Ingrese un valor valido")
        return False, lista

#Función que verifica que un número sea positivo y lo agrega a la lista en caso de serlo
def verificar_numeros(num, lista):
    if num>=0:
        lista.append(num)
        return True, lista
    else:
        print("Ingrese un valor valido")
        return False, lista

#Función que registra los datos de una nueva partida,
#se asegura de que sean válidos (volviéndolos a pedir en caso de no serlo hasta que sí lo sean),
#los agrega a una lista auxiliar
#y agrega la lista auxiliar al archivo csv de datos con el que se está trabajando
def registro():
    lista1=[]
    fecha_verify=False
    while not fecha_verify:
        fecha=input("Ingrese la fecha del registro, el formato requerido es DD/MM/AAAA (incluya las barras diagonales) : ")
        fecha_verify, lista1=verificar_fecha(fecha, lista1)


    while True:
        mapa=input("Ingrese el mapa de la partida: ").capitalize()
        if mapa in MAPAS:
            lista1.append(mapa)
            break
        else:
            print("Ingrese un valor valido")

    while True:
        agente=input("Ingrese el agente de la partida sin usar mayúsculas: ").capitalize()
        if agente in AGENTES:
            lista1.append(agente)
            break
        else:
            print("Ingrese un valor valido")

    bajas_verify=False
    while not bajas_verify:
        bajas=int(input("Ingrese el número de bajas que obtuvo durante la partida: "))
        bajas_verify, lista1 = verificar_numeros(bajas, lista1)

    muertes_verify=False
    while not muertes_verify:
        muertes=int(input("Introduzca la cantidad de veces que fue eliminado durante la partida: "))
        muertes_verify, lista1=verificar_numeros(muertes, lista1)

    asistencias_verify = False
    while not asistencias_verify:
        asistencias = int(input("Introduzca la cantidad de asistencias que obtuvo durante la partida: "))
        asistencias_verify, lista1 = verificar_numeros(asistencias, lista1)

    rondas_verify = False
    while not rondas_verify:
        rondas = int(input("Ingrese la cantidad de rondas que hubo en la partida: "))
        rondas_verify, lista1 = verificar_rondas(rondas, lista1)

    #Aquí se pide al usuario si ganó la partida y convierte el valor a un booleano
    #para facilitar el análisis de las partidas
    resultado=int(input("¿Ganó la partida? (Ingrese 1 para sí y 2 para no): "))
    if resultado==1:
        resultado=True
    else:
        resultado=False
    lista1.append(resultado)

    #En este apartado se agrega la lista auxiliar de la partida al archivo csv con el que se está trabajando
    #y previene que el código se termine por un error si hay un problema,
    #indicando al usuario que no fue posible guardar la partida
    try:
        df1=pd.DataFrame([lista1], columns=columnas)
        df1.to_csv(r"datos_proyecto.csv", index=False, mode="a", header=False)
        print("La partida fue guardada con éxito")
    except:
        print("La partida no pudo ser guardada, intente de nuevo")

#Función que calcula e imprime las estadísticas principales del jugador
#usando funciones aditivas de pandas como .count() y .sum()
def calculo_estadisticas(df):
    total_partidas=df['fecha'].count()
    total_victorias=df['resultado'].sum()
    total_derrotas=total_partidas-total_victorias
    bajas_promedio=df['bajas'].mean()
    muertes_promedio=df['muertes'].mean()
    win_rate = total_victorias / total_partidas

    #Aquí se verifica que haya más de 0 muertes totales antes de dividir sobre ellas en kd global
    #con el objetivo de evitar un error por dividir sobre 0
    if muertes_promedio==0:
        kd_global = bajas_promedio
    else:
        kd_global=bajas_promedio/muertes_promedio

    print(f"\nPartidas jugadas: {total_partidas}")
    print(f"Partidas ganadas: {total_victorias}")
    print(f"Partidas perdidas: {total_derrotas}")
    print(f"Win rate: {win_rate}")
    print(f"Bajas promedio: {bajas_promedio}")
    print(f"Muertes promedio: {muertes_promedio}")
    print(f"K/D global: {kd_global}")

#Función que calcula el mapa con mayor K/D rate
#y define si es que hay un empate entre 2 mapas
def analizar_kd_mapa(df):
    kd_mapa_max_num = 0
    kd_mapa_max = []
    for mapa in MAPAS:
        bajas_totales_mapa=df[df['mapa'] == mapa]['bajas'].sum()
        muertes_totales_mapa = df[df['mapa'] == mapa]['muertes'].sum()
        partidas_totales_mapa = df[df['mapa'] == mapa]['agente'].count()

        #Aquí se protege de errores, si  no hubieron muertes en la partida el K/D rate se define como la cantidad de bajas
        #Además, si no se han jugado partidas con ese mapa, el K/D rate es igual a 0
        if partidas_totales_mapa==0:
            kd_mapa_num=0
        elif muertes_totales_mapa==0:
            kd_mapa_num=bajas_totales_mapa
        else:
            kd_mapa_num=bajas_totales_mapa/muertes_totales_mapa
        if kd_mapa_num>kd_mapa_max_num:
            kd_mapa_max_num=kd_mapa_num
            kd_mapa_max=[mapa]
            empate=False
        elif kd_mapa_num==kd_mapa_max_num:
            empate=True
            kd_mapa_max.append(mapa)
    return kd_mapa_max, empate

#Función que calcula el agente con mayor K/D rate
#y define si es que hay un empate entre 2 agentes
def analizar_kd_agente(df):
    kd_agente_max_num = 0
    kd_agente_max = []
    for agente in AGENTES:
        bajas_totales_agente=df[df['agente'] == agente]['bajas'].sum()
        muertes_totales_agente = df[df['agente'] == agente]['muertes'].sum()
        partidas_totales_agente = df[df['agente'] == agente]['agente'].count()
        #Aquí se protege de errores, si  no hubieron muertes en la partida el K/D rate se define como la cantidad de bajas
        #Además, si no se han jugado partidas con ese agente, el K/D rate es igual a 0
        if partidas_totales_agente==0:
            kd_agente_num=0
        elif muertes_totales_agente==0:
            kd_agente_num=bajas_totales_agente
        else:
            kd_agente_num=bajas_totales_agente/muertes_totales_agente
        if kd_agente_num>kd_agente_max_num:
            kd_agente_max_num=kd_agente_num
            kd_agente_max=[agente]
            empate=False
        elif kd_agente_num==kd_agente_max_num:
            empate=True
            kd_agente_max.append(agente)
    return kd_agente_max, empate

#Función que calcula el mapa con mayor win rate
#y define si es que hay un empate entre 2 mapas
def analizar_wr_mapa(df):
    wr_mapa_max_num = 0
    wr_mapa_max = []
    for mapa in MAPAS:
        victorias_totales_mapa=df[df['mapa'] == mapa]['resultado'].sum()
        partidas_totales_mapa = df[df['mapa'] == mapa]['agente'].count()

        #Aquí se protege de errores, si no se han jugado partidas con ese mapa, el win rate será de 0
        if partidas_totales_mapa==0:
            wr_mapa_num=0
        else:
            wr_mapa_num=victorias_totales_mapa/partidas_totales_mapa
        if wr_mapa_num>wr_mapa_max_num:
            wr_mapa_max_num=wr_mapa_num
            wr_mapa_max=[mapa]
            empate=False
        elif wr_mapa_num==wr_mapa_max_num:
            empate=True
            wr_mapa_max.append(mapa)
    return wr_mapa_max, empate

#Función que calcula el agente con mayor win rate
#y define si es que hay un empate entre 2 agentes
def analizar_wr_agente(df):
    wr_agente_max_num = 0
    wr_agente_max = []
    for agente in AGENTES:
        victorias_totales_agente=df[df['agente'] == agente]['resultado'].sum()
        partidas_totales_agente = df[df['agente'] == agente]['agente'].count()

        # Aquí se protege de errores, si no se han jugado partidas con ese agente, el win rate será de 0
        if partidas_totales_agente == 0:
            wr_agente_num = 0
        else:
            wr_agente_num=victorias_totales_agente/partidas_totales_agente
        if wr_agente_num>wr_agente_max_num:
            wr_agente_max_num=wr_agente_num
            wr_agente_max=[agente]
            empate=False
        elif wr_agente_num==wr_agente_max_num:
            empate=True
            wr_agente_max.append(agente)
    return wr_agente_max, empate

#Función que calcula e imprime los mapas y agentes con mayor win y K/D rate,
#usando funciones para cada valor
#y diferenciando el print dependiendo si hubo un empate entre 2 o más agentes o mapas
def analisis_rendimiento(df):
    kd_mapa_max, empate_mapa_kd=analizar_kd_mapa(df)
    if empate_mapa_kd:
        print(f"\nMapas con mayor K/D: {', '.join(kd_mapa_max)}")
    else:
        print(f"\nMapa con mayor K/D: {', '.join(kd_mapa_max)}")

    kd_agente_max, empate_agente_kd=analizar_kd_agente(df)
    if empate_agente_kd:
        print(f"Agente con mayor K/D: {', '.join(kd_agente_max)}")
    else:
        print(f"Agente con mayor K/D: {', '.join(kd_agente_max)}")

    wr_mapa_max, empate_mapa_wr=analizar_wr_mapa(df)
    if empate_mapa_wr:
        print(f"Mapas con mayor Win Rate: {', '.join(wr_mapa_max)}")
    else:
        print(f"Mapa con mayor Win Rate: {', '.join(wr_mapa_max)}")

    wr_agente_max, empate_agente_wr = analizar_wr_agente(df)
    if empate_agente_wr:
        print(f"Agentes con mayor Win Rate: {', '.join(wr_agente_max)}")
    else:
        print(f"Agente con mayor Win Rate: {', '.join(wr_agente_max)}")


def main():
    verificar_csv()
    #choice inicia con un valor arbitrario, para que sea diferente a 4 y el menú se muestre
    #Después, se mantiene un ciclo en donde se muestra el menú hasta que se selecciona la opción de terminar el código
    choice="inicio"
    print("Este programa tiene como objetivo ayudarte a analizar el rendimiento en tus partidas de Valorant")
    while choice != "salir" and choice != 6:
        print("\nTienes 6 opciones")
        print("1. Registrar partida")
        print("2. Ver estadísticas")
        print("3. Analizar rendimiento")
        #Con el propósito de añadir la función enumerate al código, se incluyeron funciones para mostrar todos los agentes o mapas disponibles
        #Éstas son nuevas funcionalidades con respecto al avance 2, muestran con un for que recorre listas todos los agentes y mapas válidos a incluir
        print("4. Revisar lista de agentes")
        print("5. Revisar lista de mapas")
        print("6. Salir")
        choice=int(input("\nElige la opción que requieras seleccionando el número que le corresponda: "))

        match choice:
            case 1:
                registro()
                datos = verificar_csv()

            #Tanto en la opción 2 como en la opción 3,
            #antes de ejecutar la instrucción, se evalúa que haya partidas que analizar
            #y se indica en el caso de que no haya
            case 2:
                datos=verificar_csv()
                if datos['agente'].count()==0:
                    print("No hay partidas que analizar")
                else:
                    calculo_estadisticas(datos) #Se llama la función para calcular
            case 3:
                datos=verificar_csv()
                if datos['agente'].count()==0:
                    print("No hay partidas que analizar")
                else:
                    analisis_rendimiento(datos)
            case 4:
                print("AGENTES")
                print("-----------------------------------")
                for i, agente in enumerate(AGENTES):
                    print(f"{i}: {agente}")
            case 5:
                print("MAPAS")
                print("-----------------------------------")
                for i, mapa in enumerate(MAPAS):
                    print(f"{i}: {mapa}")
main()
