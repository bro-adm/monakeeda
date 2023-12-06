class PrioriHandlerCollisionException(Exception):
    def __init__(self, component, set_prior_handler: str, wanted_prior_handler: str):
        self.component = component
        self.set_prior_handler = set_prior_handler
        self.wanted_prior_handler = wanted_prior_handler

    def __str__(self):
        return f"{self.component} belongs to existing label group {self.component.label} which runs after {self.set_prior_handler}. You required to run after {self.wanted_prior_handler}"
