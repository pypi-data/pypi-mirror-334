"""
exceptions.py – Model parser specific exceptions
"""

# Every error should have the same format
# with a standard prefix and postfix defined here
pre = "\nState model parser: ["
post = "]"


class MPException(Exception):
    pass

class MDPopulationException(MPException):
    pass

class MismatchedStateSignature(MDPopulationException):
    def __init__(self, event, state):
        self.event = event
        self.state = event

    def __str__(self):
        return f'{pre}Event spec <{self.event}> on transition into state [{self.state}] has a different signature.{post}'

class MPIOException(MPException):
    pass

class MPUserInputException(MPException):
    pass

class ModelParseError(MPUserInputException):
    def __init__(self, model_file, e):
        self.model_file = model_file
        self.e = e

    def __str__(self):
        return f'{pre}Parse error in model "{self.model_file}"\n\t{self.e}"{post}'

class ModelInputFileOpen(MPIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this model input file: "{self.path}"{post}'

class ModelInputFileEmpty(MPIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}For some reason, nothing was read from the model input file: "{self.path}"{post}'

class ModelGrammarFileOpen(MPIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this model grammar file: "{self.path}"{post}'