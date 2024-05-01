### Deployment URL:

https://avamore-software-developer-test-4fqmcyft1.vercel.app/

### This repository contains 3 things:

1. A python script for running the ARM redemption model algorithm, called `arm_script.py`
2. A python flask server implementation for running the ARM template script,
   flask is being used to server the script to a web interface, so that we can pass data to a browser.
3. A web interface using JavaScript, HTML and CSS to call this script:
   - In the `templates` folder is the HTML file.
   - In the `static` folder you can find the CSS and JavaScript files.

### Testing the python script/server

- Open a new terminal in the root of this project:

- To avoid compatibility issues, a `venv` should be used:
  - Run the command `python3 -m venv .venv`
  - Then run the command `.venv\Scripts\activate`, you should be now in a virtual environment with a fresh python environment.
- Install requirements from the requirements.txt file with `pip install -r requirements.txt`.

## Testing the python script:

- Run the `arm_script.py` file using `python .\arm_script.py` from the root directory file which will ask you for inputs in the terminal.

## Running the server and frontend locally.

- To start the server use `flask --app app run` in your terminal, visiting `http://127.0.0.1:5000/` in your browser gives you access to the website in development mode.
