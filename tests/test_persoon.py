import datetime

from tkapi.persoon import Persoon
from tkapi.persoon import PersoonReis
from tkapi.persoon import PersoonOnderwijs
from tkapi.persoon import PersoonFunctie
from tkapi.persoon import PersoonLoopbaan

from .core import TKApiTestCase


class TestPersoon(TKApiTestCase):

    def test_get_personen(self):
        max_items = 66
        personen = self.api.get_personen(max_items=max_items)
        for persoon in personen:
            print('Roepnaam:', persoon.roepnaam)
            print('Volledige naam:', persoon.voornamen, persoon.achternaam)
            # persoon.print_json()
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

    def test_get_reizen(self):
        uid = '355337af-a30f-48b8-882a-002ce35f9d07'  # Fred Teeven
        persoon = self.api.get_item(Persoon, id=uid)
        print(persoon)
        reizen = persoon.reizen
        self.assertEqual(5, len(reizen))
        self.assertEqual('Duitsland', reizen[0].bestemming)
        self.assertEqual('Ministerie van Defensie.', reizen[0].betaald_door)
        for reis in reizen:
            print(reis.bestemming)


class TestPersoonReis(TKApiTestCase):

    def test_get_reis(self):
        uid = '6ccc8b93-e86e-4e42-bb94-103eef850715'
        reis = self.api.get_item(PersoonReis, id=uid)
        self.assertEqual('Duitsland', reis.bestemming)
        self.assertEqual('Bijwonen oefening.', reis.doel)
        self.assertEqual('Ministerie van Defensie.', reis.betaald_door)
        self.assertGreater(reis.tot_en_met, reis.van)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', reis.persoon.id)


class TestPersoonOnderwijs(TKApiTestCase):

    def test_get_onderwijs(self):
        uid = 'bb6e9fa6-f966-4ba2-9b48-4ce872d1128d'
        onderwijs = self.api.get_item(PersoonOnderwijs, id=uid)
        self.assertEqual('Master Public Management (MPM)', onderwijs.opleiding_nl)
        self.assertEqual('Master\'s degree in Public Management (MPM), University of Twente 1999-2001', onderwijs.opleiding_en)
        self.assertEqual('Universiteit Twente', onderwijs.instelling)
        self.assertEqual('', onderwijs.plaats)
        self.assertGreater(onderwijs.tot_en_met, onderwijs.van)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', onderwijs.persoon.id)


class TestPersoonFunctie(TKApiTestCase):

    def test_get_functie(self):
        uid = '310a2b85-6b99-4633-aa73-9a978cdeb3a8'
        functie = self.api.get_item(PersoonFunctie, id=uid)
        self.assertEqual('Oud Kamerlid', functie.omschrijving)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', functie.persoon.id)


class TestPersoonLoopbaan(TKApiTestCase):

    def test_get_loopbaan(self):
        uid = 'aa767276-e588-42b0-9f38-097a635081d0'
        loopbaan = self.api.get_item(PersoonLoopbaan, id=uid)
        self.assertEqual('Teamleider', loopbaan.functie)
        self.assertEqual('FIOD', loopbaan.werkgever)
        self.assertEqual('', loopbaan.omschrijving)
        self.assertEqual('Team leader, FIOD, Haarlem 1990-1993', loopbaan.omschrijving_en)
        self.assertEqual('Haarlem', loopbaan.plaats)
        self.assertGreater(loopbaan.tot_en_met, loopbaan.van)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', loopbaan.persoon.id)
