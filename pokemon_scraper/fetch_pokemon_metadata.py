# coding=utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
import os.path
import base64
import json

def load_rendered_site_from_cache(url):
	print('1')
	filename = 'rendered_html_doc'
	print('2')
	if os.path.isfile(filename):
		with open(filename, 'r') as file:
			return file.read().replace('\n', '')

def write_rendered_site_to_cache(url, source):
	filename = 'rendered_html_doc'
	with open(filename, 'w') as file:
		file.write(str(source.encode('utf-8')))

def get_parsed_rendered_site(url):
	site = load_rendered_site_from_cache(url) #check if fully rendered page already downloaded
	if site:
		return BeautifulSoup(site, 'html.parser') #parse if already exists
	else:
		driver = webdriver.Chrome('./pokemon_scraper/chromedriver') #selenium webdriver automates web interaction, must have chrome installed
		driver.get(url) #run website and render content
		write_rendered_site_to_cache(url, driver.page_source)
		return BeautifulSoup(driver.page_source, 'html.parser') #take rendered HTML doc and parse with beautiful soup

def parse_pokemon_data(pokemon_data):
	pokedex_number = int(pokemon_data[0].find('b').getText()) #isolate pokedex value
	img_url = pokemon_data[1].find('img')['src'].replace('//','') #within image tag, find src attribute and isolate image url
	name = pokemon_data[2].find('a').getText()
	average_stats = pokemon_data[9].getText()
	parsed_pokemon_data = {
		'pokedex_number': pokedex_number,
		'name': name,
		'img_url': img_url,
		'avg_stats': average_stats 
	}
	return pokedex_number, parsed_pokemon_data






def fetch_metadata():
	url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_I)"
	pokemon_list_page = get_parsed_rendered_site(url)
	generation_1_pokemon_list= pokemon_list_page.find('span', id='List_of_Pok.C3.A9mon_by_base_stats').find_next('table').find_all('tr')[1:]
	pokemon_metadata={}
	for pokemon in generation_1_pokemon_list: #for row in table
		pokemon_data= pokemon.find_all('td') #get columns
		k,v= parse_pokemon_data(pokemon_data) #isolate values as key, value pairs
		pokemon_metadata[k] = v #save as dict values
	return pokemon_metadata

