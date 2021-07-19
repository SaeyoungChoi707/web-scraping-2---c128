import enum
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("/Users/sudhe/OneDrive/Pictures/CODING!!/Python/Projects/c127,128,129 projects")
browser.get(start_url)
time.sleep(10)
headers = ["name","distance","mass","radius"]
planet_data = []
new_planet_data = []

def scrape():
    for i in range(1,430):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentPageNum = int(soup.find_all("input",attrs={"class":"page_num"})[0].get("value"))
            if currentPageNum<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentPageNum>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for td_tag in soup.find_all("td",attrs={"class","exoplanet"}):
            tr_tags = td_tag.find_all("tr")
            templist = []
            for index,tr_tag in enumerate(tr_tags):
                if index == 0:
                    templist.append(tr_tags.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(tr_tag.contents[0])
                    except:
                        templist.append("")
                        hyperlink_trtag = tr_tags[0]
            templist.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_trtag.find_all("a,href=True")[0]["href"])
            planet_data.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i}page done 1")

def scrapeMoreData(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        templist = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    templist.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
            new_planet_data.append(templist)
    except:
        time.sleep(1)
        scrapeMoreData(hyperlink)

scrape()

for index,data in enumerate (planet_data):
    scrapeMoreData(data[5])
    print(f"{index+1}page done 2")
final_planet_data = [] 
for index,data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n","")for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)

    with open ("scrapper2.csv","w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)