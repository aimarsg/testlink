#################################################################
## marcar en formato BIO los RML y EVENT del conjunto de datos ##
#################################################################

def obtenerIndices(relEvs):
    #Extraer los indices de RML y EVENT de los rels
    res = []
    #listaRels = relEvs.split('\n')
    for linea in relEvs:
        if linea:
            elems = linea.split('\t') # 2:RML 3:EVENT

            indicesRml = elems[2].split('-')
            inicioRml = indicesRml[0]
            finRml = indicesRml[1]
            rml = (inicioRml, finRml, "rml")

            indicesEv = elems[3].split('-')
            inicioEv = indicesEv[0]
            finEv = indicesEv[1]        
            event = (inicioEv, finEv, "event")

            if rml not in res:
                res.append(rml)
            if event not in res:
                res.append(event)
    return(res)

def ordenarRels(tupla):
    return(int(tupla[0])) #devuelve el indice de inicio



def marcarTexto(text, rels, fich):
    word_tag = []
    rels_ord = sorted(rels, key = ordenarRels)
    i = 0 #indice del texto
    j = 0 #indice para recorrer rels
    f = False
    for word in text.split():
        if j<len(rels):
            #si la palabra empieza por parentesis ignorarla para que coincidan los indices
            if (word[0] == '('):
                i += 1
                word = word.rstrip("(")
            if i==int(rels_ord[j][0]) or f:
                #marcar
                if i+len(word.rstrip(".,()"))==int(rels_ord[j][1]):
                    if f:
                        t = (word, 'I-'+rels_ord[j][2])
                        f = False
                    else:
                        t = (word, 'B-'+rels_ord[j][2])
                    
                    j=j+1
                else:
                    if f:
                        t = (word, 'I-'+rels_ord[j][2])
                    else:
                        f = True
                        t = (word, 'B-'+rels_ord[j][2])
            else:
                t = (word, 'O')
        else:
            t = (word, 'O')
        word_tag.append(t)
        cadena = '\t'.join(map(str, t))
        fich.write(cadena+'\n')
        i = i+len(word)

        #restar al indice lo que se ha sumado en caso de que la palabra empiece por parentesis
        if (word[0] == '('):
            i -= 1

        #contar espacios tras la palabra
        t =False
        while not t and i<len(text)-2:
            if text[i]==(' '):
                i=i+1
            else:
                t=True
    return word_tag

    



if __name__ == "__main__":
    
    archivo = open('100098.txt', 'r',  encoding='utf-8')
    #resultado = open('res.txt', 'w',  encoding='utf-8')
    doc = []
    numDoc = 0

    for linea in archivo:
        if linea.strip() != '':
            doc.append(linea)
        else:
            #linea vacia -> documento nuevo
            indices = []
            texto = doc[0].split("|t|")[1]
            numDoc = doc[0].split("|t|")[0]

            resultado = open('./res/doc'+str(numDoc)+'.txt', 'w',  encoding='utf-8')
            

            if len(doc)>1: #si existen indices obtenerlos
                indices = obtenerIndices(doc[1:len(doc)])

            res = marcarTexto(texto, indices, resultado)
            #reiniciar variables
            doc = []
            #numDoc+= 1
            #resultado.write(res)

    if len(doc)>1:
        indices = []
        texto = doc[0].split("|t|")[1]
        numDoc = doc[0].split("|t|")[0]
        
        resultado = open('./res/doc'+str(numDoc)+'.txt', 'w',  encoding='utf-8')
        

        if len(doc)>1: #si existen indices obtenerlos
            indices = obtenerIndices(doc[1:len(doc)])

        res = marcarTexto(texto, indices, resultado)

        #resultado.write(res)


    archivo.close()
    resultado.close()



'''

textoO = """Paciente de 65 a. de edad, que presentaba una elevación progresiva de las cifras de PSA desde 6 ng/ml a 12 ng/ml en el último año. Dicho paciente había sido sometido un año antes a una biopsia transrectal de próstata ecodirigida por sextantes que fue negativa.  Se decide, ante la elevación del PSA, realizar una E-RME previa a la 2ª biopsia transrectal, en la que se objetiva una lesión hipointensa que abarca zona central i periférica del ápex del lóbulo D prostático. El estudio espectroscópico de ésta lesión mostró una curva de colina discretamente más elevada que la curva de citrato, con un índice de Ch-Cr/Ci > 0,80, que sugería la presencia de lesión neoplásica, por lo que se biopsia dicha zona por ecografía transrectal. La AP de la biopsia confirmó la presencia de un ADK próstata Gleason 6."""
rel = """100001	REL	94-101		84-87		6 ng/ml	PSA

100001	REL	104-112	84-87		12 ng/ml	PSA

100001	REL	251-259	185-192	negativa	biopsia

100001	REL	619-623	598-604	0,80		índice"""
'''

'''
    textoMarcado = marcarTexto(texto, obtenerIndices(rel))
    for palabra in textoMarcado:
        print(palabra[0]+'\t'+palabra[1])'''

"""

def marcarTexto(text, rels):
    words = text.split(" ")
    word_tag = []
    word_dict = {} #crear un diccionario con palabras y tags

    #inicializar todas las palabras con O
    for word in words:
        word_dict[word] = 'O'
    
    #
    for inicio, fin, tag in rels:
        

        frag = text[inicio:fin]
        pals = frag.split()
        if (len(pals)>1): #hay mas de una palabra
            word_dict[pals[0]] = 'B-' + tag
            for i in range (1, len(pals)-1):
                word_dict[pals[i]] = 'I-' + tag
        else:
            word_dict[frag] = 'B-' + tag


    
    return word_tag
"""