from FlowCalc.Utils import SI_conversions


class Value:
    """
    Wrapper for floats to include a unit.
    """

    def __init__(self, value, unit):
        """
        Parameters
        ----------
        value: float
        unit: str

        Attributes
        ----------
        self.value: float
        self.unit: str
        """

        self.value = value
        self.unit = unit

    def standardize(self):
        """
        Convert to SI equivalent.

        Parameters
        ----------

        Returns
        -------
        """

        if SI_conversions.get(self.unit) == None:
            print(f"No conversion for unit {self.value}/ {self.unit}.")
        else:
            conversion_function, si_unit = SI_conversions[self.unit]

            si_value = conversion_function(self.value)

            self.value = si_value
            self.unit = si_unit
