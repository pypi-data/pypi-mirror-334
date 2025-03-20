
class UserPanelValue():
    def __init__(self, value_source, on_set=None):
        """initialiser method
        SmartInput objects are used to keep track of GUI input values

        Arguments:
            value_source -- GUI object to retreive self.value from

        Keyword Arguments:
            on_set -- callback to be run after self.set(), receives self.value as its first argument (default: {None})
        """
        self.__value_source = value_source
        self.value = self.__value_source.GetValue()
        self.on_set = on_set

    def set(self):
        """update self.value and then run the on_set function

        Returns:
            newest self.value
        """
        self.value = self.__value_source.GetValue()
        if self.on_set is not None:
            self.on_set(self.value)
        return self.value