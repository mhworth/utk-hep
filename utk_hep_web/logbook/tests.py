"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from subprocess import Popen

from physics_web.logbook.models import *
import ROOT

# Test for plot model
class LogbookTest(TestCase):
    
    def setUp(self):
        ""
        user = User(username="matt")
        user.save()
        
        # Create some categories
        self.c1 = Category()
        self.c1.name="Test1"
        self.c1.user = user
        self.c1.save()
        
        self.c2 = Category()
        self.c2.name="Test2"
        self.c2.parent = self.c1
        self.c2.user=user
        self.c2.save()
        
        # Create a plot collection
        self.pc = PlotCollection()
        self.pc.name = "Test"
        self.pc.category=self.c2
        self.pc.save()
        
        # Create some example plot objects
        self.p1 = Plot()
        self.p1.name = "Test Root Plot"
        self.p1.url = settings.BASE_URL+"/rootfiles/Test1/Test2/Test/test.root"
        self.p1.collection=self.pc
        self.p1.save()
        
        self.p2 = Plot()
        self.p2.name="Test Raw Plot"
        self.p2.url = settings.BASE_URL+"/plots/Test1/Test2/Test/test.eps"
        self.p2.collection=self.pc
        self.p2.save()
        
        # make raw files for plot
       
        filename1 = self.p2.full_path(1)
        filename2 = self.p2.full_path(2)
        print "f1",filename1
        
        for filename in [filename1,filename2]:
            Popen(['mkdir','-p',os.path.split(filename)[0]]).wait()
            open(filename,"w")
        
        # And a root plot file
        self.rfp = RootPlotFile()
        self.rfp.name="test.root"
        self.rfp.collection=self.pc
        self.rfp.save()
        
        # and make a file that represents the root file
        filename1 = self.rfp.full_path(1)
        filename2 = self.rfp.full_path(2)
        print "f1 = ",filename1
        
        for filename in [filename1,filename2]:
            os.system("mkdir -p %s"%os.path.split(filename)[0])
            tf = ROOT.TFile(filename,"RECREATE")
            tf.Close()
        
        
    def tearDown(self):
        ""
        os.system("rm -rf %s"% self.rfp.file_path())
        os.system("rm -rf %s"% os.path.sep.join(self.p2.get_path()))
    
    def test_plot(self):
        """
        Test algorithm for finding versions
        """
        
        #
        # ROOT Based plots
        #
        
        # Get list of versions
        versions = self.p1.get_all_versions()
        self.failUnlessEqual(versions,[1,2])
        
        # Get current version
        current = self.p1.get_current_version()
        self.failUnlessEqual(current,2)
        
        # Get next version
        next = self.p1.get_next_version()
        self.failUnlessEqual(next,3)
        
        # Get the associated root plot file
        self.failUnlessEqual(self.rfp,self.p1.get_root_plot_file())
        
        # Get the category
        self.failUnlessEqual(self.c2,self.p1.get_category())
        
        #
        # Raw pots
        #
        versions = self.p2.get_all_versions()
        self.failUnlessEqual(versions,[1,2])
        
    def test_root_plot_file(self):
        ""
        rpf = self.rfp
        
        # Current version
        self.failUnlessEqual(2,rpf.get_current_version())
        
        # Next version
        self.failUnlessEqual(3,rpf.get_next_version())
        
        # Full path
        self.failUnlessEqual(os.path.join(rpf.file_path(),str(1),rpf.name),rpf.full_path(1))
        
        # Next filename
        self.failUnlessEqual(rpf.full_path(rpf.get_next_version()),rpf.get_next_path())
        
        # Current filename
        self.failUnlessEqual(rpf.full_path(rpf.get_current_version()),rpf.get_current_path())

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

