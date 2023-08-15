import os
import pytest
from sftpshellfuncs import change_directory_local

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
