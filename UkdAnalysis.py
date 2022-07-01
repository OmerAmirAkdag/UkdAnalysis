#   Title: UkdAnalysis
#   Author: OmerAmirAkdag
#   
# -*- coding:utf-8 -*-
from collections import Counter
from lib2to3.pgen2 import driver
from re import I
from unicodedata import name
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re

# Printing our results
def print_results(result_opponents,tournament_count,match_count,opponents_dictionary,name,surname,galibiyet,maglubiyet,beraberlik,ukd,cities_dict,result_cities):
    print((name.upper()+" "+surname.upper()+ "\nUKD: {}".format(ukd)))
    print("*"*50)
    print("Oynanan turnuva sayısı: {}".format(tournament_count))
    print("Oynanan mac sayısı: {}".format(match_count))
    print("Toplam galibiyet sayısı: {}".format(galibiyet))
    print("Toplam maglubiyet sayısı: {}".format(maglubiyet))
    print("Toplam beraberlik sayısı: {}".format(beraberlik))
    puan = galibiyet*1 + beraberlik*0.5 
    kazanma_orani = puan/match_count*100
    print("Kazanma Yüzdesi: %{:.2f}".format(kazanma_orani))
    print("-"*50)
    print("En çok oynanan rakipler:\n ")
    for i in range(len(result_opponents)):
        print(result_opponents[i][0]," Maç sayısı: ",result_opponents[i][1]," Skor: ",opponents_dictionary[result_opponents[i][0]],"-",result_opponents[i][1]-opponents_dictionary[result_opponents[i][0]])
    print("-"*50)
    print("En çok oynanan şehirler:\n ")
    for i in range(len(result_cities)):
        degisim = cities_dict[result_cities[i][0]]
        print(result_cities[i][0]," Turnuva Sayısı: ",result_cities[i][1]," UKD Değişimi: ","{:.2f}".format(degisim))
    
#FIXED BUG: There is upper "i" as "İ" in Turkish therefore we need to make some adjustments
def upper_i(name):
    if "i" in name:
        name = name.replace("i","İ")
    name = name.upper()
    return name
# Kullandığımız değişkenler
opponents_before_formatting = []
opponents = []
turnuvalar = []
index = 1
person = None
no_id = "Lisans TCK Eksik"
no_id_count = 0
no_ukd = 0
score = 0
opponents_scores = []
total_win = 0
total_draw = 0
total_loss = 0


#Requesting inputs from the user
surname = input("Aradığınız kişinin soyadını giriniz: ")
name = input("Aradığınız kişinin ismini giriniz: ")

PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),executable_path=PATH,options=chrome_options)
chrome_options.add_argument("--headless")
Url = "https://ukd.tsf.org.tr/ukdsorgulama.php"
driver.get(Url)
search = driver.find_element(By.NAME, "soyad")
search.send_keys(surname)

button = driver.find_elements(By.CLASS_NAME, "button2")[1]
button.click() 


#finding the table we want on the page then extracting people from the table
table = driver.find_elements(By.XPATH,"//table")[10]
people_on_search = table.find_elements(By.TAG_NAME, "tr")
#EDGE CASE: There is some people who does not have UKD therefore it is messing up with the button index we need to exclude them
find_ukd = table.find_elements(By.TAG_NAME, "td")
ukd_list = []
for index in range(1,len(people_on_search)):
    finder = (index*11)+5-no_ukd
    ukd = find_ukd[finder].text
    if people_on_search[index].text.find(no_id) != -1 :
        no_id_count += 1
    elif ukd=="":
        no_ukd += 1
    elif(people_on_search[index].text.find(upper_i(name)) != -1):
        person = people_on_search[index]
        ayrinti = person.find_elements(By.XPATH, "//td/form/input[@type='submit']")[index-no_id_count-no_ukd-1]
        break

ayrinti.click()
#Clicking <Tüm Turnuva Raporları> button
tum_turnuva_button = driver.find_element(By.XPATH, "//td/form/input[@value='Tüm Turnuva Raporları']")
tum_turnuva_button.click()

turnuvalar_table = driver.find_elements(By.XPATH, "//tr/td/table")
tournament_count = (len(turnuvalar_table)/2)-4
tournament_count = int(tournament_count)
tournament_traits = []
#There is table inside of the table and we only want the insider table
for i in range(8,len(turnuvalar_table)):
    if i % 2 == 1:
        turnuvalar.append(turnuvalar_table[i].text)
    if i % 2 == 0:
        tournament_traits.append(turnuvalar_table[i].text.split("\n"))
cities = []

cities_dict = {}
tour_name_city = []
rating_change = []
for i in range(len(tournament_traits)):
    tournament_traits[i][0] = tournament_traits[i][0].replace(" ", "")
    tournament_traits[i][1] = tournament_traits[i][1].replace("Toplam UKD Değişimi ", "")
    tour_name_city.append( tournament_traits[i][0].split("/"))
    cities.append(tour_name_city[i][2])
    rating_change.append(float(tournament_traits[i][1]))
unique_cities = set(cities)
cities_dict = dict.fromkeys(unique_cities,0)
for i in range(len(cities)):
    if cities[i] in unique_cities:
        cities_dict[cities[i]] += rating_change[i]
    
    

#Formatting to get surname and name from the initial table adding the results of the match with the opponent as strings
for j in range(len(turnuvalar)):
    turnuva  = turnuvalar[j]
    turnuva = turnuva.replace("Soyad Ad TC Kimlik UKD Round Sonuç UKD Değişim\n","")
    turnuvalar[j] = turnuva
    opponents_before_formatting.append(turnuva.split("\n"))
    for k in range(len(opponents_before_formatting[j])):
        if("1.0" in opponents_before_formatting[j][k]):
            total_win += 1
            opponents_before_formatting[j][k] = (re.sub('[0-9.-]',"" , opponents_before_formatting[j][k]))
            opponents_before_formatting[j][k] = (opponents_before_formatting[j][k].strip()).upper()
            opponents_scores.append(opponents_before_formatting[j][k] + " 1.0")
        elif("0.0" in opponents_before_formatting[j][k]):
            total_loss += 1
            opponents_before_formatting[j][k] = (re.sub('[0-9.-]',"" , opponents_before_formatting[j][k]))
            opponents_before_formatting[j][k] = (opponents_before_formatting[j][k].strip()).upper()
            opponents_scores.append(opponents_before_formatting[j][k] + " 0.0")
        else:
            total_draw += 1
            opponents_before_formatting[j][k] = (re.sub('[0-9.-]',"" , opponents_before_formatting[j][k]))
            opponents_before_formatting[j][k] = (opponents_before_formatting[j][k].strip()).upper()
            opponents_scores.append(opponents_before_formatting[j][k] + " 0.5")

#Making a set of opponents and making a dictionary of opponents with the results
for i in range(len(opponents_before_formatting)):
    for j in range(len(opponents_before_formatting[i])):
        opponents.append(opponents_before_formatting[i][j])     
set_of_opponents = set(opponents)
opponents_dictionary = dict.fromkeys(set_of_opponents,0)

for i in range(len(opponents_scores)):
    if("1.0" in opponents_scores[i]):
        if opponents[i] in opponents_scores[i]:
            opponents_dictionary[opponents[i]] += 1
            
    elif("0.5" in opponents_scores[i]):
        if opponents[i] in opponents_scores[i]:
            opponents_dictionary[opponents[i]] += 0.5




match_count = len(opponents)
counts_opponents = Counter(opponents)
result_opponents = counts_opponents.most_common(20)

counts_cities = Counter(cities)
result_cities = counts_cities.most_common(10)

print_results(result_opponents,tournament_count,match_count,opponents_dictionary,name,surname,total_win,total_loss,total_draw,ukd,cities_dict,result_cities)
driver.close()









