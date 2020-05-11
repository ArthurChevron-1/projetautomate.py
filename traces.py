'''

Projet de Maths pour Info 
Groupe L2-A1

©2020
Arthur Chevron
Guillaume Brun
Flavien Lallemand
Nathan Rousselot
Nicolas Ruiz

'''
import time

class Automate:

    def __init__(self, init_list) :  # init_list correspond au contenu du fichier décrivant l'automate.
        self.init_list = init_list
        self.longueur_alphabet = int(init_list[0]) 
        self.nombre_etats = int(init_list[1])   
        self.nombre_etats_initiaux = int(init_list[2][0])
        self.nombre_etats_terminaux = int(init_list[3][0])          
        self.nombre_transitions = int(init_list[4])
        self.asynchrone = []    #Stockera (s'il y a) les transitions pour les preuves que l'automate est asynchrone
        self.non_deterministe = []  #Stockera (s'il y a) les transitions pour les preuves que l'automate est non-déterministe
        self.non_complet = []   #Stockera (s'il y a) les transitions pour les preuves que l'automate est non complet
        '''
        Création de l'automate équivalent complet mais qu'avec des liaisons vers P
        Nous servira pour la complétion pour comparer avec nos transitions actuelles
        mais aussi pour le test_complet 
        '''
        self.templateComplet = []   




    '''
     Affiche les états initiaux, terminaux et transitions d'un automate
    '''
    def afficher_infos(self) :
        if (self.nombre_etats_initiaux > 1) :
            fichier2.write("Les " + str(self.nombre_etats_initiaux) + " états initiaux sont : ")
            for i in range(2, len(self.init_list[2]), 2):
                fichier2.write(self.init_list[2][i] + " // ")
            fichier2.write("\n")
        else :
            fichier2.write("L'état initial est : " +  str(self.init_list[2][2]))
        fichier2.write("\n")
        if (self.nombre_etats_terminaux > 1) :
            fichier2.write("Les " + str(self.nombre_etats_terminaux) + " états terminaux sont : ")
            for i in range(2, len(self.init_list[3]), 2):
                fichier2.write(self.init_list[3][i] + " // ")
            fichier2.write("\n")
        elif(self.nombre_etats_terminaux == 0):
            fichier2.write("Il n'y a pas d'état terminal\n")
        else :
            fichier2.write("L'état terminal est : " + self.init_list[3][2])
        fichier2.write("\n")

        fichier2.write("Les transitions sont :\n")
        for i in range(5, 5 + self.nombre_transitions) :
            fichier2.write(self.init_list[i] + "\n")




    '''
    Test si un automate est asynchrone
    L'algorithme parcoure chaque transition voir s'il existe une liaison vers Ɛ (symbolisée par un '*') 
    On stocke les transitions qui font que l'automate est asynchrone dans asynchrone[] pour l'affichage des preuves
    '''
    def test_asynchrone(self) :
        for i in range(5, 5 + self.nombre_transitions)  :
            if self.init_list[i][1] == '*' :
                self.asynchrone.append(self.init_list[i])
        if len(self.asynchrone) == 0:
            fichier2.write("L'automate est synchrone.\n")
            return False
        else :
            fichier2.write("L'automate est asynchrone. \nPreuves : \n")
            for i in range (len(self.asynchrone)) :
                fichier2.write(self.asynchrone[i] + " // ")
            fichier2.write("\n")
            return True
    


    
    '''
    Test si un automate synchrone est déterministe 
    L'algorithme parcoure chaque transition et regarde celle d'en-dessous voir s'ils ont le même premier et deuxième caractère. 
    ex : 0a1 && 0a3
    On stocke les transitions qui font que l'automate est non-déterministe dans non-déterministe[] 
    pour l'affichage des preuves.
    '''
    def test_deterministe(self) :
        # Pour chaque transition on regarde si celle d'en dessous ne comporte pas ET le même chiffre ET la même lettre
        for i in range(5, 5 + self.nombre_transitions) :
            for j in range(i, 5 + self.nombre_transitions)  :
                if self.init_list[i][0] == self.init_list[j][0] and self.init_list[i][1] == self.init_list[j][1] and self.init_list[i]!= self.init_list[j]:
                    self.non_deterministe.append(self.init_list[i])
                    self.non_deterministe.append(self.init_list[j])
        if len(self.non_deterministe) == 0 and self.nombre_etats_initiaux == 1:
            fichier2.write("L'automate est déterministe.\n")
            return True
        else :
            fichier2.write("L'automate n'est pas déterministe. \nPreuve(s) : ")
            if self.nombre_etats_initiaux > 1 :
                fichier2.write("Il y a plus d'1 état initial. (" + str(self.nombre_etats_initiaux) + ")\n")
            if len(self.non_deterministe) > 0 :
                for i in range (0, len(self.non_deterministe), 2) :
                    fichier2.write(self.non_deterministe[i] + "&" + self.non_deterministe[i+1] + " // ")
            return False




    ''' 
    Test si un automate synchrone, déterministe est complet
    L'algorithe commence par créer le tableau self.templateComplet qui est un tableau comportant TOUTES les transitions
    (celles dans init_list + les manquante), mais les faisant pointer vers P (cela ne nous intéresse pas de savoir vers 
    quoi les transitions existantes pointent)
    On compare ensuite self.templateComplet, qui comprend TOUTES les transitions, avec init-list, pour déceler les 
    transitions manquantes dans init_list.
    On stocke les transitions qui font que l'automate est non-complet dans non-complet[] 
    pour l'affichage des preuves.
    '''
    def test_complet(self) :
        # Création du tableau comportant toutes les transitions "idéales"
        for i in range(self.nombre_etats) :
            for j in range(self.longueur_alphabet) :
                self.templateComplet.append(str(i) + chr(97+j) + "P")

        # Comparaison des transitions "idéales" avec celles de notre automate
        for i in range(len(self.templateComplet)) :
            for j in range(5, 5 + self.nombre_transitions) :
                if (self.init_list[j][0] == self.templateComplet[i][0] and self.init_list[j][1] != self.templateComplet[i][1]) :
                    if self.templateComplet[i] not in self.non_complet :
                        self.non_complet.append(self.templateComplet[i])

        # Permet de repérer les états totalement absents de notre table de transitions 
        for i in range(self.nombre_etats) :
            absent = True
            for j in range(5, 5 + self.nombre_transitions) :
                if self.init_list[j][0] == str(i) :
                    absent = False
            if absent == True :
                for j in range(self.longueur_alphabet) :
                    self.non_complet.append(str(i) + chr(97+j) + "P")

        # Ajout de l'état poubelle pour chaque lettre de l'alphabet
        for i in range(self.longueur_alphabet) :
            self.templateComplet.append("P" + chr(97+i) + "P")      

        # Test si le tableau comportant les transitions manquante (non_complet[]) est vide OU si les transitions et transitions idéales
        # sont identiques, pour savoir si l'automate est complet ou non
        if len(self.non_complet) == 0 or len(self.init_list) - 5 == len(self.templateComplet) - self.longueur_alphabet :
            fichier2.write("L'automate est complet.\n")
            return True
        else :
            fichier2.write("L'automate n'est pas complet. \nPreuves : ")
            for i in range (len(self.non_complet)) :
                fichier2.write(self.non_complet[i] + " // ")
            fichier2.write("sont manquants.\n")
            return False




    '''
    Get_transitions
    Fonction permettant de récupérer les transitions pour un état donné, vers une lettre donnée
    Nous servira notamment pour la déterminisation
    '''
    def get_transitions(self, letter, number) :
        tmp = ""
        for i in range(5, 5 + self.nombre_transitions) :
            if self.init_list[i][0] == str(number) and self.init_list[i][1] == letter :
                tmp += self.init_list[i][2]
        return tmp



    '''
    Déterminisation d'un automate synchrone
    '''
    def determinisation(self):
        fichier2.write("\n\n------ Déterminisation de l'automate ------\n\nAffichage de l'automate déterminisé :\n")
        initiaux = ""
        etats = [initiaux]  # Liste des nouveaux états initiaux, formés de la réunion des anciens états initiaux
        trans = []  # Stockera transitions
        alphabet = []   # Stockera alphabet
        anciensTerminaux = []
        terminaux = []

        for i in range(2, len(self.init_list[2]), 2):
            initiaux += self.init_list[2][i]  # Nouvel état formé de la réunion des états initiaux
        for i in range(self.longueur_alphabet) :
            alphabet.append(chr(97 + i))
        l = [initiaux]  # On enfile cette etat, dans la file des états à traiter
        tmp = ""

        # Tant qu'on a des états à traiter
        while (len(l) != 0) :

            # Pour chaque lettre de l'alphabet, pour chaque état dans la file, on regarde s'il existe des transitions,
            # que l'on concatène dans tmp (s'il y a 02 on concatène les transitions de 0 puis de 2)
            for i in alphabet :
                for j in (l[0]) :
                    for char in self.get_transitions(i, j):
                        if char not in tmp:
                            tmp += char
                            tmp = list(tmp)
                            tmp = [int(x) for x in tmp]
                            tmp.sort()
                            tmp = map(str, tmp)
                            tmp = ''.join(tmp)                           

                if len(tmp) != 0 :
                    trans += [(l[0], i, tmp)]
                    if not tmp in etats :
                        etats += [tmp]
                        l += [tmp]
                tmp = ""
            l.pop(0) # On défile l'etat traité

        # Permet de définir quels sont les nouveaux états terminaux
        for i in range(2, len(self.init_list[3]), 2):
                anciensTerminaux.append(self.init_list[3][i])
        for i in etats :
             for j in i :
                if j in anciensTerminaux : # Pour chaque état terminal, on regarde s'il est présent dans les nouveaux états
                    terminaux += [i]
                    break

        # Partie renommage des états
        fichier2.write("\n" + str(trans) + "\n\nPour assurer le bon fonctionnement de notre programme, nous allons renommer nos états.\n")
        tab = []
        for i in range (len(trans)) :
            for j in range(0, len(trans[i]), 2) :
                if trans[i][j] not in tab :
                    tab.append(trans[i][j])
        new_list = []
        for j in range(len(trans)):
            T = ""
            for k in range(len(trans[j])):
                for i in range(len(tab)) :
                    if (tab[i] == trans[j][k]) :
                        T += str(tab.index(tab[i]))
                    elif (k == 1) and trans[j][1] not in T :
                        T += trans[j][1]
            new_list.append(tuple(T))
        c = 0
        for i in range(len(tab)) :
            fichier2.write(str(tab[i]) + " -> " + str(tab.index(tab[i])) + "\n")
            if tab[i] in terminaux :
                terminaux += str(tab.index(tab[i]))
                c += 1
        for i in range(c) :
            terminaux.pop(0)

        for i in range(5, 5 + self.nombre_transitions):
            self.init_list.pop()

        fichier2.write("Nous obtenons alors : \n\n" + str(new_list) + "\n")
        self.init_list[1] = str(len(tab))
        self.nombre_etats = int(self.init_list[1])
        self.init_list[2] = "1 " + str(tab.index(tab[0]))

        # On modifie le nombre d'états initiaux, terminiaux et transitions, en fonction de l'automate déterminisé
        self.nombre_etats_initiaux = int(self.init_list[2][0])
        self.init_list[3] = str(len(terminaux))
        for i in range(len(terminaux)) :
            self.init_list[3] += " " + terminaux[i]
        self.nombre_etats_terminaux = int(self.init_list[3][0])
        self.init_list[4] = str(len(new_list))
        self.nombre_transitions = int(self.init_list[4])
        self.nombre_etats = len(tab)

        for i in range(5, 5 + self.nombre_transitions) :
            var = ""
            for j in range(len(new_list[i-5])) :
                var += new_list[i-5][j]
            self.init_list.append(var)
        fichier2.write("\nNouvel automate déterminisé :\n")
        self.afficher_infos()




    ''' 
    L'algorithme reprend le principe de test_complet. On utilise self.templateComplet, l'automate complet.
    Une chose à comprendre est que, à la fin des comparaisons, l'automate complété est d'abord dans self.templateComplet,
    ce qui explique la ligne self.init_list.extend(self.templateComplet)
    '''
    def completion(self):
        fichier2.write("\n\n------ Complétion de l'automate ------\n\nAffichage de l'automate complété :\n\n")
        for i in range(len(self.templateComplet)) :
            for j in range(5, 5 + self.nombre_transitions) :
                if self.init_list[j][0] == self.templateComplet[i][0] and self.init_list[j][1] == self.templateComplet[i][1] :
                    self.templateComplet[i] = self.init_list[j]
        for i in range(self.nombre_transitions) :
            self.init_list.pop()
        self.init_list.extend(self.templateComplet)
        self.nombre_transitions = (self.longueur_alphabet * self.nombre_etats) + (self.longueur_alphabet)
        self.init_list[4] = str((self.longueur_alphabet * self.nombre_etats) + (self.longueur_alphabet))  

        fichier2.write("\nNouvel automate complété :\n")
        self.afficher_infos()   




    '''
    Déterminisation + complétion automate asynchrone
    '''
    def determinisation_et_completion_automate_asynchrone(self):
        fichier2.write("a.determinsation_et_completion_automate_asynchrone() non-réalisé\n\n")





    '''    
    Déterminisation & complétion automate synchrone
    Utilise les fonctions de déterminisation et de complétion ci-dessus
    '''
    def determinisation_et_completion_automate_synchrone(self):
        self.determinisation()
        fichier2.write(str(self.init_list))
        if (self.test_complet() == False) :
            self.completion()
    



    '''
    Fonction intermédiaire pour la minimisation qui va séparer les classes d'états
    avec des futurs différents

    Λ représente la file d'attente des différentes classes à tester
    Initialisation de Θ qui va contenir l'état, la classe, puis ses futurs états en a, b, c, ...
    Initialisation de Ψ qui va contenir l'état, sa classe puis ses futurs classes en a, b, c, ...
    lmoore est le nouvel automate après qui contient l'état, la nouvelle classe, puis les anciennes
    futurs classes en a, b, c de Ψ
    '''
    def minim_split(self, lmoore, Ψ, Θ):
        # initialisation de la liste d'attente et des classes
        classe = 65
        Λ = []
        for i in range(len(Ψ)):
            T = ""
            for j in range(1, len(Ψ[0])):
                T += Ψ[i][j]
            # évite les doublons
            if tuple(T) not in Λ:
                Λ.append(tuple(T))

        # rénitialisation de lmoore pour pouvoir remplir avec les nouvelles classes
        lmoore.clear()
        # tant que la file n'est pas vide continuer à tester
        while(len(Λ) != 0):
            for i in range(len(Ψ)):
                # teste si l'élément de la file d'attente est dans la liste Ψ
                temp = Ψ[i][0] + chr(classe)
                for j in range(1, len(Λ[0])):
                    if(Λ[0][0] == Ψ[i][1] and Λ[0][j] == Ψ[i][j + 1]):
                        temp += Λ[0][j]
                if(len(temp) == len(Ψ[0])):
                    lmoore.append(tuple(temp))

            classe += 1
            # on enlève la valeur tester de la file
            Λ.remove(Λ[0])

        # obtention du nouveau Θ :
        Θ.clear()
        for i in range(len(lmoore)):
            for j in range(5, 5  + self.nombre_transitions, self.longueur_alphabet):
                if(lmoore[i][0] == self.init_list[j][0]):
                    temp = lmoore[i][0] + lmoore[i][1]
                    for k in range(self.longueur_alphabet):
                        temp += self.init_list[j + k][2]
                    Θ.append(tuple(temp))

        # obtention du nouveau Ψ :
        Ψ.clear()
        for i in range(len(Θ)):
            temp = Θ[i][0] + Θ[i][1]
            for j in range(2, len(Θ[0])):
                for k in range(len(Θ)):
                    if(Θ[i][j] == Θ[k][0]):
                        temp += Θ[k][1]
            Ψ.append(tuple(temp))

        fichier2.write("Obtention du Ψ suivant :" + str(Ψ) + "\n")
        fichier2.write("Obtention de lmoore suivant:" + str(lmoore) + "\n")




    '''
    Minimisation d'un automate complet et déterministe. 
    '''
    def minimisation(self):
        fichier2.write("\n\n------ Minimisation de l'automate ------\n\n")
        if(self.init_list[1] == "1"):
            fichier2.write("Automate déjà minimal")
        else:
            # Initialisation 
            classe = 65
            Θ = []
            terminaux = []
            ''' 
            Initialisation de Θ qui va contenir l'état, la classe, puis ses futurs états en a, b, c, ...
            Initialisation de Ψ qui va contenir l'état, sa classe puis ses futurs classes en a, b, c, ...
            '''
            fichier2.write("Création du premier Θ : séparation des états terminaux et non terminaux.\n")
            # on ajoute les éléments terminaux en premier
            for i in range(2, len(self.init_list[3]), 2):
                for j in range(5, 5 + self.nombre_transitions, self.longueur_alphabet):
                    if(self.init_list[3][i] == self.init_list[j][0]):
                        temp = self.init_list[j][0] + chr(classe)
                        # ajoute tous les futurs de l'état j 
                        for k in range(self.longueur_alphabet):
                            temp += self.init_list[j + k][2]
                        Θ.append(tuple(temp))
                        terminaux.append(self.init_list[j][0])
            # Séparation du groupe            
            classe += 1
            # On ajoute le reste à la partition initiale
            for i in range(5, 5 + self.nombre_transitions, self.longueur_alphabet):
                if self.init_list[i][0] not in terminaux:
                    # Θ.append(tuple(self.init_list[i][0] + chr(classe) + self.init_list[i][2] + self.init_list[i + 1][2]))
                    temp = self.init_list[i][0] + chr(classe)
                    # ajoute tous les futurs de l'état j 
                    for j in range(self.longueur_alphabet):
                        temp += self.init_list[i + j][2]
                    Θ.append(tuple(temp))
            fichier2.write("Obtention du premier Θ :" + str(Θ) + "\n\n")
            fichier2.write("Création du premier Ψ : transformations des états futurs vers des classes.\n")
            # classe des partitions une à une
            classe = 65
            Ψ = []
            
            for i in range(len(Θ)):
                temp = Θ[i][0] + Θ[i][1]
                for j in range(2, len(Θ[0])):
                    if Θ[i][j] in terminaux:
                        temp += chr(classe)
                    else:
                        temp += chr(classe + 1)
                Ψ.append(tuple(temp))
            fichier2.write("Obtention du premier Ψ :" + str(Ψ) + "\n\n")

            '''
            Tant que la liste Ψ contenant les nouvelles classes varie, on split les classes
            '''
            c = 0
            lmoore = []
            self.minim_split(lmoore, Ψ, Θ)
            while(Ψ != lmoore):
                fichier2.write("\n\n----------------------------------------\n\n")
                fichier2.write("Ψ n'est pas stable, il faut séparer de nouvelles classes :\n")
                self.minim_split(lmoore, Ψ, Θ)
                c += 1

            
            if(c == 0):
                fichier2.write("L'automate était déjà minimisé\n")
            else:
                fichier2.write("\nΨ est stable, nous avons obtenu l'automate minimisé.\n")


            # obtention du dernier Θ : automate minimisé
            Θ.clear()
            T = ""
            for i in range(len(Ψ)):
                T = ""
                for j in range(1, len(Ψ[0])):
                    T += Ψ[i][j]
                # enlève les doublons
                if tuple(T) not in Θ:
                    Θ.append(tuple(T))

            # obtention du nouvel état initial : init_etat
            for i in range(len(Ψ)):
                if(self.init_list[2][2] == Ψ[i][0]):
                    init_etat = Ψ[i][1]

            # obtention du ou des états finaux
            T = ""
            for i in range(len(Ψ)):
                if Ψ[i][0] in terminaux:
                    T += Ψ[i][1]

            final_etat = ""
            for i in T : 
                if i not in final_etat: 
                    final_etat += i

            # écriture du nouvel automate selon les normes : 0a1 0b3 etc...
            Λ = ""
            for i in range(len(Θ)):
                for j in range(1, len(Θ[0])):
                    Λ += str(ord(Θ[i][0]) - 65) + chr(j + 96) + str(ord(Θ[i][j]) - 65) + "/"

            # Affichage de l'automate
            fichier2.write("\nLe nouvel automate minimal Θ de la forme suivante :\n")
            fichier2.write(" - Première élement entre parenthèse est l'état qui peut contenir la combinaison des états 0 et 3 par exemple\n")
            fichier2.write(" - Deuxième élement entre parenthèse est la classe de l'état\n")
            fichier2.write(" - Troisième élement entre parenthèse est l'état futur selon a\n")
            fichier2.write(" - Quatrième élement entre parenthèse est l'état futur selon b\n")
            fichier2.write(" - et ainsi de suite\n\n")
            fichier2.write("Automate minimisé : " + str(Θ) + "\n\n")
            fichier2.write("L'état initial de l'automate est l'état : " + str(init_etat) + "\n")
            fichier2.write("L'(es) état(s) terminal(aux) de l'automate est(sont) : " + str(final_etat) + "\n")

            '''
            Écriture du nouvel automate minimisé en modifiant init_list
            Pour exporter ce nouvel automate à toute fonction nous changeons les états
            par exemple les états de la classe A -> 0, B -> 1, etc...
            '''
            fichier2.write("Pour assurer le bon fonctionnement de notre programme, nous allons renommer nos états.\n")
            for i in range(len(Θ)):
                fichier2.write(chr(i + 65) + " -> " + str(i) + "\n")
            fichier2.write("\n")
            # changement d'init_list
            self.init_list[0] = str(self.longueur_alphabet)
            self.init_list[1] = str(len(Θ))
            self.init_list[2] = "1 " + str(ord(init_etat) - 65)
            self.init_list[3] = str(len(final_etat))
            for i in range(len(final_etat)):
                self.init_list[3] += " " + str(ord(final_etat[i]) - 65)
            self.init_list[4] = str(len(Θ) * self.longueur_alphabet)
            for i in range(5, 5 + self.nombre_transitions):
                self.init_list[i] = ""
            j = 5
            for i in range(len(Λ)):
                if(Λ[i] == '/'):
                    j += 1
                else:
                    self.init_list[j] += Λ[i]

            self.longueur_alphabet = int(self.init_list[0]) 
            self.nombre_etats = int(self.init_list[1])   
            self.nombre_etats_initiaux = int(self.init_list[2][0])
            self.nombre_etats_terminaux = int(self.init_list[3][0])          
            self.nombre_transitions = int(self.init_list[4])

            fichier2.write("Nouvel automate minimisé :\n")
            self.afficher_infos()




    '''
    Standardisation d'un automate quelconque
    '''
    def standardisation(self):
        fichier2.write("\n\n------ Standardisation de l'automate ------\n\n")
        # test si l'automate n'est pas déjà standard
        standard = True
        etats_initiaux = self.init_list[2][1:].split() # permet de caster les char en int directement
        
        if(self.nombre_etats_initiaux == 1):
            for i in range(5, 5 + self.nombre_transitions) :
                for etats in etats_initiaux:
                    if(self.init_list[i][2] == etats):
                        standard = False
                        fichier2.write("L'automate n'est pas standard car la transition " + str(self.init_list[i]) + " aboutie dans l'état initia " + etats + "\n")

        else:
            standard = False
            fichier2.write("L'automate n'est PAS standard.\nNous allons donc le rendre standard.\n")
                        
        if(standard == True):
            fichier2.write("L'automate est standard.\nAucune modifification apportée.\n")
        
        # Si l'automate n'est pas déjà standard, alors il le standardise
        else:
            etats_initiaux = self.init_list[2][1:].split() # permet de caster les char en int directement
            transitions_a_changer = []
            for i in range(5, 5 + self.nombre_transitions) :
                for etats in etats_initiaux:
                    if(self.init_list[i][0] == etats):
                        transitions_a_changer.append(self.init_list[i])
                        
            for i in range(0,len(transitions_a_changer)):
                old_transition = transitions_a_changer[i]
                transitions_a_changer[i] = "i" + transitions_a_changer[i][1:]
                self.init_list.append(transitions_a_changer[i])
                fichier2.write("Pour la transition " + str(old_transition) + " on créé " + str(transitions_a_changer[i]) + "\n")
                
            self.nombre_etats_initiaux = 1 ### i devient le seul état inital
            self.nombre_etats += 1
            self.nombre_transitions += len(transitions_a_changer)
            self.init_list[2] = '1 i'
        
        fichier2.write("\nRésultat\n")
        self.afficher_infos()




    '''
    Reconnaisance d'un mot 
    '''    
    def reconnaitre_mot(self):
        if (self.nombre_etats > 1):
            fichier2.write("\n\n------ Reconnaissance de mot ------\n\n")
            vide = 'a'
            rec_vide = False
            while vide != 'Oui' and vide != 'Non':
                vide = input("Voulez-vous reconnaitre le mot vide ? (Oui/Non) : ")
            
            if vide == 'Oui':
                etat_initial = self.init_list[2][1:].split()[0]
                etats_terminaux = self.init_list[3][1:].split()
                
                for terminal in etats_terminaux:
                    if etat_initial == terminal:
                        fichier2.write("Le mot vide est reconnu par l'automate.\n")
                        rec_vide = True
                    
                if rec_vide == False:
                    fichier2.write("Le mot vide n'est PAS reconnu par l'automate.\n")
            
            mots = input("Saisissez les mots à reconnaitre, séparez les par des espaces et terminez par le mot 'fin': ")
            if "fin" in mots :
                mots = mots.split()[:-1]
                for mot in mots:
                    fichier2.write("\n" + str(mots))
                    faute = False
                    passe = False
                    current_etat = self.init_list[2][1:].split()[0]
                    c = 0
                    while c < len(mot) and faute == False:
                        current_char = mot[c]
                        fichier2.write("Current char: " + str(current_char) + "\n")
                        
                        for i in range(5, 5 + self.nombre_transitions) :
                            fichier2.write("Transitions : " + self.init_list[i] + " | Current: " + str(current_etat) + str(current_char) + "\n")
                            if self.init_list[i][:2] == current_etat + current_char:
                                c +=  1
                                current_etat = self.init_list[i][2]
                                fichier2.write("New current: " + str(current_etat) + "\n")
                                break
                                
                            
                            elif i >= self.nombre_transitions :
                                faute = True
                    
                    etats_terminaux = self.init_list[3][1:].split()
                    
                    for terminal in etats_terminaux:
                        if terminal == current_etat:
                            fichier2.write("Le mot " + str(mot) + " est dans le language de l'automate.\n")
                        else:
                            fichier2.write("Le mot" + str(mot) + "n'est PAS dans le language de l'automate.\n")
                            fichier2.write("L'automate bloque a l'état " + str(current_etat) + " avec le caractère " + str(current_char) + " à l'index " + str(c) + "\n")





    '''
    Création de l'automate complémentaire tel que L = A devient L = *A 
    '''   
    def language_complementaire(self):
        if(self.nombre_etats > 1):
            fichier2.write("\n\n------ Langage complémentaire de l'automate ------\n\n")
            etats_list = []
            current_terminaux = self.init_list[3][1:].split()
            
            for i in range(5, 5 + self.nombre_transitions) :
                if self.init_list[i][0] not in etats_list:
                    etats_list.append(self.init_list[i][0])
                    
                if self.init_list[i][2] not in etats_list:
                    etats_list.append(self.init_list[i][2])

            new_line_terminaux = str(len(etats_list) - int(self.init_list[3][0])) + " "
            
            for etat in etats_list:
                if etat not in current_terminaux:
                    new_line_terminaux += etat + " "
                    
            self.init_list[3] = new_line_terminaux
            
            fichier2.write("En transformant la/les sortie(s) " + str(current_terminaux) + " en non sortie(s) et la/les non sortie(s) " + self.init_list[3][1:] + " en sortie(s), l'automate reconnait maintenant le langage complémentaire.\n")
            
            fichier2.write("\nNouvel automate complémentaire :\n")
            self.afficher_infos()
        else: 
            fichier2.write("L'automate ne peut être complémentaire.\n")





'''
Éxécution du code. Nous étudions le fichier txt demandé par l'utilisateur
'''
# fichier2.write("\n -------------------------------   Initiaisation du Projet   -------------------------------\n")
# fichier2.write(" ________  ___  ___  _________  ________  _____ ______   ________  _________  _______")
# time.sleep(.350)
# fichier2.write("|\\   __  \\|\\  \\|\\  \\|\\___   ___\\\\   __  \\|\\   _ \\  _   \\|\\   __  \\|\\___   ___\\\\  ___ \\")
# time.sleep(.350)
# fichier2.write("\\ \\  \\|\\  \\ \\  \\\\\\  \\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\ \\  \\|\\  \\|___ \\  \\_\\ \\   __/|")
# time.sleep(.350)
# fichier2.write(" \\ \\   __  \\ \\  \\\\\\  \\   \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\\\|__| \\  \\ \\   __  \\   \\ \\  \\ \\ \\  \\_|/__")
# time.sleep(.350)
# fichier2.write("  \\ \\  \\ \\  \\ \\  \\\\\\  \\   \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\    \\ \\  \\ \\  \\ \\  \\   \\ \\  \\ \\ \\  \\_|\\ \\")
# time.sleep(.350) 
# fichier2.write("   \\ \\__\\ \\__\\ \\_______\\   \\ \\__\\ \\ \\_______\\ \\__\\    \\ \\__\\ \\__\\ \\__\\   \\ \\__\\ \\ \\_______\\")
# time.sleep(.350)
# fichier2.write("    \\|__|\\|__|\\|_______|    \\|__|  \\|_______|\\|__|     \\|__|\\|__|\\|__|    \\|__|  \\|_______|")
# time.sleep(.500)
# fichier2.write("\n\n ----------------------------------   Projet initialisé   ----------------------------------\n\n")

quitter = 1
while (quitter == 1) :
    numero = input("Quel automate souhaitez-vous tester ? : ")
    fichier = open("Automates/A1-" + numero + ".txt", "r") # Ouverture du fichier txt demandé
    contenu_fichier = fichier.read().splitlines()

    fichier2 = open("Automates_Traces/A1-traces" + numero + ".txt", "w")
    fichier2.write("Traces pour l'automates " + "A1-" + numero + "\n\n")

    a = Automate(contenu_fichier)

    fichier2.write("\n\n------ Affichage de l'automate initial ------\n\n")
    a.afficher_infos()

    if a.test_asynchrone() == True :
        a.determinisation_et_completion_automate_asynchrone()
    else :
        if a.test_deterministe() == True :
            if a.test_complet() == True :
                fichier2.write("L'automate est déjà synchrone, déterministe et complet : aucun changement à faire.\n")
            else :
                a.completion()
        else :
            a.determinisation_et_completion_automate_synchrone()

        a.minimisation()

        fichier2.write("\n\nVoulez-vous reconnaitre un mot ? (Oui/Non) : Non\n\n")
    # if (input("\n\nVoulez-vous reconnaitre un mot ? (Oui/Non) : ") == "Oui") :
    #     a.reconnaitre_mot()
    # else : 
        fichier2.write("Nous ne reconnaitrons pas de mot.\n")

        a.language_complementaire()
        a.standardisation()

    fichier2.write("\n\n-------------------------------------------------\n\n")
    fichier2.close()

    # quitter = input("Pour essayer avec un autre automate, tapez 1\nPour quitter le projet, tapez Quit : ")
    

fichier.close()

# fichier2.write("\n\n ------------------------------   Fermeture du programme   ------------------------------\n")
# fichier2.write(" ________  ___  ___  _________  ________  _____ ______   ________  _________  _______")
# time.sleep(.350)
# fichier2.write("|\\   __  \\|\\  \\|\\  \\|\\___   ___\\\\   __  \\|\\   _ \\  _   \\|\\   __  \\|\\___   ___\\\\  ___ \\")
# time.sleep(.350)
# fichier2.write("\\ \\  \\|\\  \\ \\  \\\\\\  \\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\ \\  \\|\\  \\|___ \\  \\_\\ \\   __/|")
# time.sleep(.350)
# fichier2.write(" \\ \\   __  \\ \\  \\\\\\  \\   \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\\\|__| \\  \\ \\   __  \\   \\ \\  \\ \\ \\  \\_|/__")
# time.sleep(.350)
# fichier2.write("  \\ \\  \\ \\  \\ \\  \\\\\\  \\   \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\    \\ \\  \\ \\  \\ \\  \\   \\ \\  \\ \\ \\  \\_|\\ \\")
# time.sleep(.350) 
# fichier2.write("   \\ \\__\\ \\__\\ \\_______\\   \\ \\__\\ \\ \\_______\\ \\__\\    \\ \\__\\ \\__\\ \\__\\   \\ \\__\\ \\ \\_______\\")
# time.sleep(.350)
# fichier2.write("    \\|__|\\|__|\\|_______|    \\|__|  \\|_______|\\|__|     \\|__|\\|__|\\|__|    \\|__|  \\|_______|")
# time.sleep(.500)
# fichier2.write("\n\n ----------------------------------   Programme fermé   ----------------------------------\n\n")