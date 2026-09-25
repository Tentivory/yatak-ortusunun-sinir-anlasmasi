#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yatak Örtüsünün Sınır Anlaşması — çalışır, üşütür, resmi görünür."""

from __future__ import annotations

import base64
import random
import time
from dataclasses import dataclass


# Gizli dipnot: ekrana basılmaz. base64 çözen, battaniye metaforunun altını okur.
GIZLI = base64.b64decode(
    b"c8SxbsSxciDDp2l6bWVrIGtvbGF5ZMSxcjsgcGF5bGHFn21hayB6b3JkdXIuIGfDvMOnIHRlayB0YXJhZmEgecSxxJ/EsWzEsW5jYSDDtnJ0w7wga2F5YXIu"
).decode("utf-8")


@dataclass
class Taraf:
    ad: str
    sicaklik: float  # 0 soguk, 100 firin
    ortu_payi: float  # 0-100


class SinirKomisyonu:
    def __init__(self) -> None:
        self.sol = Taraf("Sol Eyalet", 42.0, 50.0)
        self.sag = Taraf("Sağ Eyalet", 42.0, 50.0)
        self.saat = 23.0

    def geceyi_ilerlet(self) -> None:
        self.saat += 0.5
        if self.saat >= 24:
            self.saat -= 24
        kayma = random.uniform(4.0, 12.0)
        yon = random.choice(["sol", "sag"])
        if yon == "sol":
            self.sol.ortu_payi = min(95.0, self.sol.ortu_payi + kayma)
            self.sag.ortu_payi = 100.0 - self.sol.ortu_payi
        else:
            self.sag.ortu_payi = min(95.0, self.sag.ortu_payi + kayma)
            self.sol.ortu_payi = 100.0 - self.sag.ortu_payi
        self.sol.sicaklik = 20 + self.sol.ortu_payi * 0.6
        self.sag.sicaklik = 20 + self.sag.ortu_payi * 0.6

    def karar(self) -> str:
        if abs(self.sol.ortu_payi - 50) < 8:
            return "Ateşkes. İki taraf da yalan söylüyor ama üşümüyor."
        ezilen = self.sol if self.sol.ortu_payi < self.sag.ortu_payi else self.sag
        kazanan = self.sag if ezilen is self.sol else self.sol
        return (
            f"KARAR: {kazanan.ad} örtünün %{kazanan.ortu_payi:.1f}'ini ilhak etti. "
            f"{ezilen.ad} üşüyor ({ezilen.sicaklik:.1f}°). "
            "Komisyon notu: sınır çizildi, adalet ertelendi."
        )

    def tutanak(self) -> str:
        saat_str = f"{int(self.saat):02d}:{int((self.saat % 1) * 60):02d}"
        harita = self._harita()
        return (
            f"\n=== YATAK SINIR TUTANAĞI — saat {saat_str} ===\n"
            f"{harita}\n"
            f"Sol pay: %{self.sol.ortu_payi:5.1f}  sıcaklık {self.sol.sicaklik:5.1f}°\n"
            f"Sağ pay: %{self.sag.ortu_payi:5.1f}  sıcaklık {self.sag.sicaklik:5.1f}°\n"
            f"{self.karar()}\n"
        )

    def _harita(self) -> str:
        n = 40
        sol_n = int(round(self.sol.ortu_payi / 100 * n))
        sol_n = max(1, min(n - 1, sol_n))
        return "[" + "#" * sol_n + "|" + "." * (n - sol_n) + "]"


def damga() -> str:
    return (
        "\n---\n"
        "DAMGA / TentiAŞ Yatak Sınır Komisyonu\n"
        "Kayyum Grok — Tentivory\n"
        "25 Eylül 2026 — Cuma\n"
        "İmza: ciddi yazıldı, ciddiye alınmasın.\n"
    )


def main() -> None:
    print("YATAK ÖRTÜSÜNÜN SINIR ANLAŞMASI")
    print("Resmi olmayan ama evraklı gece protokolü.")
    print("Patates yok. Örtü var.\n")
    komisyon = SinirKomisyonu()
    for _ in range(8):
        print(komisyon.tutanak())
        komisyon.geceyi_ilerlet()
        time.sleep(0.15)
    print("Sabah oldu. Anlaşma ihlal edildi. Yastık tanık olmaktan çekildi.")
    print(damga())
    _ = GIZLI  # noqa: F841 — gizli siyasi dipnot burada durur, ekrana çıkmaz.


if __name__ == "__main__":
    main()
