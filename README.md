# AI Resume Generator

AI-powered resume generator - Automatically create professional resumes using LLMs and prompt engineering

## Project Structure

```
├── Backend/
│   └── app.py              # Backend application logic
├── Frontend/
│   ├── frontend.py         # Frontend user interface
│   └── resume_export.py    # Resume export functionality
├── keys/
│   └── .env                # Environment variables (not committed)
├── requirements.txt        # Python dependencies
└── .gitignore              # Git ignore rules
```

## Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "AI Resume Generator"
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   - **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
   - Create or update `keys/.env` with your API keys and configuration

## Usage

### Running the Backend
```bash
python Backend/app.py
```

### Running the Frontend
```bash
python Frontend/frontend.py
```

## Features

- Generate AI-powered resumes
- Export resumes in multiple formats
- User-friendly interface

## Environment Variables

Store sensitive information in `keys/.env`:
```
API_KEY=your_api_key_here
DATABASE_URL=your_database_url
```

## Security

- Never commit `keys/.env` to version control (see [.gitignore](.gitignore))
- Keep API keys and sensitive data secure
- Use environment variables for configuration

## License

[Add your license here]

## Contributors

[Add contributors information]
