# Neuroscholar Bot

This repository contains the Neuroscholar bot designed to assist with answering questions about NLP papers.

## How to Run

### Setting Up the Environment

Start by setting up the Python environment using Poetry:

```console
poetry shell
poetry install
```

### Clone and Setup DeepPavlov Dialog Flow Framework (DFF)

Clone the DFF repository for monitoring and analytics capabilities, then install it with the necessary dependencies:

```bash
git clone https://github.com/deeppavlov/dialog_flow_framework.git
cd dialog_flow_framework
pip install .[stats]
docker compose --profile stats up -d
```

### Run the Bot

Navigate back to the root directory of your project and set environment variables for your bot:

```bash
cd ..
export TG_BOT_TOKEN=YOUR_TOKEN
export COHERE_API_KEY=YOUR_TOKEN
docker compose up
```

### Networking

Join the containers into a single network to facilitate communication between them:

```bash
docker network create botnetwork
docker network connect botnetwork otel-col
docker network connect botnetwork neuroscholar_bot-bot-1
```

### Analytics and Monitoring

Run the following command to generate and check analytics:

```bash
dff.stats tutorials/stats/example_config.yaml -P superset -dP pass -U superset --outfile=config_artifact.zip
```

### Accessing the Dashboard

Proceed to the dashboard by navigating to the following URL in your web browser:

```
localhost:8088
```

---

**Note:** Ensure you replace `YOUR_TOKEN` placeholders with actual API keys and tokens for Telegram and Cohere.

