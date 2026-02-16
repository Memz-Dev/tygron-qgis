from ..TygronClient.client import *
from qgis.core import QgsRasterLayer, QgsProject, QgsRectangle,QgsVectorLayer

class SessionPage:


    widget = None
    controller = None
    pageIndex = 3
    instancePrefix = "Session"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)
    
    def loadLayer(self,layerName="SATELLITE",QGISName="TygronLayer"):
        uri = self.controller.client.session.get_wms_uri(layerName)
        layer = QgsRasterLayer(uri, QGISName, "wms")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            return layer
        
    def loadVector(self,typeName="buildings",QGISName="TygronLayer"):
        uri = self.controller.client.session.get_wfs_uri(typeName)
        layer = QgsVectorLayer(uri, QGISName, "wfs")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            return layer
        else:
            error_msg = layer.error().summary()
            print(f"Invalid layer! Reason: {error_msg}")


    def killProject(self):
        if self.controller.client.session.kill():
            self.controller.switch_to_page(self.controller.home)
    
    def returnToHome(self):
        if self.controller.client.session.leave():
            self.controller.switch_to_page(self.controller.home)

    def open(self,**kwargs):
        self.controller.client.session.load_project_details()

        self.get("NameLabel").setText(f"Session {self.controller.client.session.project_name} ({self.controller.client.session.domain})")

    def loadTygronLayers(self):
        uri = self.controller.client.session.get_wms_uri("SATELLITE")
        self.controller.qgis.loadWMSLayer(uri,"Satellite View")

        uri = self.controller.client.session.get_wfs_uri("buildings")
        self.controller.qgis.loadWFSVector(uri,"Buildings Vector")

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToHome)
        self.get("KillButton").clicked.connect(self.killProject)
        self.get("LoadLayers").clicked.connect(self.loadTygronLayers)
        #self.get("BuildingsButton").clicked.connect(lambda: self.loadVector(typeName="buildings",QGISName="Buildings Vector"))