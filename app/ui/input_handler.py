class InputHandler:
    """
    A class to handle input data for the application.
    """

    def __init__(self):
        """
        Initializes the InputHandler with an empty dictionary to store inputs.
        """
        self._inputs = {}

    def set_input(self, category, key, value):
        """
        Sets the value for a given key in the input dictionary.

        :param key: The key for the input.
        :param value: The value to associate with the key.
        """
        self._inputs.setdefault(category, {})[key] = value

    def get_input(self, category, key):
        """
        Retrieves the value associated with a given key.

        :param key: The key to look up.
        :return: The value associated with the key, or None if the key does not exist.
        """
        return self._inputs.get(category, {}).get(key)

    def get_inputs(self, category):
        """
        Retrieves all inputs for a given category.

        :param category: The category to look up.
        :return: A dictionary of all inputs for the specified category.
        """
        return self._inputs.get(category, {})

    def clear_inputs(self):
        """
        Clears all inputs from the dictionary.
        """
        self._inputs.clear()
