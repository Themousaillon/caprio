import numpy as np
from scipy.optimize import approx_fprime
import random
import math

# Projection orthogonal 2 dimentions
def proj_2D(vec1, vec2):
    return (vec1.dot(vec2)/(np.linalg.norm(vec2)**2))*vec2

# projection orthogonale sur une base de orthonormale de dimention quelconque
def proj_ND(vec1, base):
    if len(base) == 0:
        return np.zeros(vec1.size)
    projections = [proj_2D(vec1, vec2) for vec2 in base]
    return sum(projections)


# Orthonormalization d'une base celon le procédé de Gram-Shmidt
def orthonormalize(base):
    orthonormalized_base = []
    for v in base:
        u = v - proj_ND(v, orthonormalized_base)
        u = u/np.linalg.norm(u)
        orthonormalized_base += [u]
    return orthonormalized_base

# Génere une base de l'espace des constraintes en fonction du nombre de dimentions du problème
def make_opti_base(nbDim):
    hyperBase = []
    if nbDim==2:
        return [np.array([1,-1])/2**(1/2)]
    for i in range(nbDim-1):
        hyperplan = []
        hyperplan = [1 for _ in range(nbDim-1)]
        hyperplan[i]=0
        hyperplan += [-sum(hyperplan)]
        hyperBase += [np.array(hyperplan)]
    return orthonormalize(hyperBase)

# fonction objectif de minimisation celon la norme 2
def moindreCarre(x,y ):
    return np.sum(np.power(x-y, 2))

# fonctiono objectif de minimisation celon le critère de satisfaction (ne marche pas car non convexe)
def satisfaction(x,y):
    rowSat = (y/x)-1
    absSat = np.abs(rowSat)
    rectifiedSat = rowSat -absSat
    return np.sum(rowSat + np.exp(-rectifiedSat*10) -1)

# Projection sur l'hyperplan des contraintes
def projHyperBase(x, hyperBase, scale):
    neworigine=(scale/len(hyperBase[0]))*np.array([1 for _ in range(len(hyperBase[0]))])
    return neworigine + proj_ND(x, hyperBase)

# descente du gradient projeté
def gradientProj(objList, scale, fObj, pas,  epsilon, maxIter):
    hyperBase = make_opti_base(len(objList))
    Xk = projHyperBase(np.array([random.randint(10,100) for _ in range(len(objList))]), hyperBase, scale)
    Xn = Xk + 2*epsilon
    i=0
    print('starting to optimize')
    while (np.linalg.norm(Xk - Xn) > epsilon) and (i < maxIter):
        Xk = Xn
        grad = approx_fprime(Xk, fObj, 0.0001, objList)
        Xn = projHyperBase(Xk-pas*grad, hyperBase, scale)
        i+=1
    return finalDistrib(np.floor(balanceVector(Xn)), objList, scale)

# Ramène tout des attributs du vecteur dans le plan positif
def balanceVector(vec):
    while vec.min() < 0:
        maxi = vec.argmax()
        mini = vec.argmin()
        miniValue = vec[mini]
        vec[maxi] +=  miniValue
        vec[mini] = 0
    return vec

# Distribut les dernières parts qui ne peuvent pas être décidées par le critère des moindes carrés
def finalDistrib(x, obj, scale):
    while scale-np.sum(x) != 0:
        satVec = x/obj
        mini = satVec.argmin()
        x[mini] += 1
        print(x)
    return x



####### EXEMPLE D'UTILISARION ######

objList = np.random.randint(1,100,200)
vlist = np.random.randint(1,600,30)
scale = sum(vlist)
solMC = gradientProj(objList, scale, moindreCarre, 1e-2, 1e-6, 1000)
#solSAT = gradientProj(objList, scale, satisfaction, 1e-2, 1e-6, 1000)

print("distrib moindres carrés --> ", solMC, sum(solMC))
print("error --> ", moindreCarre(solMC, objList))
#print("distrib satisfaction --> ",solSAT, sum(solSAT))
