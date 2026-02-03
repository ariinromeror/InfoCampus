# InfoCampus - Sistema ERP para Gestión Universitaria

![Django](https://img.shields.io/badge/Django-6.0.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

> Sistema ERP completo desarrollado en 7 días mediante metodología AI-Driven para la gestión integral de instituciones universitarias con control de acceso basado en roles (RBAC).

**Desarrollado por:** Arin Romero  
**Rol:** Arquitecto de Prompts | Product Owner | Director de Proyecto  
**Fecha:** Febrero 2026

---

## 📋 Tabla de Contenidos

- [Resumen Ejecutivo](#-resumen-ejecutivo)
- [Demo y Características](#-demo-y-características)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Módulos Funcionales](#-módulos-funcionales)
- [Sistema RBAC](#-sistema-rbac-control-de-acceso-basado-en-roles)
- [Lógica de Negocio](#-lógica-de-negocio)
- [Scripts de Población](#-scripts-de-población-de-datos)
- [API Endpoints](#-api-endpoints)
- [Métricas del Proyecto](#-métricas-del-proyecto)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Resumen Ejecutivo

**InfoCampus** es un ERP (Enterprise Resource Planning) full-stack diseñado para la gestión integral de instituciones universitarias. Implementa un robusto sistema de **Control de Acceso Basado en Roles (RBAC)** con cinco roles operacionales diferenciados.

### 🏆 Logro Principal

Desarrollo completo de un ERP funcional en **7 días** mediante una metodología de desarrollo AI-Driven que combina:
- Arquitectura de prompts estratégicos
- Supervisión técnica continua
- Orquestación inteligente de sistemas

### 🎯 Objetivo del Proyecto

Este proyecto fue desarrollado como **portafolio profesional** para demostrar:
- Capacidad de desarrollo full-stack
- Implementación de lógica de negocio compleja
- Diseño de arquitectura escalable
- Gestión de proyectos técnicos

---

## ✨ Demo y Características

### Características Principales

- ✅ **Sistema RBAC completo** con 5 roles operacionales
- ✅ **Autenticación JWT** con tokens de acceso y refresh
- ✅ **API RESTful** totalmente documentada
- ✅ **Bloqueo inteligente** por morosidad financiera
- ✅ **Auditoría completa** de cambios en calificaciones
- ✅ **Dashboard analítico** personalizado por rol
- ✅ **Sistema de becas** con cálculo automático de descuentos
- ✅ **Responsive design** adaptable a todos los dispositivos
- ✅ **Población automática** de datos realistas

### Usuarios de Prueba

Después de ejecutar los scripts de población, puedes acceder con:

```
Contraseña por defecto: campus2026
```

Las credenciales específicas se generan en `credenciales/*.txt` después de ejecutar `3_poblacion.py`

---

## 🏗️ Arquitectura del Sistema

```
infocampus/
├── backend/                    # Django REST API
│   ├── api/                   # Apps Django
│   │   ├── carreras/         # Gestión de carreras
│   │   ├── materias/         # Gestión de materias
│   │   ├── usuarios/         # Sistema de usuarios
│   │   ├── secciones/        # Secciones y horarios
│   │   ├── inscripciones/    # Registro de inscripciones
│   │   ├── calificaciones/   # Sistema de notas
│   │   └── pagos/            # Módulo financiero
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── components/       # Componentes reutilizables
│   │   ├── pages/           # Vistas por rol
│   │   ├── services/        # API calls
│   │   ├── context/         # Context API
│   │   └── utils/           # Utilidades
│   ├── package.json
│   └── vite.config.js
│
├── scripts/                    # Scripts de población
│   ├── 1_malla.py            # Estructura académica
│   ├── 2_secciones.py        # Períodos y secciones
│   ├── 3_poblacion.py        # Usuarios y roles
│   └── 4_actividad.py        # Actividad académica
│
└── credenciales/              # Generado automáticamente
    └── *.txt                  # Credenciales de usuarios
```

### Diagrama de Arquitectura

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │ ◄─────► │   Backend    │ ◄─────► │   SQLite    │
│ React + Vite│  HTTP   │ Django + DRF │  ORM    │   Database  │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │
      │                        │
      ▼                        ▼
  Tailwind CSS          JWT Authentication
  React Router          Django Middleware
  Axios Client          CORS Headers
```

---

## 🛠️ Stack Tecnológico

### Backend

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **Django** | 6.0.1 | Framework web principal |
| **Django REST Framework** | 3.16.1 | Construcción de API RESTful |
| **djangorestframework-simplejwt** | 5.5.1 | Autenticación JWT |
| **django-cors-headers** | 4.9.0 | Manejo de CORS |
| **Faker** | 40.1.2 | Generación de datos de prueba |
| **Pillow** | 12.1.0 | Procesamiento de imágenes |
| **python-dotenv** | 1.2.1 | Variables de entorno |

### Frontend

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| **React** | 19.2.0 | Biblioteca UI |
| **Vite** | 7.2.4 | Build tool y dev server |
| **Tailwind CSS** | 4.1.18 | Framework de estilos |
| **Axios** | 1.13.2 | Cliente HTTP |
| **React Router** | 7.13.0 | Enrutamiento SPA |
| **Recharts** | 3.7.0 | Gráficos y visualización |
| **Lucide React** | 0.563.0 | Iconografía |
| **Framer Motion** | 12.29.2 | Animaciones |

### Herramientas de Desarrollo

- **Git** - Control de versiones
- **ESLint** - Linting de JavaScript
- **PostCSS** - Procesamiento de CSS
- **SQLite Browser** - Exploración de BD

---

## 🚀 Instalación y Configuración

### Prerrequisitos

```bash
# Versiones requeridas
Python 3.11+
Node.js 18+
npm 9+
```

### Instalación Paso a Paso

#### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/infocampus.git
cd infocampus
```

#### 2️⃣ Configurar Backend (Terminal 1)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# Ejecutar scripts de población (EN ORDEN)
python 1_malla.py
python 2_secciones.py
python 3_poblacion.py
python 4_actividad.py

# Iniciar servidor de desarrollo
python manage.py runserver
```

**Backend disponible en:** `http://localhost:8000`

#### 3️⃣ Configurar Frontend (Terminal 2)

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

**Frontend disponible en:** `http://localhost:5173`

### ⚙️ Variables de Entorno

Crear archivo `.env` en la raíz del backend:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_NAME=db.sqlite3

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

---

## 📦 Módulos Funcionales

### 1. Gestión de Malla Curricular
- ✅ Administración de carreras
- ✅ Gestión de materias y créditos
- ✅ Sistema de prerequisitos
- ✅ Configuración de precios por crédito

### 2. Sistema de Períodos y Secciones
- ✅ Control de ciclos lectivos
- ✅ Gestión de horarios y aulas
- ✅ Asignación de profesores
- ✅ Control de cupos

### 3. Sistema de Inscripciones
- ✅ Registro de estudiantes en secciones
- ✅ Validación de cupos disponibles
- ✅ Verificación de prerequisitos
- ✅ Historial de inscripciones

### 4. Gestión de Calificaciones
- ✅ Ingreso de notas por profesores
- ✅ Consulta de calificaciones
- ✅ Auditoría de cambios
- ✅ Cálculo automático de promedios

### 5. Módulo Financiero
- ✅ Cálculo automático de deudas
- ✅ Sistema de becas (25%, 50%, 75%, 100%)
- ✅ Bloqueo por morosidad
- ✅ Registro de pagos
- ✅ Reportes financieros

### 6. Dashboard Analítico
- ✅ Indicadores clave por rol
- ✅ Gráficos interactivos
- ✅ Accesos rápidos
- ✅ Estadísticas en tiempo real

---

## 🔐 Sistema RBAC (Control de Acceso Basado en Roles)

### Roles Implementados

| Rol | Permisos | Casos de Uso |
|-----|----------|--------------|
| 👨‍🎓 **Estudiante** | - Ver materias inscritas<br>- Consultar calificaciones<br>- Ver estado financiero<br>- Descargar certificados | Acceso limitado a información personal |
| 👨‍🏫 **Profesor** | - Ingresar calificaciones<br>- Modificar notas<br>- Ver listas de alumnos<br>- Generar reportes de sección | Gestión académica de sus secciones |
| 💰 **Tesorero** | - Registrar pagos<br>- Generar reportes financieros<br>- Gestionar morosidad<br>- Configurar becas | Control financiero completo |
| 📊 **Coordinador** | - Gestionar secciones<br>- Asignar profesores<br>- Ver reportes académicos<br>- Administrar horarios | Coordinación académica |
| 👔 **Director** | - Acceso completo al sistema<br>- Configurar carreras<br>- Gestionar períodos<br>- Ver todos los reportes | Administración general |

### Implementación de Permisos

```python
# Ejemplo de decorador de permisos
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.rol not in roles_permitidos:
                return Response(
                    {"error": "No tienes permisos para esta acción"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Uso en vistas
@rol_requerido(['profesor', 'coordinador', 'director'])
def ingresar_calificacion(request):
    # Lógica de ingreso de calificación
    pass
```

---

## 💼 Lógica de Negocio

### Sistema Financiero Inteligente

#### Cálculo de Deudas

```python
def calcular_deuda_estudiante(estudiante):
    """
    Calcula la deuda total de un estudiante considerando:
    - Inscripciones sin pago
    - Becas aplicables
    - Días de gracia por carrera
    """
    deuda_total = 0
    
    for inscripcion in estudiante.inscripciones.filter(pagado=False):
        costo_materia = inscripcion.seccion.materia.creditos * \
                       inscripcion.seccion.materia.carrera.precio_credito
        
        # Aplicar descuento por beca
        if estudiante.beca_porcentaje > 0:
            descuento = costo_materia * (estudiante.beca_porcentaje / 100)
            costo_materia -= descuento
        
        deuda_total += costo_materia
    
    return deuda_total
```

#### Bloqueo por Morosidad

```python
def verificar_bloqueo_morosidad(estudiante):
    """
    Verifica si un estudiante debe ser bloqueado por morosidad
    """
    deuda = calcular_deuda_estudiante(estudiante)
    dias_gracia = estudiante.carrera.dias_gracia
    
    # Verificar si tiene deuda vencida
    for inscripcion in estudiante.inscripciones.filter(pagado=False):
        fecha_limite = inscripcion.fecha_inscripcion + timedelta(days=dias_gracia)
        
        if datetime.now() > fecha_limite and deuda > 0:
            return True  # Bloqueado
    
    return False  # No bloqueado
```

### Sistema de Becas

Fórmula de cálculo:

```
Costo Final = Créditos × Precio por Crédito × (1 - Porcentaje Beca / 100)
```

**Ejemplo:**
- Materia: 4 créditos
- Precio por crédito: $50
- Beca: 50%
- Costo final: 4 × $50 × (1 - 0.5) = **$100**

### Simulación de Realismo Operacional

El sistema genera datos que reflejan la complejidad del mundo real:

| Métrica | Valor | Propósito |
|---------|-------|-----------|
| Estudiantes Morosos | **20%** | Validar bloqueos financieros |
| Notas Reprobadas | **20%** | Probar restricciones académicas |
| Estudiantes Becados | **20%** | Validar cálculo de descuentos |

---

## 📊 Scripts de Población de Datos

### Script 1: `1_malla.py` - Estructura Académica

**Propósito:** Crear la malla curricular completa de la institución.

```python
# Ejemplo de salida
"""
✓ Creadas 5 carreras
✓ Creadas 30 materias (6 por carrera)
✓ Asignados créditos: 2-5 por materia
✓ Configurados precios: $45-$80 por crédito
"""
```

**Carreras generadas:**
- Ingeniería en Sistemas
- Derecho
- Medicina
- Administración de Empresas
- Psicología

### Script 2: `2_secciones.py` - Logística de Tiempos

**Propósito:** Configurar períodos lectivos y generar secciones operativas.

```python
# Ejemplo de salida
"""
✓ Creados 4 períodos lectivos
✓ Generadas ~60 secciones
✓ Asignados horarios: 7:00 AM - 8:00 PM
✓ Distribuidas aulas: A101-A120
"""
```

**Períodos creados:**
- 2024-2 (Cerrado)
- 2025-1 (Cerrado)
- 2025-2 (Cerrado)
- 2026-1 (Activo)

### Script 3: `3_poblacion.py` - Población de Usuarios

**Propósito:** Crear la estructura completa de usuarios y roles (RBAC).

```python
# Ejemplo de salida
"""
✓ Creados 150 estudiantes
✓ Creados 20 profesores
✓ Creados 2 directores
✓ Creados 3 coordinadores
✓ Creados 3 tesoreros
✓ Generadas credenciales en carpeta 'credenciales/'
"""
```

**Características:**
- Datos personales realistas con Faker
- Asignación automática de profesores a secciones
- Vinculación de estudiantes a carreras
- Generación de archivos `.txt` con credenciales

### Script 4: `4_actividad.py` - Actividad Académica

**Propósito:** Simular actividad académica y financiera histórica.

```python
# Ejemplo de salida
"""
✓ Generadas ~900 inscripciones actuales
✓ Generadas ~1,200 inscripciones históricas
✓ Registradas ~600 transacciones de pago
✓ Implementado 20% de reprobaciones
✓ Implementado 20% de morosidad
"""
```

---

## 🌐 API Endpoints

### Autenticación

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "estudiante123",
  "password": "InfoCampus2026"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "estudiante123",
    "rol": "estudiante",
    "nombre": "Juan Pérez"
  }
}
```

### Gestión de Carreras

```http
# Listar todas las carreras
GET /api/carreras/

# Obtener una carrera específica
GET /api/carreras/{id}/

# Crear nueva carrera (Solo Director)
POST /api/carreras/
Authorization: Bearer {access_token}

# Actualizar carrera (Solo Director)
PUT /api/carreras/{id}/
Authorization: Bearer {access_token}
```

### Gestión de Inscripciones

```http
# Inscribirse en una sección
POST /api/inscripciones/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "seccion_id": 15,
  "estudiante_id": 45
}

Response:
{
  "id": 123,
  "estudiante": "Juan Pérez",
  "seccion": "Matemáticas I - Sección A",
  "fecha_inscripcion": "2026-02-03T10:30:00Z",
  "pagado": false,
  "costo": 200.00
}
```

### Gestión de Calificaciones

```http
# Ingresar calificación (Solo Profesor)
POST /api/calificaciones/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "inscripcion_id": 123,
  "nota": 8.5,
  "periodo": "2026-1"
}

# Consultar calificaciones (Estudiante)
GET /api/calificaciones/estudiante/{id}/
Authorization: Bearer {access_token}

Response:
{
  "estudiante": "Juan Pérez",
  "periodo": "2026-1",
  "calificaciones": [
    {
      "materia": "Matemáticas I",
      "nota": 8.5,
      "creditos": 4,
      "estado": "Aprobado"
    },
    ...
  ],
  "promedio_periodo": 8.2
}
```

### Módulo Financiero

```http
# Registrar pago (Solo Tesorero)
POST /api/pagos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "estudiante_id": 45,
  "monto": 200.00,
  "metodo_pago": "efectivo",
  "concepto": "Inscripción Matemáticas I"
}

# Consultar estado financiero (Estudiante)
GET /api/pagos/estado/{estudiante_id}/
Authorization: Bearer {access_token}

Response:
{
  "estudiante": "Juan Pérez",
  "deuda_total": 600.00,
  "deuda_periodo_actual": 400.00,
  "deuda_periodos_anteriores": 200.00,
  "bloqueado": true,
  "tiene_convenio": false,
  "beca_porcentaje": 50
}
```

---

## 📈 Métricas del Proyecto

### Tiempo de Desarrollo

| Fase | Duración |
|------|----------|
| Diseño de arquitectura y modelos | 1 día |
| Desarrollo del backend (Django) | 2 días |
| Desarrollo del frontend (React) | 2 días |
| Scripts de población y testing | 2 días |
| **Total** | **7 días** |

### Volumen de Datos Generados

| Entidad | Cantidad |
|---------|----------|
| Carreras | 5 |
| Materias | 30 |
| Períodos Lectivos | 4 |
| Secciones | ~60 |
| Usuarios Totales | 178 |
| Estudiantes | 150 |
| Inscripciones Actuales | ~750-900 |
| Inscripciones Históricas | ~1,200 |
| Registros de Pago | ~600 |
| Archivos de Credenciales | 178 |

### Líneas de Código

```
Backend (Python):           ~1,500 LOC
Frontend (JavaScript/React): ~2,000 LOC
Scripts de población:        ~500 LOC
Configuración y utilidades:  ~300 LOC
────────────────────────────────────
Total:                      ~4,300 LOC
```

---

## 🎨 Diseño de Interfaz

### Características del Diseño

- ✅ **Sistema de diseño consistente**
  - Paleta de colores institucional
  - Tipografía: Arial/Sans-serif
  - Iconografía: Lucide React

- ✅ **Responsive Design**
  - Adaptación automática a móviles
  - Optimizado para tablets
  - Soporte completo desktop

- ✅ **Componentes Reutilizables**
  - Dashboard Cards
  - Tablas dinámicas
  - Formularios validados
  - Modales y notificaciones

- ✅ **Animaciones Fluidas**
  - Transiciones con Framer Motion
  - Feedback visual inmediato
  - Loading states

### Vistas Principales

#### 1. Login / Autenticación
```jsx
// Pantalla de acceso limpia y profesional
- Validación de credenciales en tiempo real
- Gestión de sesiones con JWT
- Recuperación de contraseña
- Diseño centrado y minimalista
```

#### 2. Dashboard por Rol
```jsx
// Vista personalizada según rol del usuario
- Cards con KPIs relevantes
- Gráficos interactivos (Recharts)
- Accesos rápidos a funciones principales
- Navegación intuitiva
```

#### 3. Gestión de Datos
```jsx
// Tablas responsive con funcionalidad completa
- Paginación automática
- Ordenamiento por columnas
- Búsqueda y filtrado en tiempo real
- Acciones inline (editar, eliminar, ver)
```

---

## 🗺️ Roadmap

### ✅ Versión 1.0 (Actual)
- [x] Sistema RBAC completo
- [x] Módulo financiero con bloqueos
- [x] Gestión de calificaciones
- [x] Dashboard analítico
- [x] Scripts de población

### 🚧 Versión 1.1 (En Desarrollo)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Exportación de reportes a PDF
- [ ] Sistema de mensajería interno
- [ ] Calendario académico integrado

### 🔮 Versión 2.0 (Planificado)
- [ ] Migración a PostgreSQL
- [ ] Integración con sistemas de pago (Stripe/PayPal)
- [ ] App móvil nativa (React Native)
- [ ] Sistema de asistencia biométrica
- [ ] Módulo de biblioteca digital

---

## 🤝 Contribución

Este es un proyecto de portafolio personal, pero estoy abierto a sugerencias y feedback.

### Cómo Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- **Python:** Seguir PEP 8
- **JavaScript:** Usar ESLint config de Airbnb
- **Commits:** Conventional Commits
- **Documentación:** Docstrings en funciones importantes

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto

**Arin Romero**

- Email: ariin.romeror@gmail.com

- GitHub: [ariinromeror](https://github.com/ariinromeror)

---

## 🙏 Agradecimientos

Este proyecto fue desarrollado utilizando:
- Metodología AI-Driven para acelerar el desarrollo
- Mejores prácticas de la comunidad Django y React
- Patrones de diseño empresariales establecidos
- Feedback de desarrolladores senior

---

## 📚 Recursos Adicionales

### Documentación
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/)

### Tutoriales Relacionados
- [Building RESTful APIs with Django](https://realpython.com/django-rest-framework-quick-start/)
- [React Best Practices](https://react.dev/learn/thinking-in-react)
- [JWT Authentication in Django](https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html)

---

<div align="center">

**⭐ Si este proyecto te resultó útil, no olvides darle una estrella ⭐**

*Desarrollado con ❤️ como proyecto de portafolio profesional*

</div>