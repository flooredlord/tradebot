import os

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

BASE_CURRENCY = 'USDT'
TRADE_SYMBOLS = []  # boş bırak, top 50 otomatik yüklenecek

MIN_TRADE_AMOUNT = 10  # USDT cinsinden minimum işlem değeri
TRADE_PERCENTAGE = 0.1  # bakiyenin %10’u ile işlem yap

STOP_LOSS_PERCENTAGE = 0.05  # %5 zarar kes
TAKE_PROFIT_PERCENTAGE = 0.02  # %2 kâr al

TIMEFRAMES = ['1h', '4h']
EXCLUDED_SYMBOLS = ['BNBUSDT', 'USDCUSDT']

TELEGRAM_ENABLED = True
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Teknik indikatör kontrolleri
USE_RSI = True
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70

USE_BOLLINGER = True

# Minimum sinyal eşiği (her zaman dilimi için)
MIN_BUY_SIGNALS = 2
MIN_SELL_SIGNALS = 2

CHECK_INTERVAL = 1800  # 30 dakika (saniye cinsinden)
