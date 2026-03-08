import os
import json
import pytest
import shutil
import lmdb
from unittest.mock import patch, MagicMock
from lite.lmdb_storage import LMDBStorage, LMDBConfig

@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.lmdb")

@pytest.fixture
def storage(db_path):
    s = LMDBStorage(db_path=db_path, capacity_mb=10, compression_threshold=10)
    yield s
    s.close()
    if os.path.exists(db_path):
        if os.path.isdir(db_path):
            shutil.rmtree(db_path)
        else:
            os.remove(db_path)

def test_lmdb_config_validation():
    with pytest.raises(ValueError, match="capacity_mb must be greater than 0"):
        LMDBConfig(capacity_mb=0)
    with pytest.raises(ValueError, match="compression_threshold must be non-negative"):
        LMDBConfig(compression_threshold=-1)
    with pytest.raises(ValueError, match="db_path must be a non-empty string"):
        LMDBConfig(db_path="")

def test_lmdb_storage_initialization(storage, db_path):
    assert storage.db_path == db_path
    assert storage.capacity_mb == 10
    assert storage.compression_threshold == 10
    assert os.path.exists(db_path)

def test_put_get_basic(storage):
    assert storage.put("key1", "value1") is True
    assert storage.get("key1") == "value1"

def test_put_compressed(storage):
    # compression_threshold is 10
    long_value = "this is a long value that should be compressed"
    assert storage.put("long", long_value) is True
    assert storage.get("long") == long_value

def test_put_invalid(storage):
    assert storage.put("", "value") is False
    assert storage.put("key", None) is False
    
    # Key exceeds max_key_size (default 511)
    long_key = "k" * 600
    assert storage.put(long_key, "value") is False

def test_get_nonexistent(storage):
    assert storage.get("nonexistent") is None

def test_exists(storage):
    storage.put("key1", "value1")
    assert storage.exists("key1") is True
    assert storage.exists("key2") is False

def test_delete(storage):
    storage.put("key1", "value1")
    assert storage.delete("key1") is True
    assert storage.exists("key1") is False
    assert storage.delete("key1") is False

def test_clear(storage):
    storage.put("k1", "v1")
    storage.put("k2", "v2")
    assert storage.num_keys() == 2
    assert storage.clear() == 2
    assert storage.num_keys() == 0

def test_get_keys(storage):
    storage.put("k1", "v1")
    storage.put("k2", "v2")
    keys = storage.get_keys()
    assert set(keys) == {"k1", "k2"}
    
    gen = storage.get_keys(as_generator=True)
    assert set(gen) == {"k1", "k2"}

def test_stats(storage):
    storage.put("k1", "v1")
    stats = storage.get_stats()
    assert stats['entries'] == 1

def test_export_import_json(storage, tmp_path):
    storage.put("k1", "v1")
    storage.put("k2", "v2")
    json_path = str(tmp_path / "data.json")
    assert storage.export_to_json(json_path) is True
    
    # Import into a new storage
    db_path2 = str(tmp_path / "test2.lmdb")
    storage2 = LMDBStorage(db_path=db_path2)
    assert storage2.import_from_json(json_path) is True
    assert storage2.get("k1") == "v1"
    assert storage2.get("k2") == "v2"
    storage2.close()

def test_import_json_invalid(storage, tmp_path):
    json_path = str(tmp_path / "invalid.json")
    with open(json_path, "w") as f:
        f.write("not a json")
    assert storage.import_from_json(json_path) is False

def test_context_manager(db_path):
    with LMDBStorage(db_path=db_path) as s:
        s.put("k", "v")
        assert s.get("k") == "v"
    # Should be closed now, put returns False on error
    assert s.put("k2", "v2") is False

@patch("lmdb.open")
def test_lmdb_open_error(mock_open, db_path):
    mock_open.side_effect = Exception("Open failed")
    with pytest.raises(Exception, match="Open failed"):
        LMDBStorage(db_path=db_path)

def test_put_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.put("k", "v") is False

def test_get_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.get("k") is None

def test_clear_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.clear() == 0

def test_num_keys_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.num_keys() == 0

def test_get_keys_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.get_keys() == []
        assert list(storage.get_keys(as_generator=True)) == []

def test_exists_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.exists("k") is False

def test_delete_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.delete("k") is False

def test_get_stats_exception(storage):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.get_stats() == {}

def test_export_to_json_exception(storage, tmp_path):
    with patch.object(storage, "env") as mock_env:
        mock_env.begin.side_effect = Exception("Txn failed")
        assert storage.export_to_json(str(tmp_path / "err.json")) is False

def test_decode_value_fallback(storage):
    # Test old format (no flag byte)
    import gzip
    val = "old value".encode('utf-8')
    compressed = gzip.compress(val)
    assert storage._decode_value(compressed) == "old value"
    
    # Test plain text fallback
    assert storage._decode_value(b"plain text") == "plain text"
