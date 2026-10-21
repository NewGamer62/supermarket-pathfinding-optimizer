"""
Tests unitaires pour le cœur algorithmique et les modèles de données
(filepile, modeleInformations, modeleSupermarche, Projet).
Peut être exécuté sans dépendre d'une interface graphique ou de PyQt6.
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT / "deuxiemeApp"))

import filepile as fp
from modeleInformations import Informations
from modeleSupermarche import Supermarche
from modele import Projet


class TestFilePile(unittest.TestCase):
    def test_file_operations(self):
        file = fp.File(capacite=3)
        self.assertTrue(file.est_vide())
        self.assertFalse(file.est_pleine())
        self.assertEqual(file.nombre_elements, 0)

        file.enfiler("A")
        file.enfiler("B")
        self.assertEqual(file.nombre_elements, 2)
        self.assertTrue(file.contient("A"))
        self.assertFalse(file.contient("C"))

        val = file.defiler()
        self.assertEqual(val, "A")
        self.assertEqual(file.nombre_elements, 1)

    def test_pile_operations(self):
        pile = fp.Pile(capacite=3)
        self.assertTrue(pile.est_vide())

        pile.empiler(10)
        pile.empiler(20)
        self.assertEqual(pile.nombre_elements, 2)
        self.assertEqual(pile.depiler(), 20)
        self.assertEqual(pile.depiler(), 10)
        self.assertTrue(pile.est_vide())


class TestModeleInformations(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_default_values(self):
        info = Informations()
        self.assertEqual(info.getNom(), "Projet sans Nom")
        self.assertEqual(info.getAuteur(), "Auteur Inconnu")

    def test_utf8_accents_persistence(self):
        info = Informations()
        info.setNom("Supermarché Épicerie Spéciale & Pâtisserie")
        info.setAuteur("Équipe Ingénierie")
        json_path = os.path.join(self.test_dir, "informations.json")
        info.ecrireFichier(json_path)

        reloaded = Informations(json_path)
        self.assertEqual(reloaded.getNom(), "Supermarché Épicerie Spéciale & Pâtisserie")
        self.assertEqual(reloaded.getAuteur(), "Équipe Ingénierie")


class TestModeleSupermarcheAndProjet(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sauvegarde_test_reading(self):
        sauvegarde_path = str(REPO_ROOT / "Sauvegarde-Test")
        projet = Projet(sauvegarde_path)
        self.assertEqual(projet.informations.getNom(), "Projet Test")
        self.assertGreater(len(projet.supermarche.getCaisses()), 0)
        self.assertGreater(len(projet.supermarche.getListeProduits()), 0)

    def test_projet_save_and_reload_utf8(self):
        sauvegarde_path = str(REPO_ROOT / "Sauvegarde-Test")
        projet = Projet(sauvegarde_path)
        projet.informations.setNom("Grand Magasin Central")

        out_path = os.path.join(self.test_dir, "ProjetExport")
        projet.ecrireDossier(out_path)

        reloaded = Projet(out_path)
        self.assertEqual(reloaded.informations.getNom(), "Grand Magasin Central")
        self.assertEqual(
            len(reloaded.supermarche.getListeProduits()),
            len(projet.supermarche.getListeProduits())
        )


if __name__ == "__main__":
    unittest.main()
