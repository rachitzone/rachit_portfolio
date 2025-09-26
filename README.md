# Rachit Singh — Portfolio (React + Tailwind + Framer Motion + Django REST)

A playful, interactive portfolio inspired by jhey.dev—but uniquely yours. Built with a modern React frontend and a Django REST API backend.

Sections
- Hero: Animated headline, signature SVG, live location & weather, Spotify Now Playing, particle background, parallax grid
- About: Short bio with hover tilt profile
- Projects: Cards with tilt/parallax, modal details
- Skills: Icon grid with microinteractions
- Blog: Fetched from Django API (list + detail)
- Contact: Animated form inputs, email, social links
- Footer: Minimal and clean

Tech Stack
- Frontend: React (Vite), TailwindCSS, Framer Motion, Axios
- Backend: Django, Django REST framework, django-cors-headers, requests, python-dotenv
- Optional: Docker for dev orchestration

Quickstart
1) Prereqs
- Node 18+ and npm (or pnpm/yarn)
- Python 3.10+

2) Backend setup
- Copy backend/.env.template to backend/.env and set values (especially Spotify)
- Create a virtualenv and install requirements
  - Windows (PowerShell):
    python -m venv .venv
    .venv\\Scripts\\Activate.ps1
    pip install -r requirements.txt
  - macOS/Linux:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
- Run migrations and start server
    python backend/manage.py migrate
    python backend/manage.py createsuperuser  # optional, to add blog posts via admin
    python backend/manage.py runserver 0.0.0.0:8000

3) Frontend setup
- Create frontend/.env and set VITE_API_BASE_URL (default http://127.0.0.1:8000)
- Install deps and start dev server
    cd frontend
    npm install
    npm run dev

Environment Variables
- backend/.env
  - DEBUG=true
  - ALLOWED_HOSTS=127.0.0.1,localhost
  - CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
  - SPOTIFY_CLIENT_ID=your_client_id
  - SPOTIFY_CLIENT_SECRET=your_client_secret
  - SPOTIFY_REFRESH_TOKEN=your_refresh_token
- frontend/.env
  - VITE_API_BASE_URL=http://127.0.0.1:8000

Spotify Notes
- This project expects a long-lived refresh token. Steps:
  1. Create a Spotify app at https://developer.spotify.com/dashboard
  2. Add a Redirect URI (e.g., http://localhost:8888/callback)
  3. Obtain a refresh token using an OAuth helper (you can use a temporary script or a tool like Postman)
  4. Put CLIENT_ID, CLIENT_SECRET, and REFRESH_TOKEN into backend/.env

APIs
- GET /api/location-weather/?lat={lat}&lon={lon}
  - Returns: { city, temperature, condition }
  - If lat/lon omitted, backend attempts IP lookup
- GET /api/spotify/
  - Returns current playing track metadata (if any)
- GET /api/blogs/?page=1
  - Paginated blog list (title, slug, excerpt, created_at)
- GET /api/blogs/{slug}/
  - Blog detail (title, slug, content, created_at)

Docker (optional)
- docker compose up --build
- Frontend: http://localhost:5173, Backend: http://localhost:8000

Recording a Preview (GIF + MP4)
- Start both servers
- From frontend/, run: npm run record
- Outputs to frontend/preview/portfolio.mp4 and portfolio.gif

Project Structure
portfolio/
├─ README.md
├─ .gitignore
├─ docker-compose.yml (optional)
├─ requirements.txt        # Backend deps
├─ backend/                # Django project
└─ frontend/               # React app

License
- Personal use for Rachit Singh.
