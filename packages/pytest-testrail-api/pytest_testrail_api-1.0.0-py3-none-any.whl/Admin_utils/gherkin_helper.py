class GherkinTools:
    @staticmethod
    def string_to_value(field_value):
        """
        If any other manipulations with gherkin variables require include it to this method please
        """
        return field_value == "True" if field_value in ("True", "False") else field_value
