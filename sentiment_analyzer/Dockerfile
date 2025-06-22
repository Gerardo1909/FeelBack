FROM python:3.11.4

# Establecer el directorio de trabajo
WORKDIR /sentiment_analyzer

# Copiar archivos de dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .
COPY setup.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copiar el resto del código del microservicio
COPY . .

# Exponer el puerto para la API del microservicio
EXPOSE 5001

# Comando para ejecutar el microservicio
CMD ["python", "run.py"]