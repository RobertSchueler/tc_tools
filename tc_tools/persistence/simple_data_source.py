class SimpleDataSource:
    def __init__(self, card_list: list[dict]):
        self._card_list = card_list

    def __iter__(self):
        yield from self._card_list
