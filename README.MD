# Analizador Sintáctico Predictivo (PSP)

Este proyecto se trata de un analizador sintáctico predictivo que calcula los conjuntos de **PRIMEROS**, **SIGUIENTES** y **PREDICCIÓN** para una gramática libre de contexto.

## Características

- **Cálculo de PRIMEROS**: El script calcula el conjunto de primeros para cada no terminal en la gramática.
- **Cálculo de SIGUIENTES**: Se determina el conjunto de símbolos que pueden seguir a cada no terminal.
- **Cálculo de PREDICCIÓN**: Genera el conjunto de predicción para cada producción de la gramática.
- **Soporte para gramáticas con ε**: Maneja producciones que pueden derivar en la cadena vacía.

## Cómo usar

### Paso 1: Ejecuta el script

Ejecuta el script `algoritmoPSP.py` desde la línea de comandos:

```bash
python3 algoritmoPSP.py <archivo_gramatica>
```

### Paso 2: Proporciona el archivo de gramática
Asegúrate de que el archivo de gramática tenga el siguiente formato:

```php
<no_terminal> -> <producción_1> | <producción_2> | ...
```
**Ejemplo de gramática:**
```
S -> A B
A -> id | num
B -> + A | - A | ε
```
### Paso 3: Interpretar la salida
El script calculará y mostrará los conjuntos de PRIMEROS, SIGUIENTES y PREDICCIÓN para la gramática especificada. La salida será similar a:

```
Gramática: {'S': [['A', 'B']], 'A': [['id'], ['num']], 'B': [['+', 'A'], ['-', 'A'], ['ε']]}

Conjunto de PRIMEROS:
PRIMEROS(A) = {'num', 'id'}
PRIMEROS(S) = {'num', 'id'}
PRIMEROS(B) = {'-', 'ε', '+'}

Conjunto de SIGUIENTES:
SIGUIENTES(S) = {'$'}
SIGUIENTES(A) = {'-', '$', '+'}
SIGUIENTES(B) = {'$'}

Conjunto de PREDICCIÓN:
PREDICCIÓN(S -> A B) = {'num', 'id'}
PREDICCIÓN(A -> id) = {'id'}
PREDICCIÓN(A -> num) = {'num'}
PREDICCIÓN(B -> + A) = {'+'}
PREDICCIÓN(B -> - A) = {'-'}
PREDICCIÓN(B -> ε) = {'ε'}
```

## Autores
- Santiago Garzón
- Mateo Fonseca
- Karol Guerrero
- Sebastián Barros