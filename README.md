# FeelBack: Aplicación Web Interactiva para Análisis de Sentimientos

**FeelBack** es una aplicación web que combina inteligencia artificial y diseño intuitivo para ofrecer análisis de sentimientos en tiempo real. Los usuarios pueden interactuar con un modelo de aprendizaje automático entrenado con **PyTorch** a través de una interfaz tipo chat, obteniendo clasificaciones emocionales como **positiva**, **negativa** o **neutral**. Además, la aplicación permite a los usuarios gestionar su historial de análisis y explorar sus resultados de manera organizada.

## 🚀 Tecnologías Utilizadas

- **Lenguaje de programación:** Python
- **Framework Backend:** Flask
- **Modelo de ML:** PyTorch
- **Base de datos:** PostgreSQL
- **Contenerización:** Docker y Docker Compose

## 🧩 Funcionalidades Principales

![Funcionalidades Principales](./img/funcionalidades_principales.png)

1. **Gestión de Usuarios**  
   - Sistema de registro e inicio de sesión para proteger los datos personales de cada usuario.
   - Cada usuario tiene acceso a su historial de análisis.

2. **Interacción Conversacional**  
   - Los usuarios pueden escribir comentarios en una interfaz tipo chat y recibir análisis de sentimientos en tiempo real.
   - El modelo de aprendizaje automático clasifica el texto en positivo, negativo o neutral.

3. **Historial Personalizado**  
   - Los usuarios pueden consultar sus análisis previos, filtrarlos por fecha o tipo de sentimiento, y exportarlos en formato CSV.

## 📚 Estructura del Proyecto (Actualizada)

```bash
FeelBack/
├── web_app/                    # Servicio principal: Aplicación web (Frontend + API Backend)
│   ├── app/                    # Código fuente de la aplicación Flask
│   │   ├── api/                # API RESTful: rutas para autenticación, chat y usuario
│   │   ├── auth/               # Módulo de autenticación (formularios, rutas web)
│   │   ├── main/               # Módulo principal (chat, historial, vistas web)
│   │   ├── models/             # Modelos de datos (ORM)
│   │   ├── static/             # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── templates/          # Plantillas HTML (Jinja2)
│   │   ├── utils/              # Utilidades compartidas
│   │   ├── __init__.py         # Inicialización y configuración de la aplicación Flask
│   │   └── config.py           # Configuración general de la aplicación
│   ├── Dockerfile              # Contenedor para la aplicación web
│   ├── migrations/             # Migraciones de base de datos
│   ├── tests/                  # Pruebas unitarias de la API y lógica
│   ├── requirements.txt        # Dependencias de la aplicación web
│   ├── run.py                  # Punto de entrada para ejecutar la aplicación
│   └── setup.py                # Configuración del paquete
├── sentiment_analyzer/         # Microservicio para el modelo de análisis de sentimientos
│   ├── api/                    # Endpoints RESTful para análisis de sentimientos
│   ├── core/                   # Lógica principal del modelo (PyTorch)
│   ├── dev/                    # Archivos de desarrollo (notebooks, pruebas)
│   ├── versions/               # Versiones del modelo (archivos .pt)
│   ├── Dockerfile              # Contenedor para el microservicio
│   ├── requirements.txt        # Dependencias del microservicio
│   ├── run.py                  # Punto de entrada para ejecutar el microservicio
│   └── setup.py                # Configuración del paquete
├── img/                        # Imágenes para documentación
├── docker-compose.yml          # Orquestación de servicios
└── README.md                   # Documentación principal del proyecto
```

### Arquitectura Modular y API

La aplicación está dividida en dos servicios principales:
- **Web App**: Provee tanto la interfaz de usuario como una API RESTful para autenticación, gestión de usuarios, chat y consultas de historial.
- **Sentiment Analyzer**: Microservicio dedicado al análisis de sentimientos, expuesto como API y consumido por la Web App.

Esta separación permite:
- Escalabilidad y despliegue independiente de cada servicio.
- Reutilización del microservicio de análisis por otras aplicaciones.
- Mantenimiento y desarrollo desacoplado.

## 📖 Endpoints de la API (Web App)

A continuación se listan las rutas principales de la API RESTful expuesta por la Web App, agrupadas por funcionalidad:

### Autenticación (`/api/v1/auth`)
- **POST `/register`**: Registra un nuevo usuario.  
  _Body_: username, email, password  
  _Respuesta_: Mensaje de éxito o error.

- **POST `/login`**: Inicia sesión y retorna un token JWT.  
  _Body_: username, password  
  _Respuesta_: token, user_id.

- **POST `/verify-token`**: Verifica la validez de un token JWT.  
  _Body_: token  
  _Respuesta_: Mensaje de validez y user_id.

### Chat y Análisis de Sentimientos (`/api/v1/chat`)
- **POST `/get-sentiment`**: Analiza el sentimiento de un mensaje de texto.  
  _Body_: message  
  _Respuesta_: model_response (texto), id_sentiment (código de sentimiento).

### Gestión de Mensajes e Historial (`/api/v1/user`)
- **POST `/save-message`**: Guarda un mensaje analizado en el historial del usuario.  
  _Body_: user_id, text, id_sentiment, liked  
  _Respuesta_: Mensaje de éxito y id_message.

- **POST `/delete-message`**: Elimina un mensaje del historial del usuario.  
  _Body_: user_id, message_id  
  _Respuesta_: Mensaje de éxito.

- **GET `/get-message`**: Obtiene un mensaje específico del historial.  
  _Body_: user_id, message_id  
  _Respuesta_: Detalles del mensaje.

- **GET `/get-messages`**: Obtiene todos los mensajes del usuario.  
  _Body_: user_id  
  _Respuesta_: Lista de mensajes.

- **GET `/get-stats`**: Obtiene estadísticas de uso y sentimientos del usuario.  
  _Body_: user_id  
  _Respuesta_: Conteo de positivos, negativos, neutrales, likes y dislikes.

### 📝 Notas adicionales

- Todas las rutas protegidas requieren autenticación mediante token JWT en el header `Authorization: Bearer <token>`.

## 🐳 Dockerización

FeelBack está completamente contenerizado para facilitar su despliegue y escalabilidad. Los servicios están orquestados mediante Docker Compose:

```bash
# Construcción de los contenedores
docker-compose build

# Ejecución de los servicios
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
La página de historial proporciona a los usuarios una vista completa de todos sus análisis de sentimientos previos. Implementada con su propia hoja de estilos modular `history.css`, ofrece una interfaz intuitiva y organizada que facilita el seguimiento de la evolución de los comentarios y su clasificación emocional.

![Página historial](./img/pagina_historial.png)

**Componentes principales:**
- **Lista de Análisis**: Registro detallado de todos los comentarios analizados por el usuario, con una presentación clara y estructurada.
- **Clasificación Visual**: Indicadores gráficos que muestran el sentimiento detectado (positivo, negativo, neutral) con colores distintivos para facilitar la interpretación.
- **Fecha y Hora**: Timestamp preciso que permite identificar cuándo se realizó cada análisis.
- **Texto Original**: Visualización completa del comentario analizado, manteniendo la fidelidad al texto ingresado por el usuario.
- **Filtros de Búsqueda**: Herramientas avanzadas para filtrar análisis por fecha, tipo de sentimiento o palabras clave, mejorando la experiencia de navegación.
- **Paginación**: Sistema de navegación eficiente que permite explorar grandes volúmenes de datos históricos sin perder rendimiento.
- **Opciones de Exportación**: Funcionalidad para descargar el historial en formato CSV, facilitando el análisis externo y la integración con otras herramientas.
- **Diseño Modular Responsivo**: Interfaz construida con componentes CSS independientes que se adaptan perfectamente a diferentes tamaños de pantalla, desde móviles hasta pantallas de escritorio.