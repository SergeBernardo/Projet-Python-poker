from random import randint
from random import choice
import sys
import names

# 10 | 100 | 1000 | 10000
symbole = ['♥', '♠', '♣', '♦']
carteVierge = {"number": 0, "symbole": "x", "write": 'x' }

listesGenerate = []
maxPlayer = 5
minSold = 1000
maxSold = 5000
listesPlayers = {'user': {}, "player": []}



def showCartes(listeCartes):
    ligneH, ligneB, ligne1, ligne2, ligne3, ligneBase = "", "", "", "", "", ""
    for carte in listeCartes:
        ligneH +="┌───────────┐"
        ligneB +="└───────────┘"
        ligne1 +="│       "+str(listeCartes[0]["write"])+" │"
        ligne2 +="│     "+str(listeCartes[0]["symbole"])+"     │"
        ligne3 +="│ "+str(listeCartes[0]["write"])+"       │"
        ligneBase +="│           │"

    print(ligneH)
    print(ligne1)
    print(ligneBase)
    print(ligneBase)
    print(ligne2)
    print(ligneBase)
    print(ligneBase)
    print(ligne3)
    print(ligneB)
    

def generateCarte(nbCarte = 2):
    listeCarte = [] # Stocker les carte qui vont etre envoyez
    for i in range(nbCarte): # Boucle pour generer n carte
        global symbole, listesGenerate
        myCarte = {"number": randint(1, 13), "symbole": choice(symbole)}
        if len(listesGenerate) < 52:
            for cartes in listesGenerate:
                if myCarte["symbole"] == cartes["symbole"]:
                    if (myCarte["number"]) == (cartes["number"]):
                        myCarte = generateCarte(1)[0]
        if myCarte["number"] > 10:
            if myCarte["number"] == 11:
                myCarte["write"] = " V"+myCarte["symbole"]
            elif myCarte["number"] == 12:
                myCarte["write"] = " D"+myCarte["symbole"]
            else:
                myCarte["write"] = " R"+myCarte["symbole"]
        elif myCarte["number"] == 10:
            myCarte["write"] = "10"+myCarte["symbole"]
        else:
            myCarte["write"] = " "+str(myCarte["number"])+myCarte["symbole"]
        listesGenerate.append(myCarte)
        listeCarte.append(myCarte)
    return listeCarte

def menu():
    global maxPlayer, minSold, maxSold, listesPlayers
    print("=========================")
    print("|                       |")
    print("|        Poker          |")
    print("|                       |")
    print("=========================")
    print("|                       |")
    print("|     (1) Solo          |")
    print("|     (2) Multi         |")
    print("|     (3) Quit          |")
    print("|                       |")
    print("=========================")
    choix = input('Entrez votre choix: ')
    if choix == '2':
        print("Le choix n'est pas accessible")
        menu()
    elif choix == '1':
        while True:
            choix = input('Nb de player (1 - '+str(maxPlayer)+'): ')
            if choix.isnumeric() == False:
                continue
            elif int(choix) < 1 or int(choix) > maxPlayer:
                continue
            else:
                sold = randint(minSold, maxSold)
                for i in range(int(choix)):
                    listesPlayers["player"].append({"name": names.get_full_name(), "sold": sold, id: i, "partie": [], "tauxRelance": 5, "tauxCoucher":2})
                while True:
                    name = input('Enter your fucking name!! ')
                    if len(name) > 2:
                        end = True
                        for player in listesPlayers["player"]:
                            if player["name"] == name:
                                end = False
                        if end == True:
                            listesPlayers["user"] = {"name": name, "sold": sold, "partie": []}
                            break
                    # print(listesPlayers)
                break
        game()
    elif choix == '3':
        # import sys
        sys.exit(0)
    else:
        menu()

def menuPlayer(partie):
    global listesPlayers
    print("=========================")
    print("|                       |")
    print("    Name: "+listesPlayers["user"]["name"]+"       ")
    print("    Sold: "+str(listesPlayers["user"]["sold"])+"€       ")
    print("    Pot: "+str(partie["pot"])+"€      ")
    print("    Cagnotte: "+str(partie["cagnotte"])+"€      ")
    print("|                       |")
    print("=========================")
    print("|                       |")
    print("|     (0) mes carte     |")
    # print("|     (1) check         |")
    print("|     (2) suivre        |")
    # print("|     (3) relance       |")
    print("|     (4) coucher       |")
    print("|                       |")
    print("=========================")
    while True:
        choix = input("Qu'est-ce que tu veux faire, petit branleur: ")
        if choix == '0':
            showCartes(listesPlayers["user"]["partie"][partie["id"]-1]["carte"])
            continue
        elif choix == '2':
            # listesPlayers["user"]["sold"] =  listesPlayers["user"]["sold"] - partie["pot"]
            listesPlayers["user"]["sold"] -= partie["pot"]
            print("Votre sold est actuellement de :"+str(listesPlayers["user"]["sold"])+"€")
            return True
        elif choix == '4':
            print('Tu t\'es coucher, petite fiotte!')
            return False
        else:
            continue


def partie(numPartie):
    global listesPlayers
    listesPlayers["user"]["partie"].append({"carte": generateCarte(), "miseTotal": 0, "gainTotal": 0, "isWin": False, "down": False})
    for player in listesPlayers["player"]:
        player["partie"].append({"carte": generateCarte(), "miseTotal": 0, "gainTotal": 0, "isWin": False, "down": False})
    partie = {"id": numPartie,  "pot": 0, "cagnotte": 0, "coucher": []}
    for manche in range(4):
        choix = menuPlayer(partie)
        if choix == False:
            return False
        for player in listesPlayers["player"]:
            if player["tauxRelance"]> randint(0, 20):
                prime = randint(100, 300)
                print("'+player['name']+' relance de '+str(prime)+'€")
                player["sold"] -= prime
                partie["cagnotte"] += prime
                choix = menuPlayer(partie)
                if choix == False:
                    return False
                else:
                    listesPlayers["user"]["sold"] -= prime
                    partie["pot"] += prime
                    print("T\'as suvie de '+str(prime)+'€")
            elif player["tauxCoucher"]> randint(0, 100):
                partie["coucher"].append(player)
        partie["cagnotte"] += partie["pot"]
        partie["pot"] = 0
        print(manche)
        if manche == 1:
            partie["carte"] = generateCarte(3)
            showCartes(partie["carte"])
        elif manche == 2:
            partie["carte"].append(generateCarte(1))
            showCartes(partie["carte"])
        elif manche == 3:
            partie["carte"].append(generateCarte(1))
            showCartes(partie["carte"])
        
                
        

def game():
    global listesPlayers
    nbPartie = 1
    while True:
        finish = False
        if (len(listesPlayers["player"])+1) == 1:
            finish = True
        if finish == True:
            break
        partie(nbPartie)
        nbPartie += 1
        break


menu()
