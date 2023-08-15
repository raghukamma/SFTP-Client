import os
import pytest
from unittest.mock import patch
from sftpshellfuncs import list_files_folder_local

def test_list_files_folder_local_success():
    path = "."
    try:
        expected = ["Displaying the files and folders from current directory present in the local machine: "]
        entries = os.listdir(path)
        entries.sort(key=os.path.getctime)
        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                expected.append(entry)
            else:
                expected.append(entry)

    except OSError as e:
        print(f"Error: {e}")
    with patch("builtins.print") as mock_print:
        list_files_folder_local(None, args=None)
        captured_output = [call_args[0] for call_args, _ in mock_print.call_args_list]
        print(captured_output)
        assert captured_output == expected, "Output does not match the expected output"


def test_list_files_folder_local_failure():
    path = "."
    try:
        expected = ["Displaying the files and folders from current directory present in the local machine: "]
        entries = os.listdir(path)
        entries.sort(key=os.path.getctime)
        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                expected.append(entry)
            else:
                expected.append(entry)

    except OSError as e:
        print(f"Error: {e}")

    expected = expected.append("filedoestexists.txt")
    with patch("builtins.print") as mock_print:
        list_files_folder_local(None, args=None)
        captured_output = [call_args[0] for call_args, _ in mock_print.call_args_list]
        print(captured_output)
        assert captured_output != expected, "Output does not match the expected output"