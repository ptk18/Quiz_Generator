## Backend Setup Instructions

Follow these steps to set up the backend for the project.

### Prerequisites

- Python 3.x
- `pip` package manager

### Installation

1. Clone the repository:

   git clone https://github.com/yourusername/yourproject.git
   cd yourproject/backend

2. Set up a virtual environment:

    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:

    pip install -r requirements.txt

4. Set up environment variables:

- Create a .env file in the backend folder and add the required environment variables such as API_KEY and database configurations. In .env file:

    API_KEY=your_api_key_here

- Alternatively, export the API_KEY directly in your terminal before starting the server:

export API_KEY=your_api_key_here   # On Windows, use `set API_KEY=your_api_key_here`

5. Run the FastAPI server:

    uvicorn main:app --reload