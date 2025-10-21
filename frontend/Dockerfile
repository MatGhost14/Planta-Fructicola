# Usar Node.js 18 como imagen base
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 5173

# Comando para ejecutar en desarrollo
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
