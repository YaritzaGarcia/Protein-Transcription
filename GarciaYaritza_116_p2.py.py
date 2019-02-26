#Yaritza M. García Chaparro CIIC3011-116 Project2: Protein Transcription
#Variables globales:
Dict_Table = {}
Start_Codons = list()
Stop_Codons = list()
Almost_Final_Input = list()
Final_Output = list()

#Funciones utilizadas en el programa:

#Función1: Creando un diccionario de la tabla de valores que se le asigna.
def Codon_Dict_Table(nombre_archivo):
    archivo_abierto = open(nombre_archivo, "r")
    Count = 0
    for line in archivo_abierto:
        #Separando el texto del documento para guardarlo en una lista de manera individual.
        Lista = line.split(' ')
        #Borrando todo elemento de la lista que este vacío, o sea, eliminando los espacios que hay demás.
        for element in Lista[:]:
            if element == '':
                Lista.remove(element)
        #Eliminando '\n' de cada elemento de la lista.
        if Lista[len(Lista)-1].endswith('\n'):
            Lista[len(Lista) - 1] = Lista[len(Lista)-1].rstrip('\n')
        #Separando Start y Stop de los amino acidos.
        if Lista[0] == 'Start':
            for x in Lista[3:]:
                Start_Codons.append(x)
        elif Lista[0] == 'Stop':
            for x in Lista[3:]:
                Stop_Codons.append(x)
        #Añadiendo amino a un diccionario.
        else:
            #Creando tupla con el nombre completo del amino y su abreviación.
            Nombre_Completo_Abreviacion = (Lista[0],Lista[1])
            #Asignando valores a cada amino.
            Dict_Table[Nombre_Completo_Abreviacion] = Lista[3:]
    archivo_abierto.close()

#Función2: Procesando el archivo de input y añadiendolo a una lista.
def Procesar_Archivo_Input(nombre_archivo):
    archivo_abierto = open(nombre_archivo, "r")
    File_Input_List = list()
    for line in archivo_abierto:
        #Eliminando '\n' de cada elemento de la lista.
        if line[len(line)-1] == '\n':
            line = line.rstrip('\n')
        File_Input_List.append(line)
    #Leyendo las lineas individualmente y dividiendo cada una en grupos de tres para añadirlo a Final_Input.
    for Three in File_Input_List:
        List_three = list()
        Count = 0
        a = 0
        b = 3
        while Count != int((len(Three)/3)+1):
            if Three[a:b] != '':
                List_three.append(Three[a:b])
                a = a + 3
                b = b + 3
                Count = Count + 1
            else:
                a = a + 3
                b = b + 3
                Count = Count + 1
        Almost_Final_Input.append(List_three)
    archivo_abierto.close()

#Función3: Comparar la lista del archivo de input procesado con los elementos en el diccionario del archivo codonTable.
def Transcribe(DNA_String):
    Proccessing_List = list()
    FindStart = None
    FindStop = None
    countline = 0
    String_provisional = ''
    #Loop para leer línea por línea.
    while countline != len(DNA_String):
        countline+=1
        count = 0
        #Determina donde empieza una línea de DNA y donde termina.
        for Codon in DNA_String:
            if Codon in Start_Codons:
                FindStart = count + 1
                count += 1
            elif Codon in Stop_Codons:
                FindStop = count
                count += 1
            else:
                count = count + 1
    #Añadiendo todo a una lista para que sea procesada. Si la línea de DNA no empieza ni acaba se identifica y se añade a la lista el tipo de ERROR.
    if FindStart == None:
        Proccessing_List.append('ERROR: Transcription never starts')
    elif FindStop == None:
        Proccessing_List.append('ERROR: Transcription never stops')
    else:
        Proccessing_List.append(Line[FindStart:FindStop])
        
    #Procesando cada codon string e identificándolos por su nombre de tres caracteres. En el caso de que tenga un ERROR se salta la línea.
    for Codon_List in Proccessing_List:
        #Si en el codon string ya se detectaba que nunca comenzaba o nunca terminaba se sigue con el próximo
        if Codon_List == 'ERROR: Transcription never starts' or Codon_List == 'ERROR: Transcription never stops':
            Final_Output.append(Codon_List)
            continue
        for One_Codon in Codon_List:
            #Con la variable Found_NeverFound se indica si uno de los codones en la línea no existe para así decir si es un Bad codon string o no.
            Found_Neverfound = 0
            for TriName in Dict_Table:
                for Dict_Codon in Dict_Table[TriName]:
                    if One_Codon == Dict_Codon:
                        Found_Neverfound += 1
                        String_provisional += TriName[1] + ':'
            if Found_Neverfound == 0:
                String_provisional = 'ERROR: Bad codon string'
        # Para sacar ':' si los tiene al final.
        if String_provisional.endswith(':'):
            String_provisional = String_provisional.rstrip(':')
        Final_Output.append(String_provisional)


#Función4: Para Buscar cual codon fue el que mas apareció.
def Find_Max_Codon(TriName_List):
    Counting_Dict = {}
    Max_CodonName = None
    Max_Codon = 0
    for TriName in TriName_List:
        if TriName == 'ERROR: Transcription never starts' or TriName == 'ERROR: Transcription never stops' or TriName == 'ERROR: Bad codon string':
            continue
        Find_Codon = TriName.split(':')
        #Añadiendo valores a un diccionario en el que te da el nombre completo del amino ácido junto al número de veces en que apareció.
        for CodonTriName in Find_Codon:
            for Name in Dict_Table:
                if Name[1] == CodonTriName:
                    if Name[0] not in Counting_Dict:
                        Counting_Dict[Name[0]] = 1
                    else:
                        Counting_Dict[Name[0]] += 1
    #Buscando en el diccionario cual fue el amino acido que más veces apareció.
    for TriName, Times in Counting_Dict.items():
        if Max_Codon < Times:
            Max_Codon = Times
            Max_CodonName = TriName
        elif Max_Codon == Times:
            Max_CodonName += ' and ' + TriName
    return Max_CodonName, Max_Codon

#Invocando funciones.
Codon_Dict_Table("codonTable.txt")
Procesar_Archivo_Input("DNAInput.txt")
for Line in Almost_Final_Input:
    Transcribe(Line)
#Guardando el output final en un archivo de texto y imprimiendolo en la pantalla.
Output_Archivo = open('DNAOutput.txt', 'w')
for item in Final_Output:
    Output_Archivo.write(item)
    print(item)
MaxCodon = Find_Max_Codon(Final_Output)
print("The protein(s) that appeared the most times" + " (" + str(MaxCodon[1]) + ' times) '+ "is(are): \n" + str(MaxCodon[0]))
Output_Archivo.write("The protein(s) that appeared the most times" + " (" + str(MaxCodon[1]) + ' times) '+ "is(are): \n" + str(MaxCodon[0]))
Output_Archivo.close()
