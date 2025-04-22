# MCP Scheduler

This is an MCP server that provides tools to manage events in your google calendar and tasks.

## Adding the MCP Server

## Installation Steps

1. Install [uv](https://docs.astral.sh/uv/) to manage the dependencies, as recomended by [Model context protocol](https://github.com/modelcontextprotocol/python-sdk)

2. **Clone the Repository**

    ```bash
    git clone https://github.com/JorgeVanco/Scheduler-MCP.git
    cd Scheduler-MCP
    ```

3. **Configure Google API Credentials**

    - Go to the [Google Cloud Console](https://console.cloud.google.com/)
    - Create a new project
    - Enable the Google Calendar API and Google Tasks API
    - Create OAuth 2.0 credentials and download the `credentials.json` file
    - Place the `credentials.json` file in the project root directory

4. **Add the MCP config to the model configuration file**
   Add the following JSON configuration to the configuration file:

```json
"mcpServers": {
    "Scheduler": {
        "command": "uv",
        "args": [
            "--directory",
            "C:\\Path\\to\\Scheduler-MCP",
            "run",
            "-m",
            "src.main"
        ]
    }
}
```

> **Note** Replace `C:\\Path\\to\\Scheduler-MCP` with the full path to the Scheduler-MCP folder

This configuration runs the `src.main` module using `uv` in the specified directory.

## Usage

Once configured, your language model will be able to interact with Google Calendar and Google Tasks through this MCP server.

### Example Commands

-   "Schedule a meeting for tomorrow at 10:00 AM"
-   "Show my events for this week"
-   "Create a task to buy groceries"

## Troubleshooting

### Google Authentication

The first time the model starts the MCP server, a Google authentication window will pop up to request access to your calendars. Access tokens are stored in `token.json` to avoid logging in every time.

If you encounter errors, it might be because the token has expired. To fix this, delete the `token.json` file from the Scheduler-MCP folder.

> **Coming Soon:** A tool to automatically manage authentication tokens.
