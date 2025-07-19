# MCP_tutorials
MCP tutorials


## JIRA MCP Server 
Steps1 - Login to jira ->  https://id.atlassian.com/login
Step2 - Go to https://id.atlassian.com/manage-profile/security/api-tokens
Step3 - # Pull Pre-built Image
docker pull ghcr.io/sooperset/mcp-atlassian:latest

### JIRA MCP Server configuration 
  "mcp-atlassian": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e", "JIRA_URL",
                "-e", "JIRA_USERNAME", 
                "-e", "JIRA_API_TOKEN",
                "ghcr.io/sooperset/mcp-atlassian:latest"
            ],
            "env": {
                "JIRA_URL": "https://najiabootrain.atlassian.net/",
                "JIRA_USERNAME": "najiaboo.train@gmail.com",
                "JIRA_API_TOKEN": "ATATT3xFfGF0fP_iraiYHuFwbTrtdq8ZFBlFzBX40_ZI5-705DOgFVFEuZkGmyr0Lw5keMuOmunkasPRsg7ko-MlqcyyOxMVxxoESEV4f8F29IlIRVw_yt05K6b210_Yw2U1j6-GS0sD73KtouYesge11NLMqSuM_eEDeJydqLkawB4oy93ryAw=C32C4D5A"
            },
            "transport": "stdio",
        }
