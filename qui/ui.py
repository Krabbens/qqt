from .palette import palette
from .spacing import spacing

from qqt import qqtDictModel

class UI(qqtDictModel):
    '''
    This class contains all the UI elements.
    '''

    def __init__(self):
        self.ui = {}
        self.palette = palette
        self.spacing = spacing
        
        self.ui.update(self.palette)
        self.ui.update(self.spacing)

        super().__init__("ui", list(self.ui.keys()))
        self.set_dict(self.ui)
