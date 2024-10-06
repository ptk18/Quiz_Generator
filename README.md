# OS_Project
The is a Docker-based multi-tier web application designed to provide a user-friendly quiz generation and management system. It leverages **SvelteKit** for the frontend, delivering a responsive and dynamic user interface, while the backend is powered by **FastAPI**, ensuring fast and efficient API interactions. The application connects to a **MySQL** database, managed through SQLAlchemy for seamless data manipulation and ORM capabilities. Additionally, it incorporates the **Google Generative AI LLM model** to generate quiz questions dynamically, enhancing user engagement and personalization. The entire application is containerized using **Docker**, allowing for easy deployment and scalability, making it a robust solution for quiz generation and management in various environments. With its well-structured architecture and innovative features, the OS_Project aims to deliver an engaging experience for users while maintaining simplicity and performance.

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
