import pytest
import socket
import argparse
from unittest.mock import Mock, patch
import sys
import os

# 添加项目路径到 sys.path
sys.path.append(os.path.abspath("E:/Paimeng/Digital_Life_Server"))

from SocketServer import Server, parse_args, str2bool

@pytest.fixture
def mock_args():
    """Mock command-line arguments."""
    args = Mock()
    args.chatVer = 3
    args.APIKey = "test_api_key"
    args.email = "test@example.com"
    args.password = "test_password"
    args.accessToken = None
    args.proxy = None
    args.paid = False
    args.model = "gpt-4"
    args.stream = True
    args.character = "paimon"
    args.ip = None
    args.brainwash = False
    return args

@pytest.fixture
def mock_server(mock_args):
    """Mock server instance."""
    with patch("ASR.ASRService.ASRService", autospec=True), \
         patch("GPT.GPTService.GPTService", autospec=True), \
         patch("TTS.TTService.TTService", autospec=True), \
         patch("SentimentEngine.SentimentEngine", autospec=True):
        return Server(mock_args)

def test_str2bool():
    """Test str2bool function."""
    assert str2bool("yes") is True
    assert str2bool("no") is False
    assert str2bool("true") is True
    assert str2bool("false") is False
    assert str2bool("1") is True
    assert str2bool("0") is False
    with pytest.raises(argparse.ArgumentTypeError):
        str2bool("invalid")

def test_parse_args(monkeypatch):
    """Test argument parsing."""
    monkeypatch.setattr("sys.argv", [
        "SocketServer.py", "--chatVer", "3", "--stream", "true", "--character", "paimon"
    ])
    args = parse_args()
    assert args.chatVer == 3
    assert args.stream is True
    assert args.character == "paimon"

def test_server_initialization(mock_server):
    """Test server initialization."""
    assert mock_server.host == socket.gethostbyname(socket.gethostname())
    assert mock_server.port == 38438
    assert isinstance(mock_server.char_name, dict)

# 其他测试函数...
