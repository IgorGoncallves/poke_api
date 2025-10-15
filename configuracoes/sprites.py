import re

def get_sprite_url(nome_pokemon: str) -> str:

    if not nome_pokemon or not isinstance(nome_pokemon, str):
        return ""

    nome = nome_pokemon.strip().lower()
    nome = re.sub(r"\s+", " ", nome)

    especiais = {
        "nidoran♀": "nidoran-f",
        "nidoran♀️": "nidoran-f",
        "nidoran-f": "nidoran-f",
        "nidoran♂": "nidoran-m",
        "nidoran♂️": "nidoran-m",
        "nidoran-m": "nidoran-m",
        "mr. mime": "mr-mime",
        "mr mime": "mr-mime",
        "mime jr.": "mime-jr",
        "mime jr": "mime-jr",
        "farfetch’d": "farfetchd",
        "farfetchd": "farfetchd",
        "sirfetch’d": "sirfetchd",
        "sirfetchd": "sirfetchd",
        "type: null": "type-null",
        "jangmo-o": "jangmo-o",
        "hakamo-o": "hakamo-o",
        "kommo-o": "kommo-o",
        "tapu koko": "tapu-koko",
        "tapu lele": "tapu-lele",
        "tapu bulu": "tapu-bulu",
        "tapu fini": "tapu-fini",
        "ho-oh": "ho-oh",
    }

    if nome in especiais:
        nome = especiais[nome]

    if nome.startswith("mega "):
        base = nome.replace("mega ", "").strip()
        if base.endswith(" x"):
            base = base.replace(" x", "")
            nome = f"{base}-mega-x"
        elif base.endswith(" y"):
            base = base.replace(" y", "")
            nome = f"{base}-mega-y"
        else:
            nome = f"{base}-mega"


    elif nome.startswith("primal "):
        nome = nome.replace("primal ", "").strip() + "-primal"
    elif " forme" in nome or " form" in nome or " mode" in nome or " size" in nome:
        nome = nome.replace(" forme", "").replace(" form", "").replace(" mode", "").replace(" size", "").replace(" ", "-")
    elif nome.endswith(" male"):
        nome = nome.replace(" male", "-male")
    elif nome.endswith(" female"):
        nome = nome.replace(" female", "-female")

    nome = (
        nome.replace("’", "")
        .replace(" ", "-")
        .replace(".", "")
        .replace("é", "e")
        .replace(":", "")
        .strip("-")
    )

    url = f"https://img.pokemondb.net/sprites/home/normal/{nome}.png"

    fallback = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    return url or fallback
