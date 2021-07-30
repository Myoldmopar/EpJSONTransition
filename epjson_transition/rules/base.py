class EpJSONTransitionRuleBase:
    def __init__(self):
        ...

    def transform(self, file_contents):
        raise NotImplementedError("Need to override transform() method in EpJSONTransitionRuleBase derived classes")
