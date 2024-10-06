# OS_Project
 Docker-based project

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repo-url>
   ```

2. Copy `.env.example` files:
   ```bash
   cp .env.example .env
   cp frontend/.env.example frontend/.env
   cp backend/.env.example backend/.env
   ```

3. Run Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: `http://localhost:5173`
   - Backend (API): `http://localhost:8000`
   - Database: `http://localhost:3306`
