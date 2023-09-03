import sys
from scapy.all import rdpcap
from collections import Counter

def get_most_significant_byte(packet):
    if 'ICMP' in packet:
        icmp_packet = packet['ICMP']
        if 'Raw' in icmp_packet:
            raw_data = icmp_packet['Raw'].load
            if raw_data:
                return raw_data[0]
    return None

def decrypt_cesar_cipher(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted_char = chr(((ord(char) - shift - 65) % 26) + 65) if char.isupper() else chr(((ord(char) - shift - 97) % 26) + 97)
            decrypted_text += shifted_char
        else:
            decrypted_text += char
    return decrypted_text

def main(file_name):
    packets = rdpcap(file_name)
    payload = ""
    for packet in packets:
        msb = get_most_significant_byte(packet)
        if msb is not None:
            payload += chr(msb)

    print("Byte más significativo del payload:")
    print(payload)

    # Calcular frecuencia de letras en español
    spanish_letter_frequency = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    probabilities = {}

    for shift in range(26):
        decrypted_text = decrypt_cesar_cipher(payload, shift)
        letter_counts = Counter(decrypted_text.upper())
        total_letters = sum(letter_counts.values())
        score = 0
        for letter, frequency in letter_counts.items():
            if letter in spanish_letter_frequency:
                index = spanish_letter_frequency.index(letter)
                score += frequency * (1 / (index + 1))
        probabilities[shift] = score / total_letters

    print("\nProbabilidades de descifrado:")
    max_prob_shift = max(probabilities, key=probabilities.get)
    for shift, probability in probabilities.items():
        if shift == max_prob_shift:
            print(f"{shift}: {probability:.4f} (Probable) - {decrypt_cesar_cipher(payload, shift)}")
        else:
            print(f"{shift}: {probability:.4f} - {decrypt_cesar_cipher(payload, shift)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python decode_icmp.py archivo.pcapng")
    else:
        main(sys.argv[1])
