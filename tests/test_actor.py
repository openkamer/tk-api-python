import datetime

from tkapi.actor import Persoon
from tkapi.actor import Fractie
from tkapi.actor import FractieLid

from .core import TKApiTestCase


class TestFractie(TKApiTestCase):
    # start_datetime = datetime.datetime(year=2017, month=1, day=1)
    # end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_fractie(self):
        fractie = self.api.get_item(Fractie, id='97d432a7-8a64-4db9-9189-cc9f70a4109b')
        print('fractie:', fractie.naam)
        self.assertEqual('GroenLinks', fractie.naam)
        self.assertEqual('GL', fractie.afkorting)
        self.assertEqual(datetime.date(year=1990, month=11, day=24), fractie.datum_actief)
        self.assertEqual(None, fractie.datum_inactief)
        # fractie.print_json()
        leden = fractie.leden
        for lid in leden:
            # lid.print_json()
            print(lid.van, '-', lid.tot_en_met)
            if lid.persoon:
                print(lid.persoon)
        print('fractieleden:', len(leden))
        self.assertGreater(len(leden), 53)

    def test_get_fracties(self):
        fracties = self.api.get_fracties(max_items=50)
        for fractie in fracties:
            # fractie.print_json()
            print('fractie:', fractie.naam, '| zetels:', fractie.zetels)
        self.assertEqual(39, len(fracties))

    def test_filter_fracties_actief(self):
        filter = Fractie.create_filter()
        filter.filter_actief()
        fracties = self.api.get_fracties(max_items=50, filter=filter)
        for fractie in fracties:
            fractie.print_json()
            print('fractie:', fractie.naam, '| zetels:', fractie.zetels)
        self.assertEqual(13, len(fracties))

    def test_filter_actieve_leden(self):
        fractie = self.api.get_item(Fractie, id='97d432a7-8a64-4db9-9189-cc9f70a4109b')
        leden_actief = fractie.leden_actief
        print(fractie.naam, fractie.zetels)
        for lid in leden_actief:
            print('\t', lid.persoon)
        self.assertEqual(fractie.zetels, len(leden_actief))


class TestPersoon(TKApiTestCase):

    def test_get_personen(self):
        max_items = 66
        personen = self.api.get_personen(max_items=max_items)
        for persoon in personen:
            print('Roepnaam:', persoon.roepnaam)
            print('Volledige naam:', persoon.voornamen, persoon.achternaam)
            persoon.print_json()
            # if persoon.fractie_lid is not None:
            #     persoon.fractie_lid.print_json()
            #     if persoon.fractie_lid.fractie is not None:
            #         persoon.fractie_lid.fractie.print_json()
        self.assertEqual(max_items, len(personen))

    def test_persoon_get_fracties(self):
        uid = '96a61016-76f0-4e73-80f0-0f554d919a93'
        persoon = self.api.get_item(Persoon, id=uid)
        fractieleden = persoon.fractieleden
        print(persoon.roepnaam, persoon.achternaam)
        print('fractieleden:', len(fractieleden))
        for lid in persoon.fractieleden:
            print(lid.fractie.naam)
        for fractie in persoon.fracties:
            print(fractie.naam)
        self.assertEqual(4, len(persoon.fracties))

    def test_get_functies(self):
        uid = '20415249-f14a-4375-b2c1-36608cbf0a76'
        persoon = self.api.get_item(Persoon, id=uid)
        functies = persoon.functies
        for functie in functies:
            print(functie.omschrijving)


class TestFractieLid(TKApiTestCase):

    def test_get_fractie_leden(self):
        leden = self.api.get_fractie_leden(max_items=10)
        print('fractieleden:', len(leden))
        self.assertEqual(10, len(leden))
        for lid in leden:
            lid.print_json()

    def test_get_fractie_leden_actief(self):
        filter = FractieLid.create_filter()
        filter.filter_actief()
        leden = self.api.get_fractie_leden(max_items=10, filter=filter)
        print('fractieleden:', len(leden))
        for lid in leden:
            lid.print_json()
            self.assertEqual(lid.tot_en_met, None)
            self.assertEqual(lid.is_actief, True)
