import sys
import textwrap
from core.similarity import find_alternatives

_WRAP_WIDTH = 60
_INDENT = "    "


def main():
    card_name = input("Nome da carta: ").strip()
    if not card_name:
        print("Nome inválido.")
        sys.exit(1)

    print(f"\nBuscando alternativas para '{card_name}'...\n")
    card, alternatives = find_alternatives(card_name, top_n=10, cmc_range=1)

    if card is None:
        print(f"Carta '{card_name}' não encontrada no banco.")
        sys.exit(1)

    card_price_str = (card.get("prices") or {}).get("usd")
    card_price = f"${float(card_price_str):.2f}" if card_price_str else "N/A"
    oracle_text = card.get("oracle_text") or ""
    wrapped_text = textwrap.fill(oracle_text, width=_WRAP_WIDTH, subsequent_indent=_INDENT)
    print(f"Carta   : {card['name']}")
    print(f"Tipo    : {card.get('type_line', '?')}")
    print(f"Custo   : {card.get('mana_cost') or '—'}")
    print(f"USD     : {card_price}")
    if wrapped_text:
        print(f"Texto   : {wrapped_text}")
    print("─" * 62)

    if not alternatives:
        print("Nenhuma alternativa encontrada com os filtros aplicados.")
        print("Tente ampliar o cmc_range ou reduzir o min_similarity em find_alternatives().")
        sys.exit(0)

    header = f"{'#':<3} {'Nome':<30} {'Custo':<14} {'USD':<10} {'Similaridade'}"
    print(header)
    print("─" * len(header))

    for i, alt in enumerate(alternatives, 1):
        name = alt["name"][:30]
        mana_cost = (alt.get("mana_cost") or "—")[:14]
        price = f"${alt['_price']:.2f}" if alt["_price"] != float("inf") else "N/A"
        sim = f"{alt['similarity']:.1%}"
        print(f"{i:<3} {name:<30} {mana_cost:<14} {price:<10} {sim}")
        type_line = alt.get("type_line") or ""
        if type_line:
            print(f"{_INDENT}{type_line}")
        alt_text = alt.get("oracle_text") or ""
        if alt_text:
            wrapped = textwrap.fill(alt_text, width=_WRAP_WIDTH, initial_indent=_INDENT, subsequent_indent=_INDENT)
            print(wrapped)


if __name__ == "__main__":
    main()
