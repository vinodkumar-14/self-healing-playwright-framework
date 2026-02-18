## Step 1: Install Python
`python3 --version`

## Step 2: Create Virtual Environment
```
mkdir ai_playwright_framework
cd ai_playwright_framework

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```

## Step 3: Install Dependencies
```
pip install playwright pytest pytest-html requests
playwright install
```

## Step 4: Install Ollama (Free Local LLM)
Install Ollama: https://ollama.com
### Download
`curl -fsSL https://ollama.com/install.sh | sh`
### Pull Model
`ollama pull mistral`
### Run Test
`ollama run mistral`