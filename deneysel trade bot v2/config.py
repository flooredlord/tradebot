import os


def str_to_bool(value: str) -> bool:
    return str(value).lower() in ("1", "true", "yes", "on")


BINANCE_API_KEY = os.getenv(
    "BINANCE_API_KEY",
    "PNVYm40GR79ElQsZ886rC6wpdhEDRloqJ5qUOP0jr0sNdTUwiBWiHt0jAlw8vGmE",
)
BINANCE_API_SECRET = os.getenv(
    "BINANCE_API_SECRET",
    "yN8Z2Kdp0yfnL5hcP8Tj1DvTMAFbXc1E1kNcAVOs50EtG81oiI8iOz4Eg1UeL03K",
)

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USDT")
TRADE_SYMBOLS = [
    s.strip()
    for s in os.getenv("TRADE_SYMBOLS", "").split(",")
    if s.strip()
]  # boş bırak, top 50 otomatik yüklenecek

MIN_TRADE_AMOUNT = float(os.getenv("MIN_TRADE_AMOUNT", "10"))  # USDT cinsinden minimum işlem değeri
TRADE_PERCENTAGE = float(os.getenv("TRADE_PERCENTAGE", "0.1"))  # bakiyenin %10’u ile işlem yap

STOP_LOSS_PERCENTAGE = float(os.getenv("STOP_LOSS_PERCENTAGE", "0.05"))  # %5 zarar kes
TAKE_PROFIT_PERCENTAGE = float(os.getenv("TAKE_PROFIT_PERCENTAGE", "0.02"))  # %2 kâr al

TIMEFRAMES = [tf.strip() for tf in os.getenv("TIMEFRAMES", "1h,4h").split(",")]
EXCLUDED_SYMBOLS = [s.strip() for s in os.getenv("EXCLUDED_SYMBOLS", "BNBUSDT,USDCUSDT").split(",")]

TELEGRAM_ENABLED = str_to_bool(os.getenv("TELEGRAM_ENABLED", "True"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7825739294:AAEYnSVBKsDxjsLvLgLquYnTHW8Z5Jv0bZU")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "418989376")

# Teknik indikatör kontrolleri
USE_RSI = str_to_bool(os.getenv("USE_RSI", "True"))
RSI_BUY_THRESHOLD = int(os.getenv("RSI_BUY_THRESHOLD", "30"))
RSI_SELL_THRESHOLD = int(os.getenv("RSI_SELL_THRESHOLD", "70"))

USE_BOLLINGER = str_to_bool(os.getenv("USE_BOLLINGER", "True"))

# Minimum sinyal eşiği (her zaman dilimi için)
MIN_BUY_SIGNALS = int(os.getenv("MIN_BUY_SIGNALS", "2"))
MIN_SELL_SIGNALS = int(os.getenv("MIN_SELL_SIGNALS", "2"))

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "1800"))  # 30 dakika (saniye cinsinden)
