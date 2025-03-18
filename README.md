# Flask App com Docker

Um aplicativo Flask simples usando Docker para facilitar a implantação e execução em qualquer ambiente.

## Descrição

Este projeto é uma aplicação web Flask básica containerizada com Docker. A estrutura permite o desenvolvimento local e a implantação simplificada em ambientes de produção, garantindo consistência em diferentes plataformas.

## Pré-requisitos

* [Docker](https://www.docker.com/get-started) instalado na sua máquina
* [Docker Compose](https://docs.docker.com/compose/install/) (opcional, para facilitar a execução)
* Git para clonar o repositório

## Estrutura do Projeto

```
flask-app-docker/
│
├── .github/
│   └── workflows/
│       └── cloud-run.yml
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── templates/
│       └── index.html
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## Instalação e Execução

### Usando Docker Compose (recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/william-clnunes/flask-app-docker.git
   cd flask-app-docker
   ```

2. Execute o aplicativo com Docker Compose:
   ```bash
   docker-compose up
   ```

3. Acesse o aplicativo em seu navegador:
   ```
   http://localhost:5000
   ```

### Usando Docker diretamente

1. Clone o repositório:
   ```bash
   git clone https://github.com/william-clnunes/flask-app-docker.git
   cd flask-app-docker
   ```

2. Construa a imagem Docker:
   ```bash
   docker build -t flask-app .
   ```

3. Execute o contêiner:
   ```bash
   docker run -p 5000:5000 flask-app
   ```

4. Acesse o aplicativo em seu navegador:
   ```
   http://localhost:5000
   ```

## Desenvolvimento

Para desenvolvimento local, você pode editar os arquivos na pasta `app/` e reiniciar o contêiner para ver suas alterações.

Se você estiver fazendo alterações frequentes, considere montar o diretório como um volume:

```bash
docker run -p 5000:5000 -v $(pwd)/app:/app/app flask-app
```

## Implantação

Este projeto está pronto para ser implantado em qualquer ambiente que suporte Docker, como:

* AWS ECS
* Google Cloud Run
* Azure Container Instances
* Kubernetes
* Plataformas PaaS como Heroku (com suporte a Docker)

## CI/CD com GitHub Actions

Este projeto utiliza GitHub Actions para automatizar o processo de implantação contínua no Google Cloud Run. O workflow está configurado no arquivo `.github/workflows/cloud-run.yml`.

### Funcionalidades do Workflow

O workflow de CI/CD realiza as seguintes operações automaticamente quando há um push para a branch `main`:

1. Configura a autenticação com o Google Cloud
2. Configura o Docker para usar a autenticação do Google Cloud
3. Constrói a imagem Docker da aplicação
4. Envia a imagem para o Google Container Registry
5. Implanta a imagem no Google Cloud Run

### Requisitos para o GitHub Actions

Para que o workflow funcione corretamente, você precisa configurar os seguintes secrets no seu repositório GitHub:

- `GCP_PROJECT_ID`: ID do seu projeto no Google Cloud
- `GCP_SA_KEY`: Chave de conta de serviço do Google Cloud em formato JSON (codificada em base64)
- `GCP_APP_NAME`: Nome da sua aplicação no Google Cloud Run

### Como funciona

```yaml
# Quando é feito um push na branch main, o workflow é acionado
on:
  push:
    branches:
      - main

# Permissões necessárias para implantação
permissions:
  contents: read
  id-token: write

# Jobs a serem executados
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      # Checkout do código-fonte
      - uses: actions/checkout@v3

      # Autenticação com o Google Cloud
      - uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      # Configuração do Docker para o Google Cloud
      - uses: google-github-actions/setup-gcloud@v1
      - run: gcloud auth configure-docker

      # Build e push da imagem Docker
      - name: Build & Push
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/${{ secrets.GCP_APP_NAME }}:${{ github.sha }} .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/${{ secrets.GCP_APP_NAME }}:${{ github.sha }}

      # Implantação no Google Cloud Run
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy ${{ secrets.GCP_APP_NAME }} \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/${{ secrets.GCP_APP_NAME }}:${{ github.sha }} \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --project ${{ secrets.GCP_PROJECT_ID }}
```
