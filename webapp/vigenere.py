# A module to decode and encode using vigenere cipher
import base64


def encode(key: str, clear: str) -> str:
    """Encode using vigenere cipher"""

    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key: str, enc: str) -> str:
    """Decode using vigenere cipher"""

    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def link_encode(key: str, link: str) -> str:
    """Encode link using vigenere cipher"""

    parts = link.split('/')
    _id = parts[-1]
    enc_id = encode(key, _id)
    enc_link = '/'.join(parts[:-1]) + '/' + enc_id
    return enc_link


def link_decode(key: str, link: str) -> str:
    """Decode link using vigenere cipher"""

    parts = link.split('/')
    _id = parts[-1]
    dec_id = decode(key, _id)
    dec_link = '/'.join(parts[:-1]) + '/' + dec_id
    return dec_link

