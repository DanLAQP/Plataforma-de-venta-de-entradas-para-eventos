import requests

BASE_URL = "http://127.0.0.1:5000" 

def probar_seguridad():
    #caso 1 de validacion de recursos existentes get 404
    res_1 = requests.get(f"{BASE_URL}/api/events/999")    
    print(f"Buscamos un evento inexistente, (ID : 999)): {res_1.status_code}")
    assert res_1.status_code == 404, f"Expected 404, got {res_1.status_code}"

    #caso 2 de validacion de datos incompletos en compra de boletos post 400
    datos_incompletos = {
        "evento_id": 1,
        "asientos": ["A1", "A2"]
    }
    res_2 = requests.post(f"{BASE_URL}/api/compras", json=datos_incompletos)
    print(f"Enviamos datos incompletos en la compra de boletos: {res_2.status_code}")
    assert res_2.status_code == 400, f"Expected 400, got {res_2.status_code}"

    #caso 3 de validacion de tipos de datos incorrectos post 400
    datos_incorrectos = {
        "evento_id": "uno",  # debería ser un entero
        "nombre": "Gordon Shomguey",
        "correo": "alf@gmail.com",
        "asientos": "A1, A2"  
    }
    res_3 = requests.post(f"{BASE_URL}/api/compras", json=datos_incorrectos)
    print(f"Enviamos datos con tipos incorrectos: {res_3.status_code}")
    assert res_3.status_code == 400, f"Expected 400, got {res_3.status_code}"

    #caso 4 metodos HTTP no permitidos (PATCH o POST endpoints bloqueados) 405
    res_4 = requests.patch(f"{BASE_URL}/api/eventos/1/asientos")
    print(f"Intentamos usar un método HTTP no permitido: {res_4.status_code}")
    assert res_4.status_code == 405, f"Expected 405, got {res_4.status_code}"

if __name__ == "__main__":
    probar_seguridad()
    print("Todas las pruebas de seguridad pasaron exitosamente.")   