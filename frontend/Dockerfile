# Etapa 1: Compilación de Angular
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build -- --configuration production

# Etapa 2: Servidor Nginx para producción
FROM nginx:alpine
# Nota: La ruta exacta depende del nombre de tu proyecto en angular.json
# Usualmente es /app/dist/[nombre-proyecto]/browser
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]