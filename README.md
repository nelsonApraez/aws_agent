# AwsAgent Crew

Welcome to the AwsAgent Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

- Modify `src/aws_agent/config/agents.yaml` to define your agents
- Modify `src/aws_agent/config/tasks.yaml` to define your tasks
- Modify `src/aws_agent/crew.py` to add your own logic, tools and specific args
- Modify `src/aws_agent/main.py` to add custom inputs for your agents and tasks

## Running the Agent Locally

To run the agent locally for development or testing, follow these steps:

1. **Ensure your `.env` file is configured** as described above.
2. **Install dependencies** (if you haven't already):
   ```powershell
   pip install uv
   uv pip install -r aws_agent/pyproject.toml
   ```
3. **Run the FastAPI server locally:**
   ```powershell
   uvicorn src.aws_agent.api:app --host 0.0.0.0 --port 8000 --reload
   ```
   This will start the API at `http://localhost:8000`.

4. **Test the API endpoint:**
   You can use `curl`, Postman, or any HTTP client to test the `/run-agent` endpoint. Example with `curl`:
   ```powershell
   curl -X POST "http://localhost:8000/run-agent" -H "Content-Type: application/json" -d '{"topic": "your_topic", "session_id": "your_session_id"}'
   ```

## Unit Testing

To run the unit tests for this project, use the following command from the root of the repository (PowerShell):

```powershell
$env:PYTHONPATH="aws_agent/src"; .venv/Scripts/python.exe -m pytest aws_agent/src/aws_agent/tests/ --maxfail=3 --disable-warnings -q
```

This will execute all tests and display a summary of the results.

## Understanding Your Crew

The aws-agent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Environment Variables

The project requires several environment variables to be set in a `.env` file at the root of the `aws_agent` directory. Below is a list of required variables and their explanations:

| Variable                        | Description                                                                                   |
|----------------------------------|-----------------------------------------------------------------------------------------------|
| `MODEL`                         | The model used for Bedrock integration (e.g., `bedrock/amazon.titan-text-express-v1`).        |
| `AWS_ACCESS_KEY_ID`             | Your AWS access key for programmatic access.                                                   |
| `AWS_SECRET_ACCESS_KEY`         | Your AWS secret access key for programmatic access.                                            |
| `AWS_DEFAULT_REGION`            | The AWS region where your resources are deployed (e.g., `us-east-1`).                         |
| `APPINSIGHTS_CONNECTION_STRING` | Azure Application Insights connection string for logging and monitoring.                       |
| `OPENAI_API_KEY`                | (Optional) Your OpenAI API key if you use OpenAI models or services.                          |

**Example `.env` file:**

```env
MODEL=bedrock/amazon.titan-text-express-v1
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...;LiveEndpoint=...;ApplicationId=...
OPENAI_API_KEY=your_openai_api_key
```

### Variable Explanations
- **MODEL**: Specifies the Bedrock model to use for agent tasks.
- **AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY**: Credentials for AWS SDK and CLI operations. Required for accessing AWS services such as ECS, ECR, EC2, and Bedrock.
- **AWS_DEFAULT_REGION**: The default AWS region for all operations.
- **APPINSIGHTS_CONNECTION_STRING**: Used by the application to send logs and telemetry to Azure Application Insights for monitoring and diagnostics.
- **OPENAI_API_KEY**: Only required if you plan to use OpenAI services in your agent configuration.

## Deploying on AWS ECS with Docker

To deploy this solution on AWS ECS using Docker, follow these high-level steps:

1. **Build your Docker image locally:**
   ```powershell
   docker build -t crewai-agent:latest ./aws_agent
   ```
2. **Create an ECR repository and push your image:**
   - Create the repository:
     ```powershell
     aws ecr create-repository --repository-name aws_ecr_container_registry --region us-east-1
     ```
   - Authenticate Docker to ECR:
     ```powershell
     aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com/aws_ecr_container_registry
     ```
   - Tag and push your image:
     ```powershell
     docker tag crewai-agent:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/aws_ecr_container_registry:latest
     docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/aws_ecr_container_registry:latest
     ```
3. **Create an ECS cluster and launch an EC2 instance:**
   - Create the ECS cluster (with tags):
     ```powershell
     aws ecs create-cluster --cluster-name asw_ecs_container_services --region us-east-1 --tags key=project,value=agentic-base key=env,value=dev
     ```
   - Launch an EC2 instance with the ECS-optimized AMI and register it to the cluster (replace values as needed):
     ```powershell
     $CLUSTER_NAME = "asw_ecs_container_services"
     $AMI_ID = "ami-09cc96665c243d56f"
     $INSTANCE_TYPE = "t3.micro"
     $KEY_NAME = "your_key_pair"
     $SECURITY_GROUP = "your_security_group_id"
     $SUBNET_ID = "your_subnet_id"
     $USER_DATA = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("echo ECS_CLUSTER=$CLUSTER_NAME >> /etc/ecs/ecs.config"))
     aws ec2 run-instances `
       --image-id $AMI_ID `
       --count 1 `
       --instance-type $INSTANCE_TYPE `
       --key-name $KEY_NAME `
       --security-group-ids $SECURITY_GROUP `
       --subnet-id $SUBNET_ID `
       --user-data $USER_DATA `
       --region us-east-1
     ```
4. **Register the EC2 instance in ECS:**
   - The instance will automatically register to the ECS cluster if the user-data is set correctly.
   - Verify registration:
     ```powershell
     aws ecs list-container-instances --cluster asw_ecs_container_services --region us-east-1
     ```
5. **Create a Task Definition and Service in ECS:**
   - Define your ECS Task to use the image from ECR and set environment variables as needed.
   - Create a Service to run and manage your container.

For more details, refer to the [AWS ECS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html).

## AWS Lambda and API Gateway Integration

This solution also includes an AWS Lambda function that acts as a bridge between the API exposed by the EC2 instance (running the agent) and an API Gateway. The Lambda function forwards requests to the agent's API and returns the response to the API Gateway, which serves as the public endpoint for external clients.

### Infrastructure Flow
1. **Lambda Function**: Communicates with the agent's API running on EC2. The URL of the agent's API is stored in the Lambda's environment variable `AGENT_API_URL`.
2. **API Gateway**: Triggers the Lambda function and exposes it as a public HTTP endpoint.

### Example Request to API Gateway
To interact with the agent via the API Gateway, send a POST request with the following JSON body:

```json
{
  "topic": "the weight of an elephant",
  "session_id": "123654"
}
```

The API Gateway will trigger the Lambda, which will forward the request to the agent API and return the agent's response.

### Environment Variable
- **AGENT_API_URL**: The URL of the agent's API running on EC2. This must be set in the Lambda's environment variables so it knows where to forward requests.

### Architecture Overview
- **API Gateway** → **Lambda Function** → **EC2 (Agent API)**
- The Lambda function acts as a secure proxy, allowing you to expose your agent API to the internet without exposing the EC2 instance directly.

## Lambda Function Code Example

Below is an example of the AWS Lambda function used to forward requests from API Gateway to the agent API running on EC2. You can include this code directly in your Lambda function in the AWS Console or as part of your infrastructure as code setup.

```python
import os
import json
import urllib.request

def lambda_handler(event, context):
    try:
        url = os.environ['AGENT_API_URL']

        body = json.dumps(event["body"]) if isinstance(event["body"], dict) else event["body"]

        req = urllib.request.Request(
            url=url,
            method="POST",
            headers={"Content-Type": "application/json"},
            data=body.encode("utf-8")
        )

        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            return {
                "statusCode": response.status,
                "body": result
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
```

- The Lambda function expects the environment variable `AGENT_API_URL` to be set to the URL of your agent API running on EC2.
- The function receives the event from API Gateway, forwards the request to the agent API, and returns the response.

## Support

For support, questions, or feedback regarding the AwsAgent Crew or crewAI.
- Visit [documentation](https://docs.crewai.com)

