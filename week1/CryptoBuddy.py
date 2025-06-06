import random
import requests

crypto_db = {  
    "Bitcoin": {  
        "id": "bitcoin",
        "price_trend": "rising",  
        "market_cap": "high",  
        "energy_use": "high",  
        "sustainability_score": 3/10,
        "year": 2009,
        "founder": "Satoshi Nakamoto",
        "use_case": "Digital Gold"
    },  
    "Ethereum": {  
        "id": "ethereum",
        "price_trend": "stable",  
        "market_cap": "high",  
        "energy_use": "medium",  
        "sustainability_score": 6/10,
        "year": 2015,
        "founder": "Vitalik Buterin",
        "use_case": "Smart Contracts"
    },  
    "Cardano": {  
        "id": "cardano",
        "price_trend": "rising",  
        "market_cap": "medium",  
        "energy_use": "low",  
        "sustainability_score": 8/10,
        "year": 2017,
        "founder": "Charles Hoskinson",
        "use_case": "Sustainable Smart Contracts"
    }  
}

price_trend_explanation = (
    "Price trend shows if a coin's value is rising, stable, or falling over time:\n"
    "- 'rising': price is generally going up 📈\n"
    "- 'stable': price stays about the same ➖\n"
    "- 'falling': price is generally going down 📉"
)

example_questions = [
    "Which crypto is trending up?",
    "What's the most sustainable coin?",
    "Tell me about Cardano.",
    "Who founded Ethereum?",
    "Which coin is best for long-term growth?",
    "What's the current price of Bitcoin?",
    "Can you compare the price trends of all coins?"
]

def get_live_price(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data[coin_id]['usd']
    except Exception:
        return None

def chatbot(user_query, context=None):
    user_query = user_query.lower()
    # Price trends comparison intent
    if "price trends" in user_query or "compare trends" in user_query or "trend of all" in user_query:
        trends = []
        for coin, data in crypto_db.items():
            trends.append(f"{coin}: {data['price_trend']}")
        return price_trend_explanation + "\n\n" + "\n".join(trends)
    # Real-time price check
    for coin in crypto_db:
        if f"price of {coin.lower()}" in user_query or f"{coin.lower()} price" in user_query:
            price = get_live_price(crypto_db[coin]['id'])
            if price:
                return f"The current price of {coin} is ${price:,} USD."
            else:
                return "Sorry, I couldn't fetch the live price right now."
    # Sustainability intent
    if "sustainable" in user_query or "eco" in user_query or "green" in user_query:
        recommend = max(crypto_db, key=lambda x: crypto_db[x]["sustainability_score"])
        details = crypto_db[recommend]
        price = get_live_price(details['id'])
        price_info = f" Current price: ${price:,} USD." if price else ""
        return (f"Invest in {recommend}! 🌱\n"
                f"Why? It uses {details['energy_use']} energy and has a sustainability score of {int(details['sustainability_score']*10)}/10."
                f"{price_info}")
    # Trending intent
    elif "trending" in user_query or "up" in user_query or "rise" in user_query:
        trending = [coin for coin in crypto_db if crypto_db[coin]["price_trend"] == "rising"]
        trending_prices = []
        for coin in trending:
            price = get_live_price(crypto_db[coin]['id'])
            if price:
                trending_prices.append(f"{coin} (${price:,})")
            else:
                trending_prices.append(coin)
        return f"Trending up: {', '.join(trending_prices)}"
    # Long-term/growth intent
    elif "long-term" in user_query or "growth" in user_query or "future" in user_query:
        candidates = [coin for coin in crypto_db if crypto_db[coin]["price_trend"] == "rising" and crypto_db[coin]["market_cap"] in ["high", "medium"]]
        best = max(candidates, key=lambda x: crypto_db[x]["sustainability_score"])
        details = crypto_db[best]
        price = get_live_price(details['id'])
        price_info = f" Current price: ${price:,} USD." if price else ""
        return (f"{best} is trending up and has a top-tier sustainability score! 🚀\n"
                f"Why? {best} uses {details['energy_use']} energy and was founded by {details['founder']} in {details['year']}."
                f"{price_info}")
    # Personalized advice (risk)
    elif "risk" in user_query or "safe" in user_query or "stable" in user_query:
        return "If you prefer low risk, look for coins with stable trends and high market cap, like Bitcoin or Ethereum."
    # Explainability: tell me about
    elif "tell me about" in user_query or "info on" in user_query:
        for coin in crypto_db:
            if coin.lower() in user_query:
                d = crypto_db[coin]
                price = get_live_price(d['id'])
                price_info = f" Current price: ${price:,} USD." if price else ""
                return (f"{coin}: Founded by {d['founder']} in {d['year']}. Use case: {d['use_case']}. "
                        f"Energy use: {d['energy_use']}, Sustainability: {int(d['sustainability_score']*10)}/10."
                        f"{price_info}")
        return "Sorry, I don't have info on that coin."
    # Founder info
    elif "founder" in user_query or "who made" in user_query:
        for coin in crypto_db:
            if coin.lower() in user_query:
                return f"{coin} was founded by {crypto_db[coin]['founder']}."
        return "Sorry, I don't know the founder of that coin."
    # Error handling & suggestions
    elif "help" in user_query or "?" in user_query:
        return "Try asking: " + random.choice(example_questions)
    # Ethics disclaimer and fallback
    else:
        return ("Sorry, I can't answer that. Crypto is risky—always do your own research!\n"
                "Example questions: " + "; ".join(example_questions))

print("CryptoBuddy: Hi! Ask me about crypto coins. Type 'exit' to quit.")
while True:
    user = input("You: ")
    if user.lower() in ["exit", "quit"]:
        break
    print("CryptoBuddy:", chatbot(user))
