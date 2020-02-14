# coding: utf-8
import time

def return_date_of_update():
    """get the date of the bdd update"""
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre"]
    result = "Votre base de données a bien été mise à jour le : " + str(jours[time.localtime()[6]])  + \
    " " + str(time.localtime()[2]) + " " + str(mois[time.localtime()[1]-1]) + " " + str(str(time.localtime()[0]) + \
    " à " + str(time.localtime()[3]) + " heures " + str(time.localtime()[4]) +" minutes " + str(time.localtime()[5]) + \
    " secondes.")
    return result
