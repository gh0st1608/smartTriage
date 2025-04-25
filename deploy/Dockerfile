# Usar una imagen de Python
FROM python:3.10-alpine

# Definir el directorio de trabajo
WORKDIR /var/www

# Copiar el contenido esencial al contenedor
COPY requirements.txt /var/www/
COPY app/ /var/www/app/
COPY main.py /var/www/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que correrá Flask
EXPOSE 3333

# Ejecutar la aplicación Flask
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3333", "app.main:app"]