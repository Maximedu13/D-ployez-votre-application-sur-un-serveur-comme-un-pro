# coding: utf-8
"""update the database with CRON ! """
import sys
sys.path.append('/mnt/c/Users/maxim/OneDrive/Documents/D-ployez-votre-application-sur-un-serveur-comme-un-pro/NUTELLA')
import json
import requests
import django
import os
from sentry_sdk import capture_message
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nutella_stop.settings")
django.setup()
sys.path.append('/mnt/c/Users/maxim/OneDrive/Documents/D-ployez-votre-application-sur-un-serveur-comme-un-pro/NUTELLA/catalog')
from catalog.models import Product, Favorite, User
sys.path.append('/mnt/c/Users/maxim/OneDrive/Documents/D-ployez-votre-application-sur-un-serveur-comme-un-pro/NUTELLA/catalog/management')
from update_time import return_date_of_update

class Commands():
    """ commands to update the db """
    def __init__(self):
        self.categories = ['Sauces au roquefort', 'Œufs', 'Beurres', 'Muffins au chocolat', \
        'Bœuf', 'Beurres de cacahuètes', 'Pâtes à tartiner au chocolat']

    def get_favorites_before_the_update(self):
        """we need to recup the favorites before the update"""
        all_favorites = Favorite.objects.all()
        map = []
        for all in all_favorites:
            maps = []
            name_of_the_favorite_product = Product.objects.filter(id=all.product_id)
            this_user = User.objects.filter(id=all.user_id)
            for user in this_user:
                maps.append(user.username)
            for name in name_of_the_favorite_product:
                maps.append(name.name)
                maps.append(name.url_off)
                map.append(maps)
        return map

    def root_update(self):
        """the main method to update products"""
        for category in self.categories:
            r = requests.get\
            ("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0= \
            categories&tag_contains_0=contains&tag_0=" + category + \
            "&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y= \
            products_n&action=display&json=1")
            result = json.loads(r.text)
            for i in range(len(result["products"])):
                try:
                    name = result["products"][i]["product_name_fr"] or result["products"][i]["product_name"]
                except KeyError:
                    pass
                try:
                    description = result["products"][i]["generic_name"]
                except KeyError:
                    description = ""
                try:
                    nutriscore = result["products"][i]["nutrition_grade_fr"].upper() or result["products"][i]["nutrition_grades"]
                except KeyError:
                    nutriscore = ""
                try:
                    stores = result["products"][i]["stores"]
                except KeyError:
                    stores = ""
                try:
                    image = result["products"][i]["image_small_url"] or result["products"][i]["image_front_small_url"]
                except KeyError:
                    image = ""
                try:
                    brand = result["products"][i]["brands"]
                except KeyError:
                    brand = ""
                try:
                    calories = float(result["products"][i]["nutriments"]["energy_100g"])
                    # Kilojoules(kJ) to calories(cal)
                    calories /= 4.184
                    calories = calories.__round__(2)
                except KeyError:
                    pass
                try:
                    lipids = result["products"][i]["nutriments"]["fat_100g"]
                except KeyError:
                    pass
                try:
                    sugars = result["products"][i]["nutriments"]["sugars_100g"]
                except KeyError:
                    pass
                try:
                    proteins = result["products"][i]["nutriments"]["proteins_100g"]
                except KeyError:
                    pass
                try:
                    salts = result["products"][i]["nutriments"]["salt_100g"]
                except KeyError:
                    pass
                url_off = result["products"][i]["url"]
                affected_category = self.categories.index(category) + 1
                if Product.objects.filter(url_off=url_off):
                    # if an equivalent is found, we update the line
                    Product.objects.filter(url_off=url_off).update(name=name, description=description,
                                                                   nutriscore=nutriscore, stores=stores,
                                                                   image=image, brand=brand, calories=calories,
                                                                   lipids=lipids, sugars=sugars,
                                                                   proteins=proteins,
                                                                   salts=salts, category_id=affected_category)
                else:
                    # else, we create the object
                    Product.objects.create(name=name, description=description,
                                           nutriscore=nutriscore, stores=stores,
                                           image=image, brand=brand, calories=calories,
                                           lipids=lipids, sugars=sugars,
                                           proteins=proteins,
                                           salts=salts, url_off=url_off, category_id=affected_category)

    def update_with_favorites(self):
        """a method which regroups the main methods to update db"""
        favorites_before = self.get_favorites_before_the_update()
        self.root_update()
        for i in range(0, len(favorites_before)):
            try:
                y = Product.objects.filter(url_off=favorites_before[i][2])
                for yid in y:
                    yid = yid.id
                    Favorite.objects.filter(product_id=yid).update(product_id=yid)
            except:
                Favorite.objects.filter(product_id=yid).delete()
        capture_message("----Mise à jour de la base de données effectuée----", return_date_of_update())
        print("----Mise à jour de la base de données effectuée----", return_date_of_update())

if __name__ == "__main__":
    C = Commands()
    C.update_with_favorites()
