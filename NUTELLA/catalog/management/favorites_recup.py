""" manage the favorites products from users """
#from NUTELLA.catalog.models import Favorite, Product, User
from catalog.models import Favorite, Product, User

def get_favorites_before_the_update():
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
    print(map)

def get_favorites_after_the_update():
    """the same method, but we will call it after the update"""
    get_favorites_before_the_update()

if __name__ == "__main__":
    get_favorites_before_the_update()
