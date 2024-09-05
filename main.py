import requests
from bs4 import BeautifulSoup

def ScrapeSite():
    URL = "https://www.bbcgoodfood.com/recipes/slow-cooker-spaghetti-bolognese"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    ReturnIngredients(soup)

def ReturnIngredients(soup):
    results = soup.find(class_="recipe__ingredients")

    title = results.find("h2", class_="section-heading-1")
    print(title.text.strip())

    job_elements = results.find_all("li", class_="list-item")
    for job_element in job_elements:
        print(job_element.text.strip())
        print()
        
    ReturnMethod(soup)

def ReturnMethod(soup):
    results = soup.find(class_="js-piano-recipe-method")

    title = results.find("h3", class_="section-heading-1")
    print(title.text.strip())

    job_elements = results.find_all("li", class_="list-item")
    for job_element in job_elements:
        title_elements = job_element.find("span", class_="heading-6")
        body_element = job_element.find("div", class_="editor-content")
        print(title_elements.text.strip())
        print(body_element.text.strip())
        print()

ScrapeSite()