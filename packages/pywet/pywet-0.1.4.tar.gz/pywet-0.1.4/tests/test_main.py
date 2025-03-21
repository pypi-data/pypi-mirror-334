import pytest
from unittest.mock import patch, MagicMock
import win32api
from pywet import main


def test_main():
    # Mock the win32api functions
    mock_cursor_pos = (100, 100)
    # (free, total, available)
    mock_disk_space = (1000000000, 1000000000, 1000000000)
    mock_domain = "TEST-DOMAIN"
    mock_keyboard = [0] * 256  # Mock keyboard state array
    mock_system_info = MagicMock()  # Mock system info object

    with patch('win32api.GetCursorPos', return_value=mock_cursor_pos), \
            patch('win32api.GetDiskFreeSpaceEx', return_value=mock_disk_space), \
            patch('win32api.GetDomainName', return_value=mock_domain), \
            patch('win32api.GetKeyboardState', return_value=mock_keyboard), \
            patch('win32api.GetSystemInfo', return_value=mock_system_info):

        # Call main function
        main()

        # Verify that all mocked functions were called
        win32api.GetCursorPos.assert_called_once()
        win32api.GetDiskFreeSpaceEx.assert_called_once_with("C:\\")
        win32api.GetDomainName.assert_called_once()
        win32api.GetKeyboardState.assert_called_once()
        win32api.GetSystemInfo.assert_called_once()
