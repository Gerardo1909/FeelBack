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

## 📚 Estructura del Proyecto

```bash
FeelBack/
├── web_app/                    # Servicio principal: Aplicación web
│   ├── app/                    # Código fuente de la aplicación Flask
│   │   ├── auth/               # Módulo de autenticación
│   │   ├── main/               # Módulo principal (chat, historial, etc.)
│   │   ├── models/             # Modelos de datos
│   │   ├── static/             # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── templates/          # Plantillas HTML
│   │   ├── utils/              # Utilidades compartidas
│   │   ├── __init__.py         # Inicialización y configuración de la aplicación Flask
│   │   └── config.py           # Configuración general de la aplicación
│   ├── Dockerfile              # Contenedor para la aplicación web
│   ├── .dockerignore            
│   ├── migrations              # Migraciones de base de datos
│   ├── tests                   # Pruebas unitarias            
│   ├── requirements.txt        # Dependencias de la aplicación web
│   ├── run.py                  # Punto de entrada para ejecutar la aplicación
│   └── setup.py                # Configuración del paquete
├── sentiment_analyzer/         # Microservicio para el modelo de análisis
│   ├── api/                    # Endpoints RESTful para análisis de sentimientos
│   ├── core/                   # Lógica principal del modelo (PyTorch)
│   ├── dev/                    # Archivos de desarrollo (notebooks, pruebas)
│   ├── versions/               # Versiones del modelo (archivos .pt)
│   ├── Dockerfile              # Contenedor para el microservicio
│   ├── .dockerignore            
│   ├── requirements.txt        # Dependencias del microservicio
│   ├── run.py                  # Punto de entrada para ejecutar el microservicio
│   └── setup.py                # Configuración del paquete
├── img/                        # Imágenes para documentación
├── .gitignore                  
├── docker-compose.yml          # Orquestación de servicios
└── README.md                   # Documentación principal del proyecto
```

### Arquitectura Modular

La decisión de dividir la aplicación en servicios independientes responde a la necesidad de mantener una estructura organizada, escalable y fácil de mantener. Esta arquitectura modular permite separar las responsabilidades de cada componente, lo que impacta positivamente en varios aspectos de la aplicación:

1. **Separación de responsabilidades**:
   - **Web App**: Se encarga de la interacción con el usuario, gestionando las vistas, la autenticación y el historial de análisis.
   - **Sentiment Analyzer**: Se dedica exclusivamente al procesamiento de datos y análisis de sentimientos, exponiendo una API que puede ser utilizada por la aplicación web u otros clientes en el futuro.

2. **Escalabilidad**:
   - Al estar dividida en servicios, cada componente puede ser escalado de forma independiente según las necesidades. Por ejemplo, el microservicio de análisis de sentimientos puede ser replicado para manejar un mayor volumen de solicitudes sin afectar la aplicación web.

3. **Mantenimiento**:
   - La separación de lógica facilita el mantenimiento del código, ya que los cambios en un servicio no afectan directamente a los demás.
   - Los desarrolladores pueden trabajar en diferentes servicios de forma simultánea sin interferencias.

4. **Reutilización**:
   - El microservicio de análisis de sentimientos puede ser reutilizado por otras aplicaciones o integraciones externas, lo que amplía el alcance del proyecto.

5. **Despliegue independiente**:
   - Gracias a la contenerización con Docker, cada servicio puede ser desplegado de forma independiente, lo que simplifica el proceso de despliegue y actualización.

Esta arquitectura modular no solo mejora la organización del proyecto, sino que también prepara la aplicación para crecer y adaptarse a nuevas necesidades en el futuro.

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