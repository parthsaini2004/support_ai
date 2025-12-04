# support_ai

AI-powered support assistant for repositories — a starter project combining a Python backend for conversational logic and a React + Vite frontend (ai-chat-client) for the UI.

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
  - Python-based server and automation scripts (repository composition shows a significant Python portion). Use a virtualenv/venv and install dependencies from requirements.txt 

Roadmap / Next steps

- Add a complete example connector to a knowledge base and an example ticketing integration.
- Add automated tests for backend flows and CI configuration.
- Provide docker-compose and a reproducible dev container for quicker onboarding.

