
# GameGuesser

A web-based trivia game built with Django! Users can create a profile and guess which game scored higher, similar to "More or Less".


## Deployment

It's recommended to run this project in a virtual environment. You can create one using the following commands:

```bash
  python -m venv venv
```

For Windows:
```bash
  source venv/Scripts/activate
```

For Linux:
```bash
  source venv/bin/activate
```

After activation you can install the dependencies using:
```bash
  pip install -r requirements.txt
```
Finally it can be run with:
```bash
  Python manage.py runserver
```
## Running Tests

This project uses a remote database and a separate test database for running tests. TO run them you'll need to configure the environment variables for your own database. Once configured they can be run with the following command

```bash
  python manage.py test --keepdb
```

Additionally this project utilizes continuous itegration, any push to the main branch will automatically run the current test suite using Github Actions. The full commands run can be viewed in the testing.yml file.

