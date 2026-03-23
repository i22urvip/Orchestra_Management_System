# Gestión de Catálogo Musical (Orquesta)

Una aplicación web desarrollada en **Django** para gestionar el catálogo de obras y compositores de una orquesta. Este proyecto permite mantener un registro detallado del repertorio musical, con control de acceso y roles de usuario.

## Características Principales

* **Catálogo de Obras:** Visualización detallada del repertorio (título, duración, instrumentos, partitura).
* **Rocola Interactiva:** Reproductor multimedia inmersivo para escuchar las pistas de audio asociadas a las obras.
* **Buscador y Filtros:** Herramientas para localizar obras rápidamente por título, compositor o género.
* **Gestión de Compositores y Obras (CRUD):** Creación, lectura, edición y asociación de compositores a sus respectivas obras.
* **Sistema de Usuarios:** Registro e inicio de sesión de usuarios mediante formularios personalizados y limpios.
* **Seguridad y Roles:** Rutas protegidas para usuarios registrados y permisos exclusivos de Administrador (ej. borrado definitivo de compositores).
* **Base de Datos en la Nube:** Conectado a PostgreSQL a través de Neon.tech.

## Tecnologías Utilizadas

* **Backend:** Python 3.12, Django 6.0
* **Base de Datos:** PostgreSQL (Neon)
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Tarjetas, Formularios, Alertas), JavaScript (Audio API)
* **Entorno:** GitHub Codespaces / Entorno Local Windows/Mac

## Instalación y Ejecución Local

Sigue estos pasos para configurar y arrancar el proyecto en tu propio equipo:

### 1. Clonar el repositorio
Descarga el código fuente en tu ordenador y entra en la carpeta del proyecto:
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO
```
### 2. Crear y activar el entorno virtual
Es fundamental aislar las dependencias del proyecto.

En Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```
En macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
Con el entorno virtual activado (deberías ver (venv) a la izquierda en tu terminal), instala todas las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que el archivo manage.py). Abre el archivo y añade tus credenciales privadas con este formato:

* ***Fragmento de código:***
DATABASE_URL=postgres://usuario:contraseña@servidor_neon.tech/nombre_bd

### 5. Aplicar las migraciones
Sincroniza el código con la base de datos para crear todas las tablas necesarias (usuarios, obras, compositores):

```bash
python manage.py migrate
```

### 6. Crear un usuario administrador (Recomendado)
Para poder acceder al panel de administración de Django y tener control total sobre el catálogo, crea un superusuario:

```bash
python manage.py createsuperuser
```

### 7. Arrancar el servidor
Inicia el servidor de desarrollo local de Django:

```bash
python manage.py runserver
```

### 8. Acceder a la aplicación
Abre tu navegador web y visita la siguiente dirección:
http://127.0.0.1:8000/

Estructura de Directorios y Ficheros
El proyecto "El Rincón del Músico" sigue de forma estricta la arquitectura MVT (Modelo-Vista-Plantilla) propia del framework Django. Cada archivo tiene una única responsabilidad para mantener el código limpio y escalable.

```bash
Gesti-n-musical/
├── .env
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── venv/
├── docs/
│   └── avances/
│       ├── semana-01.md
│       └── semana-02.md
├── media/
│   ├── audios/
│   └── partituras/
├── orquesta/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── catalogo/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── catalogo/
```
### 1. La Raíz del Proyecto
Contiene los archivos de configuración general y el entorno de ejecución que hacen que todo el sistema funcione.

* **manage.py**: Es el script principal de Django y el punto de entrada.

* **.env e .gitignore**: Archivos para proteger variables de entorno y evitar subir carpetas basura (como el entorno virtual) al repositorio.

* **requirements.txt**: Detalla las librerías necesarias (Django, psycopg2, python-dotenv...).

* **docs/**: Almacena la documentación del proyecto y la evolución del mismo por semanas.

### 2. Archivos Multimedia: media/
Es el almacén físico de la aplicación. Gracias a la configuración del proyecto, Django guarda automáticamente aquí los archivos que suben los usuarios (como los MP3 en audios/ y los PDFs en partituras/), en lugar de sobrecargar la base de datos.

### 3. Directorio de Configuración: orquesta/
Es el núcleo central que administra el comportamiento global de la aplicación web.

* **settings.py**: Configuración de base de datos, variables de entorno, idiomas y gestión de archivos multimedia.

* **urls.py**: Enrutador principal que intercepta las peticiones web entrantes y las redirige a la aplicación correspondiente.

### 4. Aplicación Principal: catalogo/
Contiene el 90% de nuestro código y representa la lógica de negocio de la aplicación.

* **models.py**: Define la estructura de la base de datos (Entidades Compositor y Obra).

* **views.py**: El puente de comunicación. Extrae información de los Modelos y se la entrega a las Plantillas.

* **forms.py**: Gestiona la validación y creación de los formularios web (añadir obras, registro de usuarios).

* **urls.py**: Asocia rutas específicas (ej. /obras/) con sus vistas correspondientes.

* **templates/catalogo/**: Directorio que almacena los archivos HTML, aplicando Bootstrap 5 para el diseño de la interfaz visual.
