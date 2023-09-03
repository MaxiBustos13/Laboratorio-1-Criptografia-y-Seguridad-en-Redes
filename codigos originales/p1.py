import sys

def cifrar_cesar(texto, corrimiento):
    resultado = ""
    for letra in texto:
        if letra.isalpha():
            mayuscula = letra.isupper()
            letra = letra.upper()
            codigo = ord(letra) + corrimiento
            if codigo > ord('Z'):
                codigo -= 26
            nueva_letra = chr(codigo)
            if not mayuscula:
                nueva_letra = nueva_letra.lower()
            resultado += nueva_letra
        else:
            resultado += letra
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cifrado_cesar.py <texto> <corrimiento>")
    else:
        texto = sys.argv[1]
        corrimiento = int(sys.argv[2])
        texto_cifrado = cifrar_cesar(texto, corrimiento)
        print("Texto cifrado:", texto_cifrado)
