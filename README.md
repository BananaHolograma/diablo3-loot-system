# Python virtual env packages

`pip install -r requirements.txt`

# Aproximación sistema de loot Diablo 3

## El equipamiento se divide en:

Yelmo
Peto
hombros
brazos
cinto
piernas
pies
2 \***_anillos_**
amuleto
arma 2 manos
arma 1 mano + extra (escudo, orbe, etc)

Esto influye a la hora de seleccionar un rango amplio de objetos a la hora de lootear por lo que da una experiencia mas variada

## Rareza del objeto

La rareza del objeto se divide en:
Normal,Magico,Raro,Legendario,Legendario ancestral, Legendario ancestral primigenio, Conjunto (ancestral, primigenio)

Las piezas de conjunto tienen efectos adicionales si se equipan varias de las piezas.
Ademas de la rareza, el equipo tiene su propio nivel que va acorde con el personaje esto quiere decir que las estadísticas generadas del objeto tendran esta limitación y habra que formar un calculo para ello.

Para empezar a poder lootear legendarios y piezas de conjunto el personaje debe ser nivel 70.

Si en el loot aparece un legendario, hay una posibilidad 1 entre x (habra que definir x) de que este sea ancestral o primigenio los cuales pueden ofrecer estadisticas mas altas.

Los objetos de tipo ancestral o primigenio solo se podran acceder si se jugan fallas de nivel superior +70 en dificultades superiores a tormento I

## Exclusividad de equipo

Hay equipo global que puede usar cualquier personaje pero su generación será diferente, si el atributo principal es inteligencia, estos objetos vendran con propiedades mágicas acorde a este atributo o habilidades que solo la clase puede utilizar.

Segun la clase elejida habra equipamiento especial o conjuntos que solo se podra desbloquear con esa clase en particular,

## Nivel y dificultad

El nivel y la dificultad en la que se está jugando influye en los porcentajes de loot para los objetos legendarios y de conjunto.

## Rango de estadisticas

El equipamiento se lootea con unas estadísticas aleatorios siempre en base a unas reglas básicas que ese objeto puede admitir y pueden ser por ejemplo, entre 700 y 1000 de daño, 4 propiedades magicas aleatorias, inteligencia del personaje \* 0.4 + (400 ~700) y un largo etc.

## Origen del loot

Este apartado se refiere a si se ha abierto un cofre, matado un enemigo, completado un evento. Segun el origen, el proceso de loot recibirá ciertas reglas y calculos especiales para ese loot en especifico.

Condition: killed_entity
entity_type: diablo:skeleton
