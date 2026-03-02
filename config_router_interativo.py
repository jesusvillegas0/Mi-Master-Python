import json
from netmiko import ConnectHandler
import re


def cargar_configuracion():
    with open('routers.json', 'r') as f:
        return json.load(f)


def reporte_estacional(net_connect):
    print("\n" + "="*30)
    print("Reporte de registro SIP")
    print("="*30)
    print(net_connect.send_command("show voice register statistics | include Total|Active"))
    print(net_connect.send_command("show voice register sessions"))


def configurar_interactivo():
    try:
        routers = cargar_configuracion()
        print("Routers disponibles:", list(routers.keys()))
        seleccion = input("A que router desea conectarse? ")

        if seleccion not in routers:
            print("Router no encontrado en el JSON")
            return
        device = routers[seleccion]
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        while True:
            print("\n" + "-"*40)
            print(f"--- Menú de Configuración de Voz --- {seleccion}")
            nuevo_numero = input("Ingrese el número de extensión (o 'salir' para terminar): ")
            
            if nuevo_numero.lower() == 'salir':
                break

            nuevo_nombre = input(f"Ingrese el nombre para la extensión {nuevo_numero}: ")

            print("\nVerificando disponibilidad en el router...")
            current_config = net_connect.send_command("show run | section voice register")
            
            # 1. Verificar si el número ya existe
            if nuevo_numero in re.findall(r'number\s+(\d+)', current_config):
                print(f"¡Atención! El número {nuevo_numero} ya está configurado. Intente con otro.")
                continue

            # 2. Calcular el siguiente DN disponible automáticamente
            dns_usados = re.findall(r'voice register dn\s+(\d+)', current_config)
            dns_int = [int(x) for x in dns_usados]
            siguiente_dn = max(dns_int) + 1 if dns_int else 1
            
            print(f"Asignando etiqueta DN {siguiente_dn} para la extensión {nuevo_numero}...")

            # 3. Preparar comandos
            config_commands = [
                f"voice register dn {siguiente_dn}",
                f" number {nuevo_numero}",
                f" name {nuevo_nombre}",
                "exit",
                f"voice register pool {siguiente_dn}",
                " id mac 0000.0000.0000",
                f" number 1 dn {siguiente_dn}",
                f" username {nuevo_numero} password 1234",
                "exit",
                "voice register global",
                "create profile"
            ]

            # 4. Enviar configuración
            output = net_connect.send_config_set(config_commands)
            print(output)
            print(f"\n¡Extensión {nuevo_numero} ({nuevo_nombre}) creada exitosamente!")

        # Al salir del bucle, mostrar reporte y desconectar
        reporte_estacional(net_connect)
        net_connect.disconnect()
        print("\nSesión finalizada. ¡Buen trabajo!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    configurar_interactivo()