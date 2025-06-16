BINANCE_API_KEY = 'PNVYm40GR79ElQsZ886rC6wpdhEDRloqJ5qUOP0jr0sNdTUwiBWiHt0jAlw8vGmE'
BINANCE_API_SECRET = 'yN8Z2Kdp0yfnL5hcP8Tj1DvTMAFbXc1E1kNcAVOs50EtG81oiI8iOz4Eg1UeL03K'

BASE_CURRENCY = 'USDT'
TRADE_SYMBOLS = []  # boş bırak, top 50 otomatik yüklenecek

MIN_TRADE_AMOUNT = 10  # USDT cinsinden minimum işlem değeri
TRADE_PERCENTAGE = 0.1  # bakiyenin %10’u ile işlem yap

STOP_LOSS_PERCENTAGE = 0.05  # %5 zarar kes
TAKE_PROFIT_PERCENTAGE = 0.02  # %2 kâr al

TIMEFRAMES = ['1h', '4h']
EXCLUDED_SYMBOLS = ['BNBUSDT', 'USDCUSDT']

TELEGRAM_ENABLED = True
TELEGRAM_TOKEN = '7825739294:AAEYnSVBKsDxjsLvLgLquYnTHW8Z5Jv0bZU'
TELEGRAM_CHAT_ID = '418989376'

# Teknik indikatör kontrolleri
USE_RSI = True
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70

USE_BOLLINGER = True

# Minimum sinyal eşiği (her zaman dilimi için)
MIN_BUY_SIGNALS = 2
MIN_SELL_SIGNALS = 2

CHECK_INTERVAL = 1800  # 30 dakika (saniye cinsinden)
