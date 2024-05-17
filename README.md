# Neuroscholar Bot

This repository contains the Neuroscholar bot designed to assist with answering questions about NLP papers.

## How to Run

### Setting Up the Environment

Start by setting up the Python environment using Poetry:

```console
poetry shell
poetry install
```

### Configure env file

```bash
mv .env_example .env
```

Set ***TG_BOT_TOKEN*** and ***COHERE_API_KEY***

### Run the bot

```bash
docker compose up
```

### Analytics and Monitoring

Run the following command to generate and check analytics:

```bash
dff.stats example_config.yaml -P superset -dP pass -U superset --outfile=config_artifact.zip
```

### Accessing the Dashboard

Proceed to the dashboard by navigating to the following URL in your web browser:

```
localhost:8088
```