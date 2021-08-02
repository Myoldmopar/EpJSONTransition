from epjson_transition.logger import SimpleLogger


class EpJSONTransitionRuleBase:
    """
    An abstract base class for declaring transition rules from any one single EnergyPlus version to the next.
    """

    def message(self):
        """
        Returns a descriptive message
        :return:
        """
        raise NotImplementedError("Must override message() method in EpJSONTransitionRuleBase derived classes")

    def old_version(self) -> float:
        """

        :return:
        """
        raise NotImplementedError("Must override old_version() method in EpJSONTransitionRuleBase derived classes")

    def new_version(self) -> float:
        """

        :return:
        """
        raise NotImplementedError("Must override new_version() method in EpJSONTransitionRuleBase derived classes")

    def transform(self, file_contents, logger: SimpleLogger):
        """

        :param logger:
        :param file_contents:
        :return:
        """
        raise NotImplementedError("Must override transform() method in EpJSONTransitionRuleBase derived classes")

    def variable_map(self):
        """

        :return:
        """
        raise NotImplementedError("Must override variable_map() method in EpJSONTransitionRuleBase derived classes")
