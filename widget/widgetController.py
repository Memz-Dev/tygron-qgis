from ..TygronClient.client import *
from ..qgisController import QGISController

from .homePage import HomePage
from .login import LoginPage
from .projectSelection import ProjectSelectionPage
from .session import SessionPage

class widgetController:

    widget = None
    openPage = None

    def __init__(self,plugin):
        self.widget = plugin.dockwidget
        self.login = LoginPage(self.widget,self)
        self.home = HomePage(self.widget,self)
        self.openProject = ProjectSelectionPage(self.widget,self)
        self.session = SessionPage(self.widget,self)
        self.client = plugin.client
        self.qgis = QGISController()

        self.start()

    def switch_to_page(self,instance,**kwargs):
        if (instance == None):
            return

        self.widget.stackedWidget.setCurrentIndex(instance.pageIndex)
        self.openPage = instance
        instance.open(**kwargs)

    def start(self):
        self.switch_to_page(self.login)


    
    