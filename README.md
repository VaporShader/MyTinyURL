# Running the Project

To run the project follow these steps:

1) open a terminal and navigate to the project's directory  ({PATH}/mytinyurl)
2) type and run the following lines

   ```bash
      python3 -m venv venv
      venv/bin/pip install Flask
      export FLASK_APP=main.py
      venv/bin/python3 -m flask run
   ```

3) open any browser you use and type in the address bar

```url
   http://localhost:5000/
```

The server will now send you the web page of the project
