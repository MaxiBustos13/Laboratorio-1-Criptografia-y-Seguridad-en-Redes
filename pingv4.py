import sys
import random
from scapy.all import IP, ICMP, send

def send_string_as_ping_requests(input_string):
    try:
        destination_ip = "127.0.0.1"  # IP de localhost
        identifier = 1
        sequence_number = 1

        for char in input_string:
            # Generar un paquete ICMP Echo Request similar a ping
            packet = IP(dst=destination_ip) / ICMP(type=8, code=0, id=identifier, seq=sequence_number)

            # Estructura del payload del paquete
            payload = bytes([ord(char)])  # Convertir el carácter a byte

            # Agregar bytes aleatorios diferentes
            random_bytes = [random.randint(0, 255) for _ in range(2)]
            while random_bytes[0] == random_bytes[1]:
                random_bytes[1] = random.randint(0, 255)
            payload += bytes(random_bytes)

            # Agregar ceros
            payload += b'\x00\x00\x00\x00\x00'

            # Agregar bytes del 10 al 37
            payload += bytes(range(0x10, 0x38))

            # Establecer el payload en el paquete
            packet = packet / payload

            # Incrementar el número de secuencia
            sequence_number += 1

            # Enviar el paquete
            send(packet)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <cadena>")
    else:
        input_string = sys.argv[1]
        send_string_as_ping_requests(input_string)