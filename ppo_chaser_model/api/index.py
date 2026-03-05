from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allow CORS for frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        # Fetch last 5 days of data
        history = stock.history(period="5d")
        
        if history.empty:
            return {"error": f"No data found for ticker: {ticker}"}
            
        data = []
        for index, row in history.iterrows():
            data.append({
                "date": index.strftime('%Y-%m-%d'),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"])
            })
            
        # Get basic info
        info = stock.info
        current_price = info.get("currentPrice", data[-1]["close"])
        short_name = info.get("shortName", ticker.upper())
        currency = info.get("currency", "USD")
            
        return {
            "ticker": ticker.upper(),
            "name": short_name,
            "current_price": current_price,
            "currency": currency,
            "history": data
        }
    except Exception as e:
        return {"error": str(e)}

# Note: to run locally, use the command:
# uvicorn test:app --reload
