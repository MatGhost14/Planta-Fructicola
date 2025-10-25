# 🚀 Inicio Rápido para Colaboradores

## ⚡ Inicio en 3 pasos

### 1. Verificar Docker
```cmd
docker --version
docker-compose --version
```
Si no tienes Docker, descárgalo de: https://www.docker.com/products/docker-desktop/

### 2. Iniciar Sistema
```cmd
.\start-docker.bat
```

### 3. Acceder
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔑 Credenciales de Prueba

| Rol | Email | Password |
|-----|-------|----------|
| **Inspector** | juan.diaz@empresa.com | 123456 |
| **Supervisor** | maria.lopez@empresa.com | 123456 |
| **Admin** | carlos.ruiz@empresa.com | 123456 |

## 🛠️ Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `start-docker.bat` | **Iniciar todo el sistema** |
| `stop-docker.bat` | Detener todos los servicios |
| `docker-restart.bat` | Reiniciar servicios |
| `docker-status.bat` | Verificar estado del sistema |
| `docker-logs.bat` | Ver logs en tiempo real |
| `docker-clean.bat` | Limpieza completa (elimina datos) |
| `docker-dev.bat` | Modo desarrollo (solo BD) |
| `verify-users.bat` | Verificar usuarios de prueba |
| `init-users.bat` | Inicializar usuarios si faltan |
| `test-system.bat` | **Prueba completa del sistema** |

## 🔧 Solución de Problemas

### "Docker no encontrado"
- Instala Docker Desktop
- Reinicia el sistema
- Verifica que Docker esté ejecutándose

### "Puerto en uso"
```cmd
# Ver qué está usando el puerto
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Detener servicios
.\stop-docker.bat
```

### "Error al cargar catálogos"
```cmd
# Reiniciar backend
docker restart planta_backend

# Ver logs
.\docker-logs.bat
```

### "Sin respuesta del servidor"
```cmd
# Verificar estado
.\docker-status.bat

# Reiniciar todo
.\docker-restart.bat
```

### "Error de login" / "Credenciales incorrectas"
```cmd
# Verificar usuarios
.\verify-users.bat

# Si no hay usuarios, inicializar
.\init-users.bat

# Limpiar y reiniciar desde cero
.\docker-clean.bat
.\start-docker.bat
```

### "No se pueden verificar los usuarios"
```cmd
# Verificar estado de la base de datos
.\docker-status.bat

# Si la BD no responde, reiniciar
.\docker-restart.bat

# Si persiste, limpiar todo
.\docker-clean.bat
.\start-docker.bat
```

## 📊 Comandos Docker Útiles

```cmd
# Ver contenedores
docker ps

# Ver logs de un servicio
docker logs planta_backend
docker logs planta_frontend
docker logs planta-mysql

# Entrar a un contenedor
docker exec -it planta_backend bash
docker exec -it planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor

# Reiniciar un servicio
docker restart planta_backend
```

## 🗄️ Base de Datos

```cmd
# Conectar a MySQL
docker exec -it planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor

# Backup
docker exec planta-mysql mysqldump -u planta_user -pplanta_password inspeccioncontenedor > backup.sql

# Restaurar
docker exec -i planta-mysql mysql -u planta_user -pplanta_password inspeccioncontenedor < backup.sql
```

## 🚨 Si algo no funciona

1. **Verificar Docker**: `docker ps`
2. **Ver logs**: `.\docker-logs.bat`
3. **Reiniciar**: `.\docker-restart.bat`
4. **Limpieza completa**: `.\docker-clean.bat` (⚠️ elimina datos)
5. **Reiniciar desde cero**: `.\start-docker.bat`

---

**¿Necesitas ayuda?** Revisa el README.md completo o contacta al equipo de desarrollo.
