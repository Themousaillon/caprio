import client.libCli as libCli
import simulation.libSimu as libSimu

# paramétrage de la simulation

listeActions = ["Danone", "Air France", "Ubisoft", "Cafe", "Apple", "Google"]
maxPrix = 30
maxQte = 20
maxActions = 5
nbClients = 5

clientList = libCli.genRandomClients(maxPrix, maxQte, maxActions, listeActions, nbClients)

# on démare la simulation

if __name__ == "__main__":
    libSimu.simulate(clientList, 10, listeActions)