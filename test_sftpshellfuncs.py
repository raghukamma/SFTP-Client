#import sftpclient
import pysftp
import sftpshellfuncs
import os
import pytest
from unittest.mock import patch
from sftpshellfuncs import change_directory_local, list_files_folder_local, rename_file_on_local, get_file_remote_server
#pytest unit testing file 
#add your unit tests below

def test_remove_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username='', password='', cnopts=cnopts)
    #create remote file
    valfoo.put('test.txt')
    #call remove remote
    x = ["rm", "test.txt"]
    sftpshellfuncs.commands["rm"](valfoo, x)
    #assert the file has been removed
    assert valfoo.exists('test.txt') == False

def test_rename_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username='', password='', cnopts=cnopts)
    #create remote file
    valfoo.put('test.txt')
    #call rename remote
    x = ["rename", "test.txt", "success.txt"]
    sftpshellfuncs.commands["rename"](valfoo, x)
    assert valfoo.exists('success.txt') == True


#using monkeypatch to mock the user input
#using capsys to capture the output printed

def test_change_directory_local(tmpdir, monkeypatch, capsys):
    #using tmpdir to create a temporary directory for testing
    test_dir = tmpdir.mkdir("test_directory")
    input_path = str(test_dir)
    
    # Mocking the input function to return the provided path
    monkeypatch.setattr('builtins.input', lambda: input_path)
    
    args = None
    sftp = None
    
    change_directory_local(sftp, args)
    
    captured = capsys.readouterr()
    assert "Your current working directory changed successfully" in captured.out
    assert input_path in captured.out
    assert os.getcwd() == input_path

def test_change_directory_local_error(monkeypatch, capsys):
    input_path = '/non_existent_directory'
    
    # Mocking the input function to return the provided path
    monkeypatch.setattr('builtins.input', lambda: input_path)
    
    args = None
    sftp = None
    
    change_directory_local(sftp, args)
    
    captured = capsys.readouterr()
    assert "Error while changing the directory.\n Please try again!" in captured.out

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