```markdown
# Francesco Boito

## Bienvenido a mi proyecto

### Pasos de instalación

1. Clonar el repositorio
    ```bash
    git clone https://github.com/franb0/etec-pi-2024-backend-franb0.git
    ```

2. Ir al directorio del proyecto
    ```bash
    cd etec-pi-2024-backend-franb0
    ```

3. Ejecutar Docker Compose (importante que sea por separado)
    ```bash
    docker compose up --build mysql

    docker compose up --build app
    ```

Utiliza la IP del contenedor para probar las conexiones. El puerto 3000 está asignado al servidor.

¡Y eso es todo! Ahora tu proyecto debería estar funcionando.

### Testeo del Proyecto

Puedes probar el funcionamiento del proyecto utilizando herramientas como Postman o cURL. A continuación, se muestran algunos ejemplos de solicitudes HTTP que puedes realizar:

#### Obtener todos los usuarios

```http
GET http://localhost:3000/users HTTP/1.1
```

#### Obtener un usuario específico

```http
GET http://localhost:3000/users/1 HTTP/1.1
```

#### Crear un nuevo usuario

```http
POST http://localhost:3000/users HTTP/1.1
Content-Type: application/json

{
  "name": "John",
  "email": "a@a.com",
  "password": "1234"
}
```

#### Actualizar un usuario existente

```http
PUT http://localhost:3000/users/1 HTTP/1.1
Content-Type: application/json

{
  "name": "Jane",
  "email": "b@b.com",
  "password": "4321"
}
```

#### Eliminar un usuario

```http
DELETE http://localhost:3000/users/1 HTTP/1.1
```

