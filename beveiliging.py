# door Fred AI
import base64

def versleutel_tekst(tekst):
    """
    Versleutelt een tekst door deze om te zetten naar base64 en vervolgens
    de ASCII-waarden van elk karakter met 3 op te hogen.
    """
    # Zet de tekst om naar base64
    base64_bytes = base64.b64encode(tekst.encode('utf-8'))
    base64_tekst = base64_bytes.decode('utf-8')

    # Verschuif elke karaktercode in de base64-string
    verschoven_base64 = ''.join([chr(ord(c) + 3) for c in base64_tekst])

    return verschoven_base64

def ontsleutel_en_vergelijken(versleutelde_tekst, te_vergelijken_tekst):
    """
    Ontsleutelt de tekst door de verschuiving van 3 ongedaan te maken en base64 te decoderen.
    Vergelijkt vervolgens met de originele tekst.
    """
    # Maak de verschuiving ongedaan
    originele_base64 = ''.join([chr(ord(c) - 3) for c in versleutelde_tekst])

    # Decodeer de base64-string terug naar de oorspronkelijke tekst
    ontsleutelde_bytes = base64.b64decode(originele_base64)
    ontsleutelde_tekst = ontsleutelde_bytes.decode('utf-8')

    # Vergelijk de ontsleutelde tekst met de opgegeven tekst
    return ontsleutelde_tekst == te_vergelijken_tekst