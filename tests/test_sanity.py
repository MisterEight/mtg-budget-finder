import pytest
from core.similarity import find_alternatives

pytestmark = pytest.mark.integration


KNOWN_PAIRS = [
    ("Llanowar Elves",  ["Elvish Mystic", "Fyndhorn Elves"]),
    ("Counterspell",    ["Absorb", "Dismiss", "Mana Leak"]),
    ("Wrath of God",    ["Kirtar's Wrath", "Winds of Rath", "Catastrophe"]),
]


@pytest.mark.parametrize("card_name, expected", KNOWN_PAIRS)
def test_known_alternatives_appear(card_name, expected):
    _, alternatives = find_alternatives(card_name, top_n=10, cmc_range=2)
    names = [a["name"] for a in alternatives]
    assert any(e in names for e in expected), (
        f"Nenhuma alternativa esperada encontrada para '{card_name}'. "
        f"Esperado algum de {expected}, obtido: {names}"
    )


@pytest.mark.parametrize("card_name, _", KNOWN_PAIRS)
def test_color_identity_respected(card_name, _):
    card, alternatives = find_alternatives(card_name, top_n=10, cmc_range=2)
    query_ci = set(card.get("color_identity") or [])
    for alt in alternatives:
        alt_ci = set(alt.get("color_identity") or [])
        assert alt_ci.issubset(query_ci), (
            f"'{alt['name']}' tem color identity {alt_ci} "
            f"que não cabe em {query_ci} de '{card_name}'"
        )


@pytest.mark.parametrize("card_name, _", KNOWN_PAIRS)
def test_cmc_range_respected(card_name, _):
    cmc_range = 1
    card, alternatives = find_alternatives(card_name, top_n=10, cmc_range=cmc_range)
    query_cmc = card.get("cmc") or 0
    for alt in alternatives:
        alt_cmc = alt.get("cmc") or 0
        assert abs(alt_cmc - query_cmc) <= cmc_range, (
            f"'{alt['name']}' tem CMC {alt_cmc}, fora do range "
            f"{query_cmc} ± {cmc_range} de '{card_name}'"
        )
