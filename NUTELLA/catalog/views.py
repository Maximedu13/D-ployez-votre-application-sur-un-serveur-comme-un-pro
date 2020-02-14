"""views.py app catalog"""
# Create your views here.
from os import listdir
from os.path import isfile, join
import json
import socket
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.shortcuts import redirect
from django.template.defaulttags import register
from .models import Product, Favorite
from .database import insert, results
from sentry_sdk import capture_message
from .management.update_database import Commands
# pylint: disable=no-member

@register.filter
def get_range(value):
    """range method"""
    return range(1, value)

def catalog(request):
    """catalog"""
    return redirect('index')

def notices(request):
    """notices page"""
    template = loader.get_template('catalog/notices.html')
    files = sorted([f for f in listdir('catalog/static/catalog/img') if \
    isfile(join('catalog/static/catalog/img', f))])
    content_picture = [
        "Emoticone triste par \
        <a href='https://www.flaticon.com/free-icon/crying_136366#term=cry&page=1&position=13' \
        target='_blank'>Flaticon</a>",
        "Colette par <a href='http://personnages-disney.com/Page%20Colette.html' \
        target='_blank'>personnages-disney</a>",
        "Logo de carotte par <a href='https://www.flaticon.com/free-icon/ \
        carrot_1041355#term=carrot&page=1&position=22' target='_blank'>Flaticon</a>",
        "Colette par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/ \
        pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'> Pur Beurre - \
        Charte Graphique </a>", "Logo de Pur Beurre par \
        <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/ \
        pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'>\
        Pur Beurre - Charte Graphique </a>", "Logo de déconnexion par \
        <a href='https://www.flaticon.com/free-icon/logout_1828490#term=logout&page=1&position=28' \
        target='_blank'>Flaticon</a>", "Favicon logo Pur Beurre par \
        <a href='https://www.favicon-generator.org/'>favicon-generator</a>",
        "Fond d‘écran de la bannière par \
        <a href='https://unsplash.com/photos/eqsEZNCm4-c' target='_blank'> Olenka Kotyk</a>",
        "Rémy par <a href='https://company-82435.frontify.com/d/6Yy9WFJdtp8j/ \
        pur-beurre-style-guide#/introduction/Notre-identité' target='_blank'> \
        Pur Beurre - Charte Graphique </a>", "Logo d‘utilisateur par \
        <a href='https://www.flaticon.com/free-icon/carrot_1041355#term=carrot&page=1&position=22' \
        target='_blank'>Flaticon</a>"
    ]
    d = {x:y for x, y in zip(files, content_picture)}
    context = {
        'd' : d
    }
    return HttpResponse(template.render(context, request=request))

def index(request):
    """index page"""
    template = loader.get_template('catalog/index.html')
    insert()
    try:
        capture_message("Un utilisateur visite la page d'accueil, voici son adresse IP : " + socket.gethostbyname(socket.gethostname()))
    except:
        capture_message("Un utilisateur visite la page d'accueil")
    return HttpResponse(template.render(request=request))
    #get_favorites_before_the_update()
    #get_all_products_in_api()
    #C = Commands()
    #C.update_with_favorites()
    #get_the_new_product_id_from_old_url_off()
    return HttpResponse(template.render(request=request))

def autocomplete(request):
    """autocomplete ajax"""
    if request.is_ajax():
        query_autocomplete = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=query_autocomplete).order_by('id')[:10]
        results = []
        global data
        for p in products:
            product_dict = {}
            product_dict = p.name
            results.append(product_dict)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, 'application/json')

def substitute(request):
    """substitute page"""
    template = loader.get_template('catalog/substitute.html')
    global query_two
    query_two = None
    if request.GET.get('query_two') is not None:
        query_two = request.GET.get('query_two')
    query_two_infos = Product.objects.filter(name=query_two)
    global q_2
    for q_2 in query_two_infos:
        pass
    try:
        if q_2 is not None:
            subs = Product.objects.filter(category_id=q_2.category_id,
                                          nutriscore="A").order_by('id')
            if not subs:
                subs = Product.objects.filter(category_id=q_2.category_id,
                                              nutriscore="B").order_by('id')
            if not subs:
                subs = Product.objects.filter(category_id=q_2.category_id,
                                              nutriscore="C").order_by('id')
    except:
        messages.error(request, 'Ceci n‘est pas un produit. Veuillez réessayer')
        return redirect('index')
    global substitutes
    substitutes = {
        'query_two' : query_two,
        'q_2' : q_2,
        'subs' : subs,
    }
    return HttpResponse(template.render(substitutes, request=request))

def favorite(request, id):
    """favorite add"""
    messages.success(request, 'Le produit a été ajouté à vos favoris.')
    current_user = request.user
    Favorite.objects.get_or_create(user_id=current_user.id, product_id=id)
    return redirect('index')

def search(request):
    """search page"""
    template = loader.get_template('catalog/search.html')
    if request.GET.get('query_one') is not None:
        global query_one
        query_one = request.GET.get('query_one')
    query_one_infos = Product.objects.filter(name__contains=query_one).order_by('id')
    message = "{}".format(query_one)
    global msg
    msg = {
        'message' : message,
        'query_one_infos' : query_one_infos,
    }
    capture_message("Une nouvelle recherche utilisateur a été effectuée. La voici : " + query_one)
    return HttpResponse(template.render(msg, request=request))

def product(request, product_id):
    """product page"""
    template = loader.get_template('catalog/product.html')
    results(product_id)
    message = results(product_id)
    return HttpResponse(template.render(message, request=request))
