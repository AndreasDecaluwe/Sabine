
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:33:23 2022

@author: Andreas
"""

"""imports"""

import pandas as pd
import os
import matplotlib.pyplot as plt 

print(os.getcwd())
"""inputs systeem"""  #♦op dit moment handmatig enkele waarden ingegeven, al deze waarden zouden voor een volledig jaar (per kwartier) ingelezen moeten worden van een excell 
path = os.getcwd()
pathcsv = os.path.join(path, "overzichtSLPs.csv")
print(pathcsv)
data = pd.read_csv(os.path.join(path, "overzichtSLPs.csv"))


data.head()
#print(data)  
timeValues = data.iloc[:,0]
pointCount = [i for i in range(len(timeValues))]  #aantal punten in timevalues tellen (35000+), nodig voor de plots 
SLPe = data.iloc[:,6] #profiel van de VREG
SLPg = data.iloc[:,8] #profiel van de VREG
COP = data.iloc[:,9].tolist() #nu is er de mogelijkheid om de COP variabel te maken, op dit moment nog steeds een constante waarde in de csv 
elecEff = data.iloc[:,10]
PV_opbrengst = data.iloc[:,11].tolist()
#print(PV_opbrengst)

print(timeValues)
#print(len(timeValues))
#print(SLPe)
#print(SLPg)
PV = False
PV_cost = 0




"""lijst voorzieningen"""
toepassingen = ["Ruimteverwarming", "Sanitair Warm Water","Elektriciteit"]

list_voorzieningen = []  #moet ingelezen worden van een csv file 
heatPump_LW_3_3 = {"naam":"Lucht-water Warmtepomp","Toepassing":"Ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":3.3,"prijs":5289}
heatPump_LW_4_6 = {"naam":"Lucht-water Warmtepomp","Toepassing":"Ruimteverwarming","verbruiker": "elektriciteit","efficientie":COP,"maxVermogen":4.6,"prijs":6370}
heatPump_LW_8_5 = {"naam":"Lucht-water Warmtepomp","Toepassing":"Ruimteverwarming","verbruiker": "elektriciteit","efficientie":8.5,"maxVermogen":8.5,"prijs":9385}
condensketel_30 = {"naam":"condensatiesketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.96,"maxVermogen":30}
doorstroomboiler_5 = {"naam":"elektrische doorstroomboiler","Toepassing":"sanitair warm water","verbruiker": "elektriciteit","efficientie":1,"maxVermogen":5,"prijs":500}
warmtepomp_LW = [heatPump_LW_3_3,heatPump_LW_4_6,heatPump_LW_8_5]
condensatieketels = [condensketel_30]
list_voorzieningenRV = [warmtepomp_LW,condensatieketels]

cvKetel_gas_25 = {"naam":"Gasketel","Toepassing":"Ruimteverwarming","verbruiker": "aardgas","efficientie":0.9,"maxVermogen":30}

electriciteit_net = {"naam":"Electriciteitsnet","Toepassing":"electriciteit","verbruiker": "elektriciteit","efficientie":1}

"""scenarios"""
#hier komt een lijst van dictionaries die een scenario voorstellen, voor elke voorziening een toepassing. op deze manier kunnen interessante combinaties van voorzieningen vergeleken worden

scenario1 = {"scenario":"scenario 1", "ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler","electriciteit":"het net"}
scenario2 = {"scenario":"scenario 2","ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"het net"}
scenario3 = {"scenario":"scenario 3","ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler gas","electriciteit":"het net"}
scenario4 = {"scenario":"scenario 4","ruimteverwarming":"warmtepomp","sanitair warm water":"warmtepomp","electriciteit":"het net"}
scenarios = [scenario1, scenario2,scenario3,scenario4]



"""vraagprofielen definieren""" #de SLPs voor ruimteverwarming, sanitair genereren op basis van het SLPg van de VREG
#het onderscheid maken tussen de profielen voor ruimteverwarming, sanitair ww en electriciteit
min_gas = min(SLPg)  #minimum van het gasprofiel = waarde voor sanitair ww 
#print(min_gas)
SLPsww =[min_gas]*len(timeValues)  #SLP voor sanitair ww genereren, de constante waarde (min van gasprofiel) voor elk kwartier. To dp: variatie in het profiel brengen, is meer realistisch dan altijd eenzelfde waarde
#print(SLPsww)
SLPrv = [round(SLPg[i]-SLPsww[i],5) for i in range(len(timeValues))]  #SLP voor ruimteverwarming genereren door de waarde voor SWW af te trekken van het totaal profiel voor gas
print(sum(SLPsww))
profielen = [SLPrv, SLPsww, SLPe]
#print(SLPrv)



"""INPUTS VAN DE GEBRUIKER"""
"""voorzieningen"""  #dit moet een input worden van de gebruiker
huidigeVoorzieningSWW = cvKetel_gas_25
huidigeVoorzieningRV = cvKetel_gas_25
huidigeVoorzieningElec = electriciteit_net

"""huidige energieverbruik""" #dit moet een input worden van de gebruiker
Jaarverbruik_stookolie = 0 #kWh
Jaarverbruik_gas = 20000 #kWh
Jaarverbruik_elec = 3500 #kWh



"""INPUTS VAN DE GEBRUIKER VERWERKEN"""
"""huidig verbruik verdelen over verbruikprofiel -> verbruikprofiel genereren"""
def verbruikProfiel(voorziening, profiel):  #functie vermenigvuldigt elk percentage per kwartier van de slpo met het overeenkomstige  totaal jaarverbruik 
    if voorziening.get("verbruiker") =="elektriciteit":
            jaarverbruik = Jaarverbruik_elec
            verbruikersVraag = [i*jaarverbruik for i in profiel]        
    elif voorziening.get("verbruiker") =="aardgas":
            jaarverbruik = Jaarverbruik_gas
            verbruikersVraag = [i*jaarverbruik for i in profiel]           
    elif voorziening.get("verbruiker") =="stookolie":
            jaarverbruik = Jaarverbruik_stookolie
            verbruikersVraag = [i*jaarverbruik for i in profiel]
#    print(verbruikersVraag)
    return verbruikersVraag


def verbruikersSom(voorziening, som): #functie verdeelt het verbruik over alle gedefinieerde verbruikers (gas, stookolie, elec), maakt het vergelijken voor besparingen achteraf gemakkelijker
    verbruikers = {"aardgas":0.0,"stookolie":0.0,"elektriciteit":0.0}
    if voorziening.get("verbruiker") =="elektriciteit":
        verbruikers["elektriciteit"] = verbruikers.get("elektriciteit") + som
    elif voorziening.get("verbruiker") =="aardgas":
        verbruikers["aardgas"] = verbruikers.get("aardgas") + som
    elif voorziening.get("verbruiker") =="stookolie":
        verbruikers["stookolie"] = verbruikers.get("stookolie") + som
#    print(verbruikers)
    return verbruikers


"""CO2 uitstoot"""
#https://www.energids.be/nl/vraag-antwoord/wat-houdt-een-ton-co2-precies-in/2141/
co2_gas = 0.206 #kg/kWh
co2_elec = 0.220 #kg/kWh
co2_stookolie = 0.271 #kg/kWh


def emissions(verbruiker, verbruik):  #returns kg co2/kwh voor een bepaalde verbruiker
    if verbruiker == "elektriciteit":
            co2 = round(verbruik * co2_elec,3)
    elif verbruiker == "aardgas":
            co2 = round(verbruik * co2_gas,3)
    elif verbruiker == "stookolie":
            co2 = round(verbruik * co2_stookolie,3)
#    print(co2)
    return co2



"""energievraag bepalen""" #energievraag of nuttige energie bepalen op basis van huidige efficientie

def energieVraag(huidigeVoorziening,huidigVraagProfiel):
    if type (huidigeVoorziening.get("efficientie")) == list: #if functie is nodig om te bepalen of de efficientie tijdsafhankelijke is of niet, tijdsafhankelijk staat in een list, niet-afhankelijk is gwn een integer
        vraag = [a*b for a,b in zip(huidigVraagProfiel, huidigeVoorziening.get("efficientie") )]
    else:
        vraag = [i*huidigeVoorziening.get("efficientie") for i in huidigVraagProfiel]
    return vraag

"""nieuw verbruik bepalen""" #nieuw verbruik voor nieuwe situatie

def newConsumption(vraagprofiel,nieuweVoorziening):   #op basis van de energievraag en een nieuwe efficientie het nieuwe verbruik berekenen
    if type (nieuweVoorziening.get("efficientie")) == list:  #voorbeeld een variable COP staat in een tijdafhankelijke lijst geschreven, elk verbruik
        newCons = [a/b for a,b in zip(vraagprofiel,nieuweVoorziening.get("efficientie"))]
    else:  #als we een constante COP gebruiken
        newCons = [i/nieuweVoorziening.get("efficientie") for i in vraagprofiel]
    return newCons

def newConsumptionPV(verbruikprofiel, PV_opbrengst):  #PV opbrengst aftrekken van huidig verbruik voor electriciteit, per kwartier
    newCons = [None]*len(verbruikprofiel)
    for i in range(len(verbruikprofiel)):
        newCons[i] = (round(verbruikprofiel[i] - PV_opbrengst[i],3)) 
    return newCons

def verbruikvergelijking(dict1, dict2):  #2 dictionaries van verbruikers vergelijken met elkaar, gebruikt om nieuw verbruik te vergelijken met huidig verbruik. Geeft duidelijk weer waar er een besparing is en waar een extra/nieuw verbruik is
    besparingsdict= {"aardgas":0.0,"stookolie":0.0,"elektriciteit":0.0}
    besparingsdict['aardgas'] = round(dict1.get("aardgas") - dict2.get("aardgas"),3)
    besparingsdict['elektriciteit'] = round(dict1.get("elektriciteit") - dict2.get("elektriciteit"),3)
    besparingsdict['stookolie'] = round(dict1.get("stookolie") - dict2.get("stookolie"),3)
    return besparingsdict
  
 #primaire energie berekenen 
#input is een dictionary van verbruikers met een overeenkomstige verbruiks waarde ex {"gas":100}   
def primaryEnergy(dictionary): 
    #https://www.vlaanderen.be/epb-pedia/rekenmethode/rekenmethode-e-peil/karakteristiek-jaarlijks-primair-energieverbruik
    mulFactorGas = 1
    mulFactorElec = 2.5
    mulFactorStookolie = 1
    primE = 0
    for key, value in dictionary.items():
        if key == "elektriciteit":
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
costAardgas = 0.4 #€/kWh
costStookolie = 0.3 #€/kWh

#returns verbruikskost per jaar afhahnkelijk van welke verbruiker
#input is een dict van een voorziening {'naam':'...','toepassing':'...',...} en een Integer voor verbruik
def usageCostYear(voorziening, verbruik):  
    verbruiker = voorziening.get('verbruiker')
    cost = 0
    if verbruiker == "elektriciteit":
            cost = verbruik * costElec
    elif verbruiker == "aardgas":
            cost = verbruik * costAardgas
    elif verbruiker == "stookolie":
            cost = verbruik * costStookolie
    return cost

#returns verbruikskost per jaar afhahnkelijk van welke verbruiker 
#input is een dictionary {'verbruiker':IntVerbruik}
def usageCostTotal(verbruik): 
    cost = 0
    for key, val in verbruik.items():
            if key == "elektriciteit":
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
    if key == "elektriciteit":
        cost += round(value * costElec,2)
    elif key == "aardgas":
        cost += round(value * costAardgas,2)
    elif key == "stookolie":
        cost += round(value * costStookolie,2)
    return cost


def cashflows(oudverbruik, nieuwverbruik,investering):  #de cashflow per jaar berekenen, periode is het aantal jaar. Eerste waarde is het jaar 0 = de investering
    print("###berekening cashflows###")
    periode = 10 #jaar
    cashflow = [None]*periode
    developmentVerbruik = 0.03  #elk jaar 3% meer verbruik dan het jaar voordien
    developmentCost = 0.05 #elk jaar stijgt de prijs met 5%
    kostHuidig = usageCostTotal(oudverbruik) #♣initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
    kostNieuw = usageCostTotal(nieuwverbruik)
    onderhoud = 100 #jaarlijkse kost onderhoud
    cashflow[0] = -1*investering
    for i in range( 1,len(cashflow)):
        cashflow[i] = round(cashflow[i-1] + kostHuidig - kostNieuw - onderhoud,3)
        oudverbruik.update((key,value*developmentVerbruik) for key, value in oudverbruik.items())
        nieuwverbruik.update((key,value*developmentVerbruik) for key, value in nieuwverbruik.items())
        kostHuidig = kostHuidig*(1+developmentCost)
        kostNieuw = kostNieuw*(1+developmentCost)
#    print(cashflow)
    return cashflow
        

def payback_of_investment(investment, cashflows): #payback periode berekenen op basis van investering en cashflow per jaar
    print("###terugverdientijd berekenen###")
    """The payback period refers to the length of time required 
       for an investment to have its initial cost recovered.
       
       >>> payback_of_investment(200.0, [60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    total, years, cumulative = 0.0, 0, []
    if not cashflows or (sum(cashflows) < investment):
        raise Exception("insufficient cashflows")
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
    return A,months

def payback(cashflows): #functie om de payback periode op te roepen
    """The payback period refers to the length of time required
       for an investment to have its initial cost recovered.
       
       (This version accepts a list of cashflows)
       
       >>> payback([-200.0, 60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    investment, cashflows = cashflows[0], cashflows[1:]
    if investment < 0 : investment = -investment
    return payback_of_investment(investment, cashflows)


"""dictionary van huidig verbruiksprofiel maken"""

huidigProfiel = {}
huidigProfielRV = {}
huidigProfielSWW = {}
huidigProfielElec = {}

huidigeProfielen = [huidigProfielRV,huidigProfielSWW,huidigProfielElec]
huidigeVoorziening = [huidigeVoorzieningRV,huidigeVoorzieningSWW,huidigeVoorzieningElec]
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


huidigProfiel["ruimteverwarming"] = huidigProfielRV.get('voorziening').get('naam')
huidigProfiel["sanitair warm water"] = huidigProfielSWW.get('voorziening').get('naam')
huidigProfiel["electriciteit"] = huidigProfielElec.get('voorziening').get('naam')
huidigProfiel["totaal verbruik"] = {}
huidigProfiel["totale verbruikskost"] = {}
for i,j in huidigProfielRV.get("verbruikersverdeling").items():
    for k,l in huidigProfielSWW.get("verbruikersverdeling").items():
        for m,n in huidigProfielElec.get('verbruikersverdeling').items():
            if i == k == m:
                huidigProfiel['totaal verbruik'][i] = j+l+n #totaal verbruik per verbruiker (gas, stookolie, elec)
                huidigProfiel['totale verbruikskost'][i]= usageCostItem(i,j+l+n) #totaal kost per verbruiker (gas, stookolie, elec)
huidigProfiel["primaire energie"] = primaryEnergy(huidigProfiel.get("totaal verbruik"))             
huidigProfiel['CO2'] = huidigProfielRV.get('totaal CO2') + huidigProfielSWW.get('totaal CO2') + huidigProfielElec.get('totaal CO2')
                
       
        
"""Nieuwe voorzieningen bepalen & dimensioneren"""
"""dimensionering van de vraag"""
maxVraagRV = max(huidigProfielRV.get("verbruikProfiel"))/1000 #in kW
maxVraagSWW = max(huidigProfielSWW.get("verbruikProfiel"))/1000
#print(maxVraagSWW)
#print("max warmte",maxVraagRV)

"""nieuwe energievoorzieningen RUIMTEVERWARMING bepalen"""

#for i in range(len(list_voorzieningenRV)):
#    if list_voorzieningenRV[i] == warmtepomp_LW:
#        for j in range(len(list_voorzieningenRV[i])):
#            ratio = maxVraagRV/list_voorzieningenRV[i][j].get("maxVermogen")
#            if ratio >= 1 and ratio <= 1.2:
#                nieuwVoorzieningenRV.append(list_voorzieningenRV[i][j])
#            
#    if list_voorzieningenRV[i] == condensatieketels:
#        for j in range(len(list_voorzieningenRV[i])):
#            nieuwVermogen = list_voorzieningenRV[i][j].get("maxVermogen")
#            if nieuwVermogen == huidigeVoorzieningRV.get("maxVermogen"):
#                nieuwVoorzieningenRV.append(list_voorzieningenRV[i][j])
#dit aanvullen met alle soorten die we uiteindelijk aan hebben - GW, LW WW         
#print(nieuwVoorzieningenRV)

nieuwVoorzieningRV = heatPump_LW_4_6
nieuwVoorzieningSWW =  doorstroomboiler_5
nieuwVoorzieningElec = electriciteit_net
nieuweVoorzieningen = [nieuwVoorzieningRV,nieuwVoorzieningSWW,nieuwVoorzieningElec]

"""hier het nieuw profiel op basis van de nieuwe voorzieningen bepalen"""

""" dictionary van nieuw verbruiksprofiel maken"""


#door een lijst van verschillende scenarios lopen --> code hieronder. Nog een code vinden om de exacte voorzieningen uit de scenarios te halen
#overzichtVGL = []
#for i in range(len(scenarios)):
#    nieuwProfiel = {} 
#    nieuwProfielRV = scenarios[i].get('ruimteverwarming')
#    nieuwProfielSWW = scenarios[i].get('sanitair warm water')
#    nieuwProfielElec = scenarios[i].get('electriciteit')
#    nieuweProfielen = [nieuwProfielRV,nieuwProfielSWW,nieuwProfielElec]
#    
#    for i in range(len(nieuweProfielen)):
#        nieuweProfielen[i]["voorziening"] = nieuweVoorzieningen[i]
#        nieuweProfielen[i]["verbruikProfiel"] = newConsumption(huidigeProfielen[i].get("energievraag"),nieuweProfielen[i].get("voorziening"))
#        nieuweProfielen[i]["totaal verbruik"] = sum(nieuweProfielen[i].get("verbruikProfiel"))
#        nieuweProfielen[i]["verbruikersverdeling"] = verbruikersSom(nieuweProfielen[i].get("voorziening"),nieuweProfielen[i].get("totaal verbruik"))
#        nieuweProfielen[i]["besparing verbruik"] = verbruikvergelijking(huidigeProfielen[i].get("verbruikersverdeling"),nieuweProfielen[i].get("verbruikersverdeling"))
#        nieuweProfielen[i]["CO2"] = {}
#        for key, value in nieuweProfielen[i].get("verbruikersverdeling").items():
#            nieuweProfielen[i]["CO2"][key] = emissions(key,value)
#        nieuweProfielen[i]["totaal CO2"] = sum(nieuweProfielen[i].get("CO2").values())
#        nieuweProfielen[i]["Besparing CO2"] = round(huidigeProfielen[i].get("totaal CO2") - nieuweProfielen[i].get("totaal CO2"),3)
#
#    nieuwProfiel["Ruimteverwarming"] = nieuwProfielRV.get('voorziening').get('naam')
#    nieuwProfiel["Sanitair warm water"] = nieuwProfielSWW.get('voorziening').get('naam')
#    nieuwProfiel["Electriciteit"] = nieuwProfielElec.get('voorziening').get('naam')
#    nieuwProfiel["totaal verbruik"] = {}
#    nieuwProfiel["totale verbruikskost"] = {}
#    for i,j in nieuwProfielRV.get("verbruikersverdeling").items():
#        for k,l in nieuwProfielSWW.get("verbruikersverdeling").items():
#            for m,n in nieuwProfielElec.get('verbruikersverdeling').items():
#                if i == k == m:
#                    nieuwProfiel['totaal verbruik'][i] = j+l+n
#                    nieuwProfiel['totale verbruikskost'][i]= usageCostItem(i,j+l+n)
#    if PV == True:  #opbrengst van PV aftrekken van totaal verbruik electriciteit
#        newConsumptionPV(nieuwProfiel.get('totaal verbruik').get('electriciteit'),PV_opbrengst)
#        PV_cost = 0
#    nieuwProfiel["primaire energie"] = primaryEnergy(nieuwProfiel.get("totaal verbruik"))                
#    if huidigProfielRV.get('voorziening') != nieuwProfielRV.get('voorziening'):  #checken of huidige voorziening gelijk is aan de nieuwe, als dit zo is is er geen nieuw installatie --> dus ook geen investering. dit herhaalt voor elke toepassing, kan in een for loop geschreven worden
#        nieuwProfiel['investering RV'] = nieuwProfielRV.get('voorziening').get('prijs')
#    else:
#        nieuwProfiel['investering RV'] = 0
#    if huidigProfielSWW.get('voorziening') != nieuwProfielSWW.get('voorziening'):
#        nieuwProfiel['investering SWW'] = nieuwProfielSWW.get('voorziening').get('prijs')
#    else:
#        nieuwProfiel['investering SWW'] = 0
#    if huidigProfielElec.get('voorziening') != nieuwProfielElec.get('voorziening'):
#        nieuwProfiel['investering Elec'] = nieuwProfielElec.get('voorziening').get('prijs')
#    else:
#        nieuwProfiel['investering Elec'] = 0
#    nieuwProfiel['totale investering'] = nieuwProfiel.get('investering RV') + nieuwProfiel.get('investering SWW') + nieuwProfiel.get('investering Elec') + PV_cost  #som van de investeringen voor elke toepassing
#    nieuwProfiel['CO2'] = nieuwProfielRV.get('totaal CO2') + nieuwProfielSWW.get('totaal CO2') + nieuwProfielElec.get('totaal CO2')
#    """vergelijking huidig profiel en nieuw profiel""" #probeersel om de vergelijking duidelijker te maken, de vollegie dict van huidig en nieuw profiel vgl met elkaar ipv dit ook op te splitsen in RV, SWW en elec 
#    vergelijking = {}
#    vergelijking["besparing verbruik"] = verbruikvergelijking(huidigProfiel.get('totaal verbruik'),nieuwProfiel.get('totaal verbruik'))
#    vergelijking["besparing primaire energie"] = (round(1-(nieuwProfiel.get("primaire energie")/huidigProfiel.get("primaire energie")),3))*100
#    vergelijking["kostbesparing"] =verbruikvergelijking(huidigProfiel.get('totale verbruikskost'),nieuwProfiel.get('totale verbruikskost'))
#    vergelijking["CO2 besparing"] = round(huidigProfiel.get('CO2') - nieuwProfiel.get('CO2'),3)
#    
#    overzichtVGL.append({"scenario":scenarios[i].get("scenario"),"nieuw profiel":nieuwProfiel,"vergelijking":vergelijking})

    
    
nieuwProfiel = {}   
nieuwProfielRV = {} 
nieuwProfielSWW = {} 
nieuwProfielElec = {}
nieuweProfielen = [nieuwProfielRV,nieuwProfielSWW,nieuwProfielElec]

for i in range(len(nieuweProfielen)):
    nieuweProfielen[i]["voorziening"] = nieuweVoorzieningen[i]
    nieuweProfielen[i]["verbruikProfiel"] = newConsumption(huidigeProfielen[i].get("energievraag"),nieuweProfielen[i].get("voorziening"))
    nieuweProfielen[i]["totaal verbruik"] = sum(nieuweProfielen[i].get("verbruikProfiel"))
    nieuweProfielen[i]["verbruikersverdeling"] = verbruikersSom(nieuweProfielen[i].get("voorziening"),nieuweProfielen[i].get("totaal verbruik"))
    nieuweProfielen[i]["besparing verbruik"] = verbruikvergelijking(huidigeProfielen[i].get("verbruikersverdeling"),nieuweProfielen[i].get("verbruikersverdeling"))
    nieuweProfielen[i]["CO2"] = {}
    for key, value in nieuweProfielen[i].get("verbruikersverdeling").items():
        nieuweProfielen[i]["CO2"][key] = emissions(key,value)
    nieuweProfielen[i]["totaal CO2"] = sum(nieuweProfielen[i].get("CO2").values())
    nieuweProfielen[i]["Besparing CO2"] = round(huidigeProfielen[i].get("totaal CO2") - nieuweProfielen[i].get("totaal CO2"),3)

nieuwProfiel["Ruimteverwarming"] = nieuwProfielRV.get('voorziening').get('naam')
nieuwProfiel["Sanitair warm water"] = nieuwProfielSWW.get('voorziening').get('naam')
nieuwProfiel["Electriciteit"] = nieuwProfielElec.get('voorziening').get('naam')
nieuwProfiel["totaal verbruik"] = {}
nieuwProfiel["totale verbruikskost"] = {}
for i,j in nieuwProfielRV.get("verbruikersverdeling").items():
    for k,l in nieuwProfielSWW.get("verbruikersverdeling").items():
        for m,n in nieuwProfielElec.get('verbruikersverdeling').items():
            if i == k == m:
                nieuwProfiel['totaal verbruik'][i] = j+l+n
                nieuwProfiel['totale verbruikskost'][i]= usageCostItem(i,j+l+n)
if PV == True:  #opbrengst van PV aftrekken van totaal verbruik electriciteit
    newConsumptionPV(nieuwProfiel.get('totaal verbruik').get('electriciteit'),PV_opbrengst)
    PV_cost = 0

nieuwProfiel["primaire energie"] = primaryEnergy(nieuwProfiel.get("totaal verbruik"))                
if huidigProfielRV.get('voorziening') != nieuwProfielRV.get('voorziening'):  #checken of huidige voorziening gelijk is aan de nieuwe, als dit zo is is er geen nieuw installatie --> dus ook geen investering. dit herhaalt voor elke toepassing, kan in een for loop geschreven worden
    nieuwProfiel['investering RV'] = nieuwProfielRV.get('voorziening').get('prijs')
else:
    nieuwProfiel['investering RV'] = 0
if huidigProfielSWW.get('voorziening') != nieuwProfielSWW.get('voorziening'):
    nieuwProfiel['investering SWW'] = nieuwProfielSWW.get('voorziening').get('prijs')
else:
    nieuwProfiel['investering SWW'] = 0
if huidigProfielElec.get('voorziening') != nieuwProfielElec.get('voorziening'):
    nieuwProfiel['investering Elec'] = nieuwProfielElec.get('voorziening').get('prijs')
else:
    nieuwProfiel['investering Elec'] = 0
    
nieuwProfiel['totale investering'] = nieuwProfiel.get('investering RV') + nieuwProfiel.get('investering SWW') + nieuwProfiel.get('investering Elec') + PV_cost  #som van de investeringen voor elke toepassing
    
nieuwProfiel['CO2'] = nieuwProfielRV.get('totaal CO2') + nieuwProfielSWW.get('totaal CO2') + nieuwProfielElec.get('totaal CO2')

print("##########################################")

print(huidigProfiel)
print("##########################################")
print(nieuwProfiel)
print("##########################################")
        


"""vergelijking huidig profiel en nieuw profiel""" #probeersel om de vergelijking duidelijker te maken, de vollegie dict van huidig en nieuw profiel vgl met elkaar ipv dit ook op te splitsen in RV, SWW en elec 
vergelijking = {}
vergelijking["besparing verbruik"] = verbruikvergelijking(huidigProfiel.get('totaal verbruik'),nieuwProfiel.get('totaal verbruik'))
vergelijking["besparing primaire energie"] = (round(1-(nieuwProfiel.get("primaire energie")/huidigProfiel.get("primaire energie")),3))*100
vergelijking["kostbesparing"] =verbruikvergelijking(huidigProfiel.get('totale verbruikskost'),nieuwProfiel.get('totale verbruikskost'))
vergelijking["CO2 besparing"] = round(huidigProfiel.get('CO2') - nieuwProfiel.get('CO2'),3)
print(vergelijking)

"""plotting"""
y1 = huidigProfielRV.get("verbruikProfiel")
y2 = nieuwProfielRV.get("verbruikProfiel")
x = pointCount #aantal punten in de timevalue list want printen met de timevalues gaat niet 

plt.plot(x,y1)
plt.plot(x,y2, color = 'red')
plt.show()