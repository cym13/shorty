import string
import hashlib

# Consonants and Vowel sounds
SYLLABUS = ([ x for x in string.ascii_lowercase if x not in 'aeiouy' ],
            [ 'a',  'e',  'i',  'o',  'u', 'y',
              'ai', 'au', 'eu', 'ay', 'ao', 'ay',
              'ey', 'ei', 'eo', 'ou', 'ia', 'io',
              'ua', 'ui' ])


def translate(hsh, syllabus=SYLLABUS):
    """
    Translates an hexadecimal hash into a human readable one
    """
    result = ""

    if len(hsh) % 2 == 1:
        hsh = '0' + hsh

    while hsh:
        val = int(hsh[0:2], 16)
        hsh = hsh[2:]

        result += syllabus[0][val // 20]
        result += syllabus[1][val %  20]

    return result


def generate(content, minsize=8):
    """
    Returns a human readable minimal hash of content
    """
    return translate(hashlib.md5(content.encode('utf8'))
                            .hexdigest()[0:minsize])

if __name__ == '__main__':
    import sys
    print(generate(sys.argv[1]))
