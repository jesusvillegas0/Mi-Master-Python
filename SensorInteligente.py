class SensorIteligente:
    def __init__(self):
        self._temperatura = 24.0

    @property
    def temperatura(self):
        return round(self._temperatura, 1)
    
    @temperatura.setter
    def temperatura(self, nuevo_valor):
        if 15 <= nuevo_valor <= 45:
            print(f"Exito: Guardando {nuevo_valor}°C en la base de datos")
            self._temperatura = nuevo_valor
        else:
            print(f"Error {nuevo_valor}°C es una temperatura imposible o peligrosa. Registro bloqueado.")


mi_sensor = SensorIteligente()

print("--- Sistema de Monitoreo ---")
print("Escribe 'salir' para terminar")

while True:
    entrada = input("\nIngresa la temperatura actual: ").capitalize()

    if entrada.lower() == 'salir':
        print("Cerrando sistema de seguridad, Adios!")
        break
    try:
        valor_numerico = float(entrada)

        mi_sensor.temperatura = valor_numerico

        print(f"Estado actual del sensor: {mi_sensor.temperatura}°C")
    except ValueError:
        print("Por favor, introduce un numero valido o escribe 'salir'")

