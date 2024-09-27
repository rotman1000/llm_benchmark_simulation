## LLM Benchmark Microservices

This project contains two microservices for benchmarking various Large Language Models (LLMs):

1. API Service (FastAPI): Exposes an endpoint to query the ranking of LLM models based on specific metrics.
2. Randomizer Service (FastAPI): Generates either real (using Ollama) or fake random data for LLM models and stores the results in PostgreSQL.
3. Frontend Service (React): UI for accessing the saved metrics.
3. PostgreSQL Database: Stores LLM performance metrics such as Time to First Token (TTFT), Tokens per Second (TPS), and End-to-End Latency (e2e_latency).

## Features
- Query rankings of LLMs based on their performance metrics.
- Generate performance data using real or fake LLM models.
- Store and retrieve data from a PostgreSQL database.
- Interact with the API through a user-friendly frontend.
- Deployed using Docker Compose for local setup and Helm for Kubernetes.
- Swagger UI for API and Randomizer services to explore and test endpoints.

## Getting Started
### Prerequisites
- Docker: You can install Docker [here](https://www.docker.com/products/docker-desktop/).
- Docker Compose: Make sure you have Docker Compose installed.
- Helm: You need Helm installed for Kubernetes deployment. Install it [here](https://helm.sh/docs/intro/install/).
- Kubernetes: Use Minikube for local development or a managed Kubernetes service (like GKE, EKS, or AKS).

## Running Locally with Docker Compose
To run the microservices locally using Docker Compose, follow these steps:

1. Clone the repository:

```
git clone <repository-url>
cd llm-benchmark
```

2. Build and start the services:
```
docker-compose up --build
```
3. The services will start with the following ports:
- Frontend Service: localhost:3000
- API Service: localhost:8081
- Randomizer Service: localhost:8080
- PostgreSQL: Exposed on localhost:5432

4. Access the services:
- Frontend: Open http://localhost:3000 in your browser to interact with the system.
- API Swagger Documentation: Visit http://localhost:8081/docs to access the API service Swagger UI.
- Randomizer Swagger Documentation: Visit http://localhost:8080/docs to explore the Randomizer service API.

5. To test the API service, query the rankings endpoint:
```
curl http://localhost:8081/rankings/TTFT
```
5. To test the Randomizer service, generate fake data:
```
curl http://localhost:8080/generate?factory_type=fake
```
## Running with Kubernetes (Helm)
To deploy the services to a Kubernetes cluster using Helm, follow these steps:

1. Ensure Helm is installed and initialized:
```
helm init
```
2. Deploy the PostgreSQL service:
```
cd charts/db
helm install postgres-db .
```
3. Deploy the API service:
```
cd ../api
helm install api-service .
```
4. Deploy the Randomizer service:
```
cd ../randomizer
helm install randomizer-service .
```
5. Verify the services are running:
```
kubectl get pods
```
6. Get the external IPs of the services to access them.

### Environment Variables
Ensure the following environment variables are set for the API and Randomizer services:

DATABASE_URL: The PostgreSQL connection string in the format postgresql://<user>:<password>@<hostname>:5432/<database>.
API_KEY: The API key

Ensure the following environment variables are set for the frontend service:

REACT_APP_API_BASE_URL=http://localhost:8081 (for local setup)
REACT_APP_API_KEY=secret_api_key (for local setup)

## Stopping the Services
To stop the services when running locally with Docker Compose:
```
docker-compose down
```

## Swagger Documentation
Both the API and Randomizer services include auto-generated Swagger UI for API documentation and testing. Once the services are up and running, you can access the Swagger UI for each service:

- API Service Swagger: `http://localhost:8081/docs`
- Randomizer Service Swagger: `http://localhost:8080/docs`
The Swagger UI provides an interactive interface for testing the API endpoints, viewing parameters, and checking responses.
