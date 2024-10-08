import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", arr="", len=0)


@app.route("/scrape", methods=['POST'])
def ScrapeSite():
    
    content = request.form['chosen']

    checkQuery = f"SELECT * FROM saved WHERE addr = '{content}';"
    check = DataQuery(checkQuery, "select-one")

    saved = "yes"
    if check == None:
        saved = "no"

    url = content
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    ingArr = []
    methodArr = []

    ingredients = ReturnIngredients(soup)
    methods = ReturnMethod(soup)

    for job_element in ingredients:
        ingArr.append(job_element.text.strip())
    
    for job_element in methods:
        methodArr.append(job_element.find("div", class_="editor-content").text.strip())

    image_container = soup.find(class_="post-header__container")
    image = image_container.find("img", class_="image__img").attrs['src']

    title = soup.find("h1", class_="heading-1").text.strip()

    return render_template('recipe.html', saved=saved, url=url, image=image, title=title, ingArr=ingArr, methodArr=methodArr, ingLen=len(ingArr), methLen=len(methodArr))


def ReturnIngredients(soup):
    results = soup.find(class_="recipe__ingredients")
    job_elements = results.find_all("li", class_="list-item")
    return job_elements


def ReturnMethod(soup):
    results = soup.find(class_="js-piano-recipe-method")
    job_elements = results.find_all("li", class_="list-item")
    return job_elements


@app.route("/search", methods=['POST'])
def FindingMeal():

    meal = request.form['meal']

    URL = "https://www.bbcgoodfood.com/search?q=" + meal
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(class_="search-results")
    meal_results = results.find_all("article", class_="card")

    arr = []
    imageArr = []
    timeArr = []
    linkArr = []

    for meal_element in meal_results:

        ##Title of the meal
        title_element = meal_element.find("div", class_="card__content")
        final_title_element = title_element.find("h2", class_="heading-4").text.strip()
        arr.append(final_title_element)


        ##Cook time
        time_element = meal_element.find("li", class_="pr-md")
        final_time_element = time_element.find("span", class_="terms-icons-list__text").text.strip()
        timeArr.append(final_time_element)

        ##Image
        image_element = meal_element.find("img", class_="image__img")
        final_image = image_element.attrs['src']
        imageArr.append(final_image)

        ##Link to recipe
        link_element = meal_element.find("a", class_="link")
        final_link = link_element.attrs['href']
        linkArr.append(final_link)

    return render_template('index.html', arr=arr, len=len(arr), imageArr=imageArr, timeArr=timeArr, linkArr=linkArr)

def DataQuery(query, type):
    con = sqlite3.connect("food.db")
    cur = con.cursor()
    
    if type == "create" or type == "insert" or type == "delete":
        cur.execute(query)
        con.commit()
        con.close()
        return cur
    
    elif type == "select-one":
        response = cur.execute(query)
        finalRes = response.fetchone()
        con.commit()
        con.close()
        print(finalRes)
        return finalRes

    elif type == "select-all":
        response = cur.execute(query)
        finalRes = response.fetchall()
        con.commit()
        con.close()
        return finalRes

    return cur          


@app.route("/SaveMeal", methods=['POST'])
def SaveMeal():
    try:
        mealName = request.form['savemeal']
        mealLink = request.form['address']
        print(mealLink, mealName)
    except Exception as err:
        print(err + "one")

    try:
        con = sqlite3.connect("food.db")
        cur = con.cursor()

        checkQuery = f"SELECT * FROM saved WHERE addr = '{mealLink}';"
        check = DataQuery(checkQuery, "select-one")
        if check == None:
            query = """INSERT INTO saved (name, addr) VALUES (?, ?)"""
            query_values = (mealName, mealLink)
            cur.execute(query, query_values)

            con.commit()
            cur.close()

            return SavedMeals()
        
        else: 
            return "Already Exists"

    except sqlite3.Error as error:
        print(error)
        return "erro"
   
        
@app.route("/RemoveMeals", methods=["POST"])
def RemoveMeals():
    mealLink = request.form['address']
    query = f"DELETE FROM saved WHERE addr = '{mealLink}'"
    DataQuery(query, "delete")
    return SavedMeals()
        
@app.route("/SavedMeals", methods=["POST"])
def SavedMeals():
    query = "SELECT * FROM saved"
    response = DataQuery(query, "select-all")
    return render_template('saved.html', response=response, len=len(response))