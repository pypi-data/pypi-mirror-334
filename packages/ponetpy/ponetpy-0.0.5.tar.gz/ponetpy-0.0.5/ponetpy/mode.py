class Mode:
    def __init__(self, duration: float, cost: float, **kwargs):
        self.duration = duration
        self.cost = cost
        self._set_kwargs(kwargs)

    def _set_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_param(self, param: str):
        return getattr(self, param)
