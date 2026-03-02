class CuentaBebe:
    def __init__(self, saldo_inicial):
        self._saldo = saldo_inicial
    
    @property
    def saldo(self):
        return f"${self._saldo:,.2f}"

    @saldo.setter
    def saldo(self, monto_nuevo):

        if monto_nuevo < 0:
            return
        self._saldo = monto_nuevo

        if self._saldo < 20:
            print("ALERTA: el sado de la bebe es bajo (menor a $20)")

        else:
            print("Saldo actualizado con exito")
    

    """
        if monto_nuevo >= 0:
            self._saldo = monto_nuevo
            print("Saldo actualizado con exito")
        else:
            print("Error: Fondos Insuficientes. No puedes quedar en negativo.")
    """
mi_cuenta = CuentaBebe(100)

print(f"Saldo inicial {mi_cuenta.saldo}")

mi_cuenta.saldo = 19
print(f"Nuevo saldo: {mi_cuenta.saldo}")


