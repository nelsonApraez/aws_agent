# Utiliza una imagen oficial de Python como base
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instala poetry para gestionar dependencias
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copia el resto del código fuente al contenedor
COPY ./src ./src

ENV MODEL=bedrock/amazon.titan-text-express-v1
ENV AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=us-east-1
ENV APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=YOUR_INSTRUMENTATION_KEY;IngestionEndpoint=https://region.in.applicationinsights.azure.com/;LiveEndpoint=https://region.livediagnostics.monitor.azure.com/;ApplicationId=YOUR_APPLICATION_ID

# Expone el puerto 8000 para FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.aws_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]
