import client.libCli as libCli

listeActions = ["Danone", "Kalashnokov", "Cocktail Molotov", "Cafe", "Slip borat", "Krakus"]
maxPrix = 30
maxQte = 20
maxActions = 5
nbClients = 5

clients = libCli.genRandomClients(maxPrix, maxQte, maxActions, listeActions, nbClients)

