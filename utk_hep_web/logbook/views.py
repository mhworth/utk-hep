from django.http import HttpResponse 
from django.template import RequestContext 
from django.template.loader import get_template
from django.conf import settings
import itertools

from physics_web.logbook.models import *

def context_processor(request):
    return {'MEDIA_URL':settings.MEDIA_URL}

def plot_collection(request,user,path):
    
    template = get_template('logbook/plot_collection.html')
    variables = RequestContext(request,{})
    
    # Find the associated user
    results = User.objects.filter(username=user)
    if len(results) != 1:
        error_message = "User %s not found" % (user,)
        variables['error'] = True
        variables['error_message'] = error_message
        output = template.render(variables)
        return HttpResponse(output)
    
    user = results[0]
    
    # First, try to find the plot collection referenced by the path
    elements = filter(lambda x: x!="",path.split("/"))
    
    # The first element is the first category, the last element is the PC
    root = Category.objects.filter(name=elements[0],parent=None,user = user)
    if len(root) != 1:
        error_message = "Root-level category called %s not found" % (elements[0],)
        variables['error'] = True
        variables['error_message'] = error_message
        output = template.render(variables)
        return HttpResponse(output)
    
    current = root
    for level in xrange(1,len(elements)-2):
        results = Category.objects.filter(name=elements[level],parent = current)
        if not len(results) == 1:
            error_message = "Level %d category named %s not found" %(level,elements[level])
            variables['error'] = True
            variables['error_message'] = error_message
            output = template.render(variables)
            return HttpResponse(output)
        current = results[0]
    
    # Now we can get the PC
    results = PlotCollection.objects.filter(category = current,name=elements[-1])
    if not len(results) == 1:
        error_message = "Plot collection named %s not found in category %s" %(elements[-1],elements[-2])
        variables['error'] = True
        variables['error_message'] = error_message
        output = template.render(variables)
        return HttpResponse(output)
    
    # We have our PC!
    pc = results[0]
    
    # Now get its associated plots
    plots = Plot.objects.filter(collection=pc)
    
    # And it's associated root plot files
    rpfs = RootPlotFile.objects.filter(collection=pc)
    
    template = get_template('logbook/plot_collection.html')
    variables['plot_collection'] = pc
    variables['root_files'] = rpfs
    variables['plots'] = plots
    variables['title'] = pc.name
    
    output = template.render(variables)
    return HttpResponse(output)
    
def categories(request,user,path):
    ""
    path = filter(lambda x: x!='',path.split("/"))
    template = get_template('logbook/categories.html')
    username = request.user.username
    
    print path
    if len(path) > 0:
        # The first element is definitely a category with no parent
        results = Category.objects.filter(name=path[0],parent=None)
        if len(results) < 1:
            error_message = "Category named %s wasn't found!" % path[0]
            variables = RequestContext(request,{
                                 'error':True, 
                                 'error_message': error_message,
                                 })
            
            output = template.render(variables)
            return HttpResponse(output)
        if len(results) >1:
            error_message = "Category named %s was found more than once in the root.  This shouldn't happen, tell Matt about this" % path[0]
            variables = RequestContext(request,{
                                 'error':True, 
                                 'error_message': error_message,
                                 })
            
            output = template.render(variables)
            return HttpResponse(output)
        
        category = results [0]
        categories = Category.objects.filter(parent=category)
        collections = PlotCollection.objects.filter(category = category)
        title = "Category: " + str(category)
    else:
        categories = Category.objects.filter(parent=None)
        collections = PlotCollection.objects.filter(category = None)
        title = "Category: Default"
    
    
    nodes = itertools.chain(collections, categories)
    variables = RequestContext(request,{
                         'categories':categories,
                         'collections':collections,
                         'nodes':nodes,
                         'title':title,
                         'base': settings.BASE_URL + "logbook/",
                         })
    
    output = template.render(variables)
    return HttpResponse(output)

def main_page(request):
    ""
    template = get_template('logbook/main_page.html')
    variables = RequestContext(request,{
                         'MEDIA_URL' : settings.MEDIA_URL,
                         
                         })
    output = template.render(variables)
    return HttpResponse(output)


    