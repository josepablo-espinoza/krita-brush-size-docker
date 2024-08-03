from .brushSizeDocker import BrushSizeDocker
from krita import DockWidgetFactory,  DockWidgetFactoryBase# type: ignore

__ver__ = "1.0.0"

DOCKER_NAME = 'Brush Size Docker'
DOCKER_ID = 'pykrita_brushSizeDocker'

# Register the Docker with Krita
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockRight, BrushSizeDocker)

instance.addDockWidgetFactory(dock_widget_factory)