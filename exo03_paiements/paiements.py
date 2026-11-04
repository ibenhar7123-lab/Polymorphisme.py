from abc import ABC, abstractmethod


def luhn_valide(numero: str) -> bool:
    """Vérifie un numéro de carte avec l'algorithme de Luhn."""
    if not numero.isdigit():
        return False
    total = 0
    for i, chiffre in enumerate(reversed(numero)):
        n = int(chiffre)
        if i % 2 == 1:      # un chiffre sur deux, en partant de la droite
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


class Paiement(ABC):
    def __init__(self, montant: float):
        if montant <= 0:
            raise ValueError("Le montant doit être strictement positif.")
        self._montant = float(montant)   # attribut protégé

    @abstractmethod
    def payer(self) -> str:
        """Retourne une chaîne de confirmation."""


class CarteBancaire(Paiement):
    def __init__(self, montant, numero: str, cvv: str):
        super().__init__(montant)
        numero = numero.replace(" ", "")
        if not (13 <= len(numero) <= 19) or not luhn_valide(numero):
            raise ValueError("Numéro de carte invalide (échec du contrôle de Luhn).")
        if not (cvv.isdigit() and len(cvv) == 3):
            raise ValueError("Le CVV doit contenir exactement 3 chiffres.")
        self._numero = numero
        self._cvv = cvv

    def payer(self) -> str:
        return (f"Paiement par carte bancaire de {self._montant:.2f} € accepté "
                f"(carte se terminant par {self._numero[-4:]}).")


class PayPal(Paiement):
    def __init__(self, montant, email: str, token: str):
        super().__init__(montant)
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Adresse e-mail invalide.")
        if len(token) < 8:
            raise ValueError("Token d'API invalide (8 caractères minimum).")
        self._email = email
        self._token = token

    def payer(self) -> str:
        return f"Paiement PayPal de {self._montant:.2f} € accepté pour le compte {self._email}."


class Crypto(Paiement):
    RESEAUX = ("BTC", "ETH", "USDT", "LTC")

    def __init__(self, montant, wallet_id: str, reseau: str):
        super().__init__(montant)
        if reseau.upper() not in self.RESEAUX:
            raise ValueError(f"Réseau non supporté : {reseau} (choix : {', '.join(self.RESEAUX)}).")
        if len(wallet_id) < 10:
            raise ValueError("Identifiant de portefeuille trop court (10 caractères minimum).")
        self._wallet_id = wallet_id
        self._reseau = reseau.upper()

    def payer(self) -> str:
        return (f"Paiement crypto de {self._montant:.2f} € accepté sur le réseau {self._reseau} "
                f"(portefeuille {self._wallet_id[:6]}...).")


def traiter_paiements(liste):
    """Polymorphisme : aucun isinstance, chaque objet sait payer à sa façon."""
    for p in liste:
        print(p.payer())


def demo():
    paiements = [
        CarteBancaire(120.50, "4111 1111 1111 1111", "123"),
        PayPal(45.00, "alice@example.com", "tok_abcdef123"),
        Crypto(300, "0xA1B2C3D4E5F6", "ETH"),
        CarteBancaire(89.99, "5500000000000004", "456"),
        PayPal(15.75, "bob@example.org", "tok_987654321"),
        Crypto(1200, "bc1qxyz1234567890", "btc"),
    ]
    traiter_paiements(paiements)

    print("\n=== Cas invalides ===")
    for essai in (
        lambda: CarteBancaire(50, "1234567890123456", "123"),
        lambda: PayPal(-10, "alice@example.com", "tok_abcdef123"),
        lambda: Crypto(20, "short", "BTC"),
    ):
        try:
            essai()
        except ValueError as e:
            print("Refusé :", e)


if __name__ == "__main__":
    demo()
