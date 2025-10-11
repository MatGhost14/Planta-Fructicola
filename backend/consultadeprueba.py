import requests # importa la librería requests para hacer solicitudes HTTP

# Define la URL base de la API
API = "http://127.0.0.1:8000"

# Función para iniciar sesión y obtener un token de acceso
def login(email, password):
    r = requests.post(f"{API}/auth/login", json={"email": email, "password": password}, timeout=10)# Realiza una solicitud POST a la ruta de login con el correo y la contraseña proporcionados
    r.raise_for_status()# Lanza una excepción si la solicitud no fue exitosa
    return r.json()# Devuelve la respuesta en formato JSON

# Función para obtener información del usuario autenticado usando el token de acceso
def me(token):# Realiza una solicitud GET a la ruta de "me" con el token de acceso en los encabezados
    r = requests.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {token}"}, timeout=10)# Lanza una excepción si la solicitud no fue exitosa
    r.raise_for_status()# Devuelve la respuesta en formato JSON
    return r.json()# Devuelve la respuesta en formato JSON



# Bloque principal para ejecutar el código de prueba
if __name__ == "__main__":
    data = login("usuariodeprueba@gmail.com", "123456")# Inicia sesión con un correo y contraseña de prueba
    print(me(data["token"]["access_token"]))# 
