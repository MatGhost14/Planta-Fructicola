# 🚀 Instrucciones de Despliegue en Producción

## 📋 Índice

- [Requisitos Previos](#requisitos-previos)
- [Preparación del Servidor VPS](#preparación-del-servidor-vps)
- [Instalación de Dependencias](#instalación-de-dependencias)
- [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
- [Despliegue del Backend](#despliegue-del-backend)
- [Despliegue del Frontend](#despliegue-del-frontend)
- [Configuración de NGINX](#configuración-de-nginx)
- [Configuración de SSL/HTTPS](#configuración-de-sslhttps)
- [Gestión de Procesos con PM2](#gestión-de-procesos-con-pm2)
- [Variables de Entorno de Producción](#variables-de-entorno-de-producción)
- [Backups Automáticos](#backups-automáticos)
- [Monitoreo y Logs](#monitoreo-y-logs)
- [Mantenimiento](#mantenimiento)
- [Troubleshooting](#troubleshooting)

---

## ✅ Requisitos Previos

### Servidor VPS Recomendado

**Especificaciones Mínimas:**
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Almacenamiento:** 50 GB SSD
- **OS:** Ubuntu 22.04 LTS (recomendado) o Debian 11+
- **Ancho de banda:** 1 TB/mes

**Proveedores Recomendados:**
- DigitalOcean (Droplet)
- AWS Lightsail
- Linode
- Vultr
- Hetzner

### Dominio y DNS

- Dominio registrado (ej: `miempresa.com`)
- Acceso a configuración DNS
- Registros A apuntando al VPS:
  ```
  @ (root)          → IP del VPS
  www               → IP del VPS
  api.miempresa.com → IP del VPS (subdomain para backend)
  ```

### Acceso al Servidor

- SSH habilitado
- Usuario con privilegios sudo
- Firewall configurado (UFW)

---

## 🖥️ Preparación del Servidor VPS

### 1. Conectarse al Servidor

```bash
ssh root@TU_IP_VPS
# o
ssh usuario@TU_IP_VPS
```

### 2. Actualizar el Sistema

```bash
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo reboot
```

### 3. Crear Usuario de Despliegue

```bash
# Crear usuario
sudo adduser deploy
sudo usermod -aG sudo deploy

# Configurar SSH para nuevo usuario
sudo mkdir -p /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys

# Cambiar a usuario deploy
su - deploy
```

### 4. Configurar Firewall

```bash
# Habilitar UFW
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

---

## 📦 Instalación de Dependencias

### 1. Instalar Python 3.10+

```bash
sudo apt install -y python3.10 python3.10-venv python3-pip
python3 --version  # Verificar versión
```

### 2. Instalar Node.js y npm

```bash
# Instalar Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verificar instalación
node --version  # Debe mostrar v18.x.x
npm --version
```

### 3. Instalar MySQL 8.0

```bash
# Instalar MySQL
sudo apt install -y mysql-server mysql-client

# Asegurar instalación
sudo mysql_secure_installation

# Configuración recomendada:
# - Password validation: YES (STRONG)
# - Remove anonymous users: YES
# - Disallow root login remotely: YES
# - Remove test database: YES
# - Reload privilege tables: YES
```

### 4. Instalar NGINX

```bash
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### 5. Instalar Certbot (SSL)

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 6. Instalar PM2 (Process Manager)

```bash
sudo npm install -g pm2
pm2 startup systemd  # Ejecutar el comando que devuelve
```

### 7. Instalar Git

```bash
sudo apt install -y git
git --version
```

---

## 🗄️ Configuración de la Base de Datos

### 1. Acceder a MySQL

```bash
sudo mysql -u root -p
```

### 2. Crear Base de Datos y Usuario

```sql
-- Crear base de datos
CREATE DATABASE impeccioncontenedor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario de producción
CREATE USER 'planta_user'@'localhost' IDENTIFIED BY 'PASSWORD_SEGURA_AQUI';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON impeccioncontenedor.* TO 'planta_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

⚠️ **IMPORTANTE**: Cambiar `PASSWORD_SEGURA_AQUI` por una contraseña fuerte.

### 3. Importar Schema

```bash
# Si tienes el archivo SQL
mysql -u planta_user -p impeccioncontenedor < /path/to/impeccioncontenedor.sql

# O crear tablas con Alembic (recomendado)
# Se hará después de clonar el proyecto
```

### 4. Configurar MySQL para Producción

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Agregar/modificar:
```ini
[mysqld]
max_connections = 200
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
```

Reiniciar MySQL:
```bash
sudo systemctl restart mysql
```

---

## 🐍 Despliegue del Backend

### 1. Clonar el Repositorio

```bash
cd /home/deploy
git clone https://github.com/TU_USUARIO/planta-fruticola.git
cd planta-fruticola/backend
```

### 2. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
nano .env
```

Contenido:
```env
# Base de Datos
DATABASE_URL=mysql+pymysql://planta_user:PASSWORD_SEGURA_AQUI@localhost/impeccioncontenedor

# Seguridad
SECRET_KEY=genera_una_clave_super_secreta_con_openssl_rand_base64_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Entorno
ENVIRONMENT=production
DEBUG=False

# CORS
ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Uploads
UPLOAD_DIR=/home/deploy/planta-fruticola/backend/uploads
MAX_FILE_SIZE=10485760

# Email (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
```

**Generar SECRET_KEY seguro:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Aplicar Migraciones

```bash
source venv/bin/activate
alembic upgrade head
```

### 6. Crear Usuario Administrador

```bash
python scripts/create_admin.py
```

### 7. Crear Directorio de Uploads

```bash
mkdir -p /home/deploy/planta-fruticola/backend/uploads/fotos
mkdir -p /home/deploy/planta-fruticola/backend/uploads/firmas
chmod -R 755 /home/deploy/planta-fruticola/backend/uploads
```

### 8. Configurar PM2 para Backend

Crear archivo `ecosystem.config.js`:
```bash
nano /home/deploy/planta-fruticola/backend/ecosystem.config.js
```

Contenido:
```javascript
module.exports = {
  apps: [{
    name: 'planta-backend',
    script: '/home/deploy/planta-fruticola/backend/venv/bin/uvicorn',
    args: 'app.main:app --host 0.0.0.0 --port 8000',
    cwd: '/home/deploy/planta-fruticola/backend',
    instances: 2,
    exec_mode: 'cluster',
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production',
      PYTHONPATH: '/home/deploy/planta-fruticola/backend'
    },
    error_file: '/home/deploy/logs/backend-error.log',
    out_file: '/home/deploy/logs/backend-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

Crear directorio de logs:
```bash
mkdir -p /home/deploy/logs
```

Iniciar backend con PM2:
```bash
cd /home/deploy/planta-fruticola/backend
pm2 start ecosystem.config.js
pm2 save
```

Verificar que esté corriendo:
```bash
pm2 status
pm2 logs planta-backend
```

---

## 🎨 Despliegue del Frontend

### 1. Navegar al Directorio Frontend

```bash
cd /home/deploy/planta-fruticola/frontend
```

### 2. Configurar Variables de Entorno

```bash
nano .env.production
```

Contenido:
```env
VITE_API_URL=https://api.tudominio.com
VITE_APP_NAME=Inspección de Contenedores
```

### 3. Instalar Dependencias

```bash
npm ci --production
```

### 4. Build de Producción

```bash
npm run build
```

Esto generará la carpeta `dist/` con archivos optimizados.

### 5. Mover Archivos al Directorio Web

```bash
sudo mkdir -p /var/www/planta-frontend
sudo cp -r dist/* /var/www/planta-frontend/
sudo chown -R www-data:www-data /var/www/planta-frontend
sudo chmod -R 755 /var/www/planta-frontend
```

---

## 🌐 Configuración de NGINX

### 1. Crear Configuración para Backend

```bash
sudo nano /etc/nginx/sites-available/planta-backend
```

Contenido:
```nginx
# Backend API
server {
    listen 80;
    server_name api.tudominio.com;

    # Redirect HTTP to HTTPS (se configurará después)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.tudominio.com;

    # SSL Certificates (se generarán después)
    # ssl_certificate /etc/letsencrypt/live/api.tudominio.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/api.tudominio.com/privkey.pem;

    # Logs
    access_log /var/log/nginx/planta-backend-access.log;
    error_log /var/log/nginx/planta-backend-error.log;

    # Proxy settings
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Uploads - servir archivos estáticos
    location /uploads/ {
        alias /home/deploy/planta-fruticola/backend/uploads/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # Aumentar tamaño máximo de subida
    client_max_body_size 50M;
}
```

### 2. Crear Configuración para Frontend

```bash
sudo nano /etc/nginx/sites-available/planta-frontend
```

Contenido:
```nginx
# Frontend
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tudominio.com www.tudominio.com;

    # SSL Certificates (se generarán después)
    # ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;

    # Logs
    access_log /var/log/nginx/planta-frontend-access.log;
    error_log /var/log/nginx/planta-frontend-error.log;

    # Root directory
    root /var/www/planta-frontend;
    index index.html;

    # SPA routing (todas las rutas apuntan a index.html)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache de assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
}
```

### 3. Habilitar Sitios

```bash
# Crear symlinks
sudo ln -s /etc/nginx/sites-available/planta-backend /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/planta-frontend /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Si todo está OK, reiniciar NGINX
sudo systemctl restart nginx
```

---

## 🔒 Configuración de SSL/HTTPS

### 1. Obtener Certificados SSL con Let's Encrypt

```bash
# Para el frontend
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Para el backend
sudo certbot --nginx -d api.tudominio.com
```

Certbot configurará automáticamente SSL en los archivos de NGINX.

### 2. Verificar Renovación Automática

```bash
# Probar renovación
sudo certbot renew --dry-run

# Verificar timer de renovación automática
sudo systemctl status certbot.timer
```

Los certificados se renovarán automáticamente cada 60 días.

### 3. Descomentar Líneas SSL en NGINX

Editar los archivos de configuración y descomentar las líneas de SSL:
```bash
sudo nano /etc/nginx/sites-available/planta-backend
sudo nano /etc/nginx/sites-available/planta-frontend
```

Reiniciar NGINX:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## ⚙️ Gestión de Procesos con PM2

### Comandos Básicos de PM2

```bash
# Ver procesos
pm2 status

# Ver logs en tiempo real
pm2 logs planta-backend

# Ver logs específicos
pm2 logs planta-backend --lines 100

# Reiniciar aplicación
pm2 restart planta-backend

# Detener aplicación
pm2 stop planta-backend

# Eliminar aplicación
pm2 delete planta-backend

# Ver métricas
pm2 monit

# Guardar configuración actual
pm2 save

# Listar aplicaciones guardadas
pm2 list
```

### Actualizar Aplicación (Deploy)

```bash
# 1. Detener aplicación
pm2 stop planta-backend

# 2. Actualizar código
cd /home/deploy/planta-fruticola
git pull origin main

# 3. Actualizar dependencias (si es necesario)
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 4. Aplicar migraciones
alembic upgrade head

# 5. Reiniciar aplicación
pm2 restart planta-backend
```

---

## 🔐 Variables de Entorno de Producción

### Checklist de Seguridad

- [ ] ✅ `SECRET_KEY` generado con 32+ caracteres aleatorios
- [ ] ✅ `DEBUG=False` en producción
- [ ] ✅ Contraseñas de BD únicas y seguras
- [ ] ✅ `ALLOWED_ORIGINS` solo con dominios específicos
- [ ] ✅ Archivo `.env` **NO** commiteado a Git
- [ ] ✅ Permisos 600 en archivos `.env`

```bash
chmod 600 /home/deploy/planta-fruticola/backend/.env
chmod 600 /home/deploy/planta-fruticola/frontend/.env.production
```

---

## 💾 Backups Automáticos

### 1. Crear Script de Backup

```bash
mkdir -p /home/deploy/backups
nano /home/deploy/scripts/backup.sh
```

Contenido:
```bash
#!/bin/bash

# Configuración
BACKUP_DIR="/home/deploy/backups"
DB_NAME="impeccioncontenedor"
DB_USER="planta_user"
DB_PASS="PASSWORD_SEGURA_AQUI"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup de base de datos
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup de uploads
tar -czf $BACKUP_DIR/uploads_backup_$DATE.tar.gz /home/deploy/planta-fruticola/backend/uploads/

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "uploads_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
```

Dar permisos:
```bash
chmod +x /home/deploy/scripts/backup.sh
```

### 2. Programar con Cron

```bash
crontab -e
```

Agregar:
```cron
# Backup diario a las 2 AM
0 2 * * * /home/deploy/scripts/backup.sh >> /home/deploy/logs/backup.log 2>&1
```

---

## 📊 Monitoreo y Logs

### 1. Logs de NGINX

```bash
# Access logs
sudo tail -f /var/log/nginx/planta-frontend-access.log
sudo tail -f /var/log/nginx/planta-backend-access.log

# Error logs
sudo tail -f /var/log/nginx/planta-frontend-error.log
sudo tail -f /var/log/nginx/planta-backend-error.log
```

### 2. Logs de PM2

```bash
pm2 logs planta-backend
pm2 logs planta-backend --err  # Solo errores
pm2 flush  # Limpiar logs
```

### 3. Logs del Sistema

```bash
# Ver logs del sistema
sudo journalctl -u nginx -f
sudo journalctl -u mysql -f
```

### 4. Configurar Logrotate

```bash
sudo nano /etc/logrotate.d/planta
```

Contenido:
```
/home/deploy/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 deploy deploy
    sharedscripts
}
```

---

## 🔧 Mantenimiento

### Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
sudo systemctl restart nginx
pm2 restart all
```

### Monitorear Recursos

```bash
# CPU y RAM
htop

# Espacio en disco
df -h

# Uso de PM2
pm2 monit
```

### Reiniciar Servicios

```bash
# NGINX
sudo systemctl restart nginx

# MySQL
sudo systemctl restart mysql

# Backend (PM2)
pm2 restart planta-backend
```

---

## 🐛 Troubleshooting

### Problema: Backend no inicia

**Solución:**
```bash
# Ver logs
pm2 logs planta-backend --err

# Verificar variables de entorno
cat /home/deploy/planta-fruticola/backend/.env

# Verificar conexión a BD
mysql -u planta_user -p -e "SELECT 1" impeccioncontenedor

# Reiniciar manualmente
cd /home/deploy/planta-fruticola/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Problema: Frontend muestra error 502

**Solución:**
```bash
# Verificar que NGINX esté corriendo
sudo systemctl status nginx

# Verificar configuración de NGINX
sudo nginx -t

# Ver logs de NGINX
sudo tail -f /var/log/nginx/planta-frontend-error.log

# Verificar que el backend esté corriendo
pm2 status
curl http://localhost:8000/docs
```

### Problema: No se pueden subir fotos

**Solución:**
```bash
# Verificar permisos del directorio uploads
ls -la /home/deploy/planta-fruticola/backend/uploads/

# Ajustar permisos
chmod -R 755 /home/deploy/planta-fruticola/backend/uploads/
chown -R deploy:deploy /home/deploy/planta-fruticola/backend/uploads/

# Verificar límite de tamaño en NGINX
sudo nano /etc/nginx/sites-available/planta-backend
# Buscar: client_max_body_size
```

### Problema: SSL no funciona

**Solución:**
```bash
# Verificar certificados
sudo certbot certificates

# Renovar certificados
sudo certbot renew

# Verificar configuración SSL en NGINX
sudo nano /etc/nginx/sites-available/planta-frontend
```

---

## ✅ Verificación Final del Despliegue

### Checklist de Producción

- [ ] ✅ Backend responde en `https://api.tudominio.com/docs`
- [ ] ✅ Frontend carga en `https://tudominio.com`
- [ ] ✅ Login funciona correctamente
- [ ] ✅ Se pueden crear inspecciones
- [ ] ✅ Cámara funciona (requiere HTTPS)
- [ ] ✅ Subida de fotos funciona
- [ ] ✅ Dashboard muestra estadísticas
- [ ] ✅ SSL configurado correctamente (candado verde)
- [ ] ✅ PM2 procesos corriendo sin errores
- [ ] ✅ Backups programados funcionando
- [ ] ✅ Logs accesibles y configurados
- [ ] ✅ Variables de entorno seguras
- [ ] ✅ Firewall configurado correctamente

---

## 📞 Soporte Post-Despliegue

### Información para Clientes

**URLs del Sistema:**
- Frontend: `https://tudominio.com`
- Backend API: `https://api.tudominio.com`
- Documentación API: `https://api.tudominio.com/docs`

**Credenciales Iniciales:**
```
Email: admin@tudominio.com
Contraseña: [Proporcionada por el administrador]
```

⚠️ **IMPORTANTE:** Cambiar la contraseña después del primer login.

**Contacto Técnico:**
- Email de soporte: soporte@tudominio.com
- Horario: Lunes a Viernes, 9:00 - 18:00

---

## 📚 Referencias Adicionales

- [NGINX Documentation](https://nginx.org/en/docs/)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)

---

**Última actualización:** Octubre 2025  
**Versión del Documento:** 1.0.0

---

## 🎯 Próximos Pasos

Después del despliegue exitoso:

1. **Monitoreo Continuo:** Configurar alertas con herramientas como Uptime Robot
2. **Optimización:** Analizar métricas de rendimiento y optimizar queries lentas
3. **Escalabilidad:** Considerar load balancers si el tráfico aumenta
4. **Seguridad:** Auditorías de seguridad periódicas
5. **Actualizaciones:** Plan de actualización de dependencias mensual

---

**¡Despliegue completado exitosamente! 🎉**
