import sys

# Función para leer la gramática desde un archivo
def leer_gramatica(archivo):
    gramatica = {}
    with open(archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            no_terminal, producciones = linea.split('->')
            no_terminal = no_terminal.strip()
            producciones = [p.strip().split() for p in producciones.split('|')]
            gramatica[no_terminal] = producciones
    return gramatica

# Diccionarios globales para PRIMEROS y SIGUIENTES
primeros = {}
siguientes = {}
en_proceso = {}

# Función para calcular el conjunto de primeros de un símbolo
def primeros_de_simbolo(simbolo):
    if simbolo not in gramatica:
        # Si el símbolo no está en la gramática, es terminal, no calcular PRIMEROS para terminales
        return {simbolo}

    if en_proceso.get(simbolo, False):
        return primeros[simbolo]
    
    if simbolo in primeros:
        return primeros[simbolo]
    
    en_proceso[simbolo] = True
    resultado = set()

    # Solo calcular primeros para símbolos no terminales
    if simbolo in gramatica:  
        for produccion in gramatica[simbolo]:
            for s in produccion:
                if s == simbolo:  # Evitar la recursión infinita para producciones recursivas directas
                    break
                primeros_s = primeros_de_simbolo(s)
                resultado.update(primeros_s - {'ε'})
                if 'ε' not in primeros_s:
                    break
            else:
                resultado.add('ε')
    else:
        resultado.add(simbolo)  # En este punto ya sabemos que es terminal

    primeros[simbolo] = resultado
    en_proceso[simbolo] = False
    return resultado

# Función para calcular el conjunto de PRIMEROS de toda la gramática
def calcular_primeros(gramatica):
    for nt in gramatica:
        primeros_de_simbolo(nt)
    return primeros


# Función para calcular el conjunto de SIGUIENTES
def calcular_siguientes(gramatica, primeros):
    for nt in gramatica:
        siguientes[nt] = set()

    siguientes[list(gramatica.keys())[0]].add('$')  # Agregar el símbolo de fin de cadena al primer no terminal

    cambio = True
    while cambio:
        cambio = False
        for nt in gramatica:
            for produccion in gramatica[nt]:
                for i, simbolo in enumerate(produccion):
                    if simbolo in gramatica:  # Solo calcular SIGUIENTES para no terminales
                        siguientes_de_simbolo = siguientes[simbolo]
                        siguiente_temporal = set()
                        for s in produccion[i+1:]:
                            if s in gramatica:  # Si es un no terminal
                                primeros_s = primeros[s] - {'ε'}
                                siguiente_temporal.update(primeros_s)
                                if 'ε' not in primeros[s]:
                                    break
                            else:  # Si es un terminal
                                siguiente_temporal.add(s)
                                break
                        else:
                            siguiente_temporal.update(siguientes[nt])

                        if not siguiente_temporal.issubset(siguientes_de_simbolo):
                            siguientes[simbolo].update(siguiente_temporal)
                            cambio = True
    return siguientes

# Función para calcular el conjunto de predicción
def calcular_prediccion(gramatica, primeros, siguientes):
    prediccion = {}
    
    for nt, producciones in gramatica.items():
        prediccion[nt] = []  # Inicializa la lista de predicciones para el no terminal
        for produccion in producciones:
            prediccion_produccion = set()
            puede_derivar_epsilon = False
            
            for simbolo in produccion:
                if simbolo not in gramatica:  # Si es terminal
                    prediccion_produccion.add(simbolo)
                    break  # Salimos porque encontramos un terminal
                else:  # Si es no terminal
                    prediccion_produccion.update(primeros[simbolo] - {'ε'})
                    if 'ε' not in primeros[simbolo]:  # Si no hay ε, salimos del bucle
                        break
                    else:
                        puede_derivar_epsilon = True
            
            # Si se puede derivar ε, agregamos los SIGUIENTES
            if puede_derivar_epsilon:
                prediccion_produccion.update(siguientes[nt])

            # Si la producción es ε y puede derivar en ε, la agregamos
            if all(simbolo == 'ε' for simbolo in produccion):
                prediccion_produccion.add('ε')

            prediccion[nt].append(prediccion_produccion)  # Agregamos el conjunto a la lista de predicción

    return prediccion


 

# Función principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python algoritmoPSP.py <archivo_gramatica>")
        sys.exit(1)

    archivo_gramatica = sys.argv[1]
    global gramatica
    gramatica = leer_gramatica(archivo_gramatica)

    print("Gramática:", gramatica)

    # Calcular PRIMEROS
    primeros = calcular_primeros(gramatica)
    print("\nConjunto de PRIMEROS:")
    for nt, conjunto in primeros.items():
        print(f"PRIMEROS({nt}) = {conjunto}")

    # Calcular SIGUIENTES
    siguientes = calcular_siguientes(gramatica, primeros)
    print("\nConjunto de SIGUIENTES:")
    for nt, conjunto in siguientes.items():
        print(f"SIGUIENTES({nt}) = {conjunto}")

    # Calcular PREDICCIÓN
    prediccion = calcular_prediccion(gramatica, primeros, siguientes)
    print("\nConjunto de PREDICCIÓN:")
    for nt, producciones in prediccion.items():
        for i, conjunto in enumerate(producciones):
            # Aquí es donde se hace la impresión correctamente
            print(f"PREDICCIÓN({nt} -> {' '.join(gramatica[nt][i])}) = {conjunto}")

if __name__ == "__main__":
    main()
