from typing import *

NODEENV = 'development' # development | debug | production

eseDatas = {
    'name': 'Company Name',
    'datas': [
        'BP.292 Douala',
        'CAMEROUN',
        '+237697545963',
        'contact@email.com',
    ]
}

encoder = "UTF-8"

langs = ['en', 'fr']
langCodes = {
    'fr': 'fr_FR',
    'en': 'en_US',
}

dateTimeFormatInitial = '%Y-%m-%dT%H:%M:%S.%fZ'
dateFormatInitial = '%Y-%m-%d'
timeFormatInitial = '%H:%M:%S.%fZ'

dateFormatForFile = '%Y%m%d%H%M%S'
dateFormat1 = '%Y/%m/%d %H:%M:%S.%fZ'
dateFormat2 = '%Y/%m/%d %H:%M:%S'
dateFormat3 = '%Y/%m/%d %H:%M'
dateFormat4 = '%d/%m/%Y %H:%M:%S GMT%z'
dateFormat5 = '%Y/%m/%d'
timeFormat1 = '%H:%M:%S.%fZ'
timeFormat2 = '%H:%M:%S'
pagesPossibles = [ 5, 10, 15, 25, 50, 100, -1 ]

regExpForAlphanumeric = r"^[\w\s]{1,}"

tabNumerique = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
tabNumerique = list(map(lambda x: str(x), tabNumerique))
tabAlphabetique = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
tabAlphabetique = list(map(lambda x: x.lower(), tabAlphabetique))
tabAlphabetiqueInsensitive = tabAlphabetique + list(map(lambda x: x.upper(), tabAlphabetique))
tabAlphanumerique = tabNumerique + tabAlphabetique
tabAlphanumeriqueInsensitive = tabNumerique + tabAlphabetiqueInsensitive