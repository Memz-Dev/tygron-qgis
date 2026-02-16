from qgis.core import QgsRasterLayer, QgsProject, QgsRectangle,QgsVectorLayer,QgsTask, QgsApplication,QgsSettings

class PluginTask(QgsTask):
    def __init__(self, description, background_fn, callback_fn=None):
        super().__init__(description, QgsTask.CanCancel)
        self.background_fn = background_fn
        self.callback_fn = callback_fn     
        self.data = None

    def run(self):
        try:
            self.data = self.background_fn()
            return True
        except Exception as e:
            print(f"Task failed: {e}")
            return False

    def finished(self, result):
        if result and self.callback_fn:
            self.callback_fn(self.data)

class QGISController():


    def save_credentials(self, username, password):
        settings = QgsSettings()
        settings.setValue("tygron/username", username)
        settings.setValue("tygron/password", password)

    def load_credentials(self):
        settings = QgsSettings()
        username = settings.value("tygron/username", "")
        password = settings.value("tygron/password", "")
        return username, password

    def __init__(self):
        self.tasks = []
        pass

    def addLayer(self,layer):
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            return layer

    def loadWFSVector(self,uri,QGISName):
        def run():
            return QgsVectorLayer(uri, QGISName, "wfs")
        def complete(result):
            self.addLayer(result)
            if task in self.tasks:
                self.tasks.remove(task)
        
        task = PluginTask(f"Loading WFS: '{QGISName}'",run,complete)
        self.tasks.append(task)
        QgsApplication.taskManager().addTask(task)

    def loadWMSLayer(self,uri,QGISName):
        layer = QgsRasterLayer(uri, QGISName, "wms")
        self.addLayer(layer)

