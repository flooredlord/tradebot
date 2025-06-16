import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deneysel trade bot v2')))

import position_manager


def test_load_save_positions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = {'AAA': 'LONG'}
    position_manager.save_positions(data)
    assert os.path.exists('positions.json')
    loaded = position_manager.load_positions()
    assert loaded == data
