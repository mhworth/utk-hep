from django.contrib import admin
from physics_web.logbook.models import Plot,PlotCollection, Category

class PlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection')
    

class PlotCollectionAdmin(admin.ModelAdmin):
    list_display = ('name','category')
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Plot, PlotAdmin)
admin.site.register(PlotCollection, PlotCollectionAdmin)
admin.site.register(Category, CategoryAdmin)