'''Scraper.py

This is my web scraping program, which makes use of my caching system (Cache.py). Using a webdriver (for chrome), I am able to open the
web page below, parse through all of the data after clearing through the advertisements, save a rendered html doc of all info, and then isolate what
info I need from that. The caching system will look in the Pokemon Images folder, see if the the image already exisrs (from previous ganeplay) and won't download it again
if it does. This means the user can empty the folder whenever they want to free up space on their computer,
and it prevents duplicate copies from being made as pokemon are randomly rechosen.

All data is then formatted in a dictionary that is called in Pokemon.py
'''

# coding=utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import os.path
import base64
import json
import Cache

def getParsedRenderedSite(url):
	site = Cache.loadRenderedSiteFromCache() #check if fully rendered page already downloaded
	if site:
		return BeautifulSoup(site, 'html.parser') #parse if already exists
	else:
		driver = webdriver.Chrome('./pokemon_scraper/chromedriver') #selenium webdriver automates web interaction, must have chrome installed
		driver.get(url) #run website and render content
		Cache.writeRenderedSiteToCache(driver.page_source)
		return BeautifulSoup(driver.page_source, 'html.parser') #take rendered HTML doc and parse with beautiful soup

def parsePokemonData(pokemon_data):
	pokedex_number = int(pokemon_data[0].find('b').getText()) #isolate pokedex value
	img_url = pokemon_data[1].find('img')['src'].replace('//','') #within image tag, find src attribute and isolate image url
	name = pokemon_data[2].find('a').getText()
	average_stats = float(pokemon_data[9].getText().replace('\n', '').replace('\\n', ''))
	#create a dictionary of all data scraped from web
	parsed_pokemon_data = {
		'pokedex_number': pokedex_number,
		'name': name,
		'img_url': img_url,
		'avg_stats': average_stats 
	}
	return pokedex_number, parsed_pokemon_data


def fetchMetadata():
	#formats all chached/ scraped data for easy use in game programming
	url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_I)"
	pokemon_list_page = getParsedRenderedSite(url)
	generation_1_pokemon_list= pokemon_list_page.find('span', id='List_of_Pok.C3.A9mon_by_base_stats').find_next('table').find_all('tr')[1:]
	pokemon_metadata={}
	for pokemon in generation_1_pokemon_list: #for row in table
		pokemon_data= pokemon.find_all('td') #get columns
		k,v= parsePokemonData(pokemon_data) #isolate values as key, value pairs
		pokemon_metadata[k] = v #save as dict values
	return pokemon_metadata

