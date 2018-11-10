import spacy

spacy.info() # Muestra los metadatos de los modelos.

# Leer el modelo:

# nlp = spacy.load('en') # No funciona en MacOS a menos que antes se corra el siguiente comando con sudo:
# $sudo python -m spacy link MODELO es
# siendo MODELO 'es_core_news_md' o 'es_core_news_sm' (el que se haya descargado).

nlp = spacy.load('/Users/lino/anaconda3/lib/python3.6/site-packages/es_core_news_sm/es_core_news_sm-2.0.0')

# Cargar un texto

doc = nlp(u'Apenas faltan 24 horas para que Tim Cook, consejero delegado de Apple, vuelva al Steve Jobs Theatre, la única zona de su nuevo campus, junto con el centro de visitantes donde pueden acceder los no empleados de la manzana.')

# Tokenización:

tokens = [t.text for t in doc]
tokens_palabras = [t.orth_ for t in doc if not t.is_punct] # Tokens sin signos de puntuación
tokens_enteros = [token.orth for token in doc] # Usa una representación NUMERICA de los tokens
tokens_lexicos = [t.orth_ for t in doc if not t.is_punct | t.is_stop] # Tokens sin puntuación ni stopwords


from spacy.symbols import ORTH, LEMMA, POS, TAG
casos_especiales = [{ORTH: u'a', LEMMA: u'a', POS: u'PREP'}, {ORTH: u'l', LEMMA: u'el', POS: u'DET'}]

nlp.tokenizer.add_special_case(u'al', casos_especiales)

print([w.lemma_ for w in nlp(u'voy al puente')]) # Se comprueba que la regla anterior funciona.

# Etiquetado de POS:

# Las anotaciones son atributos de los tokens. spaCy usa una representación numérica por razones de eficiencia.
# Para obtener una representación legible, se usa underscore al final del atributo.

anotaciones = [(t.text, t.lemma_, t.pos_, t.tag_, t.dep_, t.shape_, t.is_alpha, t.is_stop) for t in doc]
print(anotaciones)

# ATRIBUTOS (nota: esta anotación es estadística y depende del modelo importado)
# text: Forma original del token en el texto.
# lemma: Forma de diccionario del token.
# pos: Clase de palabra general del token.
# tag: POS detallado del token.
# dep: Dependencia sintáctica del token en relación con otras palabras.
# shape: Esquema del la forma de la palabra; mayúsculas, puntuación, dígitos.
# is_alpha: True si está compuesto de caracteres alfabéticos.
# is_stop: True si es una stopword (palabras funcionales, palabras muy comunes, etc.)

# PARSING:

# Chunks nominales

doc.is_parsed # Devuelve True si el documento fue parseado correctamente.

chunks = [(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text) for chunk in doc.noun_chunks]
print(chunks)

# ATRIBUTOS
# text: Forma original del token en el texto.
# root.text: Forma original de la palabra que conecta el chunk con el resto del parsing.
# root.dep: Relación de dependencia que conecta el núcleo del chunk con la raíz de la que parte el chunk.
# root.head text: El texto del token que es núcleo de la raíz de la que parte el chunk.

# Arbol de dependencias

# En un árbol de dependencias, head es el nodo madre y child el nodo hija (los dos puntos de un arco o dep).
# El arco dep indica la relación entre head y child.

for t in doc:
    print(t.text, t.dep_, t.head.text, t.head.pos_,
          [child for child in t.children])

# ATRITUBOS
# text: Forma original del token en el texto.
# dep: Relación sintáctica que conecta child con head.
# head.text: Texto del nodo head del que depende el token.
# head.pos_: Clase de palabra del head del que depende el token.
# children: Constituyentes inmediatos del token.
# lefts: Secuencia de hijos a la izquierda del token.
# n_lefts: Da el número de hijos a la izquierda del token.
# rights: Secuencia de hijos a la derecha del token.
# n_rights: Da el número de hijos a la derecha del token.
# subtree: Recorre un sub-árbol de un token.
# ancestors: Devuelve los ancestros de un token
# is_ancestor(Y): Devuelve True si el ancestro es Y.
# left_edge: Primer token se un sub-árbol.
# right_edge: Último token de un sub-árbol.


# Recorrer hacia ARRIBA el árbol para buscar una secuencia de interés

from spacy.symbols import nsubj, VERB

verbs = set()
for sujeto_posible in doc:
    if sujeto_posible.dep == nsubj and sujeto_posible.head.pos == VERB: # token = sujeto y head = verbo
        verbs.add(sujeto_posible.head)
print(verbs)

print([token.text for token in doc[3].lefts])
print(doc[3].n_lefts)

# Recorrer el árbol con subtree para obtener una secuencia ordanada que funciona como un frase.

doc2 = nlp(u"La conferencia de Apple del próximo 13 de septiembre será la más importante de los últimos años.")

root = [t for t in doc2 if t.head == t][0]
sujeto = list(root.lefts)[0]
for descendiente in sujeto.subtree:
    assert sujeto is descendiente or sujeto.is_ancestor(descendiente)
    print(descendiente.text, descendiente.dep_, descendiente.n_lefts,
          descendiente.n_rights,
          [ancestro.text for ancestro in descendiente.ancestors])

# Se usa left_edge y right_edge para seleccionar un span completo:

span = doc2[doc2[1].left_edge.i : doc2[1].right_edge.i+1] # Este span engloba al Sujeto.
span.merge()
for t in doc2:
    print(t.text, t.pos_, t.dep_, t.head.text)

# Visualización de un árbol de dependencias
# displacy acepta tanto un doc como una lista de docs.

from spacy import displacy
displacy.render(doc, style='dep', jupyter=True) # Versión para Jupyter Notebook
displacy.render(doc, style='dep') # Versión HTML
displacy.serve([doc, doc2], style='dep') # Levanta un servidor en http://localhost:5000 (es el método más sencillo)

# Reconocimiento de entidades (Named Entities)

for ent in doc.ents: # Esta forma itera el documento completo.
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

# ATRIBUTOS
# text: Forma original del token en el texto.
# start_char: Index del comienzo de la entidad en el Doc.
# end_char: Index del final de la entidad en el Doc.
# label_: Tipo de entidad.

# Visualización de las entidades reconocidas

from spacy import displacy

doc3 = nlp(u'Si Sherlock Holmes estuviese vivo, trabajaría para Google en New York, hablaría Japonés, y usaría un Audi.')


displacy.serve(doc3, style='ent')

doc3.user_data['title'] = 'Organizaciones'
colors = {'ORG': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)'} # Destacar uno o varios tipos de entidades por color.
options = {'ents': ['ORG'], 'colors': colors}
displacy.serve(doc3, style='ent', options=options)

# Segmentación de oraciones

# La segmentación en spaCy se realiza, por defecto, a partir del análisis de dependencias.

doc4 = nlp(u"Esta es la primera oración. Esta es la segunda.")

for oracion in doc4.sents:
    print(oracion.text)

