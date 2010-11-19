import tagging
import os
import ROOT
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from urlparse import urlparse


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    user = models.ForeignKey(User,null=False)
    
    def get_parent(self):
        return self.parent
    
    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.get_parent()
            p_list.append(p)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    def _parents_repr(self):
        p_list = self._recurse_for_parents(self)
        
        return self.get_separator().join(p_list)
    _parents_repr.short_description = "Category parents"

    # TODO: Does anybody know a better solution???
    def _pre_save(self):
        p_list = self._recurse_for_parents(self)
        names = [p.name for p in p_list]
        if self.category_name in names:
            raise "You must not save a category in itself!"

    def __repr__(self):
        p_list = self._recurse_for_parents(self)
        names = [p.name for p in p_list]
        names.append(self.name)
        return self.get_separator().join(names)
    
    def __unicode__(self):
        return self.__repr__()
    def full_path(self):
        p_list = self._recurse_for_parents(self)
        names = [self.user.username] + [p.name for p in p_list]
        names.append(self.name)
        return names
    def path(self):
        names = self.full_path()
        return 'categories/' + '/'.join(names)

class PlotCollection(models.Model):
    ""
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category,null=False,blank=False)
    
    def __unicode__(self):
        return self.name
    def full_path(self):
        base = self.category.full_path()
        base.append(self.name)
        return base
    def path(self):
        fp = self.full_path()
        return 'plot_collections/' + "/".join(fp)
    
class Plot(models.Model):
    """
    
    """
    name = models.CharField(max_length=300)
    collection = models.ForeignKey(PlotCollection,null=False,blank=False)
    url = models.URLField(null=False,blank=False)
    
    def __unicode__(self):
        return self.name
    
    def is_root(self,filename):
        path = self.get_path()
        filename = path[-1]
        ext = os.path.splitext(filename)[1]
        return ext == ".root"
        
    def get_all_versions(self):
        path = self.get_path()
        full_path = os.path.sep.join(path)
        
        filename = path[-1]
        collection = path[-2]
        ext = os.path.splitext(filename)[1]
        
        if self.collection == None and (ext!=".root"):
            collection = 'Default'
        
        versions = []
        
        # Check to see if it's associated with a root file
        if ext == ".root":
            # Get the root plot file
            rpf = self.get_root_plot_file()
            
            # now we can get all the versions from the rpf
            return rpf.get_all_versions()
        
        # Otherwise, they're raw plots
        
        # List all of the folders in the directory which corresponds to the path with the files in it
        dirs = os.listdir(self.base_path())
        
        versions = []
        for dir in dirs:
            versions.append(int(dir))
        
        return versions
    
    def get_category(self):
        return self.collection.category
    
    def get_user(self):
        return self.get_category().user
    
    def get_collection(self):
        return self.collection
    
    def get_root_plot_file(self):
        path = self.get_path()
        filename = self.filename()
        collection = path[-2]
        
        # Get the category
        category = self.get_category()
        
        # and the collection
        pc = self.collection
        
        # Now we can get the root file that corresponds to this path
        results = RootPlotFile.objects.filter(name=filename,collection=pc)
        if len(results)!=1:
            return []
        rpf = results[0]
        
        return rpf
    
    def get_current_version(self):
        # Get all of the versions
        versions = self.get_all_versions()
        
        # Find the maximum
        return max(versions)
    
    def get_next_version(self):
        
        current = self.get_current_version()
        return current + 1
    
    def generate_next_filename(self,version):
        # Get all of the pre-existing versions
        versions = self.get_all_versions()
        
        # The new version number is the minimum +1
        minimum = 0
        minimum = max(versions)
        
    def get_path(self):
        "Returns the path as seen from Category,PlotCollection view"
        collection = self.get_collection()
        path = collection.full_path()
        path.append(self.filename())
        return path
    
    def filename(self):
        u = urlparse(self.url)
        return u.path.split('/')[-1]
    
    def base_path(self):
        "Returns"
        path = self.get_path()[:-1]
        path.append(self.filename())
        
        return os.path.join(settings.UPLOAD_PATH,*path)
    
    def full_path(self,version=None):
        if version is None:
            version = self.get_current_version()
        
        version = str(version)
        path = self.get_path()
        
        path.append(version)
        path.append(self.filename())
        return os.path.join(settings.UPLOAD_PATH,*path)
    
class RootPlotFile(models.Model):
    """
    filepath/name/version/name gives you the full path to the root file
    """
    name = models.CharField(max_length=300)
    collection = models.ForeignKey(PlotCollection,null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    
    
    
    def get_all_versions(self):
        
        # List all of the folders in the directory which corresponds to the path with the files in it
        dirs = os.listdir(self.file_path())
        
        versions = []
        for dir in dirs:
            versions.append(int(dir))
        
        return versions
    
    def get_category(self):
        return self.collection.category
    
    def get_collection(self):
        return self.collection
    
    def get_user(self):
        return self.collection.category.user
    
    #
    # Path functions
    #
    def get_path(self):
        "Returns the path as seen from Category,PlotCollection view"
        collection = self.get_collection()
        path = collection.full_path()
        path.append(self.name)
        return path
    
    def file_path(self):
        path = self.get_path()
        user = self.get_user()
        username = user.username
        return os.path.join(settings.UPLOAD_PATH,*path)
    
    def full_path(self,version=None):
        if version is None:
            version = self.get_current_version()
        
        version = str(version)
        path = self.get_path()
        
        path.append(version)
        path.append(self.name)
        return os.path.join(settings.UPLOAD_PATH,*path)
    
    def url(self):
        path = self.get_path()
        return settings.UPLOAD_ROOT + "/" + '/'.join(path)
    
    def full_url(self,version=None):
        if version is None:
            version = self.get_current_version
        
        version = str(version)
        path = self.get_path()
        
        path.append(version)
        path.append(self.name)
        return os.path.join(settings.UPLOAD_ROOT,*path)
    
    #
    # Versioning functions
    #
    def get_current_version(self):
        versions = self.get_all_versions()
        return max(versions)
    
    def get_next_version(self):
        current = self.get_current_version()
        return current+1
    
    def get_next_path(self):
        next = self.get_next_version()
        return self.full_path(next)
    
    def get_current_path(self):
        current = self.get_current_version()
        return self.full_path(current)

tagging.register(Plot)
tagging.register(PlotCollection)