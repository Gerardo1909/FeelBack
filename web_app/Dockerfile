FROM python:3.11.4

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .
COPY setup.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]