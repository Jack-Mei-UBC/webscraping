import requests as requests
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger
import os, glob


def pullSheets(urlpage):
    print(urlpage)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    # run phantomJS webdriver from executable path of your choice

    # get web page
    driver.get(urlpage)
    pageContainer = driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div/section/main/div/div[3]/div/div/*")
    # print(pageContainer)
    pianoSheet = []
    for page in pageContainer:
        driver.execute_script("arguments[0].scrollIntoView();", page)
        time.sleep(0.2)
        pianoSheet.append(
            driver.find_element(by=By.XPATH, value='//img[contains(@alt,"arranged by")]').get_attribute("src"))
    pianoSheet = list(dict.fromkeys(pianoSheet))
    print(pianoSheet)
    merger = PdfFileMerger()
    for index, sheet in enumerate(pianoSheet):
        with open("sheet" + str(index) + ".svg", "wb") as file:
            file.write(requests.get(sheet).content)
        drawing = svg2rlg("sheet" + str(index) + ".svg")
        renderPDF.drawToFile(drawing, "sheet" + str(index) + ".pdf")
        merger.append("sheet" + str(index) + ".pdf")
    merger.write("result.pdf")
    merger.close()
    for filename in glob.glob("./sheet*"):
        os.remove(filename)

    driver.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pullSheets("User input Website")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
