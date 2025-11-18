# Medical Emergency AI System

[![Repository](https://img.shields.io/badge/GitHub-ZouhairChoufa/medical--emergency--ai--system-blue)](https://github.com/ZouhairChoufa/medical-emergency-ai-system.git)

An AI-powered multi-agent system for managing medical emergencies, built with CrewAI and Flask. This project leverages collaborative AI agents to handle emergency response coordination, patient information processing, and decision-making support in critical medical situations.

## Features

- **Multi-Agent AI Coordination**: Utilizes CrewAI to deploy specialized AI agents for emergency management tasks.
- **Web Interface**: Flask-based web application for user interaction and patient information input.
- **Configurable Agents and Tasks**: Easily customize agents via YAML configurations.
- **Knowledge Base Integration**: Includes a knowledge base for user preferences and medical data.
- **Dependency Management**: Uses UV for fast and reliable Python package management.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling.

1. Install UV if you haven't already:
   ```bash
   pip install uv
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/ZouhairChoufa/medical-emergency-ai-system.git
   cd medical-emergency-ai-system
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env` (if available) or create a new `.env` file.
   - Add your `OPENAI_API_KEY` and any other required API keys to the `.env` file.

## Configuration

- **Agents**: Modify `src/systeme_urgences_medicales/config/agents.yaml` to define your AI agents.
- **Tasks**: Modify `src/systeme_urgences_medicales/config/tasks.yaml` to define tasks for the agents.
- **Crew Logic**: Customize `src/systeme_urgences_medicales/crew.py` for specific logic, tools, and arguments.
- **Inputs**: Adjust `src/systeme_urgences_medicales/main.py` for custom inputs.

## Running the Project

### AI Crew Execution
To run the AI crew and execute tasks:
```bash
uv run crewai run
```
This will initialize the medical emergency AI system, assembling agents and assigning tasks as configured.

### Web Application
To start the Flask web app:
```bash
uv run python web_app.py
```
Access the web interface at `http://localhost:5000` (or the configured port).

## Project Structure

- `src/systeme_urgences_medicales/`: Core AI crew implementation.
- `web_app.py`: Flask web application for user interface.
- `patient_info_page.py`: Patient information handling.
- `knowledge/`: Knowledge base files.
- `tests/`: Unit tests.
- `config/`: Agent and task configurations.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, questions, or feedback:
- Visit the [GitHub repository](https://github.com/ZouhairChoufa/medical-emergency-ai-system.git)
- Check CrewAI [documentation](https://docs.crewai.com)
- Join the CrewAI [Discord](https://discord.com/invite/X4JWnZnxPb)

Let's save lives with the power of AI!
