# **📄 ProjectManagementPF - Gestión de Productos con Django**

Una aplicación web basada en Django para la gestión de productos con categorías, imágenes y una interfaz responsiva gracias a Bootstrap. Sigue buenas prácticas de estructura, control de versiones, pruebas, documentación y despliegue continuo.

🔗 **App en vivo:** [https://projectmanagementpf.onrender.com](https://projectmanagementpf.onrender.com) 🛠 \*\*CI/CD:\*\*GitHub Actions (pruebas con PostgreSQL) 📅 **Última actualización:** 2025-06-22 👥 **Equipo:** `TeamLeadGPT` – Senior Dev & Tech PM

---

## **📂 Estructura de Carpetas y Archivos**

```
ProjectManagementPF/
├── .github/                        # Configuraciones de GitHub (workflows, PR templates, etc.)
├── config/                         # Configuración global del proyecto Django
├── core/                           # App principal para vistas generales y página de inicio
│   ├── migrations/                 # Migraciones de base de datos para core
│   ├── templates/
│   │   └── core/
│   │       └── home.html          # Página principal del sitio
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── fixtures/                      # Datos de prueba en formato JSON
├── htmlcov/                       # Reportes de cobertura de pruebas
├── libretranslate/                # Integración o cliente para traducción de textos
├── locale/                        # Archivos de internacionalización (i18n)
│   └── es/
│       └── LC_MESSAGES/
│           ├── django.po         # Archivo de traducción editable (mensajes en español)
│           └── django.mo         # Archivo compilado para uso por Django
├── media/                         # Archivos multimedia subidos por usuarios (productos)
├── orders/                        # App para gestionar pedidos de usuarios
│   ├── migrations/                # Migraciones de base de datos para orders
│   ├── __init__.py
│   ├── admin.py                   # Panel de administración para pedidos y items
│   ├── apps.py                    # Configuración y verbose_name traducible
│   ├── forms.py                   # Formularios personalizados (ej. OrderItemInlineForm)
│   ├── models.py                  # Modelos: Order y OrderItem, soporte multiidioma
│   ├── tests.py                   # Pruebas unitarias para pedidos
│   └── views.py                   # Vistas (próximamente: historial, detalle, gestión)
├── products/                      # App principal para la gestión de productos y categorías
│   ├── migrations/                # Migraciones de base de datos para products
│   ├── static/
│   │   └── products/             # Archivos estáticos específicos de productos (CSS, JS, imágenes)
│   ├── templates/
│   │   └── products/
│   │       ├── _product-card.html # Partial: tarjeta para vista en cuadrícula
│   │       ├── product-detail.html # Detalle de un producto individual
│   │       └── product-list.html # Listado de productos
│   ├── __init__.py
│   ├── admin.py                  # Registro de modelos en panel de administración
│   ├── apps.py                   # Configuración de la app, incluye verbose_name traducible
│   ├── models.py                 # Modelos de producto y categoría
│   ├── tests.py                  # Pruebas unitarias de productos
│   ├── translation.py            # Configuración de traducción para campos de modelo
│   ├── urls.py                   # Rutas de productos (lista y detalle)
│   └── views.py                  # Vistas basadas en clase para productos
├── static/                       # Archivos estáticos globales (CSS, JS, img)
│   ├── css/
│   │   └── product.css           # Estilos personalizados para productos
│   ├── img/
│   │   ├── defaults/
│   │   │   └── no-image-available.png # Imagen por defecto si no hay imagen del producto
│   │   ├── favicon.ico           # Icono del sitio web
│   │   └── logo.png              # Logotipo principal del sitio
├── staticfiles/                  # Carpeta generada para deploy (collectstatic)
├── templates/                    # Plantillas HTML globales
│   ├── components/
│   │   ├── footer.html           # Pie de página reutilizable
│   │   ├── messages.html         # Mensajes del sistema (éxito, error, etc.)
│   │   ├── navbar.html           # Barra de navegación principal
│   │   └── base.html             # Plantilla base principal del sitio
├── users/                        # App para gestión de usuarios (login, perfiles, etc.)
│   ├── migrations/               # Migraciones de base de datos para users
│   ├── __init__.py
│   ├── admin.py                  # Administración del modelo CustomUser en el panel admin
│   ├── apps.py                   # Configuración y verbose_name traducible de la app
│   ├── managers.py               # Manager personalizado para crear usuarios y superusuarios
│   ├── models.py                 # Modelo CustomUser basado en AbstractBaseUser
│   ├── tests.py                  # Pruebas unitarias relacionadas con usuarios
│   └── views.py                  # Vistas para funcionalidades de usuario
├── utils/                        # Funciones auxiliares o servicios comunes
├── .coverage                     # Archivo de cobertura de pruebas
├── .env                          # Variables de entorno (Django secret, DB, etc.)
├── .gitignore                    # Archivos ignorados por Git
├── db.sqlite3                    # Base de datos local SQLite
├── Django_secret_key_for_render # Clave secreta usada en despliegue con Render
├── identifier.sqlite             # Posible BD auxiliar (traducciones o tests)
├── manage.py                     # Comando principal para gestionar Django
├── README.md                     # Documentación inicial del proyecto
├── requirements.txt              # Dependencias del proyecto
├── tareas_semanales.md           # Planificación de tareas y progreso
└── translate_data.py             # Script para traducir datos utilizando libretranslate
```


---

### 🛠️ Personalizaciones importantes en `config/settings.py`

Este informe resume cuidadosamente todas las configuraciones personalizadas o adaptadas en el archivo `settings.py` del proyecto, más allá de la configuración por defecto generada por Django.

---

#### 🔐 Seguridad y entorno

- \*\*Claves sensibles desde \*\*\`\`:
  ```
  from decouple import config
  SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key')
  DEBUG = config('DEBUG', default=False, cast=bool)
  ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

  ```
  > Se utiliza `python-decouple` para proteger datos sensibles mediante variables de entorno. Esto facilita el cambio entre entornos local y producción.

---

#### 📊 Logging personalizado

- **Sistema de ****\`\`**** avanzado activado**:
  ```
  LOGGING = {
      'version': 1,
      'handlers': {
          'console': {
              'class': 'logging.StreamHandler',
              'stream': sys.stdout,
              'formatter': 'verbose',
          },
      },
      'formatters': {
          'verbose': {
              'format': '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
          },
      },
      'root': {
          'handlers': ['console'],
          'level': 'DEBUG',
      },
  }

  ```
  > Se activan logs detallados por consola, útiles para depurar durante el desarrollo.

---

#### 🗃️ Base de datos condicional (PostgreSQL o SQLite)

- **Conmutación dinámica entre SQLite y PostgreSQL**:
  ```
  USE_POSTGRES = config('USE_POSTGRES', default=False, cast=bool)

  ```
  Si `USE_POSTGRES=True` se cargan parámetros desde `.env` para PostgreSQL, de lo contrario se utiliza SQLite local.

---

#### 👤 Usuario personalizado

- **Uso de modelo de usuario propio**:
  ```
  AUTH_USER_MODEL = 'users.CustomUser'

  ```
  El modelo de usuario ha sido redefinido para permitir autenticación basada en email y más control sobre los campos.

---

#### 🌍 Internacionalización (i18n)

- **Idioma por defecto y soporte multilingüe**:
  ```
  LANGUAGE_CODE = 'en-en'
  LANGUAGES = (
      ('en', 'English'),
      ('es', 'Spanish'),
  )
  LOCALE_PATHS = [ BASE_DIR / 'locale' ]
  MIDDLEWARE += ['django.middleware.locale.LocaleMiddleware']

  ```
  > Se ha activado el sistema de traducciones de Django para manejar múltiples idiomas en el sitio web.

---

#### 🧩 Aplicaciones instaladas (INSTALLED\_APPS)

Incluye:

- `modeltranslation`: traducción automática de campos en modelos.
- `products.apps.ProductsConfig`: configuración personalizada con `verbose_name`, `ready()` y traducciones.
- `users`: con `CustomUser`.
- `orders`, `core`: apps personalizadas del proyecto.

---

#### ⚙️ Middleware extra

- `whitenoise.middleware.WhiteNoiseMiddleware`: para servir archivos estáticos comprimidos en producción.
- `django.middleware.locale.LocaleMiddleware`: activa idioma según preferencia del navegador del usuario.

---

#### 📁 Archivos estáticos y medios

- **Configuración clara y adaptada al despliegue**:
  ```
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [BASE_DIR / 'static']
  STATIC_ROOT = BASE_DIR / 'staticfiles'

  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

  ```
  > Se configura `WhiteNoise` para servir archivos estáticos comprimidos y versionados.

---

#### 🧱 TEMPLATES: Procesadores personalizados

- Se incluye `core.context_processors.global_categories`, lo que sugiere que las categorías de productos se cargan globalmente en los templates.

---

#### 🔑 Primary key personalizada

- Uso de campos `BigAutoField` por defecto:
  ```
  DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

  ```
  > Ideal para bases de datos grandes, previene desbordamiento de claves primarias.

---

¿Deseas extender este informe incluyendo el bloque de `TEMPLATES`, validadores de contraseña o configuración WSGI? Puedo añadirlo si quieres documentar al máximo esta configuración.



# 📦Aplicaciones y funcionalidades 


##  Actualización de desarrollo: Gestión de Pedidos (`orders`) en Django



---

## 🟢 Resumen de mejoras implementadas

Durante esta jornada se han introducido optimizaciones clave en la app `orders` enfocadas en:

- La definición de modelos robustos y multilanguage.
- Un panel de administración seguro y cómodo.
- Control granular de permisos y edición.
- Mejoras UX para la gestión de productos en cada pedido.

---

### 🔧 Modelos y migraciones
- Se han definido los modelos `Order` y `OrderItem` con soporte para multiidioma (`gettext_lazy`).
- Métodos auxiliares como `get_total()` para pedidos y `get_total_price()` para cada item.
- Se gestionó la rama `feature/orders` y se integraron migraciones iniciales controladas.

### 🛡️ Panel de administración
- Se registraron ambos modelos y se personalizó la presentación con columnas y filtros útiles.
- Se implementó el filtrado y traducción del estado de cada pedido.

### 🚀 Git y flujo de trabajo
- Se limpiaron los commits históricos.
- Se estructuró la rama de trabajo y el flujo de versiones (naming y PRs).

---

## 💡 Optimización de usabilidad en el admin

### Problemas identificados
- El selector de producto en los `OrderItem` era poco informativo.

### Solución aplicada
- Se personalizó el `OrderItemInline` mediante un formulario que muestra: `Nombre (ID, Categoría)`.
- El desplegable de productos ahora es mucho más claro y práctico para el administrador.

### Siguiente nivel (propuesto)
- Añadir filtrado dinámico por categoría (campos encadenados tipo smart-selects).

---

## ⚙️ Control de permisos y edición avanzada

- El campo **usuario** del pedido es siempre solo lectura (tanto creación como edición).
- El campo **status** siempre editable, para permitir avanzar el estado desde el admin.
- Los **OrderItems** solo son editables si el pedido está pendiente; en cualquier otro estado son solo lectura (ni añadir, ni modificar, ni borrar).
- La lógica del admin garantiza que cualquier pedido es accesible (puede verse y auditarse), pero solo los pendientes se pueden modificar.

### Extracto del código implementado

```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class ReadOnlyOrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete = False
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    def has_add_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'calculated_total')
    list_filter  = ('status', 'created_at')
    search_fields = ('user__email',)
    def get_inline_instances(self, request, obj=None):
        if obj and obj.status != 'pendiente':
            return [ReadOnlyOrderItemInline(self.model, self.admin_site)]
        return [OrderItemInline(self.model, self.admin_site)]
    def get_readonly_fields(self, request, obj=None):
        return ('user', 'transaction_id', 'created_at')
    def has_change_permission(self, request, obj=None):
        return True
```

---

## 🏁 Resultado final
- Gestión profesional y segura de pedidos en el admin.
- Menos errores humanos y máxima trazabilidad.
- UX mejorada para los usuarios responsables de pedidos.
- Base sólida para añadir vistas y funcionalidades públicas/privadas en próximos sprints.




## **📊 Módulos y Bibliotecas y paquetes**

### 📦 Dependencias del proyecto (`requirements.txt`)

A continuación se describen los paquetes instalados hasta ahora para el desarrollo, prueba, despliegue y funcionamiento general del proyecto:

#### 🧱 Núcleo del framework

- **Django==5.2.3**: Framework principal del proyecto. Permite la creación de modelos, vistas, rutas, sistema de autenticación y panel de administración.
- **asgiref==3.8.1**: Componente esencial para el soporte de ASGI en Django, habilita funcionalidades asíncronas.
- **sqlparse==0.5.3**: Analizador y formateador de sentencias SQL, utilizado internamente por Django.

#### 🌍 Internacionalización y traducción

- **django-modeltranslation==0.19.16**: Permite traducir dinámicamente los campos de los modelos a múltiples idiomas, integrándose con el admin.

#### 🌐 Cliente HTTP y dependencias relacionadas

- **requests==2.32.4**: Biblioteca HTTP robusta para consumir APIs externas como LibreTranslate.
- **certifi==2025.7.14**: Certificados raíz utilizados para validar conexiones HTTPS seguras.
- **charset-normalizer==3.4.2**: Detecta y normaliza codificaciones de texto en respuestas HTTP.
- **idna==3.10**: Soporte para dominios internacionalizados en URLs.
- **urllib3==2.5.0**: Cliente HTTP de bajo nivel, utilizado internamente por `requests`.

#### 🖼️ Multimedia y archivos

- **pillow==11.2.1**: Biblioteca de manipulación de imágenes en Python. Se usa para campos `ImageField` en productos.

#### 🧪 Testing y calidad de código

- **coverage==7.9.1**: Herramienta para medir el porcentaje de código cubierto por pruebas unitarias.

#### 🔐 Configuración y entorno

- **python-decouple==3.8**: Separa parámetros de configuración del código fuente mediante archivos `.env`, mejorando la seguridad y la portabilidad.
- **packaging==25.0**: Utilidad para manejar versiones y comparaciones de paquetes. Dependencia auxiliar.

#### 🚀 Despliegue en producción

- **gunicorn==23.0.0**: Servidor WSGI ligero y eficiente para ejecutar Django en producción.
- **psycopg2-binary==2.9.10**: Adaptador de base de datos PostgreSQL requerido para producción y CI.
- **whitenoise==6.9.0**: Middleware que permite servir archivos estáticos directamente desde Django, útil cuando no hay un servidor como Nginx.

> Todos estos paquetes están definidos con versión fija para asegurar reproducibilidad entre entornos de desarrollo, CI y despliegue.

##

### **♻️ Backend**

- **Django**: Framework principal para desarrollo web.



### 🌐 Traducción con gettext / locale

Se utilizó el sistema estándar de traducción de Django mediante `gettext` y la estructura `locale/`, que permite internacionalizar textos en la aplicación de forma limpia y modular.

Los archivos de idioma se almacenan en la siguiente estructura de carpetas:

```
locale/
└── es/
    └── LC_MESSAGES/
        ├── django.po   # Archivo fuente con traducciones editables
        └── django.mo   # Archivo compilado que Django utiliza
```

El archivo `.po` se edita manualmente con los textos traducidos, y luego se compila al formato `.mo` mediante el comando `django-admin compilemessages`, necesario para que Django lo utilice en tiempo de ejecución.

-
  - Comandos para gestionar las traducciones:
  - Generar archivo con todos los textos marcados para traducción: `django-admin makemessages -l es`
  - Compilar las traducciones al archivo `.mo` (obligatorio para que Django las use): `django-admin compilemessages`
- **modeltranslation**: Se emplea para traducir dinámicamente campos de modelos (`name`, `description` en `Product` y `Category`). La configuración se encuentra en `products/translation.py`, y se registra automáticamente en `apps.py` mediante `import products.translation` en el método `ready()`.
- **libretranslate**: API externa para traducción automática de contenidos dinámicos o scripts de utilidad (`translate_data.py`).

### **🔧 Herramientas y desarrollo**

- **Git**: Control de versiones con flujo de trabajo por ramas (`main`, `develop`, `feature/*`).
- **GitHub**: Alojamiento del repo y revisión de Pull Requests.
- **unittest**: Pruebas unitarias.
- **coverage**: Generación de reportes de cobertura de tests.
- **GitHub Actions**: CI automatizada para tests con PostgreSQL.
- **python-decouple**: Para manejo seguro de variables de entorno.

### **🌐 Frontend**

- **Bootstrap**: Framework CSS responsivo.
- **FontAwesome**: Iconos vectoriales.
-

### **🔧 Otros**

- **dotenv**: Uso de `.env` para variables sensibles.
- **faker** (plan futuro): Generación de datos de prueba.
- **gunicorn, psycopg2**: Despliegue en Render con PostgreSQL.

---

## **4. Documentar archivos**

### Archivo: `.env`

Contiene variables de entorno sensibles y de configuración, usadas tanto en desarrollo local como en producción (por ejemplo, cuando se despliega en Render). Estas variables permiten definir el comportamiento de la aplicación sin exponer datos directamente en el código fuente.

Incluye configuraciones como:

- Activación o desactivación del uso de PostgreSQL.
- Habilitación del modo `DEBUG` en entornos de desarrollo.
- Datos de conexión para la base de datos PostgreSQL: nombre de base de datos, usuario, contraseña, host y puerto.
- La clave secreta (`SECRET_KEY`) necesaria para la seguridad interna de Django.

Es importante mantener este archivo fuera del control de versiones para evitar exponer datos sensibles.

### Archivo: `manage.py`

Script principal para gestionar tareas administrativas en proyectos Django. Permite ejecutar comandos como iniciar el servidor de desarrollo, crear migraciones, interactuar con la base de datos o ejecutar pruebas. Es el punto de entrada para casi todas las operaciones del framework durante el desarrollo y despliegue.

### Archivo: `requirements.txt`

Archivo de texto que lista todas las dependencias Python necesarias para ejecutar el proyecto. Facilita la instalación rápida y consistente de los paquetes requeridos mediante el comando:

```
pip install -r requirements.txt

```

Es fundamental tanto para desarrolladores como para servidores de despliegue automatizado.

### Archivo: `.gitignore`

Determina qué archivos y carpetas deben ser ignorados por Git en el control de versiones. Normalmente incluye entornos virtuales, archivos de configuración sensibles como `.env` y carpetas generadas automáticamente (como `__pycache__` o `staticfiles/`).

### Archivo: `Django_secret_key_for_render`

Archivo auxiliar que almacena la clave secreta utilizada por Django cuando se despliega el proyecto en la plataforma Render. Separa la administración de credenciales de desarrollo local y producción, reforzando la seguridad y el control de acceso.

### Archivo: `README.md`

Documento principal de presentación del proyecto. Explica brevemente el objetivo de la aplicación, guía su instalación, describe funcionalidades básicas y proporciona referencias a recursos adicionales y a la estructura del proyecto.

### Archivo: `tareas_semanales.md`

Registro planificado de tareas, avances y pendientes, organizado por semanas o ciclos. Útil para dar seguimiento a la evolución del proyecto, asignar responsabilidades y mantener productividad dentro del equipo.

### Archivo: `translate_data.py`

Script utilizado para traducir datos existentes en el proyecto, probablemente mediante la integración del cliente LibreTranslate. Automatiza la actualización de contenidos en múltiples idiomas, ayudando a mantener la internacionalización sincronizada.

\
**✅ Logros Clave**

| **FechaActividad** |                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------- |
| **Día 1**          | Configuración del proyecto, modelos `Product` y `Category`, estructura de apps.                                 |
| **Día 2**          | Pruebas unitarias para `ProductListView` (5 tests), corrección de paginación con `.order_by("name")`.           |
| **Día 3**          | Configuración de **GitHub Actions** con PostgreSQL, manejo de secretos con `python-decouple`, 95% de cobertura. |
| **Día 4**          | Despliegue en **Render**, solución de errores de estáticos (`collectstatic`), favicon, `gunicorn`, `psycopg2`.  |
| **Día 5+**         | Internacionalización, traducción de modelos, integración con LibreTranslate, documentación.                     |

---

## **🔄 Flujo de Desarrollo y Git**

- **Ramas**:
  - `main`: Producción (protegida).
  - `develop`: Integración.
  - `feature/*`: Nuevas funcionalidades.
- **Flujo**:
  1. Crear rama `feature/xxx`.
  2. Hacer commits con mensajes claros (`test:`, `fix:`, `feat:`).
  3. Abrir PR a `develop`.
  4. CI ejecuta pruebas.
  5. Revisión → Merge → Despliegue.

---

## **🚨 Desafíos Resueltos**

| **ProblemaSolución**              |                                                                         |
| --------------------------------- | ----------------------------------------------------------------------- |
| Paginación inconsistente en tests | Añadir `.order_by("name")` en la vista.                                 |
| Favicon no se mostraba            | Colocado en `static/img/favicon.ico` y referenciado con `{% static %}`. |
| GitHub Actions fallaba con DB     | Usar servicio PostgreSQL + variables correctas.                         |
| App crasheaba en Render           | Instalar `gunicorn` y `psycopg2` en `requirements.txt`.                 |
| Estáticos no cargaban             | Configurar `STATIC_ROOT` y ejecutar `collectstatic`.                    |

---

## **🚨 Extras**

### 🗨️ Script: `translate_data.py`

Este script permite traducir dinámicamente los campos de texto de los modelos `Product` y `Category` desde inglés a español utilizando la API de **LibreTranslate**.

#### 🔧 Funcionamiento general

- Utiliza la librería `requests` para realizar peticiones POST a un endpoint local (`http://localhost:5000/translate`), que se asume corresponde a una instancia de LibreTranslate en ejecución.
- Traduce el contenido del campo `name` y `description` si no existen versiones ya traducidas (`name_es`, `description_es`).
- Guarda los cambios en la base de datos tras realizar cada traducción.
- Muestra por consola los textos traducidos para seguimiento.

#### 🧠 Función principal

```
def translate_text(text, target_lang='es'):
    # Realiza la llamada a la API de traducción

```

- Se asegura de no traducir textos vacíos.
- Controla errores de red mediante `try-except`.

#### 📦 Dependencias necesarias

- El script requiere tener `requests` instalado.
- Supone que el proyecto tiene definidos campos como `name_en`, `name_es`, `description_en`, `description_es` en los modelos involucrados.

#### 📍Ubicación prevista

- Se encuentra ubicado en la raíz del proyecto o en una carpeta de utilidades (`/translate_data.py`, `/utils/translate_data.py`).

> Es útil para prellenar campos traducidos en bases de datos iniciales o tras incorporar nuevos registros no traducidos automáticamente.



### 🐳 Archivo: `docker-compose.yml`

Este archivo define un servicio Docker llamado **LibreTranslate**, que proporciona un servidor de traducción automática compatible con peticiones HTTP. Está diseñado para ejecutarse de forma local y facilitar la integración con proyectos como este, donde se requiere traducir contenido dinámico de la base de datos (por ejemplo, productos o categorías).

#### ⚙️ Configuración del servicio

- \`\`: Nombre asignado al contenedor.
- \`\`: Imagen oficial de Docker desde Docker Hub.
- \`\`: Asegura que el contenedor se reinicie automáticamente salvo que se detenga manualmente.
- \`\`: Expone el puerto interno del servicio para que esté accesible localmente vía `http://localhost:5000`.

#### 🌐 Variables de entorno utilizadas

- `LT_LOAD_ONLY=en,es`: Solo se cargan los modelos de inglés y español (optimiza uso de recursos).
- `LT_UPDATE_MODELS=true`: Fuerza la actualización de los modelos de traducción al iniciar.
- `LT_THREADS=2`: Define el número de hilos (optimizado para Mac M1).
- `LT_FRONTEND_TIMEOUT=2000`: Configura el tiempo de espera para la interfaz.

#### 📦 Volúmenes y persistencia

- `libretranslate_models:/home/libretranslate/.local:rw`: Monta un volumen para guardar los modelos localmente y evitar tener que descargarlos en cada reinicio.

#### ❤️ Healthcheck

Verifica que el contenedor esté funcionando correctamente ejecutando un script de chequeo de salud cada 30 segundos. Si falla 3 veces, se considera no saludable.

---

### ▶️ Comandos para ejecutar el servicio

1. **Crear el archivo** `docker-compose.yml` en la raíz del proyecto o en una carpeta como `docker/`.
2. **Levantar el servicio**:

```
docker compose up -d

```

3. **Verificar que el contenedor esté en ejecución**:

```
docker ps

```

4. **Detener el contenedor** (cuando ya no se necesita):

```
docker compose down

```

---

> Este contenedor debe estar ejecutándose para que el script `translate_data.py` pueda conectarse correctamente a `http://localhost:5000/translate` y traducir los datos desde el backend.



### 🧰 Herramientas utilizadas



Listado de utilidades técnicas integradas en el entorno de desarrollo del proyecto:

- \*\*🧪 \*\*\`\`: Herramienta para medir la cobertura de código al ejecutar pruebas automatizadas. (Documentado abajo)
- \*\*🐳 \*\*\`\`: Para levantar servicios como LibreTranslate en contenedores.
- \*\*📦 \*\*\`\`: Gestión segura de variables de entorno a través de archivos `.env`.
- \*\*🔤 \*\*\`\`: Traducción automática de campos de modelos a múltiples idiomas.
- \*\*🌐 \*\*\`\`: Cliente HTTP para consumir APIs externas como LibreTranslate.
- \*\*📸 \*\*\`\`: Procesamiento de imágenes (usado con `ImageField` en productos).
- \*\*🌀 \*\*\`\`: Middleware para servir archivos estáticos en despliegues sin servidor web.
- \*\*🚀 \*\*\`\`: Servidor WSGI para producción.
- \*\*🐘 \*\*\`\`: Adaptador PostgreSQL para Django.



### 💾 Uso de Fixtures y `inicial.json`

✅ **Las fixtures son una funcionalidad nativa de Django**, incluida directamente en el framework.

Los comandos `dumpdata` y `loaddata` forman parte del sistema de gestión de datos de Django y vienen listos para usarse.

Django permite cargar datos iniciales en la base de datos mediante **fixtures**, que son archivos estructurados (normalmente en formato JSON) con datos serializados de modelos.

#### 📁 Archivo: `inicial.json`

Este archivo actúa como una fixture personalizada del proyecto. Suele contener datos predefinidos necesarios para que la aplicación funcione correctamente desde su primer arranque, como categorías, productos, usuarios de ejemplo, o configuraciones básicas.

#### 🛠️ ¿Cómo se usa?

- Los datos deben exportarse previamente con el comando:

```
python manage.py dumpdata products --indent 2 > inicial.json

```

- Para cargarlo en la base de datos:

```
python manage.py loaddata inicial.json

```

#### 📌 Ubicación habitual

Puede almacenarse en la raíz del proyecto, o dentro de una carpeta como `fixtures/` o dentro de cada app.

#### 📋 Ejemplo de contenido

```
[
  {
    "model": "products.category",
    "pk": 1,
    "fields": {
      "name": "Juegos de mesa",
      "name_en": "Board Games",
      "name_es": "Juegos de mesa"
    }
  }
]

```

> Este mecanismo es útil para entornos de desarrollo, pruebas automatizadas, o incluso para iniciar contenido básico tras un despliegue en producción.



### 🧪 Herramienta: `coverage`

\`\` es una herramienta de análisis que mide qué partes del código fuente han sido ejecutadas al correr los **tests automatizados** del proyecto. Su objetivo principal es mejorar la calidad del software asegurando que el código esté bien probado.

---

### 🎯 ¿Para qué sirve?

- Detectar funciones o bloques de código que nunca se ejecutan.
- Verificar que las pruebas cubren todos los comportamientos esperados.
- Eliminar código muerto o innecesario.
- Establecer métricas de calidad en procesos de integración continua (CI).

---

### ⚙️ ¿Por qué se instaló?

Se incluyó `coverage==7.9.1` en el archivo `requirements.txt` durante la fase de desarrollo para:

- Evaluar objetivamente la cobertura de las pruebas unitarias.
- Integrar su uso en CI (GitHub Actions).
- Obtener informes visuales y por consola sobre la calidad de los tests.
- Alcanzar un objetivo de cobertura (se documentó que se llegó al 95%).

---

### 📂 ¿Qué es la carpeta `htmlcov/`?

Al ejecutar `coverage html`, se genera un informe visual en formato HTML dentro de una carpeta llamada `htmlcov/`. Este informe permite:

- Navegar archivo por archivo.
- Ver líneas cubiertas (verde) y no cubiertas (rojo).
- Consultar estadísticas detalladas por módulo o archivo.

Puedes abrir el archivo principal con:

```
open htmlcov/index.html  # en MacOS o Linux
start htmlcov/index.html  # en Windows

```

---

### ✅ Comandos útiles de `coverage`

```
# Ejecutar los tests con cobertura
coverage run manage.py test

# Ver resumen de cobertura en la terminal
coverage report

# Generar informe HTML visual
coverage html

# (Opcional) Borrar informes anteriores
coverage erase

```

> `coverage` forma parte de las buenas prácticas de testing en proyectos Django y contribuye a detectar errores antes de llegar a producción.





### 📝 Logging en Django

El paquete `logging` es el sistema estándar de Python utilizado para **depurar, monitorear y registrar eventos** durante la ejecución de un proyecto Django. Sirve como una alternativa más profesional y configurable que `print()`, tanto en desarrollo como en producción.

---

### ⚙️ Requiere configuración en `settings.py`

Antes de usarlo, debes tener configurado el sistema de logging en tu archivo `settings.py`. Ejemplo funcional:

```
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s] %(message)s'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

Este bloque configura que todos los mensajes de nivel `DEBUG` o superior se muestren por consola con un formato claro que incluye hora, nivel y módulo origen.

### 💡 ¿Cómo usar `logging` para depuración?

Una vez configurado, puedes usarlo en cualquier archivo Python de tu proyecto para imprimir mensajes según nivel de severidad:

```
import logging
logger = logging.getLogger(__name__)

logger.debug("Inicio de función crear_datos()")

categoria = Category.objects.create(
    name="Juegos clásicos",
    description="Colección de juegos tradicionales"
)
logger.debug(f"Categoría creada: {categoria.name}")

producto = Product.objects.create(
    name="Dominó profesional",
    description="Dominó de alta calidad con estuche",
    price=24.90,
    stock=20,
    category=categoria
)
logger.debug(f"Producto creado: {producto.name} en categoría {categoria.category.name}")
```

Este ejemplo ilustra cómo insertar puntos de seguimiento detallados durante la ejecución de operaciones comunes.

### 📊 Niveles de logging disponibles

| NivelMétodo¿Visible si nivel = DEBUG? |                     |      |
| ------------------------------------- | ------------------- | ---- |
| `DEBUG`                               | `logger.debug()`    | ✅ Sí |
| `INFO`                                | `logger.info()`     | ✅ Sí |
| `WARNING`                             | `logger.warning()`  | ✅ Sí |
| `ERROR`                               | `logger.error()`    | ✅ Sí |
| `CRITICAL`                            | `logger.critical()` | ✅ Sí |

> Cuanto más alto el nivel, más grave el evento. En desarrollo se recomienda usar `DEBUG`, en producción `WARNING` o superior.

## **📋 Próximos Pasos**

- ✅ Escribir pruebas para `ProductDetailView`.
- ✅ Añadir caso de prueba para 404.
- 🔜 Automatizar despliegue en Render desde `develop`.
- 📚 Documentar instrucciones de testing en `README.md`.
- 🔮 Generar datos de prueba con `Faker`.
- 🔐 Implementar permisos más finos (grupos de usuarios).

---

## 🧪 Verificar modo DEBUG por CLI

Puedes comprobar si el modo `DEBUG` está activado con:

```
python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)"
```

---

**🏁 Estado Final**

✅ **App en vivo**\
✅ **CI activo**\
✅ **Flujo de desarrollo profesional**\
✅ **Listo para presentación al cliente**

---

> **Preparado por:** Vasil\
> **Fecha:** 2025-08-06

