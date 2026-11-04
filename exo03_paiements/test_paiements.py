import io
import unittest
from contextlib import redirect_stdout

from paiements import (Paiement, CarteBancaire, PayPal, Crypto,
                       luhn_valide, traiter_paiements)


class TestPaiements(unittest.TestCase):
    def test_carte_message(self):
        msg = CarteBancaire(120.5, "4111111111111111", "123").payer()
        self.assertIn("120.50", msg)
        self.assertIn("carte bancaire", msg)

    def test_paypal_message(self):
        msg = PayPal(45, "a@b.com", "tok_12345678").payer()
        self.assertIn("45.00", msg)
        self.assertIn("PayPal", msg)

    def test_crypto_message(self):
        msg = Crypto(300, "0xA1B2C3D4E5", "eth").payer()
        self.assertIn("300.00", msg)
        self.assertIn("crypto", msg)
        self.assertIn("ETH", msg)

    def test_montant_invalide(self):
        with self.assertRaises(ValueError):
            PayPal(0, "a@b.com", "tok_12345678")
        with self.assertRaises(ValueError):
            Crypto(-5, "0xA1B2C3D4E5", "BTC")

    def test_luhn(self):
        self.assertTrue(luhn_valide("4111111111111111"))
        self.assertFalse(luhn_valide("1234567890123456"))
        with self.assertRaises(ValueError):
            CarteBancaire(10, "1234567890123456", "123")

    def test_cvv_invalide(self):
        with self.assertRaises(ValueError):
            CarteBancaire(10, "4111111111111111", "12")

    def test_classe_abstraite(self):
        with self.assertRaises(TypeError):
            Paiement(10)

    def test_traiter_paiements_polymorphe(self):
        liste = [CarteBancaire(10, "4111111111111111", "123"),
                 PayPal(20, "a@b.com", "tok_12345678"),
                 Crypto(30, "0xA1B2C3D4E5", "BTC")]
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            traiter_paiements(liste)
        lignes = sortie.getvalue().strip().splitlines()
        self.assertEqual(len(lignes), 3)


if __name__ == "__main__":
    unittest.main()
