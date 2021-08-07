# Countries information
This a project that obtains information of a country per region in the world for a given endpoint:

First we need to know how many regions there are in the world using this [all countries API](https://rapidapi.com/apilayernet/api/rest-countries-v1)
Later with all the regions we look up for a single country in every region using this [API](https://restcountries.eu/)

## Tools and package

- Request for getting data from every endpoint
- SQLlite for storing all data
- Pandas for managing data
- Pytes for testing our program

you only need to run

```bash
pip install -r requirements.txt
```

## Running

for running this program you have to run "main.py"

```bash
python main.py
```
