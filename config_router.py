from netmiko import ConnectHandler
import re

# Datos del router
device = {
    'device_type': 'cisco_ios',
    'host': '0.0.0.0',
    'username': 'admin1',
    'password': 'xxxxxx',
    'fast_cli': False,
    'session_log': 'log_output.txt'
}
def reporte_estacional(net_connect):
    print("\n" + "="*30)
    print("Reporte de registro SIP")
    print("="*30)
    output = net_connect.send_command("show voice register statistics")
    print(output)

    detalle = net_connect.send_command("show voice register sessions")
    print(detalle)

def configurar_inteligente():
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable(device)

        print("Analizando configuracion actual del router")
        current_config = net_connect.send_command("show run | section voice register")

        numeros_existentes = re.findall(r'number\s+(\d{4})', current_config)
        
        numeros_existentes = list(set(numeros_existentes))
        print(f"Numeros detectados en el router: {numeros_existentes}")


        config_commands = []

        for i in range(2, 26):
            numero_tel = str(1500 + i)

            if numero_tel not in numeros_existentes:
                print(f"La extension {numero_tel} no existe. Agregando a la lista de carga...")
                config_commands.extend([
                    f"voice register dn {i}",
                    f" number {numero_tel}",
                    f" name Extension_{numero_tel}",
                    "exit",
                    f"voice register pool {i}",
                    " id mac 0000.0000.0000",
                    f" number 1 dn {i}",
                    f" username {numero_tel} password 1234",
                    "exit"
                ])
            else:
                print(f"Extension {numero_tel} ya existe. Omitiendo")
        
        if len(config_commands) > 4:
            config_commands.extend(["voice register global", "create profile"])
            print("Enviando nuevos cambios al router...")
            output = net_connect.send_config_set(config_commands)
            print(output)
            print("Proceso completado con exito!")
        else:
            print("No hay extensiones nuevas que agregar. El router esta al dia")
        
        reporte_estacional(net_connect)

        net_connect.disconnect()
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    configurar_inteligente()



