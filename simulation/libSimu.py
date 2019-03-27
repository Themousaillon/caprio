import multiprocessing as mp
import client.libCli as libCli
import time
import random

def clientBehaviour(client, procQueue, listActions, jour):
    continue_simu = True
    phase = "trading"  # soit trading soit redistrib
    while (continue_simu):
        if not procQueue.empty():
            instruction = procQueue.get()
            continue_simu = instruction["continue_simu"]
            phase = instruction["phase"]
            jour = instruction["jour"]

        if phase == "trading":
            if random.random() > 0.7:
                client.genLogPositionAleatoire(listActions, jour)
            time.sleep(0.2)

#        if phase == "repartition":
#           faire la répartition ici .....


def spawnClientProcess(clientList, listActions):
    queueList = [mp.Queue() for _ in range(len(clientList))]
    processList = [{"process" : mp.Process(target=clientBehaviour, args=(clientList[i], queueList[i],listActions, 1)),
                    "queue": queueList[i]} for i in range(len(clientList))]
    
    return processList


def openTrade(processList, jour):
    instruction = {
        "continue_simu": True,
        "phase": "trading",
        "jour": jour
    }
    for p in processList:
        p["queue"].put(instruction)


def closeTrade(processList):
    instruction = {
        "continue_simu": True,
        "phase": "répartition",
        "jour": -1
    }
    for p in processList:
        p["queue"].put(instruction)

def terminateSimulation(processList):
    instruction = {
        "continue_simu": False,
        "phase": "répartition",
        "jour": -1
    }
    for p in processList:
        p["queue"].put(instruction)


def startSimulation(processList, nbJours):
    for p in processList:
        p.start()

    for j in range(nbJours):
        # open the trading for 5 seconds
        print("Le trading du jour ", j , " est ouvert !!")
        openTrade(processList, j)
        time.sleep(5)
        print("Il est 17H, la salle de marché fermée")
        print("Distribution des taches au clients et calcul de la répartition")
        # mettre ici l'appel du code de la distribution, s'inspirer de la fonciton openTrade
        # à default de l'avoir je me contente de fermer la salle de marché
        closeTrade(processList)
        time.sleep(2)
        # close the trading and process to repartition
    
    #termine la simulation
    terminateSimulation(processList)
    return 0


def simulate(clientList, nbJour, listActions):
    print("Début de la simulation")
    processList = spawnClientProcess(clientList, listActions)
    startSimulation(processList, nbJour)
    print("fin de la simulation")
    return 0

    