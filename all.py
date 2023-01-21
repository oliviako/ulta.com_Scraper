import requests
from bs4 import BeautifulSoup
import csv

def get_all_info(brand_name):
  webpage = 'https://www.ulta.com/brand/' + brand_name
  brand = requests.get(webpage)
  brand_content = brand.content
  soup = BeautifulSoup(brand_content, 'html.parser')
  
  href = soup.find(class_='shop-brand-btn')
    
  if href:
    large_link = href.a['href']
    large_brand = 'https://ulta.com' + large_link + '&No=0&Nrpp=960'
    large_brand_link = requests.get(large_brand)
    lb_content = large_brand_link.content
    soup = BeautifulSoup(lb_content, 'html.parser')
  
  product_info = soup.find_all(class_='product')
  names = []
  for each_name in product_info:
    name = each_name.find('img')
    names.append(name['alt'])

  links = []
  for each_link in product_info:
    link = each_link['href']
    links.append('https://www.ulta.com' + link)

  ingredient_list = []
  for link in links:
    product = requests.get(link)
    product_content = product.content
    product_soup = BeautifulSoup(product_content, 'html.parser')
    ingredients = product_soup.find_all(attrs={'aria-controls' : 'Ingredients'})
    if not ingredients:
      ingredient_list.append(" No Ingredients Listed")
    else:
      for ingredient in ingredients:
        ingredient_list.append(ingredient.p)
        
  with open("ulta.csv", "w") as ulta:
    writer = csv.writer(ulta)
    for x in range(len(ingredient_list)):
      writer.writerow([names[x], links[x], ingredient_list[x]])

get_all_info(insert brand here)
