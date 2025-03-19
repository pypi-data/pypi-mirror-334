class Dictify:
    @staticmethod
    def _parse_name(key: str):
        if not isinstance(key, str):
            raise ValueError(f"Invalid attribute name: {key}")

        arrow = key.find('->')
        if arrow == -1:
            yield_key = key
        else:
            yield_key = key[arrow + 2:]
            key = key[:arrow]
        return key, yield_key

    def _get_all_public_attrs(self):
        return [attr for attr in dir(self) if not attr.startswith('_')]

    def dictify(self, *attrs):
        """
        Serializes selected attributes into a dictionary or JSON string.

        Supports:
        - Renaming fields using 'field->new_name'
        - Custom serialization using `_dictify_{field}` methods
        - Additional arguments for custom serialization
        """
        data = dict()

        if not attrs:
            attrs = self._get_all_public_attrs()

        for key in attrs:  # type: str
            key, yield_name = self._parse_name(key)

            if not hasattr(self, key):
                raise AttributeError(f"Attribute '{key}' does not exist in {self.__class__.__name__}")
            value = getattr(self, key)

            dictify_func = getattr(self, f'_dictify_{key}', None)
            if callable(dictify_func):
                value = dictify_func()
            data[yield_name] = value
        return data
