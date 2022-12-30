
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:33:23 2022

@author: Andreas
"""

"""imports"""

import pandas as pd
import os
import matplotlib.pyplot as plt 

# print(os.getcwd())
"""inputs systeem"""  #ingelezen via een csv file, code hieronder nodig voor de inlezing 
path = os.getcwd()
pathcsv = os.path.join(path, "overzichtSLPs.csv")
# print(pathcsv)
data = pd.read_csv(os.path.join(path, "overzichtSLPs.csv"))
data.head()
# print(data)

# ALLE INGELEZEN DATA HIERONDER   
timeValues = data.iloc[:,0]
pointCount = [i for i in range(len(timeValues))]  #aantal punten in timevalues tellen (35000+), nodig voor de plots 
SLPe = data.iloc[:,6] #profiel van de VREG
SLPg = data.iloc[:,8] #profiel van de VREG
COP = data.iloc[:,9].tolist() #nu is er de mogelijkheid om de COP variabel te maken, op dit moment nog steeds een constante waarde in de csv, uiteindelijk zou dit ook een profiel per kwartier moeten worden van percentages. hiermee kan dan de COP van een elke warmtepomp vermenigvuldigt worden om een variable factor mee te rekenen 
elecEff = data.iloc[:,10]
PV_opbrengst = data.iloc[:,11].tolist()  #eerste PV opbrengst, op dit moment vooral om gewoon code te testen
#print(PV_opbrengst)

# print(timeValues)
#print(len(timeValues))
#print(SLPe)
#print(SLPg)





'''
HIERONDER EEN LIJST VAN VOORZIENGEN EN DE INGEGEVEN DATA
'''
toepassingen = ["Ruimteverwarming", "Sanitair Warm Water","electriciteit"]

#INPUTVOORZIENINGEN
cvKetel_gas_25 = {"naam":"Gasketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.9,"maxVermogen":30}
cvKetel_stookolie_25 = {"naam":"Gasketel","Toepassing":"Ruimteverwarming","verbruiker": "stookolie","efficientie":0.9,"maxVermogen":30}
electriciteit_net = {"naam":"Electriciteitsnet","Toepassing":"electriciteit","verbruiker": "electriciteit","efficientie":1}

###VOORZIENINGEN
#warmtepompen
heatPump_LW_3 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.8,"maxVermogen":3,"prijs":5289}
heatPump_LW_5 = {"naam":"Lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.8,"maxVermogen":5,"prijs":6370}
heatPump_LW_8 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.5,"maxVermogen":8,"prijs":9385}
heatPump_LW_10 = {"naam":"lucht-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.54,"maxVermogen":10,"prijs":7798}

heatPump_GW_3 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":3.73,"maxVermogen":3,"prijs":3800}
heatPump_GW_5 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.23,"maxVermogen":5,"prijs":7900}
heatPump_GW_8 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.4,"maxVermogen":8,"prijs":8300}
heatPump_GW_10 = {"naam":"bodem-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.5,"maxVermogen":15,"prijs":9000}

heatPump_WW_3 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.7,"maxVermogen":3,"prijs":9000}
heatPump_WW_5 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.7,"maxVermogen":5,"prijs":9300}
heatPump_WW_8 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.8,"maxVermogen":8,"prijs":9500}
heatPump_WW_10 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":4.9,"maxVermogen":10,"prijs":10000}
heatPump_WW_15 = {"naam":"water-water Warmtepomp","Toepassing":"ruimteverwarming","verbruiker": "electriciteit","efficientie":5.3,"maxVermogen":15,"prijs":11000}


doorstroomboiler_5 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":1,"maxVermogen":5,"prijs":500}

condensketel_13 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":13,"prijs":1835}
condensketel_20 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":20,"prijs":2038}
condensketel_30 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":30,"prijs":2600}
condensketel_50 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":50,"prijs":3800}
condensketel_80 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":80,"prijs":4800}
condensketel_100 = {"naam":"condensatieketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":100,"prijs":5500}


#nummer achter de naam is de boilerinhoud in Liter
zonneboiler_150 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"inhoud":150,"gezinsgrootte":3,"prijs":2543}
zonneboiler_250 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"inhoud":250,"gezinsgrootte":5,"prijs":3000}
zonneboiler_350 = {"naam":"zonneboiler","Toepassing":"sanitair warm water","verbruiker": "zonne-energie","efficientie":1,"inhoud":350,"gezinsgrootte":7,"prijs":3500}

warmtepompboiler_LW_150 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":2.5,"inhoud":150,"prijs":2294}
warmtepompboiler_LW_200 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":3.19,"inhoud":200,"prijs":2790}
warmtepompboiler_LW_270 = {"naam":"lucht-water warmtepompboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","efficientie":3.19,"inhoud":270,"prijs":2906}

elektrischeDoorstroomboiler_5 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","continue verbruik (kWh)":0.225,"inhoud":5,"efficientie":1,"maxVermogen":2,"prijs":200}
elektrischeDoorstroomboiler_10 = {"naam":"doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "electriciteit","continue verbruik (kWh)":0.273,"inhoud":10,"efficientie":1,"maxVermogen":2,"prijs":280}


###LIJSTEN VAN VOORZIENINGEN
warmtepomp_RVenSWW = []
warmtepomp_LW = [heatPump_LW_3,heatPump_LW_5,heatPump_LW_8,heatPump_LW_10]
warmtepomp_GW = [heatPump_GW_3,heatPump_GW_5,heatPump_GW_8,heatPump_GW_10]
warmtepomp_WW = [heatPump_WW_3,heatPump_WW_5,heatPump_WW_8,heatPump_WW_10,heatPump_WW_15]

condensatieketels = [condensketel_13, condensketel_20,condensketel_30,condensketel_50,condensketel_80,condensketel_100]
doorstroomboilersE = [elektrischeDoorstroomboiler_5,elektrischeDoorstroomboiler_10]
zonneboilers = [zonneboiler_150,zonneboiler_250,zonneboiler_350]
warmtepompboiler = [warmtepompboiler_LW_150,warmtepompboiler_LW_200,warmtepompboiler_LW_270]

list_voorzieningenRV = [warmtepomp_LW,condensatieketels]








'''
SCENARIOS
hier komt een lijst van dictionaries die een scenario voorstellen, voor elke voorziening een toepassing. op deze manier kunnen interessante combinaties van voorzieningen vergeleken worden
'''

#SCENARIOS
scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet","PV":False}
scenario2 = {"scenario":"scenario 2", "ruimteverwarming":"warmtepomp GW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet","PV":False}
scenario3 = {"scenario":"scenario 3", "ruimteverwarming":"warmtepomp WW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet","PV":False}
scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"electriciteitsnet","PV":False}
scenario5 = {"scenario":"scenario 5","ruimteverwarming":"warmtepomp LW","sanitair warm water":"doorstroomboiler gas","electriciteit":"electriciteitsnet","PV":False}
scenario6 = {"scenario":"scenario 6","ruimteverwarming":"warmtepomp LW","sanitair warm water":"warmtepomp LW","electriciteit":"electriciteitsnet","PV":True}
scenario7 = {"scenario":"scenario 7","ruimteverwarming":"condensatieketel","sanitair warm water":"condensatieketel","electriciteit":"electriciteitsnet","PV":False}
scenarios = [scenario1,scenario2,scenario3,scenario4,scenario6,scenario7]

"""
DIMENSIONERING VAN NIEUWE VOORZIENINGEN
"""
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
    
    elif voorziening == "zonneboiler":
        print("zonneboiler dimensionering mislukt")
        


    return newvoorziening


"""
PERCENTUELE VRAAGPROFIELEN GENEREREN
""" 
#de SLPs voor ruimteverwarming, sanitair genereren op basis van het SLPg van de VREG
#het onderscheid maken tussen de profielen voor ruimteverwarming, sanitair ww en electriciteit
min_gas = min(SLPg)  #minimum van het gasprofiel = waarde voor sanitair ww 
# print("minimaal gas sww",min_gas)
SLPsww =[min_gas]*len(timeValues)  #SLP voor sanitair ww genereren, de constante waarde (min van gasprofiel) voor elk kwartier. To dp: variatie in het profiel brengen, is meer realistisch dan altijd eenzelfde waarde
#print(SLPsww)
SLPrv = [SLPg[i]-SLPsww[i] for i in range(len(timeValues))]  #SLP voor ruimteverwarming genereren door de waarde voor SWW af te trekken van het totaal profiel voor gas
# print(sum(SLPsww))
profielen = [SLPrv, SLPsww, SLPe]
#print(SLPrv)
# print(sum(SLPrv)+sum(SLPsww))



"""INPUTS VAN DE GEBRUIKER"""
"""voorzieningen""" 
 #dit moet een input worden van de gebruiker
huidigeVoorzieningSWW = cvKetel_gas_25
huidigeVoorzieningRV = cvKetel_gas_25
huidigeVoorzieningElec = electriciteit_net
huidigeVoorzieningen = [huidigeVoorzieningRV,huidigeVoorzieningSWW,huidigeVoorzieningElec]

"""huidige energieverbruik""" #dit moet een input worden van de gebruiker
Jaarverbruik_stookolie = 0 #kWh
Jaarverbruik_gas = 20000 #kWh
Jaarverbruik_elec = 3500 #kWh



"""
INPUTS VAN DE GEBRUIKER VERWERKEN
"""
"""huidig verbruik verdelen over procentueel verbruikprofiel -> verbruikprofiel genereren"""
def verbruikProfiel(voorziening, profiel):  #functie vermenigvuldigt elk percentage per kwartier van de slp met het overeenkomstige  totaal jaarverbruik 
    if voorziening.get("verbruiker") =="electriciteit":
            jaarverbruik = Jaarverbruik_elec
            verbruikersVraag = [i*jaarverbruik for i in profiel] #delen door 0.25 op kWkwartier op te zetten naar kW, kWkwartier opmdat er per kwartier vermenigvuldigt wordt met het totaal. 
    elif voorziening.get("verbruiker") =="aardgas":
            jaarverbruik = Jaarverbruik_gas
            verbruikersVraag = [i*jaarverbruik for i in profiel]           
    elif voorziening.get("verbruiker") =="stookolie":
            jaarverbruik = Jaarverbruik_stookolie
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
CO2 uitstoot
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
FUNCTIES OVER VERBRUIK
"""
"""
energievraag bepalen
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
    besparingsdict= {"aardgas":0.0,"stookolie":0.0,"electriciteit":0.0}
    besparingsdict['aardgas'] = round(dict1.get("aardgas") - dict2.get("aardgas"),3)
    besparingsdict['electriciteit'] = round(dict1.get("electriciteit") - dict2.get("electriciteit"),3)
    besparingsdict['stookolie'] = round(dict1.get("stookolie") - dict2.get("stookolie"),3)
    return besparingsdict
  
 #primaire energie berekenen 
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

"""FINANCIEEL"""

#https://code.activestate.com/recipes/576686-npv-irr-payback-analysis/
#momenteel een vaste waarde per kWh, dit variabel maken is mogelijk maar dan moeten we ook per kwartier een lijst inlezen, en aanpassen in de functies dat het elk overeenkomstig kwartier moet vermenigvuldigen 
costElec = 0.5 #€/kWh   
costAardgas = 0.2 #€/kWh
costStookolie = 0.3 #€/kWh

#returns verbruikskost per jaar afhahnkelijk van welke verbruiker
#input is een dict van een voorziening {'naam':'...','toepassing':'...',...} en een Integer voor verbruik
def usageCostYear(voorziening, verbruik):  
    verbruiker = voorziening.get('verbruiker')
    cost = 0
    if verbruiker == "electriciteit":
            cost = verbruik * costElec
    elif verbruiker == "aardgas":
            cost = verbruik * costAardgas
    elif verbruiker == "stookolie":
            cost = verbruik * costStookolie
    return cost

#returns verbruikskost per jaar afhahnkelijk van welke verbruiker 
#input is een item van een dictionary {'verbruiker':IntVerbruik}
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




def cashflows(oudverbruik, nieuwverbruik,investering):  #de cashflow per jaar berekenen, periode is het aantal jaar. Eerste waarde is het jaar 0 = de investering
    print("###berekening cashflows###")
    periode = 20 #jaar
    cashflow = [None]*periode
    developmentVerbruik = 0.03  #elk jaar 3% meer verbruik dan het jaar voordien
    developmentCost = 0.19 #elk jaar stijgt de prijs met 5%
    kostHuidig = usageCostTotal(oudverbruik) #♣initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
    kostNieuw = usageCostTotal(nieuwverbruik)
    onderhoud = 100 #jaarlijkse kost onderhoud
    cashflow[0] = -1*investering
    for i in range(1,len(cashflow)):
        cashflow[i] = round(cashflow[i-1] + kostHuidig - kostNieuw - onderhoud,3)

        # oudverbruik.update((key,value*developmentVerbruik) for key, value in oudverbruik.items())
        # nieuwverbruik.update((key,value*developmentVerbruik) for key, value in nieuwverbruik.items())
        kostHuidig = kostHuidig*(1+developmentCost)
        kostNieuw = kostNieuw*(1+developmentCost)
    # print(cashflow)
    return cashflow
        

def payback_of_investment(investment, cashflows): #payback periode berekenen op basis van investering en cashflow per jaar
    print("###terugverdientijd berekenen###")
    """The payback period refers to the length of time required 
       for an investment to have its initial cost recovered.
       
       >>> payback_of_investment(200.0, [60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    total, years, cumulative = 0.0, 0, []
    # if not cashflows or (sum(cashflows) < investment):
    #     raise Exception("insufficient cashflows")
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



                
       
        




def dimensioneringPV(electriciteitsProductie, kost):
    #https://apps.energiesparen.be/zonnekaart
    electriciteitsProductie = electriciteitsProductie*0.85
    kost = kost*1
    return [electriciteitsProductie, kost]



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
DICTIONARY VAN HUIDIG PROFIEL GENEREREN
"""

def huidigProfiel(huidVoor):
    huidigProfiel = {}
    huidigProfielRV = {}
    huidigProfielSWW = {}
    huidigProfielElec = {}

    huidigeProfielen = [huidigProfielRV,huidigProfielSWW,huidigProfielElec]
    huidigeVoorziening = [huidVoor[0],huidVoor[1],huidVoor[2]]
    SLP = [SLPrv, SLPsww, SLPe]


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
        # print(huidigeProfielen[i].get('voorziening'),huidigeProfielen[i].get('totaal verbruik'),huidigeProfielen[i].get('verbruikersverdeling'))



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
DICTIONARY VAN NIEUW PROFIEL GENEREREN
"""
def nieuwProfiel(scenario, huidProf):
    nieuwProfiel = {}
    selectie = nieuweVoorzieningen(scenario,max(huidProf[1].get('verbruikProfiel'))*4,max(huidProf[2].get('verbruikProfiel'))*4)  #maal 4 om max(kWh) om te zetten naar kW 
    print("max RV en max SWW", max(huidProf[1].get('verbruikProfiel')), max(huidProf[2].get('verbruikProfiel')))
    nieuwVoorzieningRV = selectie[1]
    nieuwVoorzieningSWW = selectie[2]
    nieuwVoorzieningElec = selectie[3]
    PV = scenario.get('PV')
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

    nieuwProfiel["ruimteverwarming"] = nieuwProfielRV.get('voorziening').get('naam')
    nieuwProfiel["sanitair warm water"] = nieuwProfielSWW.get('voorziening').get('naam')
    nieuwProfiel["electriciteit"] = nieuwProfielElec.get('voorziening').get('naam')
    nieuwProfiel["verbruik"] = {}
    nieuwProfiel["verbruikskost"] = {}
    nieuwProfiel['investering PV'] = 0
    for i,j in nieuwProfielRV.get("verbruikersverdeling").items():
        for k,l in nieuwProfielSWW.get("verbruikersverdeling").items():
            for m,n in nieuwProfielElec.get('verbruikersverdeling').items():
                if i == k == m:
                    nieuwProfiel['verbruik'][i] = j+l+n
    if PV == True:  #opbrengst van PV aftrekken van totaal verbruik electriciteit
        #https://apps.energiesparen.be/zonnekaart
        PV_opbrengst = 3687 #kWh per jaar
        PV_kost = 4500 #€
        PV = dimensioneringPV(PV_opbrengst,PV_kost)
        nieuwProfiel.get('verbruik')['electriciteit'] = newConsumptionPV(nieuwProfiel.get('verbruik').get('electriciteit'),PV[0])
        nieuwProfiel['investering PV'] = PV[1]

    for i,j in nieuwProfiel.get("verbruik").items():
            nieuwProfiel["verbruikskost"][i] = usageCostItem(i,j)

    nieuwProfiel["totale verbruikskost"] = sum(nieuwProfiel.get("verbruikskost").values())

    nieuwProfiel["primaire energie"] = primaryEnergy(nieuwProfiel.get("verbruik"))                
    

    
    # nieuwProfiel['totale investering'] = nieuwProfiel.get('investering RV') + nieuwProfiel.get('investering SWW') + nieuwProfiel.get('investering Elec') + PV_cost  #som van de investeringen voor elke toepassing
    
    nieuwProfiel['CO2'] = nieuwProfielRV.get('totaal CO2') + nieuwProfielSWW.get('totaal CO2') + nieuwProfielElec.get('totaal CO2')

    return [nieuwProfiel,nieuwProfielRV,nieuwProfielSWW,nieuwProfielElec]

"""
VERGELIJKING MAKEN TUSSEN DICT HUIDIG PROFIEL EN DICT NIEUW PROFIEL
"""
def profileComparison(huidProf, nieuwProf):
   vergelijking = {} 
   vergelijking['huidige voorziening RV/SWW/elec'] = [huidProf[0].get('ruimteverwarming'),huidProf[0].get('sanitair warm water'),huidProf[0].get('electriciteit')]
   vergelijking['nieuwe voorziening RV/SWW/elec']= [nieuwProf[0].get('ruimteverwarming'),nieuwProf[0].get('sanitair warm water'),nieuwProf[0].get('electriciteit')]
   vergelijking['huidig verbruik'] = huidProf[0].get('verbruik')
   vergelijking["nieuw verbruik"] = nieuwProf[0].get('verbruik')
   vergelijking["besparing verbruik"] = verbruikvergelijking(huidProf[0].get('verbruik'),nieuwProf[0].get('verbruik'))
   vergelijking["besparing primaire energie"] = (round(1-(nieuwProf[0].get("primaire energie")/huidProf[0].get("primaire energie")),3))*100
   vergelijking["kostbesparing"] =verbruikvergelijking(huidProf[0].get('verbruikskost'),nieuwProf[0].get('verbruikskost'))

   if nieuwProf[1].get('voorziening') == nieuwProf[2].get('voorziening'):
        vergelijking['investering RV en SWW'] = investering(nieuwProf[1],huidProf[1])
        vergelijking['investering RV'] = 0
        vergelijking['investering SWW'] = 0
        vergelijking['investering Elec'] = investering(nieuwProf[3],huidProf[3])
   else:
        vergelijking['investering RV en SWW'] = 0
        vergelijking['investering RV'] = investering(nieuwProf[1],huidProf[1])
        vergelijking['investering SWW'] = investering(nieuwProf[2],huidProf[2])
        vergelijking['investering Elec'] = investering(nieuwProf[3],huidProf[3])
   vergelijking['investering PV'] = nieuwProf[0].get('investering PV')
   vergelijking['investering'] = vergelijking.get('investering RV') + vergelijking.get('investering SWW') + vergelijking.get('investering Elec') + vergelijking.get('investering RV en SWW') + vergelijking.get('investering PV')
   vergelijking['cashflow'] = cashflows(huidProf[0].get('verbruik'),nieuwProf[0].get('verbruik'),vergelijking.get('investering'))
   vergelijking['tvt jaar'] = payback(vergelijking.get('cashflow'))[0]
   vergelijking['tvt maand'] = payback(vergelijking.get('cashflow'))[1]
   vergelijking["CO2 besparing"] = round(huidProf[0].get('CO2') - nieuwProf[0].get('CO2'),3)
   return vergelijking



"""
 FINALE FUNCTIES OPROEPEN
"""
listVGL = []  #om alle vergelijkingen bij te houden
newProfiel = []  #om alle nieuwe profielen bij te houden
huidigProf = huidigProfiel(huidigeVoorzieningen)   #huidig profiel genereren

def callComparison(listScenarios):  
    for i in range (len(listScenarios)): #elk scenario in de lijst  van scenarios doorlopen, een nieuw profiel maken en dit nieuw profiel vergelijken met het huidige profiel en de vergelijking opslaan in een list 
        print("berekening nieuw profiel voor:",listScenarios[i].get('scenario'))
        nieuwProf = nieuwProfiel(listScenarios[i],huidigProf)
        newProfiel.append(nieuwProf)
        # print(nieuwProf)
        vgl = profileComparison(huidigProf,nieuwProf)
        vgl['scenario'] = listScenarios[i].get('scenario')
        listVGL.append(vgl)


# print(huidigProf)
def printComparison(listComp): #functie om mooi te printen
    for dict in listComp:
        print("################################")
        print("VERGELIJKING MET:",dict.get('scenario'))
        for key,value in dict.items():
            print(key, value)
        print("################################")

 

callComparison(scenarios)  #alle scnenarios in de lijst van scenarios vergelijken met huidige situatie en opslaan in lijst
printComparison(listVGL)  #de lijst van vergelijkingen oproepen en printen
# print(newProfiel[0])
    


"""plotting"""
# y1 = huidigProfiel.get("primaire energie")
# y2 = nieuwProfiel.get("primaire energie")
# x = pointCount #aantal punten in de timevalue list want printen met de timevalues gaat niet 

# plt.plot(x,y1)
# plt.plot(x,y2, color = 'red')
# plt.show()