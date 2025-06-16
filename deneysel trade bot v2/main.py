from datetime import datetime
import time
import config
from utils import (
    get_balance,
    place_order,
    adjust_quantity_to_lot_size,
    adjust_notional_to_min,
    logger,
)
from coin_utils import get_top_symbols
from strategies import generate_signal
from risk_management import calculate_atr_stop_loss_take_profit
from telegram_notifier import send_telegram_message
from utils import client
from position_manager import load_positions, save_positions
from performance_analyzer import analyze_performance
from update_loader import apply_patches
import json

apply_patches()

def load_trade_history():
    try:
        with open("trade_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_last_buy_price(symbol, history):
    for entry in reversed(history):
        if entry["symbol"] == symbol and entry["type"] == "BUY":
            return float(entry["price"]), float(entry["quantity"])
    return None, None

def main():
    start_time = datetime.now()
    logger.info("🚀 Bot başlatılıyor... Coin listesi hazırlanıyor...")
    positions = load_positions()
    symbols = get_top_symbols(base_currency=config.BASE_CURRENCY)
    logger.info(f"✅ Toplam {len(symbols)} coin yüklendi.")
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"⏱️ Başlangıç süresi: {duration:.2f} saniye")

    while True:
        usdt_balance = get_balance(config.BASE_CURRENCY)
        min_trade = config.MIN_TRADE_AMOUNT
        scores = []

        for symbol in symbols:
            score = generate_signal(symbol, config.TIMEFRAMES, return_score=True)
            if score > 0:
                scores.append((symbol, score))

        if not scores:
            logger.info("⚪ Sinyal gelen coin yok.")
            time.sleep(config.CHECK_INTERVAL)
            continue

        total_score = sum(score for _, score in scores)
        history = load_trade_history()

        for symbol, score in scores:
            weight = score / total_score
            trade_amount = usdt_balance * weight
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker["price"])
            quantity = trade_amount / current_price

            quantity = adjust_quantity_to_lot_size(symbol, quantity)
            quantity = adjust_notional_to_min(symbol, quantity, current_price)
            notional = current_price * quantity
            if notional < config.MIN_TRADE_AMOUNT:
                logger.info(f"⚠️ {symbol} için {notional:.2f} USDT altında işlem oluştu, atlandı.")
                continue

            position = positions.get(symbol, "NONE")
            signal = generate_signal(symbol, config.TIMEFRAMES)

            buy_price, held_qty = get_last_buy_price(symbol, history)
            profit_ratio = 0
            if buy_price:
                profit_ratio = (current_price - buy_price) / buy_price

            if signal == "SELL" and position == "LONG":
                order = place_order(symbol, "SELL", held_qty)
                positions[symbol] = "SHORT"
                save_positions(positions)
                logger.info(f"🔴 SELL signal: {symbol} tüm pozisyon satıldı")
                send_telegram_message(f"SELL signal: {symbol} at {current_price}, qty: {held_qty}")

            elif signal == "HOLD" and position == "LONG" and profit_ratio > 0.10:
                sell_qty = 0
                if profit_ratio >= 0.10 and profit_ratio < 0.15:
                    sell_qty = held_qty * 0.5
                elif profit_ratio >= 0.15:
                    sell_qty = held_qty * 0.5

                if sell_qty > 0:
                    sell_qty = adjust_quantity_to_lot_size(symbol, sell_qty)
                    order = place_order(symbol, "SELL", sell_qty)
                    positions[symbol] = "LONG"
                    save_positions(positions)
                    logger.info(f"🟡 Kârda kademeli satış: {symbol} %{profit_ratio*100:.1f} kârla {sell_qty} adet")
                    send_telegram_message(f"Kâr satışı: {symbol} at {current_price}, qty: {sell_qty}")

            elif signal == "BUY" and position != "LONG":
                order = place_order(symbol, "BUY", quantity)
                positions[symbol] = "LONG"
                save_positions(positions)
                logger.info(f"🟢 BUY order: {symbol} at {current_price}, qty: {quantity}")
                send_telegram_message(f"BUY order: {symbol} at {current_price}, qty: {quantity}")

            else:
                logger.info(f"⚪ HOLD: {symbol}")

        analyze_performance()
        time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()