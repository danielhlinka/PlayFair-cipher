import re

SPACE_PAIR = "ZQ"
J_PAIR = "ZL"

NUM_TO_PAIR = {
    "0": "ZA",
    "1": "ZB",
    "2": "ZC",
    "3": "ZD",
    "4": "ZE",
    "5": "ZF",
    "6": "ZG",
    "7": "ZH",
    "8": "ZI",
    "9": "ZK",
}

PAIR_TO_NUM = {
    "ZA": "0",
    "ZB": "1",
    "ZC": "2",
    "ZD": "3",
    "ZE": "4",
    "ZF": "5",
    "ZG": "6",
    "ZH": "7",
    "ZI": "8",
    "ZK": "9",
}

DIACRITICS_MAP = {
    "Á": "A", "Ä": "A", "Č": "C", "Ď": "D", "É": "E",
    "Ě": "E", "Í": "I", "Ľ": "L", "Ĺ": "L", "Ň": "N",
    "Ó": "O", "Ô": "O", "Ř": "R", "Š": "S", "Ť": "T",
    "Ú": "U", "Ů": "U", "Ý": "Y", "Ž": "Z",
}

ABC = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def replace_diacritics(text: str) -> str:
    return "".join(DIACRITICS_MAP.get(ch, ch) for ch in text)


def clean_text(text: str) -> str:
    text = text.upper()
    text = replace_diacritics(text)
    text = text.replace(" ", SPACE_PAIR)
    text = text.replace("J", J_PAIR)
    text = re.sub(r"[^A-Z0-9]", "", text)
    text = swap_nums_to_text(text)

    return text


def remove_key_duplicates(key: str) -> str:
    key = key.upper().replace("J", "I")
    key = re.sub(r"[^A-Z0-9]", "", key)
    return "".join(dict.fromkeys(key))


def key_to_list(key: str) -> list[str]:
    key_letters = list(key)
    used = set(key_letters)

    for letter in ABC:
        if letter not in used:
            key_letters.append(letter)
            used.add(letter)

    return key_letters


def restore_special_pairs(text: str) -> str:
    text = text.replace(SPACE_PAIR, " ")
    text = text.replace(J_PAIR, "J")

    for pair, number in PAIR_TO_NUM.items():
        text = text.replace(pair, number)

    return text


def create_matrix(key_letters: list[str]) -> list[list[str]]:
    if len(key_letters) != 25:
        raise ValueError(
            f"Key square must contain 25 letters, got {len(key_letters)}"
        )

    return [key_letters[i:i + 5] for i in range(0, 25, 5)]


def swap_nums_to_text(text: str) -> str:
    return "".join(NUM_TO_PAIR.get(ch, ch) for ch in text)


def prepare_playfair_text(
    text: str,
    filler: str = "X",
    backup_filler: str = "Q"
) -> str:
    result = []

    i = 0
    while i < len(text):
        a = text[i]

        if i + 1 == len(text):
            result.append(a)
            result.append(backup_filler if a == filler else filler)
            break

        b = text[i + 1]

        if a == b:
            current_filler = backup_filler if a == filler else filler
            result.extend([a, current_filler])
            i += 1
        else:
            result.extend([a, b])
            i += 2

    return "".join(result)


def make_pairs(text: str) -> list[str]:
    return [text[i:i + 2] for i in range(0, len(text), 2)]


def get_positions(square: list[list[str]]) -> dict[str, tuple[int, int]]:
    positions = {}

    for row_index, row in enumerate(square):
        for col_index, letter in enumerate(row):
            positions[letter] = (row_index, col_index)

    return positions


def encrypt_pair(
    square: list[list[str]],
    positions: dict[str, tuple[int, int]],
    pair: str
) -> str:
    a, b = pair

    ra, ca = positions[a]
    rb, cb = positions[b]

    size = len(square)

    if ra == rb:
        new_a = square[ra][(ca + 1) % size]
        new_b = square[rb][(cb + 1) % size]

    elif ca == cb:
        new_a = square[(ra + 1) % size][ca]
        new_b = square[(rb + 1) % size][cb]

    else:
        new_a = square[ra][cb]
        new_b = square[rb][ca]

    return new_a + new_b


def encrypt(square: list[list[str]], pairs: list[str]) -> str:
    positions = get_positions(square)
    encrypted_text = ""

    for pair in pairs:
        encrypted_text += encrypt_pair(square, positions, pair)

    return encrypted_text


def encrypt_text(text: str, key: str) -> dict:
    cleaned_key = remove_key_duplicates(key)
    key_letters = key_to_list(cleaned_key)
    square = create_matrix(key_letters)

    cleaned_text = clean_text(text)
    prepared_text = prepare_playfair_text(cleaned_text)
    pairs = make_pairs(prepared_text)

    cipher_text = encrypt(square, pairs)

    return {
        "cleaned_text": cleaned_text,
        "prepared_text": prepared_text,
        "pairs": pairs,
        "square": square,
        "cipher_text": cipher_text,
    }


def decrypt_pair(
    square: list[list[str]],
    positions: dict[str, tuple[int, int]],
    pair: str
) -> str:
    a, b = pair

    ra, ca = positions[a]
    rb, cb = positions[b]

    size = len(square)

    if ra == rb:
        new_a = square[ra][(ca - 1) % size]
        new_b = square[rb][(cb - 1) % size]

    elif ca == cb:
        new_a = square[(ra - 1) % size][ca]
        new_b = square[(rb - 1) % size][cb]

    else:
        new_a = square[ra][cb]
        new_b = square[rb][ca]

    return new_a + new_b


def decrypt(square: list[list[str]], pairs: list[str]) -> str:
    positions = get_positions(square)
    decrypted_text = ""

    for pair in pairs:
        decrypted_text += decrypt_pair(square, positions, pair)

    return decrypted_text


def decrypt_text(cipher_text: str, key: str) -> dict:
    cleaned_key = remove_key_duplicates(key)
    key_letters = key_to_list(cleaned_key)
    square = create_matrix(key_letters)

    cleaned_cipher_text = clean_text(cipher_text)
    pairs = make_pairs(cleaned_cipher_text)

    decrypted_text = decrypt(square, pairs)
    decrypted_text = restore_special_pairs(decrypted_text)

    return {
        "input_cipher_text": cipher_text,
        "cleaned_cipher_text": cleaned_cipher_text,
        "pairs": pairs,
        "square": square,
        "decrypted_text": decrypted_text,
    }