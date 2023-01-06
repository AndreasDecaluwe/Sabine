
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:33:23 2022

@author: Andreas
"""

"""imports"""
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server 
import pandas as pd
import os
import matplotlib.pyplot as plt 
from pywebio.platform import *
from fpdf import FPDF
from fpdf import Template






'''
================================================================================
CSV FILE INLEZEN
================================================================================
'''
# ALLE INGELEZEN DATA HIERONDER komt uit de csv: "overzichtSLPs.csv
def insertCSVinfo(filename):
    csv = str(filename)
    path = os.getcwd()
    pathcsv = os.path.join(path, csv)
    # print(pathcsv)
    data = pd.read_csv(os.path.join(path, csv))
    data.head()
    global timeValues
    global pointCount
    global SLPel
    global SLPg
    global COP
    global elecEff

    timeValues = data.iloc[:,0]
    pointCount = [i for i in range(len(timeValues))]  #aantal punten in timevalues tellen (35000+), nodig voor de plots 
    SLPel = data.iloc[:,6] #profiel van de VREG
    SLPg = data.iloc[:,8] #profiel van de VREG
    COP = data.iloc[:,9].tolist() #nu is er de mogelijkheid om de COP variabel te maken, op dit moment nog steeds een constante waarde in de csv, uiteindelijk zou dit ook een profiel per kwartier moeten worden van percentages. hiermee kan dan de COP van een elke warmtepomp vermenigvuldigt worden om een variable factor mee te rekenen 
    elecEff = data.iloc[:,10]
    return data

'''
================================================================================
HIERONDER EEN LIJST VAN INPUTVOORZIENGEN EN DE INGEGEVEN DATA
================================================================================
'''
toepassingen = ["Ruimteverwarming", "Sanitair Warm Water","electriciteit"]

#INPUTVOORZIENINGEN: de voorzieningen die de user te zien krijgt bij initiatie van de tool

cvKetel_gas_25 = {"naam":"gasketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.9,"maxVermogen":30}
cvKetel_stookolie_25 = {"naam":"stookolieketel","Toepassing":"Ruimteverwarming","verbruiker": "stookolie","efficientie":0.9,"maxVermogen":30}
electriciteit_net = {"naam":"electriciteitsnet","Toepassing":"electriciteit","verbruiker": "electriciteit","efficientie":1}
electriciteitPV = {"naam":"electriciteitsnet en PV","Toepassing":"electriciteit","verbruiker": "zonne-energie","efficientie":1,"opbrenst":0,"prijs":0}  #prijs en opbrengst hangen af van de input van de user


RVinput = [cvKetel_gas_25, cvKetel_stookolie_25]

SWWinput= [cvKetel_gas_25, cvKetel_stookolie_25]

Elecinput = [electriciteit_net]

"""
================================================================================
VOORZIENINGEN
================================================================================
"""

#warmtepompen
heatPump_LW_3 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.8,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":5289}
heatPump_LW_5 = {"naam":"Lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.8,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":6370}
heatPump_LW_8 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.5,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":9385}
heatPump_LW_10 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.54,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":7798}

heatPump_GW_3 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":3.73,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":3800}
heatPump_GW_5 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.23,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":7900}
heatPump_GW_8 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.4,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":8300}
heatPump_GW_10 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.5,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":9000}

heatPump_WW_3 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.7,"maxVermogen":3,"eenheid vermogen":'kW',"prijs":9000}
heatPump_WW_5 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.7,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":9300}
heatPump_WW_8 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.8,"maxVermogen":8,"eenheid vermogen":'kW',"prijs":9500}
heatPump_WW_10 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.9,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":10000}
heatPump_WW_15 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":5.3,"maxVermogen":15,"eenheid vermogen":'kW',"prijs":11000}

#doorstroomboilers
doorstroomboiler_5 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":1,"maxVermogen":5,"prijs":500}
elektrischeDoorstroomboiler_5 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","continue verbruik (kWh)":0.225,"inhoud":5,"efficientie":1,"maxVermogen":5,"eenheid vermogen":'kW',"prijs":200}
elektrischeDoorstroomboiler_10 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","continue verbruik (kWh)":0.273,"inhoud":10,"efficientie":1,"maxVermogen":10,"eenheid vermogen":'kW',"prijs":280}
#condensatieketels #vermogen is hier in KW
condensketel_13 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":13,"eenheid vermogen":'kW',"prijs":1835}
condensketel_20 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":20,"eenheid vermogen":'kW',"prijs":2038}
condensketel_30 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":30,"eenheid vermogen":'kW',"prijs":2600}
condensketel_50 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":50,"eenheid vermogen":'kW',"prijs":3800}
condensketel_80 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":80,"eenheid vermogen":'kW',"prijs":4800}
condensketel_100 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":100,"eenheid vermogen":'kW',"prijs":5500}
#zonneboiler
#nummer achter de naam is de boilerinhoud in Liter
zonneboiler_150 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"maxVermogen":150,"eenheid vermogen":'L', "gezinsgrootte":3,"prijs":2543}
zonneboiler_250 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"maxVermogen":250,"eenheid vermogen":'L',"gezinsgrootte":5,"prijs":3000}
zonneboiler_350 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"maxVermogen":350,"eenheid vermogen":'L',"gezinsgrootte":7,"prijs":3500}
#warmtepompboiler  #vermogen is hier in L weergegeven
warmtepompboiler_LW_150 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":2.5,"maxVermogen":150,"eenheid vermogen":'L',"prijs":2294}
warmtepompboiler_LW_200 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":3.19,"maxVermogen":200,"eenheid vermogen":'L',"prijs":2790}
warmtepompboiler_LW_270 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":3.19,"maxVermogen":270,"eenheid vermogen":'L',"prijs":2906}

#voorzieningen in een lijst per soort plaatsen, deze worden doorlopen tijdens de berekening en een wordt gekozen op basis van de dimensionering
#lijsten van voorziening
warmtepomp_RVenSWW = []
warmtepomp_LW = [heatPump_LW_3,heatPump_LW_5,heatPump_LW_8,heatPump_LW_10]
warmtepomp_GW = [heatPump_GW_3,heatPump_GW_5,heatPump_GW_8,heatPump_GW_10]
warmtepomp_WW = [heatPump_WW_3,heatPump_WW_5,heatPump_WW_8,heatPump_WW_10,heatPump_WW_15]

condensatieketels = [condensketel_13, condensketel_20,condensketel_30,condensketel_50,condensketel_80,condensketel_100]
doorstroomboilersE = [elektrischeDoorstroomboiler_5,elektrischeDoorstroomboiler_10]
zonneboilers = [zonneboiler_150,zonneboiler_250,zonneboiler_350]
warmtepompboiler = [warmtepompboiler_LW_150,warmtepompboiler_LW_200,warmtepompboiler_LW_270]

list_voorzieningenRV = [cvKetel_gas_25, warmtepomp_LW,condensatieketels]
list_voorzieningenSWW = [cvKetel_gas_25, warmtepomp_LW,warmtepomp_GW,warmtepomp_WW,doorstroomboilersE]

'''
================================================================================
SCENARIOS
hier komt een lijst van dictionaries die een scenario voorstellen, voor elke voorziening een toepassing. op deze manier heeft de code controle over met welke voorzieningen de huidige situatie vergelijken
================================================================================
'''

#scenarios
"""
mogelijkheden
ruimteverwarming: warmtepomp LW, warmtepomp GW, wartepomp WW, warmtepomp LW, gasketel, condensatiektel
sanitair warm water:warmtepomp LW, warmtepomp GW, wartepomp WW, warmtepomp LW, gasketel, condensatiektel
electriciteit: electriciteitsnet, electriciteitsnet en PV 
"""
scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet", "PV" :False}
scenario2 = {"scenario":"scenario 2", "ruimteverwarming":"warmtepomp GW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet", "PV" :False}
scenario3 = {"scenario":"scenario 3", "ruimteverwarming":"warmtepomp WW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet", "PV" : False}
scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet", "PV" : False}
scenario5 = {"scenario":"scenario 5","ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler gas","electriciteit":"electriciteitsnet", "PV" : False}
scenario6 = {"scenario":"scenario 6","ruimteverwarming":"warmtepomp LW","sanitair warm water":"warmtepomp LW","electriciteit":"electriciteitsnet", "PV" : False}
scenario7 = {"scenario":"scenario 7","ruimteverwarming":"condensatieketel","sanitair warm water":"condensatieketel","electriciteit":"electriciteitsnet", "PV" : False}
scenarios = [scenario1,scenario2,scenario3,scenario4,scenario6,scenario7]

'''
================================================================================
#DIMENSIONERING VAN NIEUWE VOORZIENINGEN
================================================================================
'''
def dimensionering(voorziening,vraag):  #input is welke soort voorziening in dit scenario gebruik worden

    newvoorziening = {}
    if voorziening  == "warmtepomp LW":
        if vraag <= 3:  
            newvoorziening = warmtepomp_LW[0]
        elif vraag > 3 and vraag <= 5:
            newvoorziening = warmtepomp_LW[1]
        elif vraag > 5 and vraag <= 8:
            newvoorziening = warmtepomp_LW[2]
        elif vraag > 8:
             newvoorziening = warmtepomp_LW[3]
        else:
            print("LW vermogen not in range")

    elif voorziening  == "warmtepomp GW":
        if vraag <= 3:  
            newvoorziening = warmtepomp_GW[0]
        elif vraag > 3 and vraag <= 5:
            newvoorziening = warmtepomp_GW[1]
        elif vraag > 5 and vraag <= 8:
            newvoorziening = warmtepomp_GW[2]
        elif vraag > 8:
            newvoorziening = warmtepomp_GW[3]
        else:
            print("GW vermogen not in range")


    elif voorziening  == "warmtepomp WW":
        if vraag <= 3:  
            newvoorziening = warmtepomp_WW[0]
        elif vraag > 3 and vraag <= 5:
            newvoorziening = warmtepomp_WW[1]
        elif vraag > 5 and vraag <= 8:
            newvoorziening = warmtepomp_WW[2]
        elif vraag > 8 and vraag <= 10:
            newvoorziening = warmtepomp_WW[3]
        elif vraag > 10:
            newvoorziening = warmtepomp_WW[4]
        else:
            print("WW vermogen not in range")

    elif voorziening  == "condensatieketel":
        if vraag <= 13:
            newvoorziening = condensatieketels[0]
        elif vraag > 13 and vraag <= 20:
            newvoorziening = condensatieketels[1]
        elif vraag > 20 and vraag <= 30:
            newvoorziening = condensatieketels[2]
        elif vraag > 30 and vraag <= 50:
            newvoorziening = condensatieketels[3]
        elif vraag > 50 and vraag <= 80:
            newvoorziening = condensatieketels[4]
        elif vraag > 80:
            newvoorziening = condensatieketels[5]
        else:
            print("condensatieketel dimensionering mislukt")
    
    elif voorziening  == "doorstroomboiler elektrisch":
        if vraag <= 5:
            newvoorziening = doorstroomboilersE[0]
        elif vraag > 5:
            newvoorziening = doorstroomboilersE[1]
        else:
            print("doorstroomboiler dimensionering mislukt")

    elif voorziening == "electriciteitsnet":
        newvoorziening = electriciteit_net
    elif voorziening == "electriciteitsnet en PV":
        newvoorziening = electriciteitPV

    elif voorziening == "zonneboiler":
        print("zonneboiler dimensionering mislukt")
        


    return newvoorziening

def dimensioneringPV(electriciteitsProductie, kost):
    #https://apps.energiesparen.be/zonnekaart
    electriciteitsProductie = electriciteitsProductie*0.85
    kost = kost*1
    return [electriciteitsProductie, kost]


"""
percentuele vraagprofielen genereren
"""
def generateSLP(SLPgas,SLPelec):
    global SLP
    global SLPrv
    global SLPsww
#de SLPs voor ruimteverwarming, sanitair genereren op basis van het SLPg van de VREG
#het onderscheid maken tussen de profielen voor ruimteverwarming, sanitair ww en electriciteit
    min_gas = min(SLPgas) #minimum van het gasprofiel = waarde voor sanitair ww 
    SLPsww =[min_gas]*len(timeValues) #SLP voor sanitair ww genereren, de constante waarde (min van gasprofiel) voor elk kwartier. To do: variatie in het profiel brengen, is meer realistisch dan altijd eenzelfde waarde
#print(SLPsww)
    SLPrv = [SLPgas[i]-SLPsww[i] for i in range(len(timeValues))] #SLP voor ruimteverwarming genereren door de waarde voor SWW af te trekken van het totaal profiel voor gas
    SLPe = SLPelec
    SLP = [SLPrv, SLPsww, SLPe]
    return SLP

"""
================================================================================
INPUTS VAN DE GEBRUIKER
================================================================================
"""

def userPVinput():
    global PV_opbrengst
    global PV_prijs
    put_text("Via onderstaande link komt op op de Zonnekaart van Vlaanderen terecht, hier kan u uw adres invullen en wordt er een schatting van zonne-opbrengst en prijs van de pv installatie gegenereert")
    put_link("zonnekaart Vlaanderen",url = "https://apps.energiesparen.be/zonnekaart",new_window = True)
    PV_opbrengst = input("Geef de geschatte jaarlijkse opbrengst van een PV installatie in [kWh]", type = FLOAT)
    PV_prijs = input("Geef de geschatte prijs van de PV installatie in [€]", type = FLOAT)
def foolProof(input):
    return -1*input

#userinputs van de site naar de code halen
def userInputsNieuw(list1, list2):
    data = input_group("user input",
    [
    select(label = "welke voorziening voor ruimteverwarming heeft u?:",options = list1, name ="voorzieningRV", required = True),
    select(label = "welke voorziening voor sanitair warm water heeft u?:",options = list2, name ="voorzieningSWW",required = True),
    input("geef uw jaarvebruik aan stookolie in kWh in:", type = FLOAT, name = "jaarverbruikStookolie",required = True),
    input("geef uw jaarvebruik aan aardgas in kWh in:", type = FLOAT,name = "jaarverbruikAardgas",required = True),
    input("geef uw jaarvebruik aan electriciteit in kWh in:", type = FLOAT,name = "jaarverbruikElectriciteit",required = True),
    input("geef uw kost voor stookolie per kWh in [€/kWh]:", type = FLOAT, name = "kostStookolie",required = True),
    input("geef uw kost voor aardgas per kWh in [€/kWh]:", type = FLOAT,name = "kostAardgas",required = True),
    input("geef uw kost voor electriciteit per kWh in [€/kWh]:", type = FLOAT,name = "kostElectriciteit",required = True),
    input("Voor volgende inputs vragen wij u om naar volgende link te gaan: https://apps.energiesparen.be/zonnekaart . Hier kan u op basis van uw adres een inschatting krijgen van de opbrengst en kost voor een zonnepaneel of zonneboilerinstallatie.",placeholder= 'Geef de geschatte jaarlijkse opbrengst van een PV installatie in [kWh]', type = FLOAT ,name = "OpbrengstPV",required = True),
    input(placeholder = "Geef de geschatte prijs van de PV installatie in [€]", type = FLOAT,name = "kostPV",required = True)
    ])

   

    return data
#userinputs verwerken door ze uit de dictionary van de functie hierboven te halen
def userInputs(RVinput,SWWinput,Elecinput):
    RV = [i.get('naam') for i in RVinput]
    SWW = [i.get('naam') for i in SWWinput]

    userinputs = userInputsNieuw(RV, SWW)
    voorzieningRV = userinputs.get('voorzieningRV')
    voorzieningSWW= userinputs.get('voorzieningSWW')
    elec = Elecinput[0]
    for i in range(len(RVinput)):
        if RVinput[i].get('naam') == voorzieningRV:
            ruimteverwarming = RVinput[i]
    for i in range(len(SWWinput)):
        if SWWinput[i].get('naam') == voorzieningSWW:
            sanWarmWater = RVinput[i]
    voorzieningen = [ruimteverwarming,sanWarmWater,elec]
    global jaarverbruik_stookolie
    jaarverbruik_stookolie =  userinputs.get('jaarverbruikStookolie')
    global jaarverbruik_aardgas
    jaarverbruik_aardgas=  userinputs.get('jaarverbruikAardgas')
    global jaarverbruik_elec
    jaarverbruik_elec=  userinputs.get('jaarverbruikElectriciteit')
    global costStookolie
    costStookolie =  userinputs.get('kostStookolie')
    global costAardgas
    costAardgas =  userinputs.get('kostAardgas')
    global costElec
    costElec =  userinputs.get('kostElectriciteit')
    prices = [costStookolie,costAardgas, costElec]
    global PV_opbrengst
    global PV_prijs
    PV_opbrengst = userinputs.get('OpbrengstPV')
    PV_prijs = userinputs.get('kostPV')
    verbruik = [jaarverbruik_stookolie,jaarverbruik_aardgas,jaarverbruik_elec]

    
    return [voorzieningen,verbruik, prices]



"""
================================================================================
INPUTS VAN DE GEBRUIKER VERWERKEN
================================================================================
"""
"""huidig verbruik verdelen over procentueel verbruikprofiel -> verbruikprofiel genereren"""
def verbruikProfiel(voorziening, profiel):  #functie vermenigvuldigt elk percentage per kwartier van de slp met het overeenkomstige  totaal jaarverbruik 
    if voorziening.get("verbruiker") =="electriciteit":
            jaarverbruik = jaarverbruik_elec
            verbruikersVraag = [i*jaarverbruik for i in profiel] #delen door 0.25 op kWkwartier op te zetten naar kW, kWkwartier opmdat er per kwartier vermenigvuldigt wordt met het totaal. 
    elif voorziening.get("verbruiker") =="aardgas":
            jaarverbruik = jaarverbruik_aardgas
            verbruikersVraag = [i*jaarverbruik for i in profiel]           
    elif voorziening.get("verbruiker") =="stookolie":
            jaarverbruik = jaarverbruik_stookolie
            verbruikersVraag = [i*jaarverbruik for i in profiel]
#    print(verbruikersVraag)
    return verbruikersVraag


def verbruikersSom(voorziening, som): #functie verdeelt het totaalverbruik van een bepaalde voorziening over alle gedefinieerde verbruikers (gas, stookolie, elec), maakt vergelijken later gemakkelijker
    verbruikers = {"aardgas":0.0,"stookolie":0.0,"electriciteit":0.0}
    if voorziening.get("verbruiker") =="electriciteit":
        verbruikers["electriciteit"] = verbruikers.get("electriciteit") + som
    elif voorziening.get("verbruiker") =="aardgas":
        verbruikers["aardgas"] = verbruikers.get("aardgas") + som
    elif voorziening.get("verbruiker") =="stookolie":
        verbruikers["stookolie"] = verbruikers.get("stookolie") + som
#    print(verbruikers)
    return verbruikers

"""
================================================================================
ENERGIEVRAAG BEPALEN
================================================================================
""" 
#energievraag of nuttige energie van huidige voorzieningen bepalen op basis van huidige efficientie

def energieVraag(huidigeVoorziening,huidigVraagProfiel):
    if type (huidigeVoorziening.get("efficientie")) == list: #if functie is nodig om te bepalen of de efficientie tijdsafhankelijke is of niet, tijdsafhankelijk staat in een list, niet-afhankelijk is gwn een integer
        vraag = [a*b for a,b in zip(huidigVraagProfiel, huidigeVoorziening.get("efficientie") )]
    else:
        vraag = [i*huidigeVoorziening.get("efficientie") for i in huidigVraagProfiel]
    return vraag
 
#nieuw verbruik voor nieuwe voorziening op basis van het vraagprofiel
def newConsumption(vraagprofiel,nieuweVoorziening):   #op basis van de energievraag en een nieuwe efficientie het nieuwe verbruik berekenen
    if type (nieuweVoorziening.get("efficientie")) == list:  #voorbeeld een variable COP staat in een tijdafhankelijke lijst geschreven, elk verbruik
        newCons = [a/b for a,b in zip(vraagprofiel,nieuweVoorziening.get("efficientie"))]
    else:  #als we een constante COP gebruiken
        newCons = [i/nieuweVoorziening.get("efficientie") for i in vraagprofiel]
    return newCons

#nieuw electriciteitsverbruik met PV
def newConsumptionPV(elecVerbruik, PV_opbrengst):  #PV opbrengst aftrekken van huidig verbruik voor electriciteit, per kwartier
    # newCons = [None]*len(verbruikprofiel)
    # for i in range(len(verbruikprofiel)):
    #     newCons[i] = (round(verbruikprofiel[i] - PV_opbrengst[i],3)) 
    newCons = elecVerbruik - PV_opbrengst
    return newCons

#verglijking maken tussen de verbruikers van een bepaalde voorziening
def verbruikvergelijking(dict1, dict2):  #2 dictionaries van verbruikers vergelijken met elkaar, gebruikt om nieuw verbruik te vergelijken met huidig verbruik. Geeft duidelijk weer waar er een besparing is en waar een extra/nieuw verbruik is
    besparingsdict= {"aardgas":0.0,"stookolie":0.0,"electriciteit":0.0,"totaal besparing":0}
    besparingsdict['aardgas'] = round(dict1.get("aardgas") - dict2.get("aardgas"),3)
    besparingsdict['electriciteit'] = round(dict1.get("electriciteit") - dict2.get("electriciteit"),3)
    besparingsdict['stookolie'] = round(dict1.get("stookolie") - dict2.get("stookolie"),3)
    besparingsdict['totaal besparing'] = besparingsdict.get('aardgas') + besparingsdict.get('electriciteit') + besparingsdict.get('stookolie')
    return besparingsdict  

#input is een item van een dictionary met een verbruiker en een verbruikswaarde eg {"gas":100}  
def primaryEnergy(dictionary): 
    #https://www.vlaanderen.be/epb-pedia/rekenmethode/rekenmethode-e-peil/karakteristiek-jaarlijks-primair-energieverbruik
    mulFactorGas = 1
    mulFactorElec = 2.5
    mulFactorStookolie = 1
    primE = 0
    for key, value in dictionary.items():
        if key == "electriciteit":
                primE += round(value * mulFactorElec,3)
        elif key == "aardgas":
                primE += round(value * mulFactorGas,3)
        elif key == "stookolie":
                primE += round(value * mulFactorStookolie,3)   
    return primE

"""
================================================================================
CO2 uitstoot
================================================================================
"""
#https://www.energids.be/nl/vraag-antwoord/wat-houdt-een-ton-co2-precies-in/2141/
co2_gas = 0.206 #kg/kWh
co2_elec = 0.220 #kg/kWh
co2_stookolie = 0.271 #kg/kWh

def emissions(verbruiker, verbruik):  #returns kg co2/kwh voor een bepaalde verbruiker
    if verbruiker == "electriciteit":
            co2 = round(verbruik * co2_elec,3)
    elif verbruiker == "aardgas":
            co2 = round(verbruik * co2_gas,3)
    elif verbruiker == "stookolie":
            co2 = round(verbruik * co2_stookolie,3)
#    print(co2)
    return co2

"""
================================================================================
FINANCIEEL
================================================================================
"""

#https://code.activestate.com/recipes/576686-npv-irr-payback-analysis/
#momenteel een vaste waarde per kWh, dit variabel maken is mogelijk maar dan moeten we ook per kwartier een lijst inlezen, en aanpassen in de functies dat het elk overeenkomstig kwartier moet vermenigvuldigen 
# costElec = 0.5 #€/kWh   
# costAardgas = 0.2 #€/kWh
# costStookolie = 0.3 #€/kWh


#returns verbruikskost per jaar afhahnkelijk van welke verbruiker 
#input is een item van een dictionary {'verbruiker':IntVerbruik,'verbruiker2":verbruik2}
# bedoelt om de totale verbruikssom op te tellen, van zowel, gas elec als stookolie
def usageCostTotal(verbruik): 
    cost = 0
    for key, val in verbruik.items():
            if key == "electriciteit":
                cost += val * costElec
            elif key == "aardgas":
                cost += val * costAardgas
            elif key == "stookolie":
                cost += val * costStookolie
    return cost

#returns verbruikskost per jaar afhahnkelijk van welke verbruiker 
#input is een item van een dictionary over verbruik
def usageCostItem(key,value):
    cost = 0
    if key == "electriciteit":
        cost += round(value * costElec,2)
    elif key == "aardgas":
        cost += round(value * costAardgas,2)
    elif key == "stookolie":
        cost += round(value * costStookolie,2)
    return cost

#functie om de cashflow en discounted cashflow(in en output per jaar) voor een bepaalde periode te berekenen.
def cashflows(oudverbruik, nieuwverbruik,investering):  #de cashflow per jaar berekenen, periode is het aantal jaar. Eerste waarde is het jaar 0 = de investering
    print("###berekening cashflows###")
    periode = 20 #jaar
    cashflow = [None]*periode
    discountedCashFlow = [None]*periode
    developmentVerbruik = 0.03  #elk jaar 3% meer verbruik dan het jaar voordien
    developmentCost = 0.19 #elk jaar stijgt de prijs met 5%
    kostHuidig = usageCostTotal(oudverbruik) #♣initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
    kostNieuw = usageCostTotal(nieuwverbruik)
    onderhoud = 100 #jaarlijkse kost onderhoud
    cashflow[0] = -1*investering
    discountedCashFlow[0] = -1*investering
    for i in range(1,len(cashflow)):
        cashflow[i] = round(cashflow[i-1] + kostHuidig - kostNieuw - onderhoud,3)
        oudverbruik = {key:value*developmentVerbruik for (key,value) in oudverbruik.items()}
        nieuwverbruik = {key:value*developmentVerbruik for (key,value) in nieuwverbruik.items()}
        kostHuidig = kostHuidig*(1+developmentCost)
        kostNieuw = kostNieuw*(1+developmentCost)
        discountedCashFlow[i] = round(cashflow[i-1] + kostHuidig - kostNieuw - onderhoud,3)
    print(cashflow)
    print(discountedCashFlow)
    return discountedCashFlow

#functie berekent de payback periode op basis van de investering en cashflows.       
def payback_of_investment(investment, cashflows): #payback periode berekenen op basis van investering en cashflow per jaar
    print("###terugverdientijd berekenen###")
    """The payback period refers to the length of time required 
       for an investment to have its initial cost recovered.
       
       >>> payback_of_investment(200.0, [60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    total, years, cumulative = 0.0, 0, []
    if not cashflows or (sum(cashflows) < investment):
        raise Exception("insufficient cashflows, did you fill in a negative value for yearly use or cost per kWh?")
    for cashflow in cashflows:
        total += cashflow
        if total < investment:
            years += 1
        cumulative.append(total)
    A = years
    B = investment - cumulative[years-1]
    C = cumulative[years] - cumulative[years-1]
#    print(A + round((B/C),3),"years")
    months = round((B/C)*12)
#    print(A,"years and",months,"months")
    return [A,months]

#roept de payback functie op, deze wordt opgeroepen in de vergelijking
def payback(cashflows): #functie om de payback periode op te roepen
    """The payback period refers to the length of time required
       for an investment to have its initial cost recovered.
       
       (This version accepts a list of cashflows)
       
       >>> payback([-200.0, 60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    investment, cashflow = cashflows[0], cashflows[1:]
    if investment < 0 : investment = -investment
    return payback_of_investment(investment, cashflow)


def investering(listnieuwProf, listhuidigProf):
    if listhuidigProf.get('voorziening') != listnieuwProf.get('voorziening'):
        invest = listnieuwProf.get('voorziening').get('prijs')
    else:
        invest = 0
    return invest

def nieuweVoorzieningen(scenario,maxVraagRV,maxVraagSWW):  #deze functie wordt doorlopen door alle scenarios die meegegeven worden en bepaalt daaruit welke de nieuwe voorzieningen worden die vergelekenn gaan worden met de huidige situatie
    warmtevraagRV =maxVraagRV
    warmtevraagSWW = maxVraagSWW
    print("warmtevraag RV", warmtevraagRV)
    print("warmtevraagSWW",warmtevraagSWW)

    if scenario.get("ruimteverwarming") == scenario.get("sanitair warm water"):
        voorzieningRV = dimensionering(scenario.get("ruimteverwarming"),warmtevraagRV + warmtevraagSWW)
        voorzieningSWW = voorzieningRV
        voorzieningElec = dimensionering(scenario.get("electriciteit"),1)
    else:    
        voorzieningRV = dimensionering(scenario.get("ruimteverwarming"),warmtevraagRV)
        voorzieningSWW = dimensionering(scenario.get("sanitair warm water"),warmtevraagSWW)
        voorzieningElec = dimensionering(scenario.get("electriciteit"),1)

    nieuwevoorzieningen = [voorzieningRV, voorzieningSWW, voorzieningElec]

    return [nieuwevoorzieningen, voorzieningRV,voorzieningSWW,voorzieningElec]

"""
================================================================================
DICTIONARY VAN HUIDIG PROFIEL GENEREREN
================================================================================
"""

def huidigProfiel(huidVoor,SLP):
    huidigProfiel = {}
    huidigProfielRV = {}
    huidigProfielSWW = {}
    huidigProfielElec = {}

    huidigeProfielen = [huidigProfielRV,huidigProfielSWW,huidigProfielElec]
    huidigeVoorziening = [huidVoor[0],huidVoor[1],huidVoor[2]] 

    for i in range(len(huidigeProfielen)): #for loop door de profielen en de huidige voorzieningen, een lijst bij de declaratie van huidige voorzieningen. moet zelfde volgorde hebben
        huidigeProfielen[i]["voorziening"] = huidigeVoorziening[i]   #dict van huidige voorziening ingeven
        huidigeProfielen[i]["verbruikProfiel"] = verbruikProfiel(huidigeProfielen[i].get('voorziening'),SLP[i])  #totaal jaarverbruik verdelen over overeenkomstige SLP 
        huidigeProfielen[i]["totaal verbruik"] = sum(huidigeProfielen[i].get("verbruikProfiel")) #som van het profiel verdeeld over SLP, bedoelt als check
        huidigeProfielen[i]["verbruikersverdeling"] = verbruikersSom(huidigeProfielen[i].get("voorziening"),huidigeProfielen[i].get("totaal verbruik"))  #het verbruik verdelen over de soorten verbruikers (gas, stookoli, elec) maakt het vgl achteraf makkelijker
        huidigeProfielen[i]["CO2"] = {} 
        for key, value in huidigeProfielen[i].get("verbruikersverdeling").items():  #CO2 per verbruiker berekenen
            huidigeProfielen[i]["CO2"][key] = emissions(key,value)
        huidigeProfielen[i]["totaal CO2"] = sum(huidigeProfielen[i].get("CO2").values())  #☻totaal CO2, som van uitstoot van alle verbruikers
        huidigeProfielen[i]["energievraag"] = energieVraag(huidigeProfielen[i].get("voorziening"),huidigeProfielen[i].get("verbruikProfiel"))  #energievraag op basis van het verbruik en de huidige efficientie bepalen
        
    huidigProfiel["ruimteverwarming"] = huidigProfielRV.get('voorziening').get('naam')
    huidigProfiel["sanitair warm water"] = huidigProfielSWW.get('voorziening').get('naam')
    huidigProfiel["electriciteit"] = huidigProfielElec.get('voorziening').get('naam')
    huidigProfiel["verbruik"] = {}
    huidigProfiel["verbruikskost"] = {}
    for i,j in huidigProfielRV.get("verbruikersverdeling").items():
        for k,l in huidigProfielSWW.get("verbruikersverdeling").items():
            for m,n in huidigProfielElec.get('verbruikersverdeling').items():
                if i == k == m:
                    huidigProfiel['verbruik'][i] = j+l+n #totaal verbruik per verbruiker (gas, stookolie, elec)
                    huidigProfiel['verbruikskost'][i]= usageCostItem(i,j+l+n) #totaal kost per verbruiker (gas, stookolie, elec)
    huidigProfiel["totaal verbruikskost"] = sum(huidigProfiel.get("verbruikskost").values())
    huidigProfiel["totaal verbruikskost check"] = usageCostTotal(huidigProfiel.get('verbruik'))
    huidigProfiel["primaire energie"] = primaryEnergy(huidigProfiel.get("verbruik"))             
    huidigProfiel['CO2'] = huidigProfielRV.get('totaal CO2') + huidigProfielSWW.get('totaal CO2') + huidigProfielElec.get('totaal CO2')

    return [huidigProfiel, huidigProfielRV,huidigProfielSWW,huidigProfielElec]

"""
================================================================================
DICTIONARY VAN NIEUW PROFIEL GENEREREN
================================================================================
"""
def nieuwProfiel(scenario, huidProf):
    # if analysePV == "ja":
    #     scenario.update({"PV":True})
    nieuwProfiel = {}
    selectie = nieuweVoorzieningen(scenario,max(huidProf[1].get('verbruikProfiel'))*4,max(huidProf[2].get('verbruikProfiel'))*4)  #maal 4 om max(kWh) om te zetten naar kW 
    print("max RV en max SWW", max(huidProf[1].get('verbruikProfiel')), max(huidProf[2].get('verbruikProfiel')))
    nieuwVoorzieningRV = selectie[1]
    nieuwVoorzieningSWW = selectie[2]
    nieuwVoorzieningElec = selectie[3]
    nieuwProfielRV = {} 
    nieuwProfielSWW = {} 
    nieuwProfielElec = {}
    nieuweProfielen = [nieuwProfielRV,nieuwProfielSWW,nieuwProfielElec]

    for b in range(len(nieuweProfielen)):
        nieuweProfielen[b]["voorziening"] = selectie[0][b]
        nieuweProfielen[b]["verbruikProfiel"] = newConsumption(huidProf[b+1].get("energievraag"),nieuweProfielen[b].get("voorziening"))
        nieuweProfielen[b]["totaal verbruik"] = sum(nieuweProfielen[b].get("verbruikProfiel"))
        nieuweProfielen[b]["verbruikersverdeling"] = verbruikersSom(nieuweProfielen[b].get("voorziening"),nieuweProfielen[b].get("totaal verbruik"))
        nieuweProfielen[b]["besparing verbruik"] = verbruikvergelijking(huidProf[b+1].get("verbruikersverdeling"),nieuweProfielen[b].get("verbruikersverdeling"))
        nieuweProfielen[b]["CO2"] = {}
        for key, value in nieuweProfielen[b].get("verbruikersverdeling").items():
            nieuweProfielen[b]["CO2"][key] = emissions(key,value)
        nieuweProfielen[b]["totaal CO2"] = sum(nieuweProfielen[b].get("CO2").values())
        nieuweProfielen[b]["Besparing CO2"] = round(huidProf[b+1].get("totaal CO2") - nieuweProfielen[b].get("totaal CO2"),3)

    nieuwProfiel["ruimteverwarming"] = nieuwProfielRV.get('voorziening').get('naam') + str(nieuwProfielRV.get('voorziening').get('maxVermogen')) + nieuwProfielRV.get('voorziening').get('eenheid vermogen')
    nieuwProfiel["sanitair warm water"] = nieuwProfielSWW.get('voorziening').get('naam') + str(nieuwProfielSWW.get('voorziening').get('maxVermogen')) + nieuwProfielSWW.get('voorziening').get('eenheid vermogen')
    nieuwProfiel["electriciteit"] = nieuwProfielElec.get('voorziening').get('naam')
    nieuwProfiel["verbruik"] = {}
    nieuwProfiel["verbruikskost"] = {}
    for i,j in nieuwProfielRV.get("verbruikersverdeling").items():
        for k,l in nieuwProfielSWW.get("verbruikersverdeling").items():
            for m,n in nieuwProfielElec.get('verbruikersverdeling').items():
                if i == k == m:
                    nieuwProfiel['verbruik'][i] = j+l+n
    

    for i,j in nieuwProfiel.get("verbruik").items():
            nieuwProfiel["verbruikskost"][i] = usageCostItem(i,j)

    nieuwProfiel["totale verbruikskost"] = sum(nieuwProfiel.get("verbruikskost").values())
    nieuwProfiel["primaire energie"] = primaryEnergy(nieuwProfiel.get("verbruik"))                
    nieuwProfiel['CO2'] = nieuwProfielRV.get('totaal CO2') + nieuwProfielSWW.get('totaal CO2') + nieuwProfielElec.get('totaal CO2')
    
    nieuwProfiel["verbruikskost PV"] = {}
    PV = dimensioneringPV(PV_opbrengst,PV_prijs)
    ElecPV = nieuwProfiel.get('verbruik').get('electriciteit') - PV[0]
    nieuwProfiel['verbruik met PV'] = {"aardgas":(nieuwProfiel.get('verbruik')).get('aardgas'),'stookolie':(nieuwProfiel.get('verbruik')).get('stookolie'),'electriciteit':ElecPV}
    print("nieuwprof",nieuwProfiel.get('verbruik met PV'))
    nieuwProfiel['investering PV'] = PV[1]
    nieuwProfiel["primaire energie PV"] = primaryEnergy(nieuwProfiel.get("verbruik"))
    for i,j in nieuwProfiel.get("verbruik met PV").items():
            nieuwProfiel["verbruikskost PV"][i] = usageCostItem(i,j)

    return [nieuwProfiel,nieuwProfielRV,nieuwProfielSWW,nieuwProfielElec]

"""
================================================================================
VERGELIJKING MAKEN TUSSEN DICT HUIDIG PROFIEL EN DICT NIEUW PROFIEL
================================================================================
"""
def profileComparison(huidProf, nieuwProf):
   vergelijking = {} 
   vergelijking['huidige voorzieningen'] = {'ruimteverwarming':huidProf[0].get('ruimteverwarming') ,'sanitair warm water': huidProf[0].get('sanitair warm water'),'electriciteit':huidProf[0].get('electriciteit')}
   vergelijking['nieuwe voorzieningen'] = {'ruimteverwarming':nieuwProf[0].get('ruimteverwarming') ,'sanitair warm water': nieuwProf[0].get('sanitair warm water'),'electriciteit':nieuwProf[0].get('electriciteit')}

   vergelijking['huidig verbruik'] = huidProf[0].get('verbruik')

#zonder PV
   vergelijking["nieuw verbruik"] = nieuwProf[0].get('verbruik')
   vergelijking["besparing verbruik"] = verbruikvergelijking(huidProf[0].get('verbruik'),vergelijking.get('nieuw verbruik'))
   vergelijking["besparing primaire energie"] = (round(1-(nieuwProf[0].get("primaire energie PV")/huidProf[0].get("primaire energie")),3))*100
   vergelijking["verbruikskostbesparing"] =verbruikvergelijking(huidProf[0].get('verbruikskost'),nieuwProf[0].get('verbruikskost'))
#met PV
   vergelijking["nieuw verbruik PV"] = nieuwProf[0].get('verbruik met PV')
   vergelijking["besparing verbruik PV"] = verbruikvergelijking(huidProf[0].get('verbruik'),vergelijking.get('nieuw verbruik PV'))
   vergelijking["besparing primaire energie PV"] = (round(1-(nieuwProf[0].get("primaire energie")/huidProf[0].get("primaire energie")),3))*100
   vergelijking["verbruikskostbesparing PV"] =verbruikvergelijking(huidProf[0].get('verbruikskost'),nieuwProf[0].get('verbruikskost PV'))


   if nieuwProf[1].get('voorziening') == nieuwProf[2].get('voorziening'):
        vergelijking['investering RV en SWW'] = investering(nieuwProf[1],huidProf[1])
        vergelijking['investering RV'] = 0
        vergelijking['investering SWW'] = 0
        vergelijking['investering Elec'] = investering(nieuwProf[3],huidProf[3])
        vergelijking['investering PV'] = nieuwProf[0].get('investering PV')
   else:
        vergelijking['investering RV en SWW'] = 0
        vergelijking['investering RV'] = investering(nieuwProf[1],huidProf[1])
        vergelijking['investering SWW'] = investering(nieuwProf[2],huidProf[2])
        vergelijking['investering Elec'] = investering(nieuwProf[3],huidProf[3])
        vergelijking['investering PV'] = nieuwProf[0].get('investering PV')

#zonder PV
   vergelijking['investering'] = vergelijking.get('investering RV') + vergelijking.get('investering SWW') + vergelijking.get('investering Elec') + vergelijking.get('investering RV en SWW')
   vergelijking['cashflow'] = cashflows(huidProf[0].get('verbruik'),vergelijking.get('nieuw verbruik'),vergelijking.get('investering'))
   vergelijking['tvt'] = payback(vergelijking.get('cashflow'))  #[0] is jaar [1] is maanden
   vergelijking['tvtInt'] = float(str(vergelijking.get('tvt')[0]) + str(vergelijking.get('tvt')[1]/100))
   print(vergelijking.get('tvtInt'))
   vergelijking["CO2 besparing"] = round(huidProf[0].get('CO2') - nieuwProf[0].get('CO2'),3)
#met PV 
   vergelijking['investering met PV'] = vergelijking.get('investering RV') + vergelijking.get('investering SWW') + vergelijking.get('investering Elec') + vergelijking.get('investering RV en SWW') + vergelijking.get('investering PV')
   vergelijking['cashflow met PV'] = cashflows(huidProf[0].get('verbruik'),vergelijking.get('nieuw verbruik PV'),vergelijking.get('investering met PV'))
   vergelijking['tvt met PV'] = payback(vergelijking.get('cashflow met PV'))
   vergelijking['tvtInt met PV'] = float(str(vergelijking.get('tvt met PV')[0]) + str(vergelijking.get('tvt met PV')[1]/100))
   print(vergelijking.get('tvtInt met PV'))
   vergelijking["CO2 besparing met PV"] = round(huidProf[0].get('CO2') - nieuwProf[0].get('CO2'),3)  
   return vergelijking

'''
================================================================================
VERGELIJKING MET ALLE SCENARIOS OPROEPEN
================================================================================
'''
def callComparison(listScenarios, profiel): 
    listNewProfiel = []  #om alle nieuwe profielen bij te houden
    listVGL = []  #om alle dictionaries van vergelijkingen bij te houden 
    for i in range (len(listScenarios)): #elk scenario in de lijst  van scenarios doorlopen, een nieuw profiel maken en dit nieuw profiel vergelijken met het huidige profiel en de vergelijking opslaan in een list 
        print("berekening nieuw profiel voor:",listScenarios[i].get('scenario'))
        nieuwProf = nieuwProfiel(listScenarios[i],profiel)
        listNewProfiel.append(nieuwProf)
            # print(nieuwProf)
        vgl = profileComparison(profiel,nieuwProf)
        vgl['scenario'] = listScenarios[i].get('scenario')
        listVGL.append(vgl)
    return [listVGL, listNewProfiel]


def printComparison1(listComp): #functie om mooi te printen
    for dict in listComp:
        print("################################")
        for key,value in dict.items():
            print(key, value)

'''
================================================================================
LIJST VAN VERGELIJKINGEN PRINTEN
================================================================================
'''
class MyPDF(FPDF):
    def header(self):
        # Select Arial bold 15
        self.set_font('Arial', 'B', 20)
        # Move to the right
        self.cell(80)
        # Framed title
        self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.ln(20)


elements = [
    {'name':"scenario",'type':'T','x1': 20.0, 'y1': 17.0, 'x2': 78.0, 'y2': 30.0, 'font': 'Arial', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'C', 'text': '', 'priority': 2},
    {'name':"scenario",'type':'T','x1': 20.0, 'y1': 17.0, 'x2': 78.0, 'y2': 30.0, 'font': 'Arial', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'C', 'text': '', 'priority': 2},
    {'name':"scenario",'type':'T','x1': 20.0, 'y1': 17.0, 'x2': 78.0, 'y2': 30.0, 'font': 'Arial', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'C', 'text': '', 'priority': 2},
    {'name':"scenario",'type':'T','x1': 20.0, 'y1': 17.0, 'x2': 78.0, 'y2': 30.0, 'font': 'Arial', 'size': 12, 'bold': 1, 'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, 'align': 'C', 'text': '', 'priority': 2}
    
    ]
f = Template(format = 'A4',elements = elements, title= "Vergelijking energievoorzieningen bij U thuis.")
def printDictItems(dict):
    putCalls = []
    tabledata = []

    putCalls.append(put_text("Hieronder de huidige voorzieningen weergegeven:"))
    for k,v in dict.get('huidige voorzieningen').items():
        putCalls.append(put_text(k,": ",v,).style('margin-left:50px'))
    putCalls.append(put_text("Hieronder nieuwe mogelijke voorziengen van:"))
    for k,v in dict.get('nieuwe voorzieningen').items():
        putCalls.append(put_text(k,": ",v).style('margin-left:50px'))
        tabledata.append(str(v))
    putCalls.append(put_text("hieronder uw huidig verbruik weergegeven"))
    for k,v in dict.get('huidig verbruik').items():
        putCalls.append(put_text("verbruik voor",k,":",round(v),"kWh").style('margin-left:50px'))
    
    putCalls.append(put_text("Met dit nieuw scenario zou u volgend verbruik bekomen"))
    for k,v in dict.get('nieuw verbruik').items():
        putCalls.append(put_text("verbruik voor",k,":",round(v),"kWh").style('margin-left:50px'))
    
    putCalls.append(put_text("Voeg de ingegeven PV installatie in en dan bekomen we het volgende:"))
    for k,v in dict.get('nieuw verbruik PV').items():
        putCalls.append(put_text("verbruik voor",k,":",round(v),"kWh").style('margin-left:50px'))
    putCalls.append(put_text("Met dit nieuw scenario zou u volgend verbruikprofiel bekomen"))
    for k,v in dict.get('besparing verbruik').items():
        if v > 0 and k != "totaal besparing":
            putCalls.append(put_text("Besparing op verbruik voor",k,":",round(v),"kWh").style('margin-left:50px'))
        elif v < 0 and k != "totaal besparing":
            putCalls.append(put_text("Extra verbruik voor",k,":",-1*round(v),"kWh").style('margin-left:50px'))

    putCalls.append(put_text("Met de ingegeven PV installatie zou het verbruikprofiel er als volgt uitzien:"))
    for k,v in dict.get('besparing verbruik PV').items():
        if v > 0 and k != "totaal besparing":
            putCalls.append(put_text("Besparing op verbruik voor",k,":",round(v),"kWh").style('margin-left:50px'))
        elif v < 0 and k != "totaal besparing":
            putCalls.append(put_text("Extra verbruik voor",k,":",-1*round(v),"kWh").style('margin-left:50px'))

    a=b=c=d=e=f = ""
    a = a.join(key + ":" + str(round(value)) + "\n" for key, value in dict.get('nieuw verbruik').items())
    b = b.join(key + ":" + str(round(value)) + "\n" for key, value in dict.get('nieuw verbruik PV').items())
    c = c.join(key + ":" + str(round(value)) + "\n" for key, value in dict.get('besparing verbruik').items())
    d = d.join(key + ":" + str(round(value)) + "\n" for key, value in dict.get('besparing verbruik PV').items())
    e = e.join(key + ":" + str(round(value)) + "\n" for key, value in dict.get('besparing verbruik PV').items())
    f = f.join(key + ":" + str(round(value)) + "\n" for key, value in dict.get('besparing verbruik PV').items())
        
    putCalls.append(put_table([
        ["","zonder PV","met PV"],
        ['verbruik [kWh/jaar]',a,b],
        ['besparing verbruik [kWh/jaar]',c,d],
       # ['besparing primaire energie',dict.get('besparing primaire energie'),dict.get('besparing primaire energie PV')],
        ['kostbesparing [€/jaar]',e,f],
        ['CO2 besparing [kg/jaar]',dict.get('CO2 besparing'),dict.get('CO2 besparing met PV')],
        ['investering [€]',dict.get('investering'),dict.get('investering met PV')],
        ['terugverdientijd',str(str(str(dict.get('tvt')[0]) + " jaar en ") + str(str(dict.get('tvt')[1]) + " maanden")),str(str(str(dict.get('tvt met PV')[0]) + " jaar en ") + str(str(dict.get('tvt met PV')[1]) + " maanden")) ]

    ]))


    # putCalls.append(put_table([tabledata], header = ['ruimteverwarming','sanitair warm water','electriciteit','besparing [€/j]','investering','terugverdientijd','co2 besparing [kg]']))
    return putCalls


def printComparison(listComp): #functie om mooi te printen
    pdf = FPDF()
    pdf.set_margins(left = 2.54,top = 2.54)
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.multi_cell(0, 10, txt = "dit is een document dat een overzicht biedt van nieuwe mogelijke energievoorziengen voor warmte en electriciteit bij u thuis", border = 1, align = 'L')
    # firstlines = "dit is een document dat een overzicht biedt van nieuwe mogelijke energievoorziengen voor warmte en electriciteit bij u thuis"
    # fileOut.writelines(firstlines)
    for dict in listComp:
        # pdf.add_page()
        # pdf.header()
        collapsTitle = ""
        collapsTitle += "VERGELIJKING MET " + dict.get('scenario')+":"+dict.get("nieuwe voorzieningen").get("ruimteverwarming")+"-"+dict.get("nieuwe voorzieningen").get("sanitair warm water")+"-"+dict.get("nieuwe voorzieningen").get("electriciteit")
        put_collapse(collapsTitle,printDictItems(dict))

        
            # strK = str(key)
            # strV = str(value)
            # pdf.multi_cell(200, 10, txt = strK + strV,align = 'C')

#code hieronder is om de gegenereerde pdf hierboven, te kunnen outen naar de website           
    # pdf.output("energievoorzieningen.pdf")
    # content = open("energievoorzieningen.pdf",'rb').read()
    # put_file("energievoorzieningen.pdf",content)
         

"""
Plotting
"""
# y1 = huidigProfiel.get("primaire energie")
# y2 = nieuwProfiel.get("primaire energie")
# x = pointCount #aantal punten in de timevalue list want printen met de timevalues gaat niet 

# plt.plot(x,y1)
# plt.plot(x,y2, color = 'red')
# plt.show()

"""
================================================================================
code oproepen en server starten
================================================================================
"""

def main():
    insertCSVinfo("overzichtSLPs.csv")
    generateSLP(SLPg,SLPel)
    userinput = userInputs(RVinput,SWWinput,Elecinput)
    huidigeVoorzieningSWW = userinput[0][1]
    huidigeVoorzieningRV = userinput[0][0]
    huidigeVoorzieningElec = userinput[0][2]
    huidigeVoorzieningen = [huidigeVoorzieningRV,huidigeVoorzieningSWW,huidigeVoorzieningElec]
    huidigProf = huidigProfiel(huidigeVoorzieningen,SLP)
    listVGL = callComparison(scenarios,huidigProf)[0]

    #hieronder code om de lijst te sorteren op basis van een specifieke value, in deze volgorde wordt dan afgeprint
    sortedList = sorted(listVGL, key=lambda i: i['CO2 besparing'],reverse=True)
    printComparison(sortedList)
    

start_server(main, port = 0,debug=True,remote_access=True)
  