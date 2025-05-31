#FROM node:20-alpine AS base
#node:lts-alpine as builder
#node:22.13.0
#FROM node:20-slim AS base
FROM node:20 AS base

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN rm -rf node_modules # Fuerza la eliminación de node_modules si existiera de una capa anterior
#RUN npm install
RUN npm ci

COPY . .

# ---- INICIO DE DEPDEBUGGING ----
RUN echo ">>> Contenido de /app/eslint.config.mjs en el contenedor:" && \
    cat /app/eslint.config.mjs && \
    echo ">>> Fin del contenido de eslint.config.mjs"

RUN echo ">>> Contenido de /app/src/app/api/kegg/pathway_graph/[pathwayId]/route.ts:" && \
    cat /app/src/app/api/kegg/pathway_graph/[pathwayId]/route.ts && \
    echo ">>> Fin del contenido de route.ts" # Asegúrate que la ruta al archivo sea correcta

RUN echo ">>> Listando archivos .eslint* en /app:" && \
    ls -la /app/.eslint* || echo "No se encontraron archivos .eslint*"
# ---- FIN DE DEBUGGING ----

# build static assets
#RUN npm run build && npm run export
RUN npm run build

# Expone el puerto en el que correrá Next.js
EXPOSE 3000

CMD ["npm", "run", "start"] 
# "dev"
