FROM python:3.13-slim

# Definir argumentos para autenticação básica
ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

# Definir variáveis de ambiente
ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD_ARG

# Definir diretório de trabalho
WORKDIR /usr

# Copiar arquivo de dependências
COPY ./requirements.txt /usr/requirements.txt

# Instalar dependências sem cache
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar código-fonte para o diretório de trabalho
COPY ./src /usr/src

# Definir ponto de entrada
ENTRYPOINT [ "python3" ]

# Definir comando padrão para executar a aplicação
CMD [ "src/main.py" ]
