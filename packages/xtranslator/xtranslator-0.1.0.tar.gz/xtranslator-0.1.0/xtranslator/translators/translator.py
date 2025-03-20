from typing import List, Union

class Translator:
    def __init__(self):
        pass

    def translate(self, text: str, dest: str) -> Union[str, List[str]]:
        raise NotImplementedError
