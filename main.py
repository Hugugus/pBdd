import sys
import time

from Bdd import Bdd


def main():
    bddT=input("Quelle Base de donnée voulez-vous utiliser? \n")
    db=bddT+'.db'
    bddC=Bdd(db)
    mMenu(bddC)

def eMenu(bdd):
    txt="Que voulez-vous faire ? \n(0) : Afficher les DF\n(1) : Ajouter une DF\n(2) : Modifier DF\n(3) : Supprimer une DF\n(4) : Supprimer les DF inutile et incoherente\n(5) : Generer de clés a partir des DF pour une table\n(6) : Verification des normes BCNF et 3NF sur toute la bdd \n(7) : Retour au menu principal\n"
    txt=txt.split("\n")
    for x in txt:
        print(x)
        time.sleep(0.3)
    c=input()
    if(c=="0"): #afficher df
        bdd.notDF()
        bdd.printFuncDep(True)
        eMenu(bdd)
    elif(c=="1"):#ajouter df
        bdd.printBdd()
        tab=input("Sur quelle table voulez-vous créer des DF ? Veuillez introduire un numéro \n")
        tabE=bdd.selectTable(int(tab))
        bdd.printTable(tabE[0],False)
        encode=input("Quelles sont les elements a gauche de la df?\n")
        dst=input("Quelle est la partie a droite de la DF?\n")
        bdd.addFuncDep(tabE[0],encode,dst)
        eMenu(bdd)
    elif (c=="2"): #modifier df
        if len(bdd.tab)>0:
            bdd.edit()
        else :
            print("Il n'ya pas de DF ")
        mMenu(bdd)
    elif (c=="3"): #delete df
        if len(bdd.tab)>0:
            bdd.printFuncDep(False)
            v=input("Quelle DF voulez-vous supprimer? Veuillez introduire un chiffre\n")
            bdd.deleteDF(int(v))
        else :
            print("Il n'ya pas de DF ")
        eMenu(bdd)
    elif (c=="4"): #DF inutile et incoherente
        res=[]
        resDN=[]
        resDL=[]
        tabT=bdd.notDF()
        if(len(tabT)==0):
            tabR=bdd.notWdF()
            print("DF non satisfaite : \n")
            #print(tabR)
            if len(tabR)>0:
                for i in range (len(bdd.tab)):
                    if not tabR[i]:
                        tab=bdd.tab[i]
                        print(i,end='')
                        res.append(i)
                        resDN.append(i)
                        print(" "+tab[0]+" : "+tab[1]+" -> "+tab[2])


            tabR=bdd.logDf()
            print("DF etant des consequences logiques : ")
            #print(tabR)
            if len(tabR)>0:
                for x in tabR:
                        i=int(x)
                        tab=bdd.tab[i]
                        print(i,end='')
                        res.append(i)
                        resDN.append(i)
                        print(" "+tab[0]+" : "+tab[1]+" -> "+tab[2])
        else:
            print("\nIl y a des DF ayant des attributs n'etant pas dans leur table a supprimer d'abord\n")
            #DF dont les attributs ne sont pas dans la table
            resNDF=[]
            tab=bdd.notDF()
            print("DF dont les attributs ne sont pas dans la table : ")
            if len(tab)>0:
                for i in tab:
                    #print(tab)
                    t=bdd.tab[int(i)]
                    resNDF.append(int(i))
                    print(str(i)+" "+t[0]+" : "+t[1]+" -> "+t[2])
            v=input("\nVoulez-vous supprimer toutes les DF ayant pas des attributs qui ne sont pas la bdd?\n(0) : Oui\n(1) : Non\n")
            if v=="0":
                tab=bdd.notDF()
                for i in tab:
                    bdd.deleteDF(int(i))

            eMenu(bdd)



        c=input("Que voulez-vous faire ?"
                "\n(0) : Supprimer toutes les DF non satistfaite\n(1) : Selectionner une DF non satisfaite a supprimer"
                "\n(2) : Supprimer toutes les DF étant des consequences logique\n(3) : Selectionner une DF étant une consequence logique a supprimer"
                "\n(4) : Supprimer toutes les DF non satisfaite et  étant des consequences logique  "
                "\n(5) : Rien\n")
        if c=="0":
            for i in resDN:
                bdd.deleteDF(i);

        elif c=="1":
            c=input("Quel DF non satisfaite voulez-vous supprimer?\n")
            tab=c.split(" ")
            #print("\n")
            print(tab)
            for i in tab:
                if int(i) in resDN:
                    bdd.deleteDF(int(i))
                else :
                    print("La DF non satisfaite avec un numero "+i+" n'existe pas\n")

        elif c=="2":
            for i in resDL:
                bdd.deleteDF(i);

        elif c=="3":
            c=input("Quel DF étant une consequence logique voulez-vous supprimer?\n")
            tab=c.split(" ")
            #print("\n")
            #print(tab)
            for i in tab:
                if int(i) in resDL:
                    bdd.deleteDF(int(i))
                else :
                    print("La DF logique avec un numero "+i+" n'existe pas\n")

        elif c=="4":

            for i in resDL:
                if int(i) in resDL:
                    bdd.deleteDF(int(i))
            for i in resDN:
                if int(i) in resDN:
                    bdd.deleteDF(int(i))

        else:
            eMenu(bdd)

        eMenu(bdd)

    elif (c=="5"):
        bdd.getKey()
        eMenu(bdd)
    elif (c=="6"):
        print()
        bdd.getTKey()
        print()
        eMenu(bdd)
    else :
        mMenu(bdd)

def mMenu(bdd):
    h="Que voulez-vous faire ?|(0) : Afficher toutes les DF|(1) : Option sur les DF|(2) : Afficher une table|(3) : Sauvegarder toutes les DF |(4) : Charger un sauvegarde des DF|(5) : Quittez"
    h=h.split("|")
    for x in h:
        print(x)
        time.sleep(0.3)

    c=input()
    if(c=="0"): #afficher df
        bdd.printFuncDep(True)
        mMenu(bdd)

    elif(c=="1"): #edit df
        eMenu(bdd)

    elif(c=='2'): #print une table
        bdd.printBdd()
        tab=input("Introduisez le numéro de la table que voulez-vous afficher \n")
        tabE=bdd.selectTable(int(tab))
        bdd.printTable(tabE[0],True)
        mMenu(bdd)

    elif(c=='3'): #sav
        if len(bdd.tab)>0:
            txt=input("Sous quel nom volez-vous sauvegarder vos DF ?\n")
            bdd.save(txt)
        else :
            print("Il n'y a pas de Df a sauvegarder")
        mMenu(bdd)

    elif (c=='4'): #load
        txt=input("Quelle sauvegarde voulez-vous charger? \n")
        bdd.load(txt)
        mMenu(bdd)

    elif(c=='5'): #quittez
        sys.exit()

    else:
        print("\nJe n'ai pas compris désolé")
        mMenu(bdd)

if __name__ == "__main__":
    main()






