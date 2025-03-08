import requests


def get_crypto_data():
    """
    Получает данные о топ-20 криптовалютах используя API CoinGecko
    """
    try:
        # URL API для получения данных о криптовалютах
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 20,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "1h,24h,7d"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }
        
        # Получаем данные с API
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            return f"Не удалось получить данные о криптовалютах. Код ошибки: {response.status_code}"
            
        # Парсим JSON данные
        data = response.json()
        
        # Формируем текст с информацией о топ-20 криптовалютах
        result = "🔍 Информация о криптовалютах 🔍\n\n"
        
        for i, crypto in enumerate(data, 1):
            name = crypto.get('name', 'Неизвестно')
            symbol = crypto.get('symbol', 'Неизвестно').upper()
            price = crypto.get('current_price', 0)
            cap = crypto.get('market_cap', 0)
            change_1h = crypto.get('price_change_percentage_1h_in_currency', 0)
            change_24h = crypto.get('price_change_percentage_24h_in_currency', 0)
            change_7d = crypto.get('price_change_percentage_7d_in_currency', 0)
            
            # Форматируем числа
            if isinstance(price, (int, float)):
                price = f"${price:,.2f}"
                
            if isinstance(cap, (int, float)):
                if cap >= 1000000000:
                    cap = f"${cap/1000000000:,.2f}B"
                elif cap >= 1000000:
                    cap = f"${cap/1000000:,.2f}M"
                else:
                    cap = f"${cap:,.2f}"
            
            # Добавляем эмодзи для изменений цены
            change_1h_symbol = "🟢" if change_1h > 0 else "🔴"
            change_24h_symbol = "🟢" if change_24h > 0 else "🔴"
            change_7d_symbol = "🟢" if change_7d > 0 else "🔴"
            
            result += f"{i}. {name} ({symbol})\n"
            result += f"   Цена: {price}\n"
            result += f"   Объем рынка: {cap}\n"
            result += f"   Изменение 1ч: {change_1h_symbol} {change_1h:.2f}%\n"
            result += f"   Изменение 24ч: {change_24h_symbol} {change_24h:.2f}%\n"
            result += f"   Изменение 7д: {change_7d_symbol} {change_7d:.2f}%\n\n"
        
        return result
        
    except Exception as e:
        return f"Произошла ошибка при получении данных о криптовалютах: {str(e)}"
