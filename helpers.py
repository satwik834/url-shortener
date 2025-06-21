import string
BASE62_ALPHABET = string.digits + string.ascii_letters
BASE62_ALPHABET_LENGTH = len(BASE62_ALPHABET)

def base62_encode(num):
    if num == 0:
        return BASE62_ALPHABET[0]
    result = []

    while num>0:
        result.append(BASE62_ALPHABET[num %BASE62_ALPHABET_LENGTH])
        num //= BASE62_ALPHABET_LENGTH
    return ''.join(result[::-1])

def base62_decode(string):
    num = 0
    for c in string:
        num = num * BASE62_ALPHABET_LENGTH + BASE62_ALPHABET.index(c)
    return num

