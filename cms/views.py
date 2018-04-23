from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from .models import Pages
from .models import Updates
from xml.sax import make_parser
from .xmlparserbarrapunto import myContentHandler
from .xmlparserbarrapunto import getRss

FORMULARIO = """
    <form action= "/" Method= "POST">
    URL:<br>
    <input type="text" name="name" placeholder= "name"><br>
    <input type="text" name="page" placeholder= "page"><br>
    <input type="submit" value="Enviar">
</form>
"""

def barra(request):
    lista = Pages.objects.all()
    respuesta = "<ul>"
    for pagina in lista:
        respuesta += '<li><a href= "/pages/' + str(pagina.id) + '">' + pagina.name + "</a>"
    respuesta += "</ul>" + FORMULARIO 
    return HttpResponse (respuesta)

def update(request):
    Updates.objects.all().delete()
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse("http://barrapunto.com/index.rss")
    barrapunto = Updates(name = 'Barrapunto', links = getRss())
    barrapunto.save()
    return HttpResponse ("La tabla ha sido actualizada con el contenido de barrapunto")

@csrf_exempt
def pages (request, numero):
    if request.method == "POST":
        print (request.POST['name'], request.POST['page'])
        page = Pages(name = request.POST['name'], page = request.POST['page'])
        page.save()

    try:
        page = Pages.objects.get(id=str(numero))
    except Pages.DoesNotExist:
        return HttpResponseNotFound('<h1>' + numero + ' not found</h1>')

    return HttpResponse(page.name + " " + str(page.page) + "</br><ul>"+ str(Updates.objects.get(name='Barrapunto').links) +"</ul>")
