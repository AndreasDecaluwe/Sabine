
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:33:23 2022

@author: Andreas
"""

"""imports"""

import pandas as pd
import os
print(os.getcwd())
"""inputs systeem"""  #♦op dit moment handmatig enkele waarden ingegeven, al deze waarden zouden voor een volledig jaar (per kwartier) ingelezen moeten worden van een excell 
path = os.getcwd()
pathcsv = os.path.join(path, "overzichtSLPs.csv")
print(pathcsv)
data = pd.read_csv(os.path.join(path, "overzichtSLPs.csv"))


data.head()
#print(data)
timeValues = data.iloc[:,0]
SLPe = data.iloc[:,6]
SLPg = data.iloc[:,8]
COP = data.iloc[:,9]
elecEff = data.iloc[:,10]
PV_opbrengst = data.iloc[:,11].tolist()
#print(PV_opbrengst)

#print(timeValues)
#print(len(timeValues))
#print(SLPe)
#print(SLPg)
PV = False 




"""lijst voorzieningen"""
toepassingen = ["Ruimteverwarming", "Sanitair Warm Water","Elektriciteit"]
list_voorzieningen = []
heatPump_LW_3_3 = {"naam":"Lucht-water Warmtepomp","Toepassing":"Ruimteverwarming","verbruiker": "elektriciteit","efficientie":4.8,"maxVermogen":3.3,"prijs":5289}
heatPump_LW_4_6 = {"naam":"Lucht-water Warmtepomp","Toepassing":"Ruimteverwarming","verbruiker": "elektriciteit","efficientie":4,"maxVermogen":4.6,"prijs":6370}
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
scenario1 = [{"ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler","electriciteit":"het net"}]
scenario2 = [{"ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler","electriciteit":"het net met PV"}]
scenario3 = [{"ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler elektrisch","electriciteit":"het net"}]
scenario4 = [{"ruimteverwarming":"warmtepomp","sanitair warm water":"doorstroomboiler gas","electriciteit":"het net"}]

"""vraagprofielen definieren"""
#het onderscheid maken tussen de profielen voor ruimteverwarming, sanitair ww en electriciteit
min_gas = min(SLPg)
#print(min_gas)
SLPsww =[min_gas]*len(timeValues)
#print(SLPsww)
SLPrv = [round(SLPg[i]-SLPsww[i],5) for i in range(len(timeValues))]

profielen = [SLPrv, SLPsww, SLPe]
#print(SLPrv)



"""INPUTS VAN DE GEBRUIKER"""
"""voorzieningen"""  #dit moet een input worden van de gebruiker
huidigeVoorzieningSWW = cvKetel_gas_25
huidigeVoorzieningRV = cvKetel_gas_25
huidigeVoorzieningElec = electriciteit_net

"""huidige energieverbruik"""
Jaarverbruik_stookolie = 0 #kWh
Jaarverbruik_gas = 20000 #kWh
Jaarverbruik_elec = 3500 #kWh



"""INPUTS VAN DE GEBRUIKER VERWERKEN"""
"""huidig verbruik verdelen over verbruikprofiel -> verbruikprofiel genereren"""
def verbruikProfiel(voorziening, profiel):  #functie vermenigvuldigt elk verbruik per kwartier met de overeenkomstige percentage van het totaal jaarverbruik 
    if voorziening.get("verbruiker") =="elektriciteit":
            jaarverbruik = Jaarverbruik_elec
            verbruikersVraag = [round(i*jaarverbruik,3) for i in profiel]        
    elif voorziening.get("verbruiker") =="aardgas":
            jaarverbruik = Jaarverbruik_gas
            verbruikersVraag = [round(i*jaarverbruik,3) for i in profiel]           
    elif voorziening.get("verbruiker") =="stookolie":
            jaarverbruik = Jaarverbruik_stookolie
            verbruikersVraag = [round(i*jaarverbruik,3) for i in profiel]
#    print(verbruikersVraag)
    return verbruikersVraag


def verbruikersSom(voorziening, som): #functie verdeelt het verbruik over alle gedefinieerde verbruikers, maakt het vergelijken voor besparingen achteraf gemakkelijker
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


def emissions(verbruiker, verbruik):  #returns kg co2/kwh
    if verbruiker == "elektriciteit":
            co2 = round(verbruik * co2_elec,3)
    elif verbruiker == "aardgas":
            co2 = round(verbruik * co2_gas,3)
    elif verbruiker == "stookolie":
            co2 = round(verbruik * co2_stookolie,3)
#    print(co2)
    return co2

#uitstoot = []
#for i in range (len(voorzieningen)):   #gaat door de lijst van huidige voorzieningen, moet uiteindelijke helemaal onderaan komen eigenlijk
#    uitstoot.append(emissions(voorzieningen[i],verbruik[i]))

"""energievraag bepalen"""

def energieVraag(huidigeVoorziening,huidigVraagProfiel):
    if type (huidigeVoorziening.get("efficientie")) == list: #if functie is nodig om te bepalen of de efficientie tijdsafhankelijke is of niet, tijdsafhankelijk staat in een list, niet-afhankelijk is gwn een integer
        vraag = [a*b for a,b in zip(huidigVraagProfiel, huidigeVoorziening.get("efficientie") )]
    else:
        vraag = [i*huidigeVoorziening.get("efficientie") for i in huidigVraagProfiel]
    return vraag

"""nieuw verbruik bepalen"""

def newConsumption(vraagprofiel,nieuweVoorziening):   #op basis van de energievraag en een nieuwe efficientie het nieuwe verbruik berekenen
    if type (nieuweVoorziening.get("efficientie")) == list:  #voorbeeld een variable COP staat in een tijdafhankelijke lijst geschreven, elk verbruik
        newCons = [round(a/b,3) for a,b in zip(vraagprofiel,nieuweVoorziening.get("efficientie"))]
    else:  #als we een constante COP gebruiken
        newCons = [round(i/nieuweVoorziening.get("efficientie"),3) for i in vraagprofiel]
    return newCons

def newConsumptionPV(verbruikprofiel, PV_opbrengst):
    newCons = [None]*len(verbruikprofiel)
    for i in range(len(verbruikprofiel)):
        newCons[i] = (round(verbruikprofiel[i] - PV_opbrengst[i],3)) 
    return newCons

def verbruikvergelijking(dict1, dict2):
    besparingsdict= {"aardgas":0.0,"stookolie":0.0,"elektriciteit":0.0}
    besparingsdict['aardgas'] = round(dict1.get("aardgas") - dict2.get("aardgas"),3)
    besparingsdict['elektriciteit'] = round(dict1.get("elektriciteit") - dict2.get("elektriciteit"),3)
    besparingsdict['stookolie'] = round(dict1.get("stookolie") - dict2.get("stookolie"),3)
    return besparingsdict
  
"""FINANCIEEL"""

#https://code.activestate.com/recipes/576686-npv-irr-payback-analysis/

costElec = 0.5 #€/kWh
costAardgas = 0.4 #€/kWh
costStookolie = 0.3 #€/kWh

def usageCostYear(voorziening, verbruik):  #returns verbruikskost per jaar
    verbruiker = voorziening.get('verbruiker')
    cost = 0
    if verbruiker == "elektriciteit":
            cost = verbruik * costElec
    elif verbruiker == "aardgas":
            cost = verbruik * costAardgas
    elif verbruiker == "stookolie":
            cost = verbruik * costStookolie
    return cost

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

def usageCostItem(key,value):
    cost = 0
    if key == "elektriciteit":
        cost += round(value * costElec,2)
    elif key == "aardgas":
        cost += round(value * costAardgas,2)
    elif key == "stookolie":
        cost += round(value * costStookolie,2)
    return cost


def cashflows(oudverbruik, nieuwverbruik,investering):
    print("###berekening cashflows###")
    periode = 10 #jaar
    cashflow = [None]*periode
    developmentVerbruik = 0.03
    developmentCost = 0.05
    kostHuidig = usageCostTotal(oudverbruik)
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
        

def payback_of_investment(investment, cashflows):
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

def payback(cashflows):
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
huidigProfielSWW = {}
huidigProfielRV = {}
huidigProfielElec = {}


huidigProfielRV["voorziening"]= huidigeVoorzieningRV
huidigProfielRV["verbruikProfiel"] = verbruikProfiel(huidigeVoorzieningRV,SLPrv)
huidigProfielRV["totaal verbruik"] = sum(huidigProfielRV.get("verbruikProfiel"))
huidigProfielRV["verbruikersverdeling"] = verbruikersSom(huidigProfielRV.get("voorziening"),huidigProfielRV.get("totaal verbruik"))
huidigProfielRV["CO2"] = {}
for key, value in huidigProfielRV.get("verbruikersverdeling").items():
    huidigProfielRV["CO2"][key] = emissions(key,value)
#huidigProfielRV["CO2"] = CO2
huidigProfielRV["totaal CO2"] = sum(huidigProfielRV.get("CO2").values())
huidigProfielRV["energievraag"] = energieVraag(huidigProfielRV.get("voorziening"),huidigProfielRV.get("verbruikProfiel"))

huidigProfielSWW["voorziening"]= huidigeVoorzieningSWW
huidigProfielSWW["verbruikProfiel"] = verbruikProfiel(huidigeVoorzieningSWW,SLPsww)
huidigProfielSWW["totaal verbruik"] = sum(huidigProfielSWW.get("verbruikProfiel"))
huidigProfielSWW["verbruikersverdeling"] = verbruikersSom(huidigProfielSWW.get("voorziening"),huidigProfielSWW.get("totaal verbruik"))
huidigProfielSWW["CO2"] = {}
for key, value in huidigProfielSWW.get("verbruikersverdeling").items():
    huidigProfielSWW["CO2"][key] = emissions(key,value)
huidigProfielSWW["totaal CO2"] = sum(huidigProfielSWW.get("CO2").values())
huidigProfielSWW["energievraag"] = energieVraag(huidigProfielSWW.get("voorziening"),huidigProfielSWW.get("verbruikProfiel"))
huidigProfielElec["voorziening"]= huidigeVoorzieningElec
huidigProfielElec["verbruikProfiel"] = verbruikProfiel(huidigeVoorzieningElec,SLPe)
huidigProfielElec["totaal verbruik"] = sum(huidigProfielElec.get("verbruikProfiel"))
huidigProfielElec["verbruikersverdeling"] = verbruikersSom(huidigProfielElec.get("voorziening"),huidigProfielElec.get("totaal verbruik"))
huidigProfielElec["CO2"] = {}
for key, value in huidigProfielElec.get("verbruikersverdeling").items():
    huidigProfielElec["CO2"][key] = emissions(key,value)
huidigProfielElec["totaal CO2"] = sum(huidigProfielElec.get("CO2").values())
huidigProfielElec["energievraag"] = energieVraag(huidigProfielElec.get("voorziening"),huidigProfielElec.get("verbruikProfiel"))



huidigProfiel["Sanitair warm water"] = huidigProfielSWW
huidigProfiel["Ruimteverwarming"] = huidigProfielRV
huidigProfiel["Electriciteit"] = huidigProfielElec
huidigProfiel["totaal verbruik"] = {}
huidigProfiel["totale verbruikskost"] = {}
for i,j in huidigProfielRV.get("verbruikersverdeling").items():
    for k,l in huidigProfielSWW.get("verbruikersverdeling").items():
        for m,n in huidigProfielElec.get('verbruikersverdeling').items():
            if i == k == m:
                huidigProfiel['totaal verbruik'][i] = round(j+l+n,3)
                huidigProfiel['totale verbruikskost'][i]= usageCostItem(i,j+l+n)        
huidigProfiel['CO2'] = huidigProfielRV.get('totaal CO2') + huidigProfielSWW.get('totaal CO2') + huidigProfielElec.get('totaal CO2')
                
#print("")
#print("############################################################")                
#print(huidigProfiel)
#print("###################################")        
        
"""Nieuwe voorzieningen bepalen & dimensioneren"""
"""dimensionering van de vraag"""
maxVraagRV = max(huidigProfielRV.get("verbruikProfiel"))/1000 #in kW
maxVraagSWW = max(huidigProfielSWW.get("verbruikProfiel"))/1000
#print(maxVraagSWW)
#print("max warmte",maxVraagRV)







"""nieuwe energievoorzieningen RUIMTEVERWARMING bepalen"""
nieuwVoorzieningenRV = [heatPump_LW_4_6]
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
  


nieuwVoorzieningenSWW =  [doorstroomboiler_5]


nieuwVoorzieningenElec = [electriciteit_net]







""" dictionary van nieuw verbruiksprofiel maken"""
nieuwProfiel = {}   
nieuwProfielRV = {}
nieuwProfielSWW = {}
nieuwProfielElec = {}


""" vergelijking tussen huidig en nieuw profiel"""
#print("")
#print("HUIDIG PROFIEL RUIMTEVERWARMING")
#print("")
#
#print(huidigProfielRV)
#
#print("")
#print("NIEUW PROFIEL RUIMTEVERWARMING")
#print("")

for i in range((len(nieuwVoorzieningenRV))):
    nieuwProfielRV["voorziening"]= nieuwVoorzieningenRV[i]
    nieuwProfielRV["verbruikProfiel"] = newConsumption(huidigProfielRV.get("energievraag"),nieuwProfielRV.get("voorziening"))
    nieuwProfielRV["totaal verbruik"] = sum(nieuwProfielRV.get("verbruikProfiel"))
    nieuwProfielRV["verbruikersverdeling"] = verbruikersSom(nieuwProfielRV.get("voorziening"),nieuwProfielRV.get("totaal verbruik"))
    nieuwProfielRV["besparing verbruik"] = verbruikvergelijking(huidigProfielRV.get("verbruikersverdeling"),nieuwProfielRV.get("verbruikersverdeling"))
    nieuwProfielRV["CO2"] = {}
    for key, value in nieuwProfielRV.get("verbruikersverdeling").items():
        nieuwProfielRV["CO2"][key] = emissions(key,value)
    nieuwProfielRV["totaal CO2"] = sum(nieuwProfielRV.get("CO2").values())
    nieuwProfielRV["Besparing CO2"] = round(huidigProfielRV.get("totaal CO2") - nieuwProfielRV.get("totaal CO2"),3)
#    print("----------------------------------------")
#    print(nieuwProfielRV)

#print("")
#print("HUIDIG PROFIEL SANITAIR WARM WATER")
#print("")
#
#print(huidigProfielSWW)
#
#print("")
#print("NIEUW PROFIEL SANITAIR WARM WATER")
#print("")
for i in range((len(nieuwVoorzieningenSWW))):
    nieuwProfielSWW["voorziening"]= nieuwVoorzieningenSWW[i]
    nieuwProfielSWW["verbruikProfiel"] = newConsumption(huidigProfielSWW.get("energievraag"),nieuwProfielSWW.get("voorziening"))
    nieuwProfielSWW["totaal verbruik"] = round(sum(nieuwProfielSWW.get("verbruikProfiel")),3)
    nieuwProfielSWW["verbruikersverdeling"] = verbruikersSom(nieuwProfielSWW.get("voorziening"),nieuwProfielSWW.get("totaal verbruik"))
    nieuwProfielSWW["besparing verbruik"] = verbruikvergelijking(huidigProfielSWW.get("verbruikersverdeling"),nieuwProfielSWW.get("verbruikersverdeling"))
    nieuwProfielSWW["CO2"] = {}
    for key, value in nieuwProfielSWW.get("verbruikersverdeling").items():
        nieuwProfielSWW["CO2"][key] = emissions(key,value)
    nieuwProfielSWW["totaal CO2"] = sum(nieuwProfielSWW.get("CO2").values())
    nieuwProfielSWW["Besparing CO2"] = round(huidigProfielSWW.get("totaal CO2") - nieuwProfielSWW.get("totaal CO2"),3)

#    print("----------------------------------------")
#    print(nieuwProfielSWW)

#print("")
#print("HUIDIG PROFIEL ELEKTRICITEIT")
#print("")
#
#print(huidigProfielElec)
#
#print("")
#print("NIEUW PROFIEL ELEKTRICITEIT")
#print("")
for i in range((len(nieuwVoorzieningenElec))):
    nieuwProfielElec["voorziening"]= nieuwVoorzieningenElec[i]
    if PV == False:
        nieuwProfielElec["verbruikProfiel"] = newConsumption(huidigProfielElec.get("energievraag"),nieuwProfielElec.get("voorziening")) #[round(a+b+c,3) for a,b,c in zip(huidigProfielElec.get('verbruikProfiel'),nieuwProfielRV.get('verbruikProfiel'),nieuwProfielSWW.get('verbruikProfiel'))]#newConsumption(huidigProfielElec.get("energievraag"),nieuwProfielElec.get("voorziening"))
    else:
        verProf = newConsumption(huidigProfielElec.get("energievraag"),nieuwProfielElec.get("voorziening"))
        nieuwProfielElec["verbruikProfiel"] = newConsumptionPV(verProf,PV_opbrengst)
    nieuwProfielElec["totaal verbruik"] = round(sum(nieuwProfielElec.get("verbruikProfiel")),3)
    nieuwProfielElec["verbruikersverdeling"] = verbruikersSom(nieuwProfielElec.get("voorziening"),nieuwProfielElec.get("totaal verbruik"))
    
        
    nieuwProfielElec["besparing verbruik"] = verbruikvergelijking(huidigProfielElec.get("verbruikersverdeling"),nieuwProfielElec.get("verbruikersverdeling"))
    nieuwProfielElec["CO2"] = {}
    for key, value in nieuwProfielElec.get("verbruikersverdeling").items():
        nieuwProfielElec["CO2"][key] = emissions(key,value)
    nieuwProfielElec["totaal CO2"] = sum(nieuwProfielElec.get("CO2").values())
    nieuwProfielElec["Besparing CO2"] = round(huidigProfielElec.get("totaal CO2") - nieuwProfielElec.get("totaal CO2"),3)

#    print("----------------------------------------")
#    print(nieuwProfielElec)


"""NIEUW PROFIEL IN EEN DICTIONARY GIETEN"""

nieuwProfiel["Ruimteverwarming"] = nieuwProfielRV
nieuwProfiel["Sanitair warm water"] = nieuwProfielSWW
nieuwProfiel["Electriciteit"] = nieuwProfielElec
nieuwProfiel["totaal verbruik"] = {}
nieuwProfiel["totale verbruikskost"] = {}
for i,j in nieuwProfielRV.get("verbruikersverdeling").items():
    for k,l in nieuwProfielSWW.get("verbruikersverdeling").items():
        for m,n in nieuwProfielElec.get('verbruikersverdeling').items():
            if i == k == m:
                nieuwProfiel['totaal verbruik'][i] = round(j+l+n,3)
                nieuwProfiel['totale verbruikskost'][i]= usageCostItem(i,j+l+n)
            
if huidigProfielRV.get('voorziening') != nieuwProfielRV.get('voorziening'):
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
    
nieuwProfiel['totale investering'] = nieuwProfiel.get('investering RV') + nieuwProfiel.get('investering SWW') + nieuwProfiel.get('investering Elec')  
    
#for i,j in nieuwProfielRV.get("CO2").items():
#    for k,l in nieuwProfielSWW.get("CO2").items():
#        for m,n in nieuwProfielElec.get('CO2').items():
#            if i == k == m:
#                nieuwProfiel['CO2'] = j+l+n
nieuwProfiel['CO2'] = nieuwProfielRV.get('totaal CO2') + nieuwProfielSWW.get('totaal CO2') + nieuwProfielElec.get('totaal CO2')
#print("###########################################################")
#print(nieuwProfiel)
         
#cashflow = cashflows(huidigProfiel.get('totaal verbruik'),nieuwProfiel.get('totaal verbruik'),nieuwProfiel.get('totale investering'))
#payback(cashflow)
#print("test")
#print(nieuwProfiel)
"""vergelijking huidig profiel en nieuw profiel"""
#vergelijking = {}
#vergelijking["verbruiksbesparing RV"] = 
#vergelijking["verbruiksbesparing SWW"] = 
#vergelijking["verbruiksbesparing Elec"] = 
#vergelijking["kostbesparing"]
#vergelijking["CO2 besparing"]

print("##########################################")
#print(huidigProfiel)

"""WEERGAVE"""
print("huidige situatie voor energievoorziening is als volgt:")
print("Voorziening voor ruimteverwarming:",huidigProfiel.get('Ruimteverwarming').get('voorziening').get('naam'))
print("Voorziening voor sanitair warm water:",huidigProfiel.get('Sanitair warm water').get('voorziening').get('naam'))
print("Voorziening voor elektriciteit:",huidigProfiel.get('Electriciteit').get('voorziening').get('naam'))
print("het verbruikprofiel per jaar ziet er uit als volgt")
for key,value in huidigProfiel.get('totaal verbruik').items():
    print(key,":",value,"kWh")
print("dit vertaalt zich in de volgende verbruikskost per jaar")
for key, value in huidigProfiel.get('totale verbruikskost').items():
    print(key,":",value,"€")


print("De CO2 uitstoot voor deze situatie bedraagt:",huidigProfiel.get('CO2'),"kg")
print("-------------------------------------------------------")
print("een mogelijke nieuwe situatie voor energievoorziening is als volgt:")
print("Voorziening voor ruimteverwarming:",nieuwProfiel.get('Ruimteverwarming').get('voorziening').get('naam'))
print("Voorziening voor sanitair warm water:",nieuwProfiel.get('Sanitair warm water').get('voorziening').get('naam'))
print("Voorziening voor elektriciteit:",nieuwProfiel.get('Electriciteit').get('voorziening').get('naam'))
print("het verbruikprofiel per jaar ziet er uit als volgt")
for key, value in nieuwProfiel.get('totaal verbruik').items():
    print(key,":",value,"kWh")
print("dit vertaalt zich in de volgende verbruikskost per jaar")
for key, value in nieuwProfiel.get('totale verbruikskost').items():
    print(key,":",value,"€")
cashflow = cashflows(huidigProfiel.get('totaal verbruik'),nieuwProfiel.get('totaal verbruik'),nieuwProfiel.get('totale investering'))  #deze moet hier staan, als deze hoger in de code staat dan flipt er iets
paybackPeriod = payback(cashflow)
print("de terugverdientijd voor deze investering is:",paybackPeriod[0],"jaar en",paybackPeriod[1],"maanden")
print("De CO2 uitstoot voor deze situatie bedraagt:",nieuwProfiel.get('CO2'),"kg")



