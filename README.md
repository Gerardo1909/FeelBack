# FeelBack: Aplicación Web Interactiva para Análisis de Sentimientos

**FeelBack** es una aplicación web interactiva desarrollada con Python, cuyo propósito es permitir a los usuarios escribir comentarios o reseñas de texto y obtener un análisis automático de su sentimiento utilizando un modelo de aprendizaje automático entrenado con **PyTorch**. La clasificación del texto puede ser **positiva**, **negativa** o **neutral**.

El sistema incluye autenticación básica para que los usuarios puedan iniciar sesión y visualizar su historial personal de análisis. La interfaz está compuesta por dos vistas principales: un formulario de acceso (login/registro) y una página tipo chat donde se realiza el análisis de sentimientos.

## 🚀 Tecnologías Utilizadas

- **Lenguaje de programación:** Python
- **Framework Backend:** Flask
- **Base de datos:** PostgreSQL
- **Modelo de ML:** PyTorch
- **Contenerización:** Docker, Docker Compose

## 🧩 Funcionalidades Principales

![Funcionalidades Principales](./img/funcionalidades_principales.png)

1. **Registro y Login de Usuarios**
   - Formulario de registro e inicio de sesión.
   - Validación y autenticación básicas para proteger los datos de cada usuario.

2. **Análisis de Sentimientos**
   - Interfaz tipo chat para ingresar comentarios.
   - Modelo entrenado en PyTorch que devuelve una clasificación del sentimiento.

3. **Historial Personal**
   - Cada usuario puede consultar los resultados anteriores de sus análisis.

## 📚 Estructura del Proyecto

```bash
FeelBack/
├── app/
│   ├── __init__.py             # Inicialización y configuración de la aplicación Flask
│   ├── config.py               # Configuración general de la aplicación
│   ├── auth/                   # Módulo de autenticación
│   │   ├── __init__.py         # Inicialización del blueprint de autenticación
│   │   ├── forms/              # Formularios de autenticación
│   │   │   ├── loginform.py    # Formulario de inicio de sesión
│   │   │   └── registerform.py # Formulario de registro
│   │   └── routes/             # Rutas de autenticación
│   │       ├── login.py        # Manejo de inicio de sesión
│   │       ├── logout.py       # Manejo de cierre de sesión
│   │       └── register.py     # Manejo de registro de usuarios
│   ├── main/                   # Módulo principal de la aplicación
│   │   ├── __init__.py         # Inicialización del blueprint principal
│   │   ├── forms/              # Formularios para funcionalidades principales
│   │   │   ├── chatform.py     # Formulario para chat y análisis
│   │   │   └── feedbackform.py # Formulario para retroalimentación
│   │   └── routes/             # Rutas principales
│   │       ├── chat.py         # Manejo del análisis de sentimientos
│   │       ├── history.py      # Vista de historial de análisis
│   │       └── home.py         # Página de inicio y dashboard
│   ├── models/                 # Modelos de datos
│   │   ├── database_schema.sql # Esquema de la base de datos
│   │   ├── message.py          # Modelo para mensajes y análisis
│   │   ├── sentiment.py        # Modelo para resultados de sentimientos
│   │   ├── stats.py            # Modelo para estadísticas
│   │   └── user.py             # Modelo de usuario
│   ├── static/                 # Archivos estáticos
│   │   ├── base.css            # Estilos base compartidos
│   │   ├── auth.css            # Estilos para autenticación
│   │   ├── chat.css            # Estilos para la interfaz de chat
│   │   ├── home.css            # Estilos para la página principal
│   │   ├── history.css         # Estilos para la página de historial
│   │   ├── error.css           # Estilos para páginas de error
│   │   └── img/                # Imágenes y recursos visuales
│   ├── templates/              # Plantillas HTML
│   │   ├── base.html           # Plantilla base con estructura común
│   │   ├── auth/               # Plantillas de autenticación
│   │   │   ├── login.html      # Página de inicio de sesión
│   │   │   └── register.html   # Página de registro
│   │   └── main/               # Plantillas principales
│   │       ├── chat.html       # Interfaz de análisis de sentimientos
│   │       ├── error.html      # Páginas de error
│   │       ├── history.html    # Vista de historial
│   │       └── home.html       # Página de inicio
│   ├── sentiment_analyzer_v/   # Modelos de análisis de sentimientos
│   └── utils/                  # Utilidades y helpers
├── img/                        # Imágenes para documentación
├── migrations/                 # Migraciones de base de datos
├── sentiment_analyzer_dev/     # Desarrollo del modelo de análisis
├── tests/                      # Pruebas unitarias
├── docker-compose.yml          # Configuración de Docker Compose
├── Dockerfile                  # Configuración de imagen Docker
├── README.md                   # Documentación del proyecto
├── requirements.txt            # Dependencias del proyecto
├── run.py                      # Punto de entrada para la app Flask
└── setup.py                    # Configuración del paquete
````

## 📡 Endpoints de la API

### Rutas de Autenticación

| Endpoint           | Método | Descripción                                 |
| ------------------ | ------ | ------------------------------------------- |
| `/auth/login`      | GET    | Muestra el formulario de inicio de sesión   |
| `/auth/login`      | POST   | Procesa el inicio de sesión                 |
| `/auth/register`   | GET    | Muestra el formulario de registro           |
| `/auth/register`   | POST   | Procesa el registro de un nuevo usuario     |
| `/auth/logout`     | GET    | Cierra la sesión del usuario actual         |

### Rutas Principales

| Endpoint           | Método | Descripción                                       |
| ------------------ | ------ | ------------------------------------------------- |
| `/`                | GET    | Página principal/inicio                           |
| `/chat`            | GET    | Muestra la interfaz de análisis de sentimientos   |
| `/chat`            | POST   | Analiza el texto y muestra el resultado           |
| `/feedback`        | POST   | Procesa retroalimentación sobre un análisis       |
| `/history`         | GET    | Muestra el historial de análisis del usuario      |
| `/reset-chat`      | GET    | Reinicia la sesión del chat                       |


## 🐳 Dockerización

El proyecto incluye archivos de configuración para contenerizar la aplicación:

* `Dockerfile`: Define la imagen para el servicio Flask.
* `docker-compose.yml`: Orquesta los servicios Flask y PostgreSQL.

```bash
# Construcción del contenedor
docker-compose build

# Ejecución
docker-compose up
```

## 📷 Capturas de pantalla 

### Página de Inicio

La página de inicio da la bienvenida a los usuarios y presenta de forma clara el propósito de FeelBack. Implementada con un diseño modular y limpio, cuenta con una estructura de CSS separada que facilita su mantenimiento. Incluye un diseño atractivo con colores cálidos, un área visual destacada y botones de acceso rápido para iniciar sesión o registrarse.

![Página de inicio](./img/pagina_inicio.png)

**Componentes principales:**
- **Barra de navegación:** Una navbar limpia y consistente que muestra el logo y nombre de la aplicación, con accesos directos para iniciar sesión o registrarse.
- **Mensaje de bienvenida:** Un encabezado principal con tipografía moderna que explica brevemente la funcionalidad del sistema y motiva al usuario a interactuar.
- **Ilustración central:** Imagen representativa de la interacción entre un usuario y un robot, con animaciones sutiles que refuerzan el enfoque en el análisis de sentimientos mediante IA.
- **Botón de acción principal:** Un llamado a la acción prominente con efectos visuales al pasar el cursor, que permite comenzar a chatear y analizar sentimientos de inmediato.
- **Diseño modular y responsivo:** Estructura basada en componentes CSS individuales que se adaptan a diferentes dispositivos para una experiencia de usuario óptima.

### Página de Inicio de Sesión
La página de inicio de sesión presenta la interfaz de autenticación donde los usuarios pueden iniciar sesión. Implementada con su propia hoja de estilos modular `auth.css`, ofrece un diseño minimalista y elegante con animaciones sutiles en los campos de entrada y botones. Incluye formularios intuitivos con validación de campos y un diseño limpio que facilita el acceso al sistema.

![Página inicio](./img/pagina_login.png)

**Componentes principales:**
- **Formulario de Login**: Campos para email y contraseña con validación en tiempo real, efectos visuales de foco y animaciones de transición.
- **Barra de navegación consistente**: Mantiene la identidad visual de la aplicación con el logo y nombre de la marca.
- **Mensajes Flash**: Sistema integrado para mostrar notificaciones de error o éxito con animaciones suaves.
- **Validación**: Mensajes de error intuitivos y confirmación visual para guiar al usuario durante el proceso.
- **Diseño Modular Responsivo**: Interfaz construida con componentes CSS independientes que se adaptan perfectamente a diferentes tamaños de pantalla, desde móviles hasta pantallas de escritorio.

### Página de Registro
La página de registro permite a los nuevos usuarios crear una cuenta en el sistema FeelBack. Desarrollada con la misma arquitectura modular CSS que la página de inicio de sesión, presenta un formulario claro y estructurado con microinteracciones y validaciones en tiempo real que mejoran la experiencia de usuario durante el proceso de registro.

![Página registro](./img/pagina_registro_cuenta_nueva.png)

**Componentes principales:**
- **Formulario de Registro Optimizado**: Campos específicos para crear una cuenta nueva (nombre, email, contraseña) con etiquetas flotantes y animaciones de transición al completar cada campo.
- **Validación de Datos Interactiva**: Verificación en tiempo real de formato de email y fortaleza de contraseña con indicadores visuales de progreso y sugerencias.
- **Términos y Condiciones**: Checkbox personalizado con estilos consistentes para aceptar los términos de uso del servicio.
- **Botón de Creación**: Elemento visual destacado con efectos de hover y transición que indica claramente la acción principal para completar el proceso de registro.
- **Navegación Intuitiva**: Enlaces contextuales con estilos consistentes para volver al formulario de inicio de sesión o acceder a información adicional.

### Página de Interacción
La página principal de la aplicación presenta una interfaz tipo chat moderna inspirada en los mejores diseños de plataformas de IA conversacional. Implementada con su propio archivo modular `chat.css`, ofrece una experiencia de usuario fluida y natural con un área de conversación de tamaño fijo y desplazamiento interno, similar a plataformas como ChatGPT.

![Página interacción](./img/pagina_interaccion.png)

**Componentes principales:**
- **Área de Chat Fija con Scroll Interno**: Interfaz conversacional con altura fija que permite mantener un diseño consistente mientras el historial de chat crece, con desplazamiento automático a nuevos mensajes.
- **Burbujas de Chat Distintivas**: Diseño asimétrico que diferencia claramente los mensajes del usuario (gris oscuro, alineados a la derecha) de las respuestas del sistema (blancas con borde, alineadas a la izquierda).
- **Indicadores de Sentimiento Visuales**: Sistema de feedback con iconos intuitivos (pulgar arriba/abajo) que permiten valorar la precisión del análisis, con estados visuales para indicar la selección actual.
- **Campo de Entrada Flotante**: Área de texto moderna con bordes redondeados y sombreado sutil, separada visualmente del área de chat pero integrada en el diseño general.
- **Botones de Acción Circulares**: Controles intuitivos para enviar mensajes y reiniciar la conversación, con efectos de hover y transición.
- **Navegación Contextual**: Accesos directos en la barra superior para gestionar la sesión y acceder a otras funcionalidades clave del sistema.


### Página de Historial
La página de historial proporciona a los usuarios una vista completa de todos sus análisis de sentimientos previos. Esta interfaz permite revisar el progreso temporal y las tendencias en los análisis realizados, facilitando el seguimiento de la evolución de los comentarios y su clasificación emocional.

![Página historial](./img/pagina_historial.png)

**Componentes principales:**
- **Lista de Análisis**: Registro de todos los comentarios analizados por el usuario
- **Clasificación Visual**: Indicadores claros del sentimiento detectado (positivo, negativo, neutral)
- **Fecha y Hora**: Timestamp preciso de cada análisis realizado
- **Texto Original**: Muestra completa del comentario que fue analizado
- **Filtros de Búsqueda**: Herramientas para filtrar análisis por fecha o tipo de sentimiento
- **Paginación**: Navegación eficiente para grandes volúmenes de datos históricos
- **Opciones de Exportación**: Posibilidad de descargar el historial en formato CSV