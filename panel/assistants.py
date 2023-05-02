import re


class Validator:
    """
    A class for handling validations for fields.
    """

    def validate(self, value: str, not_allowed: str, strip: bool = False) -> bool | str:
        """
        A method for validating strings.
        """

        pattern = re.compile(not_allowed, flags=re.IGNORECASE)
        bool_result = True if pattern.search(value) else False
        return pattern.sub('', value) if strip == True and pattern.search(value) else bool_result
