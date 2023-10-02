# main.py

from fastapi import FastAPI
from datetime import datetime
import socket, requests, re

# Global variable
SECRET_ALPHA_VTG_API_KEY = "demo"
FILE_ALPHA_VTG_API_KEY = "/etc/secret/alphavantage.secret"
URL_ALPHA_VTG_API = "https://www.alphavantage.co/query?apikey="

app = FastAPI()

# Initialize
def app_init():
    global SECRET_ALPHA_VTG_API_KEY, FILE_ALPHA_VTG_API_KEY, URL_ALPHA_VTG_API

    try:
        file_api_key = open(FILE_ALPHA_VTG_API_KEY, "r")
        SECRET_ALPHA_VTG_API_KEY = file_api_key.read()
        print("INFO:     FastAPI app initialization is successful")
    except Exception as e:
        print("ERROR:     FastAPI app initialization error: {e}")
    finally:
        file_api_key.close()

    URL_ALPHA_VTG_API = URL_ALPHA_VTG_API + SECRET_ALPHA_VTG_API_KEY
        

# Validate ticker symbol
def validate_ticker(ticker_symbol):
    if ticker_symbol is None or ticker_symbol.isspace() or len(ticker_symbol) > 15:
        return False
    
    # Valid stock: STOCK, STOCK.LON
    r = re.match(r'[a-zA-Z0-9.]+$', ticker_symbol)

    if r == None:
        return False
    else:
        return True

# Get stock quote
def get_stock_quote(ticker_symbol):
    global URL_ALPHA_VTG_API

    ticker_overview = "{}"

    is_ticker_ok = validate_ticker(ticker_symbol)

    if is_ticker_ok == True:
        url_api = URL_ALPHA_VTG_API + "&function=GLOBAL_QUOTE&symbol="
        
        response = requests.get(url_api + ticker_symbol)
        
        if response.status_code == 200:
            ticker_overview = response.json()
            
    return ticker_overview 

# Get /stock/quote/<symbol>
@app.get("/stock/quote/{symbol}")
def getStockQuote(symbol: str):
    return get_stock_quote(symbol)

# Get /liveness
@app.get("/liveness")
def getLiveness():
    return "Ok"  

# Get /readiness
@app.get("/readiness")
def getReadiness():
    return "Ok"  

# Get /healthz
@app.get("/healthz")
def getReadiness():
    return "Ok"  


# Get /sysinfo
@app.get("/sysinfo")
def getSysinfo():
    current_time = str(datetime.now())
    hostname = socket.gethostname()

    message = "time: " + current_time + ", host: " + hostname

    return message

# Get /
@app.get("/")
def root():
    message = "Option: /health, /stock/quote/<symbol>, /sysinfo"

    return {"response": message}

# Init app
app_init()