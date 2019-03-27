import random
import bdd.api as bddApi

class Client():
    def __init__(self, maxPrix, maxQte, maxActions, listeActions):
        self.maxPrix = maxPrix
        self.maxQte = maxQte
        self.maxActions = maxActions
        self.actions = self.genListActions(listeActions)

    def genListActions(self, listActions):
        l_actions = [{"action": listActions[random.randrange(len(listActions))], 
                "prix": random.randint(1, self.maxPrix)} for _ in range(self.maxActions)]
        return l_actions


def genRandomClients(maxPrix, maxQte, maxActions, listeActions, nbClients):
    r = lambda x: random.randint(1, x)
    clientList = [Client(r(maxPrix), r(maxQte), r(maxActions), r(listeActions))]
    return clientList

def genPositionnementAleatoire(client, listeActions, jour):
    position = {}
    position["type"] = ["achat", "vente"][random.randint(0,1)]
    position["prix"] = random.randint(1, client.maxPrix)
    position["qte"] = random.randint(1, client.maxQte)
    position["action"] = listeActions[random.randrange(len(listeActions))]
    position["jour"] = jour
    return position

def genLogPositionAleatoire(client, listActions, jour):
    bdd = bddApi.mongoApi()
    position = genPositionnementAleatoire(client, listActions, jour)
    bdd.insertPosition(position)
    return 0


