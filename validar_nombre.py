class RegistroPersona:
    def __init__(self):
        self._nombre = ""

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        nombre_limpio = valor.strip().capitalize()

        if len(nombre_limpio) > 0:
            self._nombre = nombre_limpio
            print(f"Nombre registrado: {self._nombre}")
        else:
            print("Error el nomre no puede quedar vacio")
        
usuario = RegistroPersona()
usuario.nombre = " bebe"
print(f"Resultado en sistema: '{usuario.nombre}'")