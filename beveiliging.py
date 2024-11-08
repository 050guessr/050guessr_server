# door Fred AI
import base64

def versleutel_tekst(tekst):
    # Zet de tekst om naar base64
    base64_bytes = base64.b64encode(tekst.encode('utf-8'))
    base64_tekst = base64_bytes.decode('utf-8')
    
    # Verschuif elke karaktercode in de base64-string
    verschoven_base64 = ''.join([chr(ord(c) + 3) for c in base64_tekst])
    
    return verschoven_base64

def ontsleutel_en_vergelijken(versleutelde_tekst, te_vergelijken_tekst):
    # Maak de verschuiving ongedaan door 3 posities terug te gaan in de ASCII-tabel
    originele_base64 = ''.join([chr(ord(c) - 3) for c in versleutelde_tekst])
    
    # Decodeer de base64-string terug naar de oorspronkelijke tekst
    ontsleutelde_bytes = base64.b64decode(originele_base64)
    ontsleutelde_tekst = ontsleutelde_bytes.decode('utf-8')
    
    # Vergelijk de ontsleutelde tekst met de opgegeven tekst
    return ontsleutelde_tekst == te_vergelijken_tekst
