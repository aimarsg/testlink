#################################################################
## marcar en formato BIO los RML y EVENT del conjunto de datos ##
#################################################################

def obtenerIndices(relEvs):
    #Extraer los indices de RML y EVENT de los rels
    res = []
    #listaRels = relEvs.split('\n')
    for linea in relEvs:
        if linea: #solo coger lineas NO vacias
            elems = linea.split('\t') # 2:RML 3:EVENT

            indicesRml = elems[2].split('-')
            inicioRml = indicesRml[0]
            finRml = indicesRml[1]
            rml = (inicioRml, finRml, "rml")

            indicesEv = elems[3].split('-')
            inicioEv = indicesEv[0]
            finEv = indicesEv[1]
            event = (inicioEv, finEv, "event")

            res.append(rml)
            res.append(event)
    return(res)

def ordenarRels(tupla):
    return(int(tupla[0])) #devuelve el indice de inicio

def insertarMarcas(elem1, elem2, texto):
    elements = []
    elements.append(elem1)
    elements.append(elem2)
    elements = sorted(elements, key=ordenarRels)
    # volver a coger los ev y rml una vez ordenados
    elem1 = elements[0]
    elem2 = elements[1]


    if elem2[2] == 'event':
        # si es event añadimos <TOKEV>
        texto = texto[:int(elem2[1])] + '<TOKEV>' + texto[int(elem2[1]):]  # añadir al final
        texto = texto[:int(elem2[0])] + '<TOKEV>' + texto[int(elem2[0]):]  # añadir al principio

    if elem2[2] == 'rml':
        # si es event añadimos <TOKRML>
        texto = texto[:int(elem2[1])] + '<TOKRML>' + texto[int(elem2[1]):]  # añadir al final
        texto = texto[:int(elem2[0])] + '<TOKRML>' + texto[int(elem2[0]):]  # añadir al principio

    if elem1[2] == 'event':
        # si es event añadimos <TOKEV>
        texto = texto[:int(elem1[1])] + '<TOKEV>' + texto[int(elem1[1]):]  # añadir al final
        texto = texto[:int(elem1[0])] + '<TOKEV>' + texto[int(elem1[0]):]  # añadir al principio

    if elem1[2] == 'rml':
        # si es event añadimos <TOKRML>
        texto = texto[:int(elem1[1])] + '<TOKRML>' + texto[int(elem1[1]):]  # añadir al final
        texto = texto[:int(elem1[0])] + '<TOKRML>' + texto[int(elem1[0]):]  # añadir al principio

    return texto

def marcarTexto(rels, fich, resultado):
    fich = fich.rstrip('\n')
    i = 0

    while i < len(rels):
        # generar ejemplo positivo

        elem1 = rels[i] # indice del elemento 1 -  RML
        elem2 = rels[i+1] # indice del elemento 2- EVENT
        texto = fich
        texto = insertarMarcas(elem1, elem2, texto)

        resultado.write(texto+'\t'+str(1)+'\n')

        #generar ejemplos negativos
        i += 2
        j= i
        while j < len(rels):
            #recorrer siguientes ev y rel
            if elem1[2] == 'event': #elem 1 EVENT y elem2 RML
                elemEv = rels[j+1]
                elemRml = rels[j]

                #emparejar ELEM1 con los rml de los demas
                if elemEv[0] != elem1[0] and elemRml[0] != elem2[0]: #si no son la misma palabra
                    textoN =fich
                    textoN = insertarMarcas(elem1, elemRml, textoN)
                    resultado.write(textoN + '\t' + str(0) + '\n')

                    # emparejar ELEM2 con event de los demas

                    textoN = fich
                    textoN = insertarMarcas(elem2, elemEv, textoN)
                    resultado.write(textoN + '\t' + str(0) + '\n')

            else: #elem1 RML elm2 EVENT
                elemEv = rels[j + 1]
                elemRml = rels[j]

                # emparejar ELEM1 con los rml de los demas
                if elemEv[0] != elem2[0] and elemRml[0] != elem1[0]:  # si no son la misma palabra
                    textoN = fich
                    textoN = insertarMarcas(elem1, elemEv, textoN)
                    resultado.write(textoN + '\t' + str(0) + '\n')

                    # emparejar ELEM2 con event de los demas

                    textoN = fich
                    textoN = insertarMarcas(elem2, elemRml, textoN)
                    resultado.write(textoN + '\t' + str(0) + '\n')

            j += 2


if __name__ == "__main__":

    archivo = open('training.txt', 'r',  encoding='utf-8')
    resultado = open('trainingParaDocumentClassification.txt', 'w',  encoding='utf-8')
    doc = []
    numDoc = 0

    for linea in archivo:
        #strip para quitar todos los espacios en blanco de la linea
        if linea.strip() != '': #si no es linea vacia
            doc.append(linea) #añadir la linea al documento
        else:
            #linea vacia -> documento nuevo
            indices = []
            texto = doc[0].split("|t|")[1]
            numDoc = doc[0].split("|t|")[0]

            #resultado = open('./res/doc'+str(numDoc)+'.txt', 'w',  encoding='utf-8')


            if len(doc)>1: #si existen indices obtenerlos
                indices = obtenerIndices(doc[1:len(doc)])

            res = marcarTexto(indices, texto, resultado)
            #reiniciar variables
            doc = []
            #numDoc+= 1
            #resultado.write(res)

    if len(doc)>1:
        indices = []
        texto = doc[0].split("|t|")[1]
        numDoc = doc[0].split("|t|")[0]

        #resultado = open('./res/doc'+str(numDoc)+'.txt', 'w',  encoding='utf-8')


        if len(doc)>1: #si existen indices obtenerlos
            indices = obtenerIndices(doc[1:len(doc)])

        res = marcarTexto(indices, texto, resultado)

        #resultado.write(res)


    archivo.close()
    resultado.close()