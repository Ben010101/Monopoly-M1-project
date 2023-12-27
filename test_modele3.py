#%% création des joueurs
%reset -f

import numpy as np 

nb_partie=1
nb_vict=np.zeros(4)


#%%Classe Joueur

class Joueur: 
    def __init__(self, argent = 1500, position = 0, patrimoine = [], carteprison = 0, cpt_double = 0, nb_gares = 0, nb_compagnies = 0 , prisonnier = 0, liste_mono = [],nb_monopole = [0]*8,elimine = False, achat_imp=False): # j'ai rajouté un compteur de cartes sortez de prison et un compteur de lancers de dés double
        self.argent = argent
        self.position = position
        self.patrimoine = patrimoine
        self.carteprison = carteprison
        self.cpt_double = cpt_double
        self.nb_gares = nb_gares
        self.nb_compagnies = nb_compagnies
        self.prisonnier = prisonnier
        self.liste_mono = liste_mono
        self.nb_monopole = nb_monopole
        self.elimine = elimine
        self.achat_imp = achat_imp
        
    def prisonnier_fct(self):
        loyer=50
        self.prisonnier=0
        if self.carteprison != 0:
            self.carteprison -= 1
            self.prisonnier = 0
            if 9 not in cartechance:
                cartechance.append(9)
            else:
                cartecommu.append(9)
        else:
            if self.argent >= 50:
                self.argent -= 50
                self.prisonnier= 0
            else:
                if(self.Vente_maison(loyer)==True):
                    self.argent-=50
                else:
                    banque.elimination(self)
        return

    
    def elimination(self,Joueur_perdant):
        
        """Methode d'elimination"""  
        #heritage gare et compagnie
        self.nb_gares+=Joueur_perdant.nb_gares
        self.nb_compagnies+=Joueur_perdant.nb_compagnies
      
        for prop in plateau:
            if prop.position in [5,15,25,35, 12, 28]:
                if prop.proprietaire == Joueur_perdant:
                    prop.proprietaire = self
        #heritage de l'argent            
        self.argent += Joueur_perdant.argent
        Joueur_perdant.argent = 0
        
        #heritage du patrimoine
        for i in range (len(Joueur_perdant.patrimoine)):
            Joueur_perdant.patrimoine[i].proprietaire = self       
            self.patrimoine.append(Joueur_perdant.patrimoine[i])
            if(Joueur_perdant.patrimoine[i].couleur == "marron"): self.nb_monopole[0] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "bleu_c"): self.nb_monopole[1] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "rose"): self.nb_monopole[2] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "orange"): self.nb_monopole[3] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "rouge"): self.nb_monopole[4] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "jaune"): self.nb_monopole[5] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "vert"): self.nb_monopole[6] += 1
            elif(Joueur_perdant.patrimoine[i].couleur == "bleu_f"): self.nb_monopole[7] += 1
            
        #Joueur_perdant.patrimoine = []
        self.update_mono()
        Joueur_perdant.elimine = True

    
    """update de la liste des monopoles"""  
    def update_mono(self):
        if(self.nb_monopole[0]==2):
            if ("marron" in self.liste_mono):
                return
            else:
                self.liste_mono.append("marron")
                
        if(self.nb_monopole[1]==3):
            if ("bleu_c" in self.liste_mono):
                return
            else:
                self.liste_mono.append("bleu_c")

        if(self.nb_monopole[2]==3):
            if ("rose" in self.liste_mono):
                return
            else:
                self.liste_mono.append("rose")
          
        if(self.nb_monopole[3]==3):
            if ("orange" in self.liste_mono):
                return
            else:
                self.liste_mono.append("orange")
            
        if(self.nb_monopole[4]==3):
            if ("rouge" in self.liste_mono):
                return
            else:
                self.liste_mono.append("rouge")

        if(self.nb_monopole[5]==3):
            if ("jaune" in self.liste_mono):
                return
            else:
                self.liste_mono.append("jaune")

        if(self.nb_monopole[6]==3):
            if ("vert" in self.liste_mono):
                return
            else:
                self.liste_mono.append("vert")

        if(self.nb_monopole[7]==2):
            if ("bleu_f" in self.liste_mono):
                return
            else:
                self.liste_mono.append("bleu_f")
   
              
        
                
    def Paye(self, case):
        loyer = case.loyer
        if case.couleur in case.proprietaire.liste_mono and (case.nb_maison == 0) and (case.nb_hotel ==0):
          loyer = loyer * 2 #Si le proprietaire possède toutes les prop de la couleur : loyer x2
        if (self.argent >= loyer):
            self.argent -= loyer
            case.proprietaire.argent += loyer
        else:
            if self.Vente_maison(loyer)== True:
                self.argent -= loyer
                case.proprietaire.argent += loyer
            else:
                case.proprietaire.elimination(self)
  
  
    def Paye_g(self,case):
          loyer= 25 * 2**(case.proprietaire.nb_gares - 1)
           #Modification du loyer selon le nb de gare possédée #Modification du loyer selon le nb de gare possédée
          if (self.argent >= loyer):
              self.argent -= loyer
              case.proprietaire.argent += loyer
          else:
              if self.Vente_maison(loyer)== True:
                  self.argent -= loyer
                  case.proprietaire.argent += loyer
              else:
                case.proprietaire.elimination(self)

  
    def Paye_comp(self, case, lancer):
        loyer=0
        if case.proprietaire.nb_compagnies == 1: #S'il n'en possède qu'une, le loyer vaut 4x le lancer de dés
              loyer = lancer * 4
        elif self.nb_compagnies == 2: #S'il possède les deux, le loyer vaut 10x le lancer de dés
              loyer = lancer * 10
        if (self.argent >= loyer):
            self.argent -= loyer
            case.proprietaire.argent += loyer
        else:
            if self.Vente_maison(loyer)== True:
                self.argent -= loyer
                case.proprietaire.argent += loyer
            else:
                case.proprietaire.elimination(self)
            
    def ajout_maison(self, case, n):   #n vaut 1 ou -1
         

        argent_avt_achat=self.argent
        
        """ Loyer de la propriété Boulevard de belleville"""
        if case.position == 1:
            if n>0:
                self.argent -= 50
            else:
                self.argent += 25
            if case.nb_maison == 0 and case.nb_hotel == 0: 
                case.loyer = 2     
            elif case.nb_maison == 1:
                case.loyer = 10
            elif case.nb_maison == 2:
                case.loyer= 30
            elif case.nb_maison == 3:
                case.loyer = 90
            elif case.nb_maison == 4:
                case.loyer = 160
            if case.nb_hotel == 1:
                case.loyer = 250
                
        """ Loyer de la propriété Rue Lecourbe"""
        if case.position == 3:
            if n>0:
                self.argent -= 50
            else:
                self.argent += 25
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 4
            elif case.nb_maison == 1:
                case.loyer = 20
            elif case.nb_maison == 2:
                case.loyer= 60
            elif case.nb_maison == 3:
                case.loyer = 180
            elif case.nb_maison == 4:
                case.loyer = 320
            if case.nb_hotel == 1:
                case.loyer = 450
        
            """ Loyer des propriétés Rue de Vaugirard et Rue de Courcelles"""
        if (case.position == 6 or case.position == 8):
            if n>0:
                self.argent -= 50
            else:
                self.argent += 25
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 6
            elif case.nb_maison == 1:
                case.loyer = 30
            elif case.nb_maison == 2:
                case.loyer= 90
            elif case.nb_maison == 3:
                case.loyer = 270
            elif case.nb_maison == 4:
                case.loyer = 400
            if case.nb_hotel == 1:
                case.loyer = 550
        
        """ Loyer de la propriété Avenue de la République"""
        if case.position == 9:
            if n>0:
                self.argent -= 50
            else:
                self.argent += 25
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 8
            elif case.nb_maison == 1:
                case.loyer = 40
            elif case.nb_maison == 2:
                case.loyer= 100
            elif case.nb_maison == 3:
                case.loyer = 300
            elif case.nb_maison == 4:
                case.loyer = 450
            if case.nb_hotel == 1:
                case.loyer = 600
        
        """ Loyer de la propriété Boulevard de la villette et Avenue de Neuilly """
        if (case.position == 11 or case.position ==13):
            if n>0:
                self.argent -= 100
            else:
                self.argent += 50
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 10
            elif case.nb_maison == 1:
                case.loyer = 50
            elif case.nb_maison == 2:
                case.loyer= 150
            elif case.nb_maison == 3:
                case.loyer = 450
            elif case.nb_maison == 4:
                case.loyer = 625
            if case.nb_hotel == 1:
                case.loyer = 750
        
        """ Loyer de la propriété Rue de Paradis """
        if case.position == 14:
            if n>0:
                self.argent -= 100
            else:
                self.argent += 50
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 12
            elif case.nb_maison == 1:
                case.loyer = 60
            elif case.nb_maison == 2:
                case.loyer= 180
            elif case.nb_maison == 3:
                case.loyer = 500
            elif case.nb_maison == 4:
                case.loyer = 700
            if case.nb_hotel == 1:
                case.loyer = 900
        """ Loyer de la propriété Avenue Mozart et Boulevard St Michel """
        if (case.position == 16 or case.position == 18):
            if n>0:
                self.argent -= 100
            else:
                self.argent += 50
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 14
            elif case.nb_maison == 1:
                case.loyer = 70
            elif case.nb_maison == 2:
                case.loyer= 200
            elif case.nb_maison == 3:
                case.loyer = 550
            elif case.nb_maison == 4:
                case.loyer = 750
            if case.nb_hotel == 1:
                case.loyer = 950
        
        """ Loyer de la propriété Place Pigalle """
        if case.position == 19:
            if n>0:
                self.argent -= 100
            else:
                self.argent += 50
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 16
            elif case.nb_maison == 1:
                case.loyer = 80
            elif case.nb_maison == 2:
                case.loyer= 220
            elif case.nb_maison == 3:
                case.loyer = 600
            elif case.nb_maison == 4:
                case.loyer = 800
            if case.nb_hotel == 1:
                case.loyer = 1000
        
        """ Loyer de la propriété Avenue Matignon et Boulevard Malesherbes"""
        if (case.position == 21 or case.position == 23):
            if n>0:
                self.argent -= 150
            else:
                self.argent += 75
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 18
            elif case.nb_maison == 1:
                case.loyer = 90
            elif case.nb_maison == 2:
                case.loyer= 250
            elif case.nb_maison == 3:
                case.loyer = 700
            elif case.nb_maison == 4:
                case.loyer = 875
            if case.nb_hotel == 1:
                case.loyer = 1050
        
        """ Loyer de la propriété Avenue Henry-Martin"""
        if case.position == 24:
            if n>0:
                self.argent -= 150
            else:
                self.argent += 75
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 20
            elif case.nb_maison == 1:
                case.loyer = 100
            elif case.nb_maison == 2:
                case.loyer= 300
            elif case.nb_maison == 3:
                case.loyer = 750
            elif case.nb_maison == 4:
                case.loyer = 925
            if case.nb_hotel == 1:
                case.loyer = 1100
                
        """ Loyer de la propriété Faubourg St-Honoré et Place de la Bourse"""
        if (case.position == 26 or case.position == 27):
            if n>0:
                self.argent -= 150
            else:
                self.argent += 75
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 22
            elif case.nb_maison == 1:
                case.loyer = 110
            elif case.nb_maison == 2:
                case.loyer= 330
            elif case.nb_maison == 3:
                case.loyer = 800
            elif case.nb_maison == 4:
                case.loyer = 975
            if case.nb_hotel == 1:
                case.loyer = 1150
            
        """ Loyer de la propriété Rue Lafayette"""
        if case.position == 29:
            if n>0:
                self.argent -= 150
            else:
                self.argent += 75
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 24
            elif case.nb_maison == 1:
                case.loyer = 120
            elif case.nb_maison == 2:
                case.loyer= 360
            elif case.nb_maison == 3:
                case.loyer = 850
            elif case.nb_maison == 4:
                case.loyer = 1025
            if case.nb_hotel == 1:
                case.loyer = 1200
                
        """ Loyer de la propriété Avenue de Breteuil et Avenue Foch"""
        if (case.position == 31 or case.position == 32):
            if n>0:
                self.argent -= 200
            else:
                self.argent += 100
            if case.nb_maison == 0:
                case.loyer = 26
            elif case.nb_maison == 1:
                case.loyer = 130
            elif case.nb_maison == 2:
                case.loyer= 390
            elif case.nb_maison == 3:
                case.loyer = 900
            elif case.nb_maison == 4:
                case.loyer = 1100
            if case.nb_hotel == 1:
                case.loyer = 1275
                
        """ Loyer de la propriété Boulevard des Capucines"""
        if case.position == 34:
            if n>0:
                self.argent -= 200
            else:
                self.argent += 100
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 28
            elif case.nb_maison == 1:
                case.loyer = 150
            elif case.nb_maison == 2:
                case.loyer= 450
            elif case.nb_maison == 3:
                case.loyer = 1000
            elif case.nb_maison == 4:
                case.loyer = 1200
            if case.nb_hotel == 1:
                case.loyer = 1400
                
        """ Loyer de la propriété Avenue des Champs-Elysées"""
        if case.position == 37:
            if n>0:
                self.argent -= 200
            else:
                self.argent += 100
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 35
            elif case.nb_maison == 1:
                case.loyer = 175
            elif case.nb_maison == 2:
                case.loyer= 500
            elif case.nb_maison == 3:
                case.loyer = 1100
            elif case.nb_maison == 4:
                case.loyer = 1300
            if case.nb_hotel == 1:
                case.loyer = 1500
                
        """ Loyer de la propriété Rue de la Paix"""
        if case.position == 39:
            if n>0:
                self.argent -= 200
            else:
                self.argent += 100
            if case.nb_maison == 0 and case.nb_hotel == 0:
                case.loyer = 50
            elif case.nb_maison == 1:
                case.loyer = 200
            elif case.nb_maison == 2:
                case.loyer= 600
            elif case.nb_maison == 3:
                case.loyer = 1400
            elif case.nb_maison == 4:
                case.loyer = 1700
            if case.nb_hotel == 1:
                case.loyer = 2000 
                  
        if(self.argent<0):
            self.achat_imp=True
            self.argent = argent_avt_achat
        else:
            self.achat_imp=False
            """Méthode pour ajouter/supprimer une maison sur la propriété et met à jour le loyer et l'argent que possède le joueur"""
            if n<0: #vente maison, vaut forcément -1
                if case.nb_hotel==1:
                    case.nb_hotel=0
                    case.nb_maison=4
                elif case.nb_maison > 0:
                    case.nb_maison-=1
                elif case.nb_maison == 0: 
                    return
            if n>0:
                if case.nb_hotel==1:
                    return
                elif case.nb_maison==4:
                    case.nb_maison=0
                    case.nb_hotel=1
                
                else:
                    case.nb_maison += 1
        
        
        
        
    def Vente_maison(self, loyer):
        for prop in self.patrimoine:
            if prop.position in [1,3,6,8,9,11,13,14,16,17,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                if prop.nb_hotel != 0:
                    self.ajout_maison(prop,-1)
            if self.argent >= loyer:
                return True
            else:
                for prop in self.patrimoine:
                    if prop.position in [1,3,6,8,9,11,13,14,16,17,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                        if prop.nb_maison==4:
                            self.ajout_maison(prop,-1)
                    if self.argent >= loyer:
                        return True
                    else:
                        for prop in self.patrimoine:
                            if prop.position in [1,3,6,8,9,11,13,14,16,17,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                                if prop.nb_maison==3:
                                    self.ajout_maison(prop,-1)
                            if self.argent >= loyer:
                                return True
                            else:
                                for prop in self.patrimoine:
                                    if prop.position in [1,3,6,8,9,11,13,14,16,17,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                                        if prop.nb_maison==2:
                                            self.ajout_maison(prop,-1)
                                    if self.argent >= loyer:
                                        return True
                                    else:
                                        for prop in self.patrimoine:
                                            if prop.position in [1,3,6,8,9,11,13,14,16,17,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                                                if prop.nb_maison==1:
                                                    self.ajout_maison(prop,-1)
                                            if self.argent >= loyer:
                                                return True
                                            else:
                                                return False
              

class Joueur_random(Joueur):
    def __init__(self, argent = 1500, position = 0, patrimoine = [], carteprison = 0, cpt_double = 0, nb_gares = 0, nb_compagnies = 0 , prisonnier = 0, liste_mono = [],nb_monopole = [0]*8,elimine = False):
        Joueur.__init__(self, argent, position, patrimoine,carteprison,cpt_double,nb_gares, nb_compagnies,prisonnier,liste_mono,nb_monopole,elimine)

    def achat_pr(self,Case):
        if (self.argent > Case.prix):                                  #Case.prix c'est l'attribut cout de l'objet case de la classe case
            tirage = np.random.rand(1)                           
            if (tirage > 0.5): 
                self.patrimoine.append(Case)
                Case.proprietaire = self
                if(Case.couleur == "marron"): self.nb_monopole[0] += 1
                elif(Case.couleur == "bleu_c"): self.nb_monopole[1] += 1
                elif(Case.couleur == "rose"): self.nb_monopole[2] += 1
                elif(Case.couleur == "orange"): self.nb_monopole[3] += 1
                elif(Case.couleur == "rouge"): self.nb_monopole[4] += 1
                elif(Case.couleur == "jaune"): self.nb_monopole[5] += 1
                elif(Case.couleur == "vert"): self.nb_monopole[6] += 1
                elif(Case.couleur == "bleu_f"): self.nb_monopole[7] += 1
                self.update_mono()
                self.argent-=Case.prix

    def achat_gare(self,Case): 
          if (self.argent > Case.prix):                           
              tirage = np.random.rand(1)                           
              if (tirage > 0.5):      
                  self.nb_gares+=1
                  Case.proprietaire = self

    def achat_comp(self,Case): 
          if (self.argent > Case.prix):                           
              tirage = np.random.rand(1)                           
              if (tirage > 0.5):    
                  self.nb_compagnies+=1
                  Case.proprietaire = self  
                  
    def achat_ma(self):
        #construction de la liste
        constructible = []
        if(len(self.liste_mono)==0):  
          return None
        else:
          for i in range(len(self.patrimoine)):
            if(self.patrimoine[i].couleur in self.liste_mono):
              constructible.append(self.patrimoine[i])

        ### modification du seuil ###
        base=self.argent
        self.seuil_ma=np.random.rand(1)[0]*(base)

        ###   STRATEGIE   ###
        hotels_joueur=0
        while(self.argent > self.seuil_ma):


            while(hotels_joueur<=len(constructible) and self.achat_imp == False):  

                for i in range(len(constructible)-1,-1,-1):
                    if(constructible[i].nb_hotel==1):
                        hotels_joueur+=1
                    else:
                        self.ajout_maison(constructible[i],1) 
                                

class Joueur_depensier(Joueur):

    def __init__(self,argent = 1500, position = 0, patrimoine = [], carteprison = 0, cpt_double = 0, nb_gares = 0, nb_compagnies = 0 , prisonnier = 0, liste_mono = [],nb_monopole = [0]*8,elimine = False,achat_imp=False):
            Joueur.__init__(self, argent, position, patrimoine,carteprison,cpt_double,nb_gares, nb_compagnies,prisonnier,liste_mono,nb_monopole,elimine,achat_imp)
            
    def achat_pr(self,Case):
        if (self.argent > Case.prix):   
            self.patrimoine.append(Case)
            Case.proprietaire = self
            if(Case.couleur == "marron"): self.nb_monopole[0] += 1
            elif(Case.couleur == "bleu_c"): self.nb_monopole[1] += 1
            elif(Case.couleur == "rose"): self.nb_monopole[2] += 1
            elif(Case.couleur == "orange"): self.nb_monopole[3] += 1
            elif(Case.couleur == "rouge"): self.nb_monopole[4] += 1
            elif(Case.couleur == "jaune"): self.nb_monopole[5] += 1
            elif(Case.couleur == "vert"): self.nb_monopole[6] += 1
            elif(Case.couleur == "bleu_f"): self.nb_monopole[7] += 1
            self.update_mono()
            self.argent-=Case.prix
        
    def achat_gare(self,Case): 
          if (self.argent > Case.prix):        
              self.nb_gares+=1
              Case.proprietaire = self

    def achat_comp(self,Case): 
          if (self.argent > Case.prix):         
              self.nb_compagnies+=1
              Case.proprietaire = self   

    def achat_ma(self):

        #construction de la liste
        constructible = []
        if(len(self.liste_mono)==0):  
          return None
        else:
          for i in range(len(self.patrimoine)):
            if(self.patrimoine[i].couleur in self.liste_mono):
              constructible.append(self.patrimoine[i])

  
        ### modification du seuil ###
        self.seuil_ma = 0
        
        ###   STRATEGIE   ###
        hotels_joueur=0
        while(self.argent > self.seuil_ma):


            while(hotels_joueur<=len(constructible) and self.achat_imp == False):  

                for i in range(len(constructible)-1,-1,-1):
                    if(constructible[i].nb_hotel==1):
                        hotels_joueur+=1
                    else:
                        self.ajout_maison(constructible[i],1) 


class Joueur_prudent(Joueur):
    def __init__(self, argent = 1500, position = 0, patrimoine = [], carteprison = 0, cpt_double = 0, nb_gares = 0, nb_compagnies = 0 , prisonnier = 0, liste_mono = [],nb_monopole = [0]*8,elimine = False, seuil=0,achat_imp=False):
      Joueur.__init__(self, argent, position, patrimoine,carteprison,cpt_double,nb_gares, nb_compagnies,prisonnier,liste_mono,nb_monopole,elimine,achat_imp)
      self.seuil = seuil
            
    def achat_pr(self,Case):
        self.seuil = 500*(Case.prix)
        if (self.argent > Case.prix):   
            if(self.argent >= self.seuil):
              self.patrimoine.append(Case)
              Case.proprietaire = self
              if(Case.couleur == "marron"): self.nb_monopole[0] += 1
              elif(Case.couleur == "bleu_c"): self.nb_monopole[1] += 1
              elif(Case.couleur == "rose"): self.nb_monopole[2] += 1
              elif(Case.couleur == "orange"): self.nb_monopole[3] += 1
              elif(Case.couleur == "rouge"): self.nb_monopole[4] += 1
              elif(Case.couleur == "jaune"): self.nb_monopole[5] += 1
              elif(Case.couleur == "vert"): self.nb_monopole[6] += 1
              elif(Case.couleur == "bleu_f"): self.nb_monopole[7] += 1
              self.update_mono()
              self.argent-=Case.prix
   
    def achat_gare(self,Case): 
      if (self.argent > Case.prix): 
        self.seuil = 8*(Case.prix)       
        if (self.argent > self.seuil):
          self.nb_gares+=1
          Case.proprietaire = self

    def achat_comp(self,Case): 
      if (self.argent > Case.prix): 
        self.seuil = 8*(Case.prix)        
        if (self.argent > self.seuil):
          self.nb_compagnies+=1
          Case.proprietaire = self

    def achat_ma(self):
        #construction de la liste
        constructible = []
        if(len(self.liste_mono)==0):  
          return None
        else:
          for i in range(len(self.patrimoine)):
            if(self.patrimoine[i].couleur in self.liste_mono):
              constructible.append(self.patrimoine[i])

        
        ### modification du seuil ###
        base = self.argent
        self.seuil_ma = (base)*0.9
        

        ###   STRATEGIE   ###
        hotels_joueur=0
        while(self.argent > self.seuil_ma):


            while(hotels_joueur<=len(constructible) and self.achat_imp == False):   

                for i in range(len(constructible)-1,-1,-1):
                    if(constructible[i].nb_hotel==1):
                        hotels_joueur+=1
                    else:
                        self.ajout_maison(constructible[i],1)   
                        
                        
class Joueur_stratege(Joueur):

    def __init__(self, argent = 1500, position = 0, patrimoine = [], carteprison = 0, cpt_double = 0, nb_gares = 0, nb_compagnies = 0 , prisonnier = 0, liste_mono = [],nb_monopole = [0]*8,elimine = False, seuil=0,achat_imp=False):
        Joueur.__init__(self, argent, position, patrimoine,carteprison,cpt_double,nb_gares, nb_compagnies,prisonnier,liste_mono,nb_monopole,elimine,achat_imp) #nb_monopole = [0]*8, bug qd execution !!
        self.seuil = seuil            
    def achat_pr(self,Case):
        if (self.argent > Case.prix):
            self.seuil=(Case.prix)*5 

            if self.argent > self.seuil:
                self.patrimoine.append(Case)
                Case.proprietaire = self
                if(Case.couleur == "marron"): self.nb_monopole[0] += 1
                elif(Case.couleur == "bleu_c"): self.nb_monopole[1] += 1
                elif(Case.couleur == "rose"): self.nb_monopole[2] += 1
                elif(Case.couleur == "orange"): self.nb_monopole[3] += 1
                elif(Case.couleur == "rouge"): self.nb_monopole[4] += 1
                elif(Case.couleur == "jaune"): self.nb_monopole[5] += 1
                elif(Case.couleur == "vert"): self.nb_monopole[6] += 1
                elif(Case.couleur == "bleu_f"): self.nb_monopole[7] += 1
                self.update_mono()
                self.argent-=Case.prix

    def achat_gare(self,Case): #juste besoin d'ajouter au compteur et de lier la case au joueur en question
         if (self.argent > Case.prix): 
             self.seuil=(Case.prix)*5        
             if (self.argent > self.seuil):
                 self.nb_gares+=1
                 Case.proprietaire = self

    def achat_comp(self,Case): 
          if (self.argent > Case.prix):
              self.seuil=(Case.prix)*5        
              if (self.argent > self.seuil):
                  self.nb_compagnies+=1
                  Case.proprietaire = self     
  
    def achat_ma(self):

        #construction de la liste
        constructible = []
        if(len(self.liste_mono)==0):  
          return None
        else:
          for i in range(len(self.patrimoine)):
            if(self.patrimoine[i].couleur in self.liste_mono):
              constructible.append(self.patrimoine[i])

        
        ### On testera differents seuils ###
        # du prudent au dépensier
        base = self.argent
        self.seuil_ma = (base)*(1/2)
  

        ### STRATEGIE adaptee aux proba ####
        hotels_joueur=0
        constructible.sort(key = lambda x: x.proba0) #on trie par facteur de passage
        while(self.argent > self.seuil_ma):
            while(hotels_joueur<=len(constructible) and self.achat_imp == False):  

                for i in range(len(constructible)-1,-1,-1):
                    if(constructible[i].nb_hotel==1):
                        hotels_joueur+=1
                    else:
                        self.ajout_maison(constructible[i],1) #j'ai mit prix psq je trouvais pas le coût de pose de maison
#%% Classe case

banque=Joueur()

class Case: 
    """ Classe python pour représenter une case du plateau """
    def __init__(self, position, cpt_case=0):
        self.position = position
        self.cpt_case = cpt_case
#%%
        
class propriete(Case):
   """La classe fille propriete hérite de la classe Case"""
   def __init__(self, position, cpt_case, prix, couleur, proba0, proba1, loyer=0, nb_maison=0, nb_hotel=0,  proprietaire=banque):
        Case.__init__(self, position, cpt_case)    #Applique le constructeur de Case à l'instance de propriete 
        self.prix=prix #prix d'achat de la propriété
        self.couleur=couleur
        self.proba0 = proba0
        self.proba1 = proba1
        self.nb_maison = nb_maison
        self.nb_hotel=nb_hotel
        self.loyer = loyer #loyer à verser si on tombe sur la propriété
        self.proprietaire = proprietaire
        
   def effet(self, Joueur):
        if (self.proprietaire == banque):
            Joueur.achat_pr(self)
        elif (self.proprietaire != Joueur):
            Joueur.Paye(self)
 

class gare(Case):
   """La classe fille gare hérite de la classe Case"""
   def __init__(self, position, cpt_case ,prix, proba0, proba1, loyer=25, proprietaire=banque):
        Case.__init__(self, position, cpt_case)
        self.prix=prix
        self.proba0 = proba0
        self.proba1 = proba1
        self.loyer = loyer
        self.proprietaire=proprietaire

   def effet(self, Joueur):
        if (self.proprietaire == banque):
            Joueur.achat_gare(self)
        elif (self.proprietaire != Joueur):
            Joueur.Paye_g(self)

class compagnie(Case):
    def __init__(self, position, cpt_case,prix, proba0, proba1, proprietaire=banque):
        Case.__init__(self, position, cpt_case)
        self.prix=prix
        self.proba0=proba0
        self.proba1=proba1
        self.proprietaire=proprietaire

    def effet(self, Joueur, Res_des):
        if (self.proprietaire == banque):
            Joueur.achat_comp(self)
        elif (self.proprietaire != Joueur):
            Joueur.Paye_comp(self, Res_des)

class taxe(Case):
    def __init__(self, position, cpt_case, prix):
        Case.__init__(self, position, cpt_case)
        self.prix=prix

    def effet(self, Joueur):
          if (Joueur.argent >= self.prix):
              Joueur.argent -= self.prix
          else:
              if Joueur.Vente_maison(self.prix)== True:
                  Joueur.argent -= self.prix
              else:
                  banque.elimination(Joueur)
                  

class impot(Case):
    def __init__(self, position,cpt_case, prix):
        Case.__init__(self, position, cpt_case)
        self.prix=prix

    def effet(self, Joueur):
          if (Joueur.argent >= self.prix):
              Joueur.argent -= self.prix
          else:
              if Joueur.Vente_maison(self.prix)== True:
                  Joueur.argent -= self.prix
              else:
                  banque.elimination(Joueur)
                  
        
class prison(Case):
    def __init__(self, position=30, cpt_case=0):
        Case.__init__(self, position, cpt_case)
        
    def effet(self, Joueur):
        Joueur.position=10
        Joueur.prisonnier=1
        #Rajout du statut prisonnier
        return

class librevisite(Case):
    def __init__(self, position=10, cpt_case=0):
        Case.__init__(self, position, cpt_case)
   
    def effet(self, Joueur):
        return     
   
class chance(Case):
    def __init__(self, position, cpt_case):
        Case.__init__(self, position, cpt_case)
        
    def effet(self, Joueur):
        index = cartechance.pop(0)
        if index != 9: # Si carte "sortez de prison" : pas ajout à la pile
            cartechance.append(index)
        if index == 1: # rue de la paix (39)
            Joueur.position = 39
            rue_paix.effet(Joueur)
            return
        if index == 2: # case depart
            Joueur.position = 0
            Joueur.argent += 200
            return
        if index == 3: # henri martin (24)
            if Joueur.position > 24:
                Joueur.argent += 200
            Joueur.position = 24
            av_henri_martin.effet(Joueur)
            return
        if index == 4: # bd de la vilette (11)
            if Joueur.position > 11:
                Joueur.argent += 200
            Joueur.position = 11
            bd_villette.effet(Joueur)
            return
        if index == 5: #reparations voierie
            amende = 0
            for prop in Joueur.patrimoine: #on regarde le patrimoine des proprietes
                if prop.position in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                    amende += 40*prop.nb_maison + 115*prop.nb_hotel 
            if (Joueur.argent >= amende):
                Joueur.argent -= amende
            else:
                if Joueur.Vente_maison(amende)== True:
                    Joueur.argent -= amende
                else:
                    banque.elimination(Joueur)
            return
        if index == 6: # gare de lyon (15)
            if Joueur.position > 15:
                Joueur.argent += 200
            Joueur.position = 15
            lyon.effet(Joueur)
            return
        if index == 7: # mots croises +100
            Joueur.argent += 100
            return
        if index == 8: #dividende +50
            Joueur.argent += 50
            return
        if index == 9: # libere de prison
            Joueur.carteprison += 1
            return
        if index == 10: # reculez de 3 cases
            Joueur.position -= 3
            Joueur.position = Joueur.position % 40
            plateau[Joueur.position].effet(Joueur)
            return
        if index == 11: # prison
            Joueur.position = 10
            prison1.effet(Joueur)
        if index == 12: # réparations
            amende = 0
            for prop in Joueur.patrimoine: #on regarde le patrimoine des proprietes
                if prop.position in [1,3,6,8,9,11,13,14,16,17,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                    amende += 25*prop.nb_maison + 100*prop.nb_hotel 
            if (Joueur.argent >= amende):
                Joueur.argent -= amende
            else:
                banque.elimination(Joueur)
            
            return
        if index == 13: #exces de vitesse -15
            Joueur.argent -= 15
            return
        if index == 14: #frais scolarite -150
            Joueur.argent -= 150
            return
        if index == 15: #ivresse -20
            amende = 20
            if (Joueur.argent >= amende):
                Joueur.argent -= amende
            else:
                if Joueur.Vente_maison(amende)== True:
                    Joueur.argent -= amende
                else:
                    banque.elimination(Joueur)
            return

        if index == 16: # immeuble et pret rapportent 150
            Joueur.argent += 150
            return
    

class caisse_communaute(Case):
    def __init__(self, position, cpt_case):
        Case.__init__(self, position, cpt_case)    
        
    def effet(self, Joueur):
        index = cartecommu.pop(0)
        if index != 9:
      
            cartecommu.append(index)
        if index == 1: # case depart
            Joueur.position = 0
            Joueur.argent += 200
            
        if index == 2: # erreur banque +200
            Joueur.argent += 200
            return
        if index == 3: # medecin -50
            amende=50
            if (Joueur.argent >= amende):
                Joueur.argent -= amende
            else:
                if Joueur.Vente_maison(amende)== True:
                    Joueur.argent -= amende
                else:
                    banque.elimination(Joueur)
            return            

        if index == 4: # vente stock +50
            Joueur.argent += 50
            return
        if index == 9: # carte sortie de prison
            Joueur.carteprison += 1
            return
        if index == 6: # allez en prison
            Joueur.position = 10
            prison1.effet(Joueur)
            return
        if index == 7: # Belleville
            Joueur.position = 1
            Joueur.argent += 100
            bd_belleville.effet(Joueur)
            return
        if index == 8: # revenu annuel +100
            Joueur.argent += 100
            return
        if index == 5: # anniversaire +10 par joueur
            Joueur.argent += 10*(len(Player) - 1) # tous les joueurs - lui meme
            for autrejoueur in Player:
                if autrejoueur != Joueur:
                    Joueur.argent -= 10
            return
        if index == 10: # contributions +20
            Joueur.argent += 20
            return
        if index == 11: # interet sur emprunt +25
            Joueur.argent += 25
        if index == 12: # police assurance -50
            amende=50
            if (Joueur.argent >= amende):
                Joueur.argent -= amende
            else:
                if Joueur.Vente_maison(amende)== True:
                    Joueur.argent -= amende
                else:
                    banque.elimination(Joueur)
            return
        if index == 13: # amende -50 ou carte chance
        # On suppose pour l'instant que la carte chance est prise aléatoirement, de manière équiprobable
          #v = (2*np.random.rand(1)+1).astype(int)
          #if v == 1:
              seuil=0
              amende=50
              if np.random.rand(1) < seuil:     
                  return chance1.effet(Joueur)
              else:
                  if (Joueur.argent >= amende):
                      Joueur.argent -= amende
                  else:
                      if Joueur.Vente_maison(amende)== True:
                          Joueur.argent -= amende
                      else:
                          banque.elimination(Joueur)
              return

        if index == 14: # gare la + proche
              while Joueur.position not in [5,15,25,35]:
                  Joueur.position += 1
                  Joueur.position = Joueur.position % 40
              plateau[Joueur.position].effet(Joueur)
              return
        if index == 15: # concours beauté +10
              Joueur.argent += 10
              return
        if index == 16: # heritage +100
              Joueur.argent += 100
              return


class depart(Case):
    def __init__(self, position=0, cpt_case=0):
        Case.__init__(self, position, cpt_case)  
  
    def effet(self, Joueur):
        Joueur.argent += 200
        return





#%% Creation du random pour les cases chance et communaute
import random

cartechance1,cartecommu1 = np.arange(1,17,1),np.arange(1,17,1)
random.shuffle(cartechance1)
random.shuffle(cartecommu1)

cartechance=[c for c in cartechance1] #devient une liste 
cartecommu=[c for c in cartecommu1]

#%% Lancer de dés
def lancer():
    #genere la somme de deux dés, ainsi que l'information sur les doubles
    u = random.randint(1,6)
    v = random.randint(1,6)
    if u == v:
        return (u+v,1) #1 si double
    return (u+v,0) #0 sinon


#%%
def joue(J):
    if J.cpt_double != 3 and J.prisonnier==0:
        Res_des = lancer()
        J.position += Res_des[0]
        J.position = J.position % 40
        if J.position not in [12,28]:
            plateau[J.position].effet(J)
            plateau[J.position].cpt_case += 1
        else:
            plateau[J.position].effet(J, Res_des[0]) #Pour le loyer des compagnies, on a besoin du résultat du lancer de dés
            plateau[J.position].cpt_case += 1
            
        if Res_des[1]==1:
            J.cpt_double+=1 
            joue(J)
        else: 
            return
    if J.prisonnier==1:
        J.prisonnier_fct()
        return    
    if J.cpt_double == 3: #Après 3 doubles consécutifs : direction prison
        J.cpt_double=0
        prison1.effet(J)
        

def tour(partie, nb_tour):
    
    for J in Player:
        if (J.argent<0):
            J.elimine=True
        if J.elimine == True:
            Player.remove(J)
            tour_elimination[partie, Player_fixe.index(J)]=nb_tour -1
        else:
            if J.prisonnier==0:
                joue(J)
                J.achat_ma()
            else:
                J.prisonnier_fct()
                joue(J)
                J.achat_ma()

    return
#%%
          
          
nb_tour_max=150

nb_partie=5000

nb_vict=np.zeros(4)
track_argent=np.zeros([nb_tour_max,4])
tour_elimination=np.zeros([nb_partie,4])
    
track_patrimoine=[[],[],[],[]]

J1=Joueur_stratege()
J2=Joueur_depensier()
J3=Joueur_prudent()
J4=Joueur_random()
Player=[J1, J2, J3, J4]

Player_fixe=[player for player in Player]



for partie in range(nb_partie):
    banque=Joueur()
    #INIT du plateau
    plateau=[]
    depart1=depart(0)
    plateau.append(depart1)
    bd_belleville=propriete(1,0, 60, 'marron', 0.02607, 0.02614,2)
    plateau.append(bd_belleville)
    Cdc1=caisse_communaute(2, 0)
    plateau.append(Cdc1)
    rue_lecourbe=propriete(3, 0, 60,'marron', 0.02198 , 0.02200, 4)
    plateau.append(rue_lecourbe)
    impot1=impot(4,0 , 200)
    plateau.append(impot1)
    montparnasse=gare(5, 0, 200, 0.02260, 0.02260, 25)
    plateau.append(montparnasse)
    rue_vaugirard=propriete(6, 0,100,'bleu_c',0.02318, 0.02318, 6)
    plateau.append(rue_vaugirard)
    chance1=chance(7, 0)
    plateau.append(chance1)
    rue_courcelle=propriete(8, 0,100,'bleu_c',0.02345 , 0.02350, 6)
    plateau.append(rue_courcelle)
    av_republique=propriete(9,0, 120,'bleu_c', 0.02297 , 0.02305, 8)
    plateau.append(av_republique)
    simple_visite=librevisite(10, 0)
    plateau.append(simple_visite)
    bd_villette=propriete(11, 0, 140,'violet', 0.02708, 0.02684, 10)
    plateau.append(bd_villette)
    electricite=compagnie(12, 0, 150,  0.02276, 0.02281)
    plateau.append(electricite)
    av_neuilly=propriete(13,0, 140,'violet',0.02367 , 0.02370, 10)
    plateau.append(av_neuilly)
    rue_paradis=propriete(14, 0, 160, 'violet',0.02483 , 0.02471, 12)
    plateau.append(rue_paradis)
    lyon=gare(15,0, 200, 0.03140 , 0.03105, 25)
    plateau.append(lyon)
    av_mozart=propriete(16,0, 180,'orange',0.02801 , 0.02795, 14)
    plateau.append(av_mozart)
    Cdc2=caisse_communaute(17, 0)
    plateau.append(Cdc2)
    bd_st_michel=propriete(18, 0,180,'orange', 0.02948, 0.02938, 14)
    plateau.append(bd_st_michel)
    place_pigalle=propriete(19, 0 ,200,'orange', 0.03071 , 0.03063, 16)
    plateau.append(place_pigalle)
    parc_gratuit=librevisite(20, 0)
    plateau.append(parc_gratuit)
    av_matignon=propriete(21,0, 220,'rouge',  0.02818 , 0.02813, 18)
    plateau.append(av_matignon)
    chance2=chance(22, 0)
    plateau.append(chance2)
    av_malesherbes=propriete(23, 0, 220,'rouge', 0.02711 , 0.02712, 18)
    plateau.append(av_malesherbes)
    av_henri_martin=propriete(24,0, 240,'rouge',0.03200 , 0.03173, 20)
    plateau.append(av_henri_martin)
    nord=gare(25,0, 200,0.02722 , 0.02724, 25)
    plateau.append(nord)
    fbg_st_honore=propriete(26, 0, 260,'jaune', 0.02726, 0.02727, 22)
    plateau.append(fbg_st_honore)
    place_bourse=propriete(27,0, 260,'jaune', 0.02700, 0.02699, 22)
    plateau.append(place_bourse)
    eau=compagnie(28,0, 150, 0.02661, 0.02659)
    plateau.append(eau)
    rue_fayette=propriete(29,0,280,'jaune', 0.02627, 0.02623, 24)
    plateau.append(rue_fayette)
    prison1=prison(30, 0)
    plateau.append(prison1)
    av_breteuil=propriete(31,0, 300,'vert', 0.02679, 0.02671, 26)
    plateau.append(av_breteuil)
    av_fosh=propriete(32,0, 300,'vert', 0.02602, 0.02597, 26)
    plateau.append(av_fosh)
    Cdc3=caisse_communaute(33, 0)
    plateau.append(Cdc3)
    bd_capucines=propriete(34,0, 320,'vert', 0.02464, 0.02461, 28)
    plateau.append(bd_capucines)
    st_lazare=gare(35, 0, 200, 0.02380, 0.02379 , 25)
    plateau.append(st_lazare)
    chance3=chance(36, 0)
    plateau.append(chance3)
    av_champs_elysees=propriete(37,0, 350,'bleu_f', 0.02140, 0.02143, 35)
    plateau.append(av_champs_elysees)
    taxe1=taxe(38,0, 100)
    plateau.append(taxe1)
    rue_paix=propriete(39,0, 400,'bleu_f', 0.02631, 0.02599, 50)
    plateau.append(rue_paix)
    
    banque.patrimoine=[prop for prop in plateau]
    J1=Joueur_stratege()
    J2=Joueur_depensier()
    J3=Joueur_random()
    J4=Joueur_prudent()
    Player=[J1, J2, J3, J4]
    Player_fixe=[player for player in Player]
    nb_tour=0
    while len(Player)>1:
        nb_tour+=1
        tour(partie, nb_tour)
    
    argent_fin_partie=[argent for argent in track_argent]
    nb_vict[Player_fixe.index(Player[0])] +=1 #celui qui a le plus d'argent à la fin est déclaré gagnant
    
    
#%%    
tour_elim_moyen=np.zeros(4)

for i in range(4):
    tour_elim_moyen[i]=np.mean(tour_elimination[:,i])

print('Ordre des Joueurs : ', Player_fixe)
print()
print('Pourcentage de victoire des joueurs : ', 100*nb_vict/nb_partie)
print()
print('Nombre de tour moyen pour chaque joueur avant d\'être éliminé : ', tour_elim_moyen)
   
