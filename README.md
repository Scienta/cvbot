# Welcome to CvBot, an OpenAI assistant with CvPartner functions

This is CvBot, an assistant with a few functions to find list all people in your CvPartner database and get their
resumes.

# Implementation

The bot is running as a [Streamlit](https://streamlit.io) application. Streamlit is an easy to use, immediate mode web
framework that doesn't require any client-side programming. All UI widgets and behavior are created with and implemented
in Python.

Streamlit is a quite special framework, as it evaluates the entire file on every run and only sends the required updates
to the web UI. This has the nice advantage that will also automatically pick up any changes in your source code whenever
the UI is reloaded, giving a very short pause for each iteration.

It uses the native OpenAI Python API, a good starting point is their
[Assistant Overview page](https://platform.openai.com/docs/assistants/overview).

CvPartner doesn't have an API client, but this repository contains an [OpenAPI specification file](./cvpartner-api.yml)
that is used to generate a Python client.

# Running CvBot

**API Keys**: CvBot requires an API keys for both systems, and they can be generated under
[OpenAI's API keys page](https://platform.openai.com/api-keys) and
[CvPartner Account -> API Keys](https://docs.cvpartner.com/configuration-&-security#overview--authorization).

The secrets can be put in `.streamlit/secrets.toml` (which is ignored by git) like this:

```toml
CVPARTNER_API_KEY = "..."
OPENAI_API_KEY = "..."
ASSISTANT_ID = "..."
```

**Create the assistant**: Go to [The assistants page](https://platform.openai.com/assistants) and create a new
assistant. Select the GPT model you want to use. This can be changed later at any time. There is no need to add any
functions as they will be added on each request.

**Getting the dependencies**: If you're on Linux (and maybe OSX) you can run `bin/python-tool` to have it automatically
create a virtualenv for you with all requirements. If you want/need to manage the dependencies by hand, create a
virtualenv and use `bin/requirements.txt` when installing the dependencies.

If you are running this from PyCharm, register `bin/env` as your current interpreter.

**Starting the application**: There are multiple ways of running the application. If you want to work on the system
and are using PyCharm there is a run configuration for `cvbot` already configured.

If you want to configure another IDE's launcher, run the `streamlit` module with `run cvbot.py` as its argument.

Another option is to run the application from the command line:

```shell
bin/streamlit run cvbot.py
```

In any case you choose, the application requires the `OPENAPI_API_KEY` and `CVPARTNER_API_KEY` environment variables to
set. Make sure `.streamlit/secrets.toml` is configured (see above).

# Resources

* OpenAI
  * [Assistants Overview](https://platform.openai.com/docs/assistants/overview)
  * [Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
* Streamlit
  * [Docs](https://docs.streamlit.io/)
  * [Cheat sheet](https://cheat-sheet.streamlit.app/)
* CV Partner
  * API: https://docs.cvpartner.com/
