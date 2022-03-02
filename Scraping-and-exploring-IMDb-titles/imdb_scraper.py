from bs4 import BeautifulSoup
import datetime
import requests
import csv


def scrape_shows() -> list:
    """Scrape show data from imdb. Data is collected with two iterations.
    Afterwards all data is merged into a single list, which is returned."""

    url = "https://www.imdb.com/chart/toptv/"

    source = requests.get(url).text

    soup = BeautifulSoup(source, "lxml")

    table = soup.find("div", class_="lister")

    # In this iteration, imdb rating and total users rated are gathered
    # [ [rating, users_rated], ... ]
    ratings = []
    for show in table.find_all("td", class_="ratingColumn imdbRating"):
        rating = show.text.replace("\n", "")
        
        _users_rated = str(show.strong).split("based on ")[1]
        users_rated = _users_rated.split(" user ratings")[0]

        ratings.append([rating, users_rated])


    # i is for connecting the previous list to the upcoming one. It's incremented manually
    i = 0
    # shows list will contain everything, and will be directly written to a .csv
    shows = []
    for show in table.find_all("td", class_="titleColumn"):
        title, *_year = show.text.replace("\n", "").split("(")
        
        title = title.split(".")[1].strip()
        
        year = _year[0].split(")")[0]
        
        _href, _actors = str(show.a).split('" title="')
        href = "https://www.imdb.com" + _href.lstrip('<a href="')
        
        show_id = href.lstrip("https://www.imdb.com/title/").rstrip("/")
        
        actors = _actors.split('">')[0]
       
        shows.append([show_id, "Show", title, "-", actors, ratings[i][0], ratings[i][1], year, href])
        i += 1

    return shows


def scrape_movies() -> list:
    """Scrape movie data from imdb. Data is collected with two iterations.
    Afterwards all data is merged into a single list, which is returned."""

    url = "https://www.imdb.com/chart/top/"

    source = requests.get(url).text

    soup = BeautifulSoup(source, "lxml")

    table = soup.find("div", class_="lister")

    # In this iteration, imdb rating and total users rated are gathered
    # [ [rating, users_rated], ... ]
    ratings = []
    for show in table.find_all("td", class_="ratingColumn imdbRating"):
        rating = show.text.replace("\n", "")
        
        _users_rated = str(show.strong).split("based on ")[1]
        users_rated = _users_rated.split(" user ratings")[0]

        ratings.append([rating, users_rated])


    # i is for connecting the previous list to the upcoming one. It's incremented manually
    i = 0
    # movies list will contain everything, and will be directly written to a .csv
    movies = []
    for movie in table.find_all("td", class_="titleColumn"):
        title, *_year = movie.text.replace("\n", "").split("(")
        
        title = title.split(".")[1].strip()
        
        year = _year[0].split(")")[0]
       
        _href, _actors = str(movie.a).split('" title="')
        href = "https://www.imdb.com" + _href.lstrip('<a href="')
        
        movie_id = href.lstrip("https://www.imdb.com/title/").rstrip("/")
        
        _actors = _actors.split('">')[0]
        director, actors = _actors.split("(dir.), ")
       
        movies.append([movie_id, "Movie", title, director, actors, ratings[i][0], ratings[i][1], year, href])
        i += 1

    return movies


csv_file = "imdb-titles.csv"

movies, shows = scrape_movies(), scrape_shows()


# Create a .csv with some data and the headers
with open(csv_file, "w", encoding="utf-8") as fp:
    fp.write(f"Data scraped on {datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')}\n\n")
    fp.write("id|category|title|director|actors|rating|users_rated|year|url\n")


# Write the data collecte to the csv
with open(csv_file, "a", encoding="utf-8") as fp:
    csv_writer = csv.writer(fp, delimiter="|")
    for movie in movies:
        csv_writer.writerow(movie)
    for show in shows:
        csv_writer.writerow(show)
