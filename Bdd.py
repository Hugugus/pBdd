import copy
import os
import sqlite3
import time

import np as np

from Key import Key


class Bdd:
    def __init__ (self,db): #on charge la bdd
        self.db=db
        self.tab=[]

    def printBdd(self): #Affiche bdd complete
        if len(self.notDF())==0:
            connect=sqlite3.connect(self.db)
            c=connect.cursor()
            res1=False
            tab=c.execute("SELECT name from sqlite_master WHERE type='table' and name NOT LIKE 'sqlite_%';")
            check=""
            j=0;
            for i in tab:
                print("(",end='')
                print(j,end='')
                print(") : ",end='')
                print(i[0])
                j+=1
        else :
            print("Il y a des DF ayant des attributs n'etant pas dans leur table \n")
        return j

    def printTable(self,tab,p): #affiche une table complete
        #print(tab)
        cTab=self.notDF()
        con = sqlite3.connect(self.db)
        s=str(""+"select * from "+tab +" limit 1")
        #print(s)
        cursor=con.execute(s)
        col_name=[i[0] for i in cursor.description]
        for i in range (len(col_name)):
            print(col_name[i],end=" |")

        print()
        cursor = con.execute('select * from '+str(tab))
        # Get the name of columns
        names = [description[0] for description in cursor.description]

        if p:
         rows = cursor.fetchall()
         for row in rows:
            for name, val in zip(names,row):
                print( val,end=" |")
            print()

    def checkDF(self,tab,arg): #Verfiei si la df créé à de bon argument
        res=True
        con = sqlite3.connect(self.db)
        s=str(""+"select * from "+tab +" limit 1")
        cT=[len(arg)]
        #print(s)
        cursor=con.execute(s)
        col_name=[i[0] for i in cursor.description]
        for j in range (len(arg)):
            for i in range (len(col_name)):
                if(col_name[i]==arg[j]):
                    cT[j]=True
                    break
            if len(cT[j])==0:
                cT[j]=False
        for i in range (len(cT)):
            if cT[i]==False:
                res=False
        return res


    def selectTable(self,x):
        connect=sqlite3.connect(self.db)
        c=connect.cursor()
        res1=False
        tab=c.execute("SELECT name from sqlite_master WHERE type='table' and name NOT LIKE 'sqlite_%';")
        res=""
        j=0
        for i in tab:
            if(j==x):
                res=i
                break
            j+=1

        return res

    def checkT(self,tabN,encode,dst): #verifie qu'une DF est dans la table de la bdd
        connect=sqlite3.connect(self.db)
        c=connect.cursor()
        res1=False
        tab=c.execute("SELECT name from sqlite_master WHERE type='table' and name NOT LIKE 'sqlite_%';")
        check=""
        for i in tab:
            #print(i)
            if i[0]==tabN:
                #print("perfect")
                check=i[0]
                res1=True
                break
        if(res1):
            #print()
            #print(check)
            tab=c.execute("select * from "+check)
            row=c.fetchall()
            #c.f
            for i in tab:
                print(i)
        connect.close()
        return res1

    def notDF(self): #Donne le numero de la DF se trouvant danns self.tab qui est incoherente
        connect=sqlite3.connect(self.db)
        c=connect.cursor()
        res1=False
        checkT=[]
        res=[]
        tab = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        check=""
        #print("notDF:\n")
        for i in tab:
            tabF=c.execute("select * from "+i[0])
            names = list(map(lambda x: x[0], tabF.description))
            for j in names:
                checkT.append(j)

        for z in range(len(self.tab)):
            i=self.tab[z]

            s1=i[1]
            s2=i[2]
            s1=s1.replace("\n","")
            s1=s1.split(" ")
            s2=s2.replace("\n","")
            s2=s2.replace(" ","")

            for x in s1:
                if x not in checkT:
                    if i not in res:
                        res.append(z)
            if s2 not in checkT:
                if i not in res:
                    res.append(z)

        connect.close()
        return res

    def printFuncDep(self,editing): #Afficher toutes les DF
        res=False
        if len(self.tab)>0:
            if(len(self.notDF())==0):
                res=True
                print("Voici les DF de la bdd\n")
                for i in range (len(self.tab)):
                    tab=self.tab[i]
                    print("("+str(i)+")",end='')
                    print(" "+tab[0]+" : "+tab[1]+" -> "+tab[2])

                if editing :

                    c=input("\nQue voulez-vous afficher de plus?\n(0) : Les DF non satisfait \n(1) : Les DF étant des consequences logique\n(2) : Rien\n")

                    if(c=="0"): #DF non satisfaite
                        tabR=self.notWdF()
                        #print(tabR)
                        print("DF non satisfaite")
                        #self.printFuncDep(False)
                        if len(tabR)>0:
                            for i in range (len(self.tab)):
                                if not tabR[i]:
                                    tab=self.tab[i]
                                    print(i,end='')
                                    print(" "+tab[0]+" : "+tab[1]+" -> "+tab[2])
                            c=input("Voulez-vous supprimer toutes ces DF?\n(0) : Oui\n(1) : Non\n")
                            if c=="0":
                                for i in range (len(self.tab)):
                                    if not tabR[i]:
                                        self.deleteDF(int(i))
                        else :
                            print ("Il n'y a pas de DF non statisfaite")

                    elif c=="1": #DF consequence logique
                        tab=self.logDf()
                        if len(tab)==0:
                            print("Il n'y pas de DF étant des consequences logique")
                        else :
                            print("DF étant des consequences logique : ")
                            if len(tab)>0:
                                for i in range (len(tab)):
                                    #print(tab)
                                    t=self.tab[int(tab[i])]
                                    print(str(tab[i])+" "+t[0]+" : "+t[1]+" -> "+t[2])

                                    #print(i,end='')
                                c=input("Voulez-vous supprimer toutes ces DF?\n(0) : Oui\n(1) : Non\n")
                                if c=="0":
                                    for i in range (len(tab)):
                                        self.deleteDF(int(tab[i]))

                            else :
                                print("Il n'y pas de DF étant des consequences logique")


            else : #Si DF avec des elements incorrects
                print("\nIl y a des DF ayant des attributs n'etant pas dans leur table a supprimer d'abord\n")
                #DF dont les attributs ne sont pas dans la table
                resNDF=[]
                tab=self.notDF()
                print("DF dont les attributs ne sont pas dans la table : ")
                if len(tab)>0:
                    for i in tab:
                        #print(tab)
                        t=self.tab[int(i)]
                        resNDF.append(int(i))
                        print(str(i)+" "+t[0]+" : "+t[1]+" -> "+t[2])
                v=input("\nVoulez-vous supprimer toutes les DF ayant pas des attributs qui ne sont pas la bdd?\n(0) : Oui\n(1) : Non\n")
                if v=="0":
                    tab=self.notDF()
                    for i in tab:
                        self.deleteDF(int(i))

        else : #Si pas de DF
            print("Il n'y a actuellement aucune DF, veuillez en génerer, en ajouter ou en charger")
        return res

    def logDf(self): # DF transitive
        res=[]
        if(len(self.tab)>2):

            x=0
            for i in self.tab:
                for j in self.tab:
                    x=0
                    for k in self.tab:

                        if i!=j and i!=k and j!=k :
                            if i[0]==j[0] and k[0]==j[0]: #meme table

                                #Corrige les erreurs des valeurs qui rendent impossible l'egalité

                                a1=np.array(i[1].replace("\n",""))
                                a2=np.array(i[2].replace("\n",""))
                                b1=np.array(j[1].replace("\n",""))
                                b2=np.array(j[2].replace("\n",""))
                                c1=np.array(k[1].replace("\n",""))
                                c2=np.array(k[2].replace("\n",""))

                                if (np.array_equal(a1,c1)):
                                    """      
                                    print("\n")
                                    print(a1,end=", ")
                                    print(a2)
                                    print(b1,end=", ")
                                    print(b2)
                                    print(c1,end=", ")
                                    print(c2)
                                    print("test")
                                    print("\n")
                                    print(a2,end=", ")
                                    print(b1,end=", ")
                                    print(np.array_equal(a2,b1))
                                    print()"""

                                    if (np.array_equal(a2,b1) ):

                                        if ( np.array_equal(b2,c2)):
                                            if(k not in res):
                                                #tab=[x,k]
                                                #res.append(tab)
                                                res.append(x)
                                            #print("ici",end=" ")
                                            #print(res)

                        x+=1
        return res


    def notWdF(self): #Affiche les Df non satisfaite

        res=[]
        con = sqlite3.connect(self.db)
        for r in range (len(self.tab)): #Parcourt les DF
            current=True
            res.append(current)
            res
            tab=self.tab[r]
            tN=tab[0]
            vi=tab[1]
            #print("check")
            #print(self.tab)
            #print(vi)
            #print("type")
            ##print(type(vi))
            cV=[] #tableau stockant toutes les valeur a gauche de la df
            vi=vi.split(" ")
            v=""
            for i in range (len(vi)):
                v=v+vi[i]
                v=v+","
            if v[len(v)-1]==",":
                v=v[:-1]
            #print("ici")
            #print(",".join(v.split(" ")))
            t=tab[2]
            cT=[]   #tablea stockant toutes les valeurs a droite de la df

            #verification si df satisfaite

            #print("ici v "+v+" ",end="")
            #print(r)
            cursor = con.execute('select '+v+' from '+str(tN))
            names = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            i=0
            for row in rows:
                    #print( row,end=" |")
                    cV.append(row)
                    i+=1
                #print()
            #print("cV",end="    ")
            #print(cV)
            i=0
            cursor = con.execute('select '+str(t)+' from '+str(tN))
            names = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            for row in rows:
                for name, val in zip(names,row):
                    #print( val,end=" |")
                    cT.append(val)
                i+=1
                #print()

           # print("cT",end="  ")
            #print(cT)
            for i in range (len(cV)):
                for j in range(len(cV)):
                    if i!=j:
                        #Converti tuple en array pour utiliser le comparateur de array
                        a=np.array(cV[i])
                        #print(a)
                        b=np.array(cV[j])

                        if( np.array_equal(a,b)):
                            aC=np.array(cT[i])
                             #print(a)
                            bC=np.array(cT[j])
                            #print("\n iZi\n")
                            #print(aC,end="   ")
                            #print(bC)
                            if not np.array_equal(aC,bC):
                                current=False
                                res[r]=current
                                break
                if not current:
                    break

        return res


    def addFuncDep(self,tabN,encode,dst): # Permet d'ajouter une DF
            check=dst.split(" ")
            if(len(check)==1): #Si dst n'a que 1 element
                tabh=[]
                if not self.tab:
                    self.tab=[]
                tabh=[]
                tabh.append(tabN)
                tabh.append(encode)
                tabh.append(dst)
                self.tab.append(tabh)
                self.apply(tabh)
            else:
                print("La partie a droite de la DF a plus d'une valeur \n")


    def apply(self,tab):
        print("ok")

    def save(self,txt): #Permet de sauvegarder les DF
        save = open(txt,"w")
        for i in range (0,len(self.tab)):
            tab=self.tab[i]
            tab[2]=tab[2].replace("\n","")
            s=''.join(tab[0])+','+"".join(tab[1])+','+"".join(tab[2]+"\n")
            save.write(s)
        print (save)
        save.close()

    def deleteDF(self,i): #Permet de supprimer une df
        print("Cette DF a été supprimé ",end='')
        print(self.tab[i][1]+" -> "+self.tab[i][2])
        self.tab.remove(self.tab[i])
        #self.printFuncDep(False)

    def edit(self): #Permet de modifier une DF
        if len(self.tab)>0:
            self.printFuncDep(False)
            print("\n Quel numero de df voulez vous selectionner ?")
            val=input()
            val=int(val)
            c=len(self.tab)
            if val<c:
                res=self.tab[val]
                print("\nDf selectionné  : ")
                print(res[1]+" -> "+res[2])
                self.printTable(str(res[0]),True)
                print("Que voulez-vous modifier ?\n(0) : Les attributs\n(1) : La cible\n(2) : Les deux")
                val=int(input())
                if(val==0):
                    c=input("Veuilliez entrer entrer le nouvel attribut\n")
                    res[1]=c
                elif (val==2):
                    c=input("Veuilliez entrer entrer une nouvelle cible\n")
                    res[2]=c
                elif (val==3):
                    c1=input("Veuilliez entrer entrer le nouvel attribut\n")
                    c2=input("Veuilliez entrer entrer une nouvelle cible\n")
                    res[1]=c1
                    res[2]=c2



    def load(self,txt): #charge une sauvegarde de DF
        self.tab=[]
        tabh=[]
        with open(txt) as file:
             lines = file.readlines()
             #print(lines)
            # print(len(lines))
             #print()
             for j in range (0,len(lines)):
                tabh=[]
                if len(lines[j])>2:
                    tab=lines[j].split(",")
                    tab[2]=tab[2].replace("\n","")
                    #print("ici")
                    #print(tab)
                    if(self.checkT(tab[0],tab[1],tab[2])): #si chargement de donéé correct
                        for i in range (len(tab)):
                            tabh.append(tab[i])
                        self.tab.append(tabh)
                    else :
                        print("Donne inutilisable")
                        self.tab=[]


    def getKey(self): #Permet d'obtenir les clé via DF
        if(self.printFuncDep(False)):
            keyF=[]
            connect=sqlite3.connect(self.db)
            c=connect.cursor()
            res1=False
            checkT=[]
            res=[]
            tab = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            print()
            print("\nVoici toutes les tab :\n")
            for i in tab:
                print(i[0])
            check=""
            #print("notDF:\n")
            v=input("\nVous voulez generer les clés de quelle table?\n")
            tabF=c.execute("select * from "+v)
            names = list(map(lambda x: x[0], tabF.description))
            print("\n       Voici les attributs present dans la table : \n")
            for j in names:
                print(j,end=", ")
            print("\nVoici les DF de la table :\n")
            df=[]
            #toutes les Df de la table selectionné
            for i in self.tab:
                if i[0]==v:
                    print(i[1],end=" -> ")
                    print(i[2])
                    df.append(i)

            # toutes les valeurs a droites
            vD=[]
            #print("\nvD")
            for i in df:
                #print(i[2])
                    s=i[2].replace(" ","")
                    vD.append(s)
            #print(vD)
            print()
            # toutes les valeurs a gauche
            vG=[]
            for i in df:
                h=i[1].split(" ")
                vG.append(i[1])

            #print("\nvG")
            #print(vG)

            name= list(map(lambda x: x[0], tabF.description)) #elements avoir
            init=Key(name,df)
            res=init.getKey()
            print("Voici les cléF de la table "+v)
            print()
            for i in res:
                print(i)
            print("\n")
            v=input("Voulez-vous verifier si cette table respecte les des normes BCNF et 3NF?\n(0) : Oui\n(1) : Non\n")
            if v=="0":
                target=init.getNorme(res,df,name)
                print(v[0],end=" : BCNF= ")
                print(target[0],end=" et  3NF= ")
                print(target[1])
                print()

            return  res

    def getTKey(self):
        if(self.printFuncDep(False)):
            print()
            connect=sqlite3.connect(self.db)
            c=connect.cursor()
            tab = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            for v in tab:
                df=[]
                #toutes les Df de la table
                for i in self.tab:
                    if i[0]==v[0]:
                        df.append(i)
                tabF=c.execute("select * from "+v[0])
                names = list(map(lambda x: x[0], tabF.description))
                init=Key(names,df)
                key=init.getKey()
                print("\nAttribut de la tab "+v[0]+" :")
                for i in names:
                    print(i,end=" | ")
                print()
                time.sleep(1)
                print("DF de la table "+v[0]+" : ")
                for i in df:
                    print(i[1],end=" -> ")
                    print(i[2])
                time.sleep(1)
                print("cle de la table "+v[0]+" : ")
                for i in key:
                    print(i)

                print()
                time.sleep(1)
                target=init.getNorme(key,df,names)
                print(v[0],end=" : BCNF= ")
                print(target[0],end=" et  3NF= ")
                print(target[1])
                print("------------------------------------------------------------------------------------------------------")
                time.sleep(2)



