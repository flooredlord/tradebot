import json
import sys
from pathlib import Path
import importlib

PROJECT_DIR = Path(__file__).resolve().parents[1] / 'deneysel trade bot v2'
sys.path.insert(0, str(PROJECT_DIR))

tax_report = importlib.import_module('tax_report')


def test_generate_tax_report(tmp_path, monkeypatch):
    history = [
        {"symbol": "BTCUSDT", "type": "BUY", "price": 10000, "quantity": 0.1, "timestamp": "t1"},
        {"symbol": "BTCUSDT", "type": "SELL", "price": 10500, "quantity": 0.1, "timestamp": "t2"}
    ]
    history_file = tmp_path / "history.json"
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f)

    reports = []
    monkeypatch.setattr(tax_report, 'FEE_RATE', 0.001)
    monkeypatch.setattr('builtins.print', lambda msg: reports.append(msg))
    tax_report.generate_tax_report(str(history_file))

    assert any("Net Profit After Fees" in line for line in reports[0].split('\n'))

