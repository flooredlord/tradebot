from datetime import datetime
import time
import json

import config
from utils import (
    get_balance,
    place_order,
    adjust_quantity_to_lot_size,
    adjust_notional_to_min,
    logger,
    log,
    client,
)
from coin_utils import get_top_symbols
from risk_management import calculate_atr_stop_loss_take_profit, calculate_trailing_stop
from telegram_notifier import send_telegram_message
from position_manager import load_positions, save_positions
from performance_analyzer import analyze_performance
from update_loader import apply_patches
from performance_graphs import generate_performance_graphs
from agent_manager import AgentManager
from agent_ml import MLAgent
from agent_swing import SwingAgent
from agent_news import NewsAgent
from sizing import calculate_position_size

apply_patches()


def load_trade_history():
    try:
        with open("trade_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception as e:
        log(f"Unexpected error loading trade history: {e}")
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

    manager = AgentManager([SwingAgent(), MLAgent(), NewsAgent()])
    highest_prices = {}

    while True:
        usdt_balance = get_balance(config.BASE_CURRENCY)
        history = load_trade_history()
        signals = manager.get_signals(symbols)

        for symbol, signal in signals.items():
            trade_amount = calculate_position_size(usdt_balance * config.TRADE_PERCENTAGE, symbol)
            ticker = client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker["price"])
            quantity = trade_amount / current_price if current_price else 0

            quantity = adjust_quantity_to_lot_size(symbol, quantity)
            quantity = adjust_notional_to_min(symbol, quantity, current_price)
            notional = current_price * quantity
            if notional < config.MIN_TRADE_AMOUNT:
                logger.info(f"⚠️ {symbol} için {notional:.2f} USDT altında işlem oluştu, atlandı.")
                continue

            position = positions.get(symbol, "NONE")
            buy_price, held_qty = get_last_buy_price(symbol, history)
            profit_ratio = (current_price - buy_price) / buy_price if buy_price else 0

            if position == "LONG":
                prev_high = highest_prices.get(symbol, buy_price or current_price)
                highest_prices[symbol] = max(prev_high, current_price)
                trailing_stop = calculate_trailing_stop(
                    buy_price or current_price,
                    highest_prices[symbol],
                    config.TRAILING_STOP_PERCENTAGE,
                )
                if current_price <= trailing_stop:
                    place_order(symbol, "SELL", held_qty)
                    positions[symbol] = "SHORT"
                    save_positions(positions)
                    log(f"🔴 Trailing stop tetiklendi: {symbol} {current_price}")
                    send_telegram_message(
                        f"Trailing stop: {symbol} at {current_price}, qty: {held_qty}"
                    )
                    continue

            if signal == "SELL" and position == "LONG":
                sl, tp = calculate_atr_stop_loss_take_profit(symbol)
                log(f"{symbol} stop_loss: {sl}, take_profit: {tp}")
                send_telegram_message(f"{symbol} SL: {sl}, TP: {tp}")
                place_order(symbol, "SELL", held_qty, stop_loss=sl, take_profit=tp)
                positions[symbol] = "SHORT"
                save_positions(positions)
                logger.info(f"🔴 SELL signal: {symbol} tüm pozisyon satıldı")
                send_telegram_message(f"SELL signal: {symbol} at {current_price}, qty: {held_qty}")

            elif signal == "HOLD" and position == "LONG" and profit_ratio > 0.10:
                sell_qty = 0
                if 0.10 <= profit_ratio < 0.15:
                    sell_qty = held_qty * 0.5
                elif profit_ratio >= 0.15:
                    sell_qty = held_qty * 0.5

                if sell_qty > 0:
                    sell_qty = adjust_quantity_to_lot_size(symbol, sell_qty)
                    sl, tp = calculate_atr_stop_loss_take_profit(symbol)
                    log(f"{symbol} stop_loss: {sl}, take_profit: {tp}")
                    send_telegram_message(f"{symbol} SL: {sl}, TP: {tp}")
                    place_order(symbol, "SELL", sell_qty, stop_loss=sl, take_profit=tp)
                    positions[symbol] = "LONG"
                    save_positions(positions)
                    logger.info(f"🟡 Kârda kademeli satış: {symbol} %{profit_ratio*100:.1f} kârla {sell_qty} adet")
                    send_telegram_message(f"Kâr satışı: {symbol} at {current_price}, qty: {sell_qty}")

            elif signal == "BUY" and position != "LONG":
                sl, tp = calculate_atr_stop_loss_take_profit(symbol)
                log(f"{symbol} stop_loss: {sl}, take_profit: {tp}")
                send_telegram_message(f"{symbol} SL: {sl}, TP: {tp}")
                place_order(symbol, "BUY", quantity, stop_loss=sl, take_profit=tp)
                positions[symbol] = "LONG"
                save_positions(positions)
                logger.info(f"🟢 BUY order: {symbol} at {current_price}, qty: {quantity}")
                send_telegram_message(f"BUY order: {symbol} at {current_price}, qty: {quantity}")
            else:
                logger.info(f"⚪ HOLD: {symbol}")

        analyze_performance()
        generate_performance_graphs()
        time.sleep(config.CHECK_INTERVAL)


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    main()
