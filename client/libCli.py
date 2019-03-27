import random
import bdd.api as bddApi


def genPositionnementAleatoire(client, listeActions, jour):
    position = {}
    position["idCli"] = client.id
    position["type"] = ["achat", "vente"][random.randint(0,1)]
    position["prix"] = random.randint(1, client.maxPrix)
    position["qte"] = random.randint(1, client.maxQte)
    position["action"] = listeActions[random.randrange(len(listeActions))]
    position["jour"] = jour
    return position


class Client():
    def __init__(self, id, maxPrix, maxQte, maxActions, listeActions):
        self.id = id
        self.maxPrix = maxPrix
        self.maxQte = maxQte
        self.maxActions = maxActions
        self.actions = self.genListActions(listeActions)

    def genListActions(self, listActions):
        nogo = []
        def customRand(length, l, nogo):
            while (l in nogo):
                l = random.randint(0, length)
            nogo.append(l)
            return l
            
        l_actions = [{"action": listActions[customRand(len(listActions)-1, random.randrange(len(listActions)), nogo)], 
                "prix": random.randint(1, self.maxPrix)} for _ in range(self.maxActions)]
        return l_actions
    
    def client_to_mongo(self):
        mongoCliDic = {
            "id": self.id,
            "maxPrix": self.maxPrix,
            "maxQte": self.maxQte,
            "maxActions": self.maxActions,
            "actions": self.actions   
        }
        return mongoCliDic

    def genLogPositionAleatoire(self, listActions, jour):
        bdd = bddApi.mongoApi()
        position = genPositionnementAleatoire(self, listActions, jour)
        bdd.insertPosition(position)
        return 0


def genRandomClients(maxPrix, maxQte, maxActions, listeActions, nbClients):
    r = lambda x: random.randint(1, x)
    clientList = [{"id": id, "client":Client(id, r(maxPrix), r(maxQte), r(maxActions), listeActions)} for id in range(nbClients)]
    return clientList

