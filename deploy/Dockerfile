# Imagen base ligera con Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto del código
COPY . .

# Expone el puerto de tu aplicación Flask
EXPOSE 3333

# Configura variables de entorno para Flask
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Comando para arrancar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=3333"]
