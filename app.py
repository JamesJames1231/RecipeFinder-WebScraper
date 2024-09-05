import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

def ScrapeSite(content):
    URL = "https://www.bbcgoodfood.com/recipes/" + content
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

@app.route("/")
def home():
    return render_template("index.html", arr="", len=0)


@app.route("/search", methods=['GET'])
def FindingMeal():

    meal = request.form['search']

    URL = "https://www.bbcgoodfood.com/search?q=" + meal
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(class_="search-results")
    meal_results = results.find_all("article", class_="card")

    arr = []

    for meal_element in meal_results:

        ##Title of the meal
        title_element = meal_element.find("div", class_="card__content")
        final_title_element = title_element.find("h2", class_="heading-4")


        ##Cook time
        time_element = meal_element.find("li", class_="pr-md")
        final_time_element = time_element.find("span", class_="terms-icons-list__text")

        combined = final_title_element.text.strip() +  " " + final_time_element.text.strip()
        arr.append(combined)

    return render_template('index.html', arr=arr, len=len(arr))


    ##ScrapeSite("slow-cooker-spaghetti-bolognese")