import tkapi


class BesluitFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_empty_zaak(self):
        filter_str = 'Zaak/any(z: true)'
        self.filters.append(filter_str)


class Besluit(tkapi.TKItem):
    url = 'Besluit'
    expand_param = 'Zaak, Stemming'

    def __init__(self, stemming_json):
        super().__init__(stemming_json)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def status(self):
        return self.get_property_or_empty_string('Status')

    @property
    def zaak(self):
        from tkapi.zaak import Zaak
        return tkapi.api.get_item(Zaak, self.json['Zaak']['Id'])

    @property
    def stemmingen(self):
        from tkapi.stemming import Stemming
        stemmingen = []
        for stemming_json in self.json['Stemming']:
            stemmingen.append(tkapi.api.get_item(Stemming, stemming_json['Id']))
        return stemmingen
