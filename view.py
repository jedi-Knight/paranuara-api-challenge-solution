from model import Model

class View(object):
    model = {}
    def __init__(self, model):
        assert isinstance(model, Model), 'Type mismatch! model must be of type Model'
        self.model = model
