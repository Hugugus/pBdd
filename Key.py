import copy

from DF import DF


class Key:
    def __init__(self,allN,df): #Permet de facilement manipuler les DF
        self.allN=allN
        self.DFv=[]
        self.DF=df
        dfH=[]
        for x in df:
            #print("ici x "+str(x))
            h=x[1].replace(" ","")
            dfH.append(DF(h,x[2].replace(" ","")))
        self.help=dfH



    def getKey(self): #Methode permettant d'obtenir les clés
        res=[]
        for i in range(len(self.DF)):
            v=[]
            allN=copy.deepcopy(self.allN) #Garde tous les attributs a avoir
            #print("all name ")
            #print(allN,end=" -> ")
            right=self.DF[i][2].replace(" ","")

            help=copy.deepcopy(self.help)

            tab=[]
            help=copy.deepcopy(self.help)
            left=self.DF[i][1].replace(" ","")

            x=left #selectionne la partie de gauche que l'on a actuellement

            for y in help: #parcourt toutes les DF
                    if y.getK()==x: #si valeur de gauche de la DF = la DF qu'on traite

                        h=self.DF[i][1].split(" ") #si partie de gauche composé
                        if x==h[0]:
                            tab.append(x)
                            if x in allN:
                                allN.remove(x)
                        else :
                            for i in help: #enleve tous les attributs qui ont le meme nom que celui qu'on a initialement (DF non composé)
                                if i.getK()==right or i.getV()==right:
                                    help.remove(i)
                                    if i.getK() in allN:
                                        allN.remove(i.getK())
                                    if i.getV() in allN:
                                        allN.remove(i.getV())

                            for v in h: #enleve tous les attributs qui ont le meme nom que celui qu'on a initialement (DF composé)
                                    tab.append(v)
                                    if v in allN:
                                        allN.remove(v)
                                    for i in help:
                                        if i.getV()==x:
                                            help.remove(i)
                                    self.deleteSame(v,allN,help)

                        for z in help: # Verification s'il existe d'autre DF avec les meme valeur a droite de la DF
                            if z!= y:
                                if z.getV()==y.getK() or z.getK()==y.getK():
                                    if z in help:
                                        help.remove(z)
                                        if z.getK() in allN:
                                            allN.remove(z.getK())

            for i in allN: #Verfication pour retirer tous les attributs issu des clé / a retirer
                for j in help:
                    if i==j.getK():
                        if i not in tab:
                            tab.append(i)
                        if j in help:
                            help.remove(j)
                        if i in allN:
                            allN.remove(i)
                        if j.getV() in allN:
                            allN.remove(j.getV())
                    if i==j.getV():
                        if i not in tab:
                            tab.append(i)
                        if j in help:
                            help.remove(j)
                        if i in allN:
                            allN.remove(i)

            for i in allN: #Rajoute tous les attributs manquants
                tab.append(i)

            help=copy.deepcopy(self.help)
            tab.sort()
            for x in tab: #Retire d'une clé : un attribut qui aurait toute sa DF (partie de gauche et de droite)
                for y in help:
                    if x==y.getK():
                        if y.getV() in tab:
                            tab.remove(y.getV())



            if tab not in res:
                res.append(tab)


        for i in res: #enleve un reponse si elle est inclus à une autre
            str="".join(i)
            for j in res:
                str2="".join(j)
                if i!=j:
                    if str in str2 and len(str)<len(str2):
                        res.remove(j)

        return res


    def deleteSame(self,y,allN,help):
        for z in help: # Verification s'il existe d'autre DF avec les meme valeur a droite de la DF (pour DF composé)
                if z.getK()==y:
                    help.remove(z)
                    if z.getV() in allN:
                        allN.remove(z.getV())
                        if z in help:
                            help.remove(z)
                if z.getV()==y:

                    if z in help:
                        help.remove(z)
                        if z.getK() in allN:
                            allN.remove(z.getK())

    def getNorme(self,key,DF,allN): #Permet de verfifier les norme BCNF et 3NF
        res=[True,False]
        for x in DF: #BCNF

            name=copy.deepcopy(allN)
            if len(name)>0 and len(DF)>=2:

                f=x[1].split(" ")
                for y in f:
                    name.remove(y)
                if x[2] in name:
                        name.remove(x[2])
                for j in DF:
                    if x[1]==j[1] and x[2]!=j[2] :
                        if j[2] in name:
                            name.remove(j[2])
                if len(name)!=0:
                    res[0]=False
                    break
        if not res[0]: #Si pas BCNF

            #3NF
            resT=[]
            for x in DF:
                name=copy.deepcopy(allN)
                for y in key: # Si parti de droite appartient à un clé
                    current=False
                    if x[2] in y:

                        current=True
                        resT.append(current)
                if not current:# Sinon : est-ce que la parti de gauche determine tout?
                        for j in DF:
                            if x[1]==j[1] and x[2]!=j[2] :
                                if j[2] in name:
                                    name.remove(j[2])
                        if len(name)!=0:
                            res[1]=False
                            break
                        else :
                            current=True
                            resT.append(current)

            if len(resT)>=len(key): #Verification qu'il ya assez de
                    res[1]=True
        else: # Si BCNF
            res=[True,True]
        if len(DF)==0: #Si pas de DF
                res=[False,False]

        return res








