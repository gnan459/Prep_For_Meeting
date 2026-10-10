# Prep_For_Meeting — AI-Powered Meeting Preparation Assistant

An AI-powered meeting preparation assistant that automates pre-meeting research, analyzes industry trends, and generates actionable talking points using a collaborative multi-agent architecture.

## Overview

Preparing for important meetings often involves researching participants, understanding the industry, identifying opportunities, and developing relevant questions. **Prep_For_Meeting** streamlines this process using specialized AI agents that work together to generate a structured meeting briefing based on the meeting context and objectives.

Built with CrewAI, Google Gemini, and Streamlit, the application transforms user-provided meeting details into a briefing to help users prepare more effectively and make informed decisions.

## Features

- **Participant Research:** Researches meeting participants using web-search tools and available professional profile information.
- **Industry Analysis:** Identifies relevant industry trends, challenges, opportunities, and developments.
- **Strategic Recommendations:** Generates objective-driven talking points, discussion questions, and recommendations.
- **Multi-Agent Collaboration:** Coordinates specialized AI agents through dependent tasks to produce a comprehensive briefing.
- **Interactive Web Interface:** Provides a Streamlit interface for entering meeting details and viewing results.
- **Downloadable Reports:** Allows users to download the generated meeting briefing as a text file.

## Architecture

The application uses a multi-agent workflow orchestrated by CrewAI.

```text
                  User Input
                      |
          +-----------+-----------+
          |           |           |
     Participants   Context    Objective
          |           |           |
          +-----------+-----------+
                      |
                CrewAI Workflow
                      |
          +-----------+-----------+
          |                       |
   Research Specialist      Industry Analyst
          |                       |
   Participant Research     Industry Insights
          |                       |
          +-----------+-----------+
                      |
               Strategy Advisor
                      |
          Talking Points and Questions
                      |
             Briefing Coordinator
                      |
               Final Meeting Brief
                      |
             Streamlit Interface
                      |
               Download Report
```

### AI Agents

| Agent | Responsibility |
|---|---|
| Research Specialist | Collects relevant information about meeting participants using search tools. |
| Industry Analyst | Examines industry trends, challenges, and potential opportunities. |
| Strategy Advisor | Develops strategic questions, talking points, and recommendations based on the research. |
| Briefing Coordinator | Synthesizes the outputs into a structured meeting briefing. |

### Workflow

1. The user enters participant names, meeting context, and the desired meeting objective.
2. Research and industry analysis tasks gather relevant information using configured search tools.
3. The strategy agent uses the findings to develop targeted discussion points and questions.
4. The briefing coordinator combines the task outputs into a report.
5. The application displays the briefing and provides an option to download it.

## Technology Stack

- **Language:** Python
- **Multi-Agent Framework:** CrewAI
- **Large Language Model:** Google Gemini 2.5 Flash
- **Frontend:** Streamlit
- **Search Tools:** Serper Search and Exa
- **Environment Configuration:** python-dotenv
- **Containerization:** Docker and Docker Compose

## Project Structure

```text
Prep_For_Meeting/
├── agents.py          # AI agent definitions
├── tasks.py           # Agent tasks and workflow dependencies
├── crew.py            # CrewAI orchestration
├── llm.py             # Language model configuration
├── tools.py           # Search and research tools
├── app.py             # Streamlit application
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker image configuration
├── docker-compose.yml # Container orchestration
├── .env.example       # Example environment configuration
└── README.md          # Project documentation
```

> **Note:** The file tree above is illustrative. Adjust filenames and commands to match the current repository.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- pip
- A Google Gemini API key
- A Serper API key
- An Exa API key, if required by the configured search tools

### 1. Clone the Repository

```bash
git clone https://github.com/gnan459/Prep_For_Meeting.git
cd Prep_For_Meeting
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the API keys required by your configuration.

```env
GOOGLE_API_KEY=your_google_gemini_api_key
SERPER_API_KEY=your_serper_api_key
EXA_API_KEY=your_exa_api_key
```

Replace the placeholders with your actual API keys. Use the variable names expected by your application's code.

**Security:** Never commit your `.env` file or expose API keys in source code. Keep your credentials private.

### 5. Run the Application

Launch Streamlit using the correct entry-point filename for your repository. For example:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the application.

## Usage

1. Launch the application.
2. Enter the names of the meeting participants.
3. Describe the meeting context and background.
4. Specify the primary objective of the meeting.
5. Start the preparation workflow.
6. Review the generated participant research, industry insights, talking points, and recommendations.
7. Download the final meeting briefing for reference during the meeting.

## Configuration

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Authenticates access to Google Gemini if expected by the LLM configuration. |
| `SERPER_API_KEY` | Enables Serper-powered web search. |
| `EXA_API_KEY` | Enables Exa-powered research, if configured. |

Ensure the variable names match those referenced in the application code.

## Docker Deployment

If Docker and Docker Compose are configured for the project, build and start the application using:

```bash
docker compose up --build
```

Check the Docker configuration and environment-variable setup before deploying. Do not embed API keys directly in the Docker image.

## Limitations

- Research quality depends on the availability and relevance of external search results.
- AI-generated information may be incomplete or inaccurate and should be verified before important meetings.
- Access to external research services depends on valid API credentials, service availability, and usage limits.
- The application generates briefing material and recommendations; it does not guarantee meeting outcomes.

## Future Improvements

- Integrate Google Calendar and Outlook for automated meeting detection.
- Generate downloadable PDF and Markdown reports.
- Add persistent storage for previous meeting briefs.
- Include source citations and links for improved research traceability.
- Add configurable agent workflows for different meeting types.
- Implement structured output validation and quality checks.
- Support additional LLM providers and caching to reduce repeated API calls.

## Security

- Store API keys in environment variables.
- Keep `.env` and other secret files out of version control.
- Review generated research before sharing sensitive meeting information.
- Follow the terms and usage policies of the configured LLM and search providers.

## Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request describing the improvements.

## License

Add the license applicable to this repository. If no license has been selected, the project remains subject to the default copyright rules.

---

**Built with Python, CrewAI, Google Gemini, and Streamlit.**
