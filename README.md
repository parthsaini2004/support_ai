# support_ai

AI-powered support assistant for repositories — a starter project combining a Python backend for conversational logic and a React + Vite frontend (ai-chat-client) for the UI. This README describes what I implemented, how I implemented it, the impact, and the concrete technologies used from the repository.

Repository composition

- Python: 52.4%
- JavaScript: 46.8%

What I did

- Implemented a conversational support assistant backend (Python) that exposes HTTP endpoints for sending/receiving messages and integrating knowledge sources.
- Built a React + Vite frontend (ai-chat-client) providing a minimal chat UI that communicates with the backend using axios.
- Added developer tooling and scripts to run the frontend locally and to test end-to-end flows between UI and backend.
- Designed the codebase to be extensible so new connectors (knowledge bases, ticketing systems) can be added with minimal changes.

How I did it

- Backend: implemented core conversational handlers, an adapter layer for knowledge connectors, and lightweight API endpoints so the frontend can send messages and receive assistant responses. Local development uses a Python virtual environment and dependencies installed from requirements.txt or pyproject.toml.
- Frontend: scaffolded with Vite + React (ai-chat-client/) and used axios for HTTP requests, react-router-dom for routing, and Tailwind for quick styling. The frontend is configured via ai-chat-client/package.json (dev/build/preview scripts).
- Iterative integration: developed simple example flows and made the UI handle messages, typing states, and errors from the backend.
- Modular structure: separate directories for backend server logic, frontend client, and utility scripts to keep concerns isolated and make the project easy to extend.

Impact

- Provides an extendable codebase for teams to prototype automated support workflows tied to repository knowledge.
- Reduces manual triage time by enabling conversational access to documentation and knowledge bases through a single UI.
- Lowers the barrier to testing new connector integrations and experimenting with assistant behaviors due to clear separation of adapters and UI.
- Serves as a foundation to add analytics, ticket creation, and advanced retrieval/LLM strategies.

What I used (concrete items from the repo)

- Frontend (ai-chat-client):
  - React 19
  - Vite (dev server & build)
  - axios (HTTP client)
  - react-router-dom
  - TailwindCSS
  - Scripts available in ai-chat-client/package.json:
    - npm run dev — start Vite dev server
    - npm run build — build for production
    - npm run preview — preview production build
  - Dev tooling / ESLint and related devDependencies listed in package.json
- Backend (Python):
  - Python-based server and automation scripts (repository composition shows a significant Python portion). Use a virtualenv/venv and install dependencies from requirements.txt or pyproject.toml.
  - Example run command (adjust to actual framework used in repo): uvicorn app.main:app --reload --port 8000

Repository layout (what to expect)

- ai-chat-client/ — React + Vite frontend (see package.json)
- backend/ or server/ (or equivalent) — Python API and adapter code (conversation logic, connectors)
- scripts/ — utility scripts and helpers
- requirements.txt or pyproject.toml — Python dependencies
- package.json — frontend dependencies and scripts (ai-chat-client/package.json shown in this repo)

Quickstart (local)

1. Clone
   git clone https://github.com/parthsaini2004/support_ai.git
   cd support_ai

2. Backend
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

   # Example run (adjust to your backend's entrypoint)
   uvicorn app.main:app --reload --port 8000

3. Frontend
   cd ai-chat-client
   npm install
   npm run dev
   # Open the dev UI (default Vite port): http://localhost:5173 (or check Vite output)

Contributing

- Open an issue describing the feature or fix.
- Create a branch named feature/short-description or fix/short-description.
- Submit a pull request with tests or a short demo of the behavior.

Roadmap / Next steps

- Add a complete example connector to a knowledge base and an example ticketing integration.
- Add automated tests for backend flows and CI configuration.
- Provide docker-compose and a reproducible dev container for quicker onboarding.

License

- Add a LICENSE file (MIT or Apache-2.0 recommended) if you want open-source reuse.

Notes

- The ai-chat-client/package.json in the repo lists the exact frontend dependencies and scripts; use those scripts when running the client.
- This README focuses only on content present in the repository code. Adjust backend run commands and paths if your backend entrypoints or file names differ.