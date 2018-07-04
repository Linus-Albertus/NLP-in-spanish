# -*- encoding: utf-8 -*-

# ----------------------------------------------------------------------------------
#                                          Silabador
# ----------------------------------------------------------------------------------
#                       Lino A. Urdaneta F.   13/08/2010
#
# Se trata de un script para separar silábicamente una palabra en español.
# El código es horrible porque lo hice cuando estaba empezando a aprender Python, y no conocía muchos de los métodos y
# módulos más usuales. En mi defensa, funciona.
#
# El silabador utiliza un algoritmo que separa primero las sílabas utilizando la información de las consonantes, y luego
# utiliza la información proporcionada por las vocales para completar el análisis.

# --- Importar módulos: ---

import os

# --- Funciones: ---

class Silaba:
    """Admite una palabra simple (token) y la separa en sílabas. La separación se marca con espacios.
    Se usa así: objeto = Silaba(cadena).
    objeto.silabas() devuelve una cadena de sílabas separadas por espacios.
    """

    def __init__(self, palabra):
        self.palabra = palabra
        print('(Admite la palabra {0})'.format(self.palabra))

    def silabas(self):
        """Realiza la separación en sílabas."""

        def extraer_prefijo(palabra):  # Separa algunos prefijos de la raíz de la palabra. Hay que
            for prefijo in ['super', 'mini']:  # tener cuidado porque no distingue entre un prefijo
                prefijo_con_espacio = prefijo + ' '  # real y uno que no lo es.
                self.palabra = palabra.replace(prefijo, prefijo_con_espacio, 1)
            return palabra

        def es_consonante(letra):
            consonantes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v',
                           'w', 'x',
                           'y', 'z']
            if letra in consonantes:
                return True
            else:
                return False

        def con_liquidas(letra):
            consonantes = ['b', 'c', 'f', 'g', 'l', 'p', 't']
            if letra in consonantes:
                return True
            else:
                return False

        def con_vibrantes(letra):
            consonantes = ['b', 'c', 'd', 'f', 'g', 'k', 'p', 't', 'r']
            if letra in consonantes:
                return True
            else:
                return False

        def es_vocal(letra):
            vocales = ['a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú', 'ü']
            if letra in vocales:
                return True
            else:
                return False

        def es_vocal_debil(letra):
            vocales = ['i', 'u', 'ü']
            if letra in vocales:
                return True
            else:
                return False

        def es_debil_acentuada(letra):
            vocales = ['í', 'ú']
            if letra in vocales:
                return True
            else:
                return False

        def es_vocal_fuerte(letra):
            vocales = ['a', 'e', 'o', 'á', 'é', 'ó']
            if letra in vocales:
                return True
            else:
                return False

        def separador_consonantico(palabra):
            consonantes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v',
                           'w', 'x',
                           'y', 'z']
            satelites = ['l', 'r']
            self.contador = 0
            salida = ''
            # Si la palabra consta de una sola letra no entrar al bucle principal:
            if len(palabra) == 1:
                return palabra
            # Bucle principal:
            while self.contador < len(palabra):
                # Si la palabra termina en consonante se ignora y termina el bucle:
                if self.contador == len(palabra) - 1 and es_consonante(palabra[self.contador]):
                    salida += palabra[self.contador]
                    return salida
                # Si la palabra empieza con una consonante se ignora:
                if self.contador == 0 and es_consonante(palabra[0]):
                    self.contador += 1
                    salida += palabra[0]
                # Si la segunda letra es también una consonante, también se ignora:
                if self.contador == 1 and es_consonante(palabra[1]) and es_consonante(palabra[0]):
                    self.contador += 1
                    salida += palabra[1]
                # Si la palabra tiene solo dos letras, empieza con vocal, y sigue con una consonante:
                if self.contador == 0 and not palabra[0] in consonantes and es_consonante(palabra[1]) and len(palabra) == 2:
                    salida += palabra[0] + palabra[1]
                    return palabra
                # Si la palabra empieza con vocal, y sigue con una consonante, separar ambas ( <axyyyy> --> <a/xyyyy> ):
                elif self.contador == 0 and not palabra[0] in consonantes and es_consonante(
                        palabra[1]) and not es_consonante(
                        palabra[2]):
                    salida += palabra[0] + ' ' + palabra[1]
                    self.contador += 2
                # Analiza correctamente palabras como "zinc":
                elif self.contador == len(palabra) - 2 and palabra[self.contador] == 'n' and palabra[self.contador + 1] == 'c':
                    salida += 'n' + 'c'
                    self.contador += 2
                # Si el dígrafo <ch> está al final de la palabra, no se separa de la sílaba anterior:
                elif (self.contador == len(palabra) - 2) and es_consonante(palabra[self.contador]) and palabra[
                    self.contador + 1] == 'h':
                    salida += palabra[self.contador] + 'h'
                    self.contador += 2
                # Si se encuentra el dígrafo <ch>, no se separa:
                elif palabra[self.contador] == 'c' and palabra[self.contador + 1] == 'h':
                    salida += ' ch'
                    self.contador += 2
                elif es_consonante(palabra[self.contador]) and palabra[self.contador + 1] == 'c' and palabra[self.contador + 2] == 'h':
                    salida += palabra[self.contador] + ' ch'
                    self.contador += 3
                # Si no es consonante, se ignora:
                elif not es_consonante(palabra[self.contador]):
                    salida += palabra[self.contador]
                    self.contador += 1
                # Si es una consonante, y la siguiente letra no lo es, se inserta un espacio antes de la consonante:
                elif es_consonante(palabra[self.contador]) and not es_consonante(palabra[self.contador + 1]):
                    salida += ' ' + palabra[self.contador] + palabra[self.contador + 1]
                    self.contador += 2
                # Revisa si una palabra termina en dos consonantes y termina el bucle en caso afirmativo (a menos que la última letra sea <y>):
                elif self.contador == len(palabra) - 2 and es_consonante(palabra[self.contador]) and es_consonante(
                        palabra[self.contador + 1]) and palabra[self.contador + 1] != 'y':
                    salida += palabra[self.contador] + palabra[self.contador + 1]
                    return salida
                # Revisa si una palabra termina en consonante y en <y> y termina el bucle en caso afirmativo:
                elif self.contador == len(palabra) - 3 and es_consonante(palabra[self.contador]) and es_consonante(
                        palabra[self.contador + 1]) and palabra[self.contador + 2] == 'y':
                    salida += palabra[self.contador] + ' ' + palabra[self.contador + 1] + 'y'
                    return salida
                elif self.contador == len(palabra) - 2 and es_consonante(palabra[self.contador]) and es_consonante(
                        palabra[self.contador + 1]) and palabra[self.contador + 1] == 'y':
                    salida += ' ' + palabra[self.contador] + palabra[self.contador + 1]
                    return salida
                elif (palabra[self.contador] and palabra[self.contador + 1]) in consonantes and not es_consonante(
                        palabra[self.contador + 2]) \
                        and not palabra[self.contador + 1] in satelites:
                    salida += palabra[self.contador] + ' ' + palabra[self.contador + 1]
                    self.contador += 2
                # Busca grupos <xl>, los mantiene unidos e inserta un espacio antes de los mismos:
                elif con_liquidas(palabra[self.contador]) and palabra[self.contador + 1] == 'l' and not es_consonante(
                        palabra[self.contador + 2]):
                    salida += ' ' + palabra[self.contador] + palabra[self.contador + 1]
                    self.contador += 2
                # Busca grupos <xr>, los mantiene unidos e inserta un espacio antes de los mismos:
                elif con_vibrantes(palabra[self.contador]) and palabra[self.contador + 1] == 'r' and not es_consonante(
                        palabra[self.contador + 2]):
                    salida += ' ' + palabra[self.contador] + palabra[self.contador + 1]
                    self.contador += 2
                # Separa <r/l> o <l/r> cuando están rodeadas por vocales:
                elif ((palabra[self.contador] == 'r' and palabra[self.contador + 1] == 'l') or (
                        palabra[self.contador] == 'l' and palabra[self.contador + 1] == 'r')) and not (
                        (palabra[self.contador - 1] and palabra[self.contador + 2]) in consonantes):
                    salida += palabra[self.contador] + ' ' + palabra[self.contador + 1]
                    self.contador += 2
                elif (palabra[self.contador] and palabra[self.contador + 1] and palabra[self.contador + 2]) in consonantes and not \
                palabra[
                    self.contador + 2] in satelites \
                        and not palabra[self.contador + 3] in consonantes:
                    salida += palabra[self.contador] + palabra[self.contador + 1] + ' ' + palabra[self.contador + 2]
                    self.contador += 3
                elif not palabra[self.contador - 1] in consonantes and (
                        palabra[self.contador] and palabra[self.contador + 1]) in consonantes and palabra[
                    self.contador + 2] in satelites:
                    salida += palabra[self.contador] + ' ' + palabra[self.contador + 1] + palabra[self.contador + 2]
                    self.contador += 3
                elif (palabra[self.contador] and palabra[self.contador + 1] and palabra[self.contador + 2]) in consonantes and palabra[
                    self.contador + 3] in satelites:
                    salida += palabra[self.contador] + palabra[self.contador + 1] + ' ' + palabra[self.contador + 2] + palabra[
                        self.contador + 3]
                    self.contador += 4
                else:
                    salida += palabra[self.contador]
                    self.contador += 1
            return salida  # revisar decidnoslo brandy cinc corps

        def separador_vocalico(palabra):
            contador = 0
            salida = ''
            while contador < len(palabra):
                if contador == len(palabra) - 1 and es_vocal(palabra[contador]):
                    salida += palabra[contador]
                    return salida
                if es_vocal(palabra[contador]) and es_vocal(palabra[contador + 1]):
                    vocal = palabra[contador]
                    vocal_siguiente = palabra[contador + 1]
                    if es_vocal_debil(vocal) and es_vocal_debil(vocal):
                        salida += vocal
                        contador += 1
                    elif (es_vocal_debil(vocal) and es_vocal_fuerte(vocal_siguiente)) or (
                            es_vocal_fuerte(vocal) and es_vocal_debil(vocal_siguiente)):
                        salida += vocal
                        contador += 1
                    elif (es_vocal_fuerte(vocal) and es_debil_acentuada(vocal_siguiente)) or (
                            es_debil_acentuada(vocal) and es_vocal_fuerte(vocal_siguiente)):
                        salida += vocal + ' '
                        contador += 1
                    elif es_vocal_fuerte(vocal) and es_vocal_fuerte(vocal_siguiente):
                        salida += vocal + ' '
                        contador += 1
                else:
                    salida += palabra[contador]
                    contador += 1
            return salida
        self.silabas_separadas = separador_vocalico(separador_consonantico(self.palabra))
        return self.silabas_separadas

    def contar(self):
        """Devuelve el número de sílabas de la cadena como entero."""
        return self.silabas_separadas.count(' ') + 1


def matriz_nula(filas, columnas):
    M = []
    for i in range(filas):
        M.append([None] * columnas)
    return M

def copiar_matriz(origen, destino):  # Esto es un procedimiento. Destino debe ser igual o más grande que Origen.
    for fila in range(len(origen)):
        for columna in range(len(origen[0])):
            celda_o = origen[fila][columna]
            destino[fila][columna] = celda_o

def sin_repetidos(lista):
    resultado = []
    for elemento in lista:
        if elemento not in resultado:
            resultado.append(elemento)
    return resultado

def limpiar_texto(cadena):
    salida = ''
    for i in cadena:
        if 97 <= ord(i) <= 122 or i == ' ':
            salida += i
        for j in ['ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü']:
            if i == j:
                salida += j
    return salida


# -----------------------------------------------------------------------
# Programa principal:
# -----------------------------------------------------------------------

if os.path.exists('/Users/lino/Dropbox/Python/Silabador'):
    # --- Apertura de los archivos: ---

    texto_entrada = open('/Users/lino/Dropbox/Python/Silabador/corpus_silabador.txt', 'rt', encoding="UTF-8")
    tabla_bigramas = open('/Users/lino/Dropbox/Python/Silabador/tabla_de_silabas.txt', 'w')

# --- Limpieza del texto y segmentación del mismo en una lista de palabras: ---

texto = ''
for linea in texto_entrada:  # Esto convierte el texto de entrada en una cadena
    texto += linea + ' '

texto_limpio = limpiar_texto(texto.lower())
texto_segmentado = texto_limpio.split()

# --- Divide las palabras del texto_segmentado en sílabas: ---

lista_silabas_redundante = []
for palabra in texto_segmentado:
    try:
        # print(palabra) # Esto se activa para verificar.
        s = Silaba(palabra)
        segmentos = s.silabas()
        segmentos_sin_tilde = ''
        for k in segmentos:
            if k == 'á':
                segmentos_sin_tilde += 'a'
            elif k == 'é':
                segmentos_sin_tilde += 'e'
            elif k == 'í':
                segmentos_sin_tilde += 'i'
            elif k == 'ó':
                segmentos_sin_tilde += 'o'
            elif k == 'ú':
                segmentos_sin_tilde += 'u'
            else:
                segmentos_sin_tilde += k
        lista_segmentos = segmentos_sin_tilde.split()
        for silaba in lista_segmentos:
            lista_silabas_redundante.append(silaba)
    except:
        print('Palabra excluida del análisis: %s' % palabra)

# --- Crea una lista no redundante de las sílabas del texto: ---

lista_silabas_no_redundante = sin_repetidos(lista_silabas_redundante)

# --- Crea una tabla con la lista no redundante de sílabas: ---

tabla_de_silabas = matriz_nula(len(lista_silabas_no_redundante), 3)

for elemento in range(len(lista_silabas_no_redundante)):
    tabla_de_silabas[elemento][0] = lista_silabas_no_redundante[elemento]

tabla_de_silabas.sort()  # Ordena alfabéticamente la lista

# --- Conteo de las sílabas en una tabla: ---

contador_total = 0
for elemento_tabla in range(len(tabla_de_silabas)):
    elemento_a_comparar = tabla_de_silabas[elemento_tabla][0]
    contador = 0
    for elemento_no_redundante in lista_silabas_redundante:
        if elemento_no_redundante == elemento_a_comparar:
            contador += 1
    tabla_de_silabas[elemento_tabla][1] = contador
    contador_total += contador

# --- Cálculo de probabilidades: ---

for elemento_tabla in range(len(tabla_de_silabas)):
    tabla_de_silabas[elemento_tabla][2] = tabla_de_silabas[elemento_tabla][1] / contador_total

for i in tabla_de_silabas:
    print(i)
print('El total de sílabas DIFERENTES es %d' % len(tabla_de_silabas))
print('El total de sílabas es %d' % contador_total)
