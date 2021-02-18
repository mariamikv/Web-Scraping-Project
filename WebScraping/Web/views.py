from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# i am using https://losangeles.craigslist.org site to practice on web scraping
BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    # getting the webpage, creating a response object
    response = requests.get(final_url)
    # extracting the source code of the page
    data = response.text
    # passing the source code to beautifull soup to create a beautifulsoup object for it.
    soup = BeautifulSoup(data, features='html.parser')
    # extracting all the <a> thags whose class name is 'result-title' into a list
    post_listings = soup.find_all('li', {'class':'result-row'})

    final_postings=[]
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        # if post dont have img we use post_image_url which is default image container
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://itsnotaboutthenumbers.files.wordpress.com/2010/11/logo.gif'

        final_postings.append((post_title, post_url, post_price, post_image_url))
    
    front = {
        'search':search,
        'final_postings':final_postings,
    }
    return render(request, 'Web/new_search.html', front)