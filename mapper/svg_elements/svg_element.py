class SVGElement:
    _label: str = None

    def set_label(self, label:str):
        self._label = label

    def get_label(self):
        return self._label