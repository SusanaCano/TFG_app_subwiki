# Usa la imagen oficial de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de package.json y package-lock.json
COPY ./app/package*.json ./app/yarm.lock* ./

# Instala las dependencias
RUN npm install
RUN yarn install

# Copia el resto de los archivos de tu aplicación
COPY . .

# Exponer el puerto en el que la app Next.js estará disponible
EXPOSE 3000

# Comando para correr Next.js en producción
CMD ["npm", "run", "dev", "yarn"]

