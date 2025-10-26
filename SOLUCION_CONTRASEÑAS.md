# 🔐 Solución de Problemas de Contraseñas

## ❌ Problema Común

Cada vez que descargas el proyecto en una nueva PC, las contraseñas no funcionan en el login, mostrando error 500.

## 🔍 Causa

El archivo `database/inspeccioncontenedor.sql` contenía hashes de contraseñas incorrectos que no funcionaban con el sistema de autenticación bcrypt.

## ✅ Solución Implementada

### 1. **Archivo SQL Corregido**
- ✅ `database/inspeccioncontenedor.sql` ahora tiene hashes correctos
- ✅ Contraseña para todos los usuarios: `123456`

### 2. **Script de Corrección Automática**
- ✅ `backend/fix_passwords.py` - Script para corregir contraseñas existentes
- ✅ Se ejecuta automáticamente en `ejecucionAutomatica.bat`

### 3. **Credenciales de Prueba**
```
Inspector:  juan.diaz@empresa.com / 123456
Supervisor: maria.lopez@empresa.com / 123456
Admin:      carlos.ruiz@empresa.com / 123456
```

## 🚀 Uso

### Opción 1: Instalación Nueva
```bash
.\ejecucionAutomatica.bat
```
El script corregirá automáticamente las contraseñas.

### Opción 2: Corrección Manual
Si ya tienes la base de datos importada:
```bash
cd backend
python fix_passwords.py
```

### Opción 3: Importar BD Corregida
1. Ve a phpMyAdmin: http://localhost/phpmyadmin
2. Elimina la base de datos `inspeccioncontenedor`
3. Crea una nueva base de datos `inspeccioncontenedor`
4. Importa el archivo `database/inspeccioncontenedor.sql` corregido

## 🔧 Detalles Técnicos

- **Hash usado**: bcrypt con salt de 12 rounds
- **Librería**: passlib[bcrypt]==1.7.4
- **Formato**: `$2b$12$...`

## 📝 Notas

- El problema ocurría porque los hashes en el SQL original no correspondían a la contraseña "123456"
- Ahora el archivo SQL tiene hashes correctos generados con la misma librería que usa el backend
- El script de corrección se ejecuta automáticamente para evitar problemas futuros
