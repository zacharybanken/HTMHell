### Welcome to HTMHell

When you click a link on this site, an LLM generates the HTML for a new page based on the current page and the ID of the link you clicked on. This requires a decent machine for running Llama2 or another LLM locally.

To run:
1. Install required python packages (pip install -r require)

```
pip install -r requirements.txt
```

2. Install llama2 with ollama (using homebrew on MacOS):

```
brew install ollama
ollama pull llama2
```

3. Run ollama in a terminal window:

```
ollama serve
```

4. Launch web server from a terminal in the project:

```
uvicorn main:app --reload
```

5. Go to http://localhost:8000/ in your browser

This project was made with the help of ChatGPT and Claude.