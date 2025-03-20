

import bluetooth
import time
import os

class Bluetoof:
    def __init__(self):
        self.interface = "hci0"
        self.scan_duration = 10

    def device_connection_interactive(self, mac_address=None, port=1):
        if mac_address is None:
            return False
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print(f"Connexion au serveur {mac_address} sur le port {port}...")
            sock.connect((mac_address, port))
            print("✅ Connexion réussie !")

            while True:
                message = input("Message à envoyer (ou 'quit' pour quitter) : ")
                if message.lower() == "quit":
                    break
                sock.send(message + "\n")

                data = b""
                while True:
                    chunk = sock.recv(1024)
                    data += chunk
                    if b"\n" in chunk:
                        break
                print(f"Réponse du serveur : {data.decode().strip()}")
        except bluetooth.btcommon.BluetoothError:
            return None
        finally:
            sock.close()

    def device_command(self, mac_address=None, port=1, command=None):
        if mac_address is None or command is None:
            return False
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((mac_address, port))
            sock.send(command + "\n")
            data = b""
            while True:
                chunk = sock.recv(1024)
                data += chunk
                if b"\n" in chunk:
                    return data.decode("utf-8").strip()
        except bluetooth.btcommon.BluetoothError:
            return None
        finally:
            sock.close()

    def device_command_eof(self, mac_address=None, port=1, command=None):
        if mac_address is None or command is None:
            return False
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((mac_address, port))
            sock.send(command + "\n")
            data = b""
            while True:
                chunk = sock.recv(1024)
                data += chunk
                if b"\xff" in chunk:
                    return data
        except bluetooth.btcommon.BluetoothError:
            return None
        finally:
            sock.close()

    def find_device(self, mac_address):
        services = bluetooth.find_service(address=mac_address)
        return services[0] if services else None

    def list_devices(self):
        devices = bluetooth.discover_devices(duration=self.scan_duration, lookup_names=True)
        return [{"name": name, "mac": mac} for mac, name in devices]
