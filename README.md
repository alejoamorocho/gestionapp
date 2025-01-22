# Cosmedical App

Sistema de gestión integral para la venta y mantenimiento de mobiliario médico y dispositivos estéticos profesionales.

## Descripción

Cosmedical App es una plataforma especializada en la gestión de equipos médicos y mobiliario estético, diseñada para facilitar el control, mantenimiento y seguimiento de los equipos utilizados en el sector médico y estético.

## Módulos Principales

### 1. Gestión de Usuarios
- Administración de diferentes tipos de usuarios:
  - Administradores del sistema
  - Clientes profesionales
  - Técnicos de mantenimiento
  - Vendedores
- Perfiles personalizados con información específica por tipo de usuario
- Control de acceso y permisos basados en roles

### 2. Gestión de Equipos
- Catálogo completo de equipos médicos y mobiliario
- Seguimiento individual por número de serie
- Gestión de documentación técnica
- Control de garantías y certificaciones
- Historial de precios
- Galería de imágenes por equipo
- Asignación de equipos a clientes específicos

### 3. Mantenimiento
- Planes de mantenimiento preventivo
- Registro de mantenimientos correctivos
- Seguimiento fotográfico de mantenimientos
- Control de repuestos utilizados
- Asignación de técnicos
- Programación de mantenimientos
- Historial completo por equipo
- Costos de mantenimiento

### 4. Eventos y Capacitaciones
- Programación de demostraciones de equipos
- Gestión de capacitaciones técnicas
- Registro de asistentes
- Certificados de capacitación
- Calendario de eventos
- Notificaciones automáticas

### 5. Documentación
- Gestión centralizada de documentos
- Manuales de usuario
- Fichas técnicas
- Certificados y garantías
- Control de versiones
- Permisos de acceso por tipo de documento

## Características Técnicas

- Backend desarrollado en Django y Django REST Framework
- API RESTful documentada con Swagger/OpenAPI
- Autenticación JWT
- Filtros avanzados para búsqueda y consulta
- Sistema de permisos granular
- Soporte para múltiples tipos de archivos
- Integración con servicios de almacenamiento

## Seguridad

- Autenticación robusta
- Control de acceso basado en roles
- Registro de auditoría
- Encriptación de datos sensibles
- Backups automáticos
- Protección contra ataques comunes

## Requisitos del Sistema

- Python 3.8+
- PostgreSQL
- Servidor web compatible con WSGI
- Almacenamiento para archivos media

## Instalación

[Instrucciones de instalación detalladas]

## Configuración

[Pasos de configuración y variables de entorno]

## Uso

[Guía básica de uso y ejemplos]

## Contribución

[Guías para contribuir al proyecto]

## Licencia

[Información de licencia]

## Contacto

[Información de contacto para soporte]

## 🏥 Sobre Cosmedical

Cosmedical es una empresa especializada en la distribución y mantenimiento de:
- Mobiliario médico especializado
- Equipos médicos de diagnóstico
- Dispositivos para tratamientos estéticos profesionales
- Equipamiento para clínicas y consultorios

## 🌟 Características Principales

- Gestión completa de equipos médicos y dispositivos estéticos
- Seguimiento de mantenimiento y calibración de equipos
- Portal personalizado para clientes profesionales
- Sistema de documentación técnica y certificaciones
- Programa de capacitación profesional
- Gestión de garantías y servicio técnico
- Sistema de seguimiento post-venta

## 💼 Funcionalidades Específicas

### Gestión de Equipos
- Catálogo detallado con especificaciones técnicas
- Registro de números de serie y garantías
- Historial de mantenimiento y calibraciones
- Documentación técnica y manuales
- Certificaciones y registros sanitarios

### Portal Profesional
- Acceso a documentación técnica
- Programación de mantenimientos
- Solicitud de servicio técnico
- Historial de compras y mantenimientos
- Acceso a capacitaciones y certificaciones

### Sistema de Soporte
- Tickets de servicio técnico
- Seguimiento de mantenimientos preventivos
- Gestión de garantías
- Soporte técnico especializado
- Programación de visitas técnicas

## 🛠️ Stack Tecnológico

### Backend
- Python 3.9+
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Celery (tareas asíncronas)
- Redis (caché)

### Frontend
- Node.js 18+
- React 18+
- React Router 6+
- Axios
- Tailwind CSS

## 📋 Estructura del Proyecto

```
cosmedical-app/
├── backend/
│   ├── apps/
│   │   ├── users/
│   │   ├── equipment/
│   │   ├── maintenance/
│   │   ├── documents/
│   │   └── training/
│   ├── core/
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
└── docker/
```

## 🚀 Pasos de Implementación

### Fase 1: Configuración Inicial
1. Configuración del entorno de desarrollo
2. Creación de la estructura base del proyecto
3. Configuración de la base de datos
4. Implementación de Docker

### Fase 2: Backend
1. Implementación de modelos de datos
2. Desarrollo de API REST
3. Configuración de autenticación JWT
4. Implementación de permisos y roles

### Fase 3: Frontend
1. Configuración del proyecto React
2. Desarrollo de componentes base
3. Implementación de autenticación
4. Desarrollo de interfaces principales

### Fase 4: Funcionalidades Específicas
1. Sistema de gestión de equipos
2. Portal de servicio técnico
3. Sistema de mantenimiento
4. Gestión de documentación técnica

## 🔧 Configuración del Entorno de Desarrollo

### Requisitos Previos
- Python 3.9+
- Node.js 18+
- PostgreSQL
- Redis
- Docker y Docker Compose

### Configuración Backend
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Migraciones
python manage.py migrate
```

### Configuración Frontend
```bash
# Instalar dependencias
cd frontend
npm install

# Iniciar servidor de desarrollo
npm run dev
```

## 📝 Convenciones de Código

- PEP 8 para Python
- ESLint y Prettier para JavaScript/React
- Conventional Commits para mensajes de commit

## 🧪 Testing

### Backend
```bash
# Ejecutar tests
python manage.py test
```

### Frontend
```bash
# Ejecutar tests
npm run test
```

## 📦 Despliegue

1. Configurar variables de entorno para producción
2. Construir imágenes Docker
3. Ejecutar migraciones de base de datos
4. Desplegar usando Docker Compose

## 🔐 Seguridad

- Autenticación JWT
- CORS configurado
- Validación de archivos
- Rate limiting
- Sanitización de datos
- Encriptación de datos sensibles
- Registro de auditoría

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request
