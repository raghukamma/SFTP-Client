#from client.sftpclient import sftpclient
import pysftp, json, os
import sftpshellfuncs 
from sftpshell import SFTPShell
from unittest.mock import patch
from sftpshellfuncs import change_directory_local, list_files_folder_local
#pytest unit testing file 
#add your unit tests below

# Retrieving the username and password from the json file - data.json
with open('data.json', 'r') as json_file:
        data = json.load(json_file)
usern = data['username']
passwd = data['password']

# remove the file from remove server
def test_remove_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    #create remote file
    valfoo.put('test.txt')
    #call remove remote
    x = ["rm", "test.txt"]
    sftpshellfuncs.commands["rm"](valfoo, x)
    #assert the file has been removed
    assert valfoo.exists('test.txt') == False

# rename the file in the remote server
def test_rename_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    #create remote file
    valfoo.put('test.txt')
    #call rename remote
    x = ["rename", "test.txt", "success.txt"]
    sftpshellfuncs.commands["rename"](valfoo, x)
    assert valfoo.exists('success.txt') == True
    #Delete the created file
    y = ["rmd", "success.txt"]
    sftpshellfuncs.commands["rmd"](valfoo, y)
    assert "success.txt" not in valfoo.pwd

# change the directory in the remote server
def test_change_dir_rem():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    #create remote file
    valfoo.mkdir('testdir')
    #call rename remote
    x = ["cd", "testdir"]
    sftpshellfuncs.commands["cd"](valfoo, x)
    assert "testdir" in valfoo.pwd
    y = ["cd", ".."]
    sftpshellfuncs.commands["cd"](valfoo, y)
    #Delete the created file
    z = ["rmd" , "testdir"]
    sftpshellfuncs.commands["rmd"](valfoo, z)
    assert "testdir" not in valfoo.pwd

# remove directory in the server
def test_remove_dir_rem():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    #create remote file
    valfoo.mkdir('testrem')
    #call remove dir remote
    x = ["rmd", "testrem"]
    sftpshellfuncs.commands["rmd"](valfoo, x)
    assert "testrem" not in valfoo.pwd
    
#copy directory in the remote server
def test_copy_dir_rem(monkeypatch):
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    valfoo.mkdir('dir1') #Creating dir1 at root
    valfoo.mkdir('dir2') #Creating dir2 at root
    user_inputs = ["dir1", "dir2"] # list of inputs for the command
    index = 0
    def mock_input():
        nonlocal index
        val = user_inputs[index]
        index += 1
        return val #input val from above list
    args = None
    monkeypatch.setattr('builtins.input', mock_input)
    sftpshellfuncs.commands["copydir"](valfoo, args) #call copy directory
    monkeypatch.undo()
    x = ["cd", "dir1"]
    sftpshellfuncs.commands["cd"](valfoo, x) # change directory to dir1
    assert "dir1" in valfoo.pwd
    a = ["cd", ".."]
    sftpshellfuncs.commands["cd"](valfoo, a) # change directory to root
    #call remove dir remote
    y = ["rmd", "dir1"]
    sftpshellfuncs.commands["rmd"](valfoo, y) #Remove dir1
    z = ["rmd", "dir2"]
    sftpshellfuncs.commands["rmd"](valfoo, z) #Remove dir2
    assert "dir1" not in valfoo.pwd
    assert "dir2" not in valfoo.pwd

# logout from remote server 
def test_logout_rem(monkeypatch):
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    # Importing the exit command from the shell
    shell = SFTPShell()
    with patch("builtins.input", side_effect=["logoff"]): # using the inbuilt logoff command
        shell.start() #starting the session to perform logout
        
# Get multiple from remote server   
def test_get_multiple_rem(monkeypatch):
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    valfoo.put('test.txt') #put test.txt to the root
    # Change the file name to success.txt
    rename1 = ["rename", "test.txt", "success1.txt"]
    sftpshellfuncs.commands["rename"](valfoo, rename1)
    assert valfoo.exists('success1.txt') == True # Validate name change to success.txt
    valfoo.put('test.txt') #put test.txt again to the root
    rename2 = ["rename", "test.txt", "success2.txt"]
    sftpshellfuncs.commands["rename"](valfoo, rename2)
    assert valfoo.exists('success2.txt') == True # Validate name change to success.txt
    user_inputs = 'success1.txt success2.txt' # list of inputs for the command
    def mock_input():
        return user_inputs #input val from above list
    args = None
    monkeypatch.setattr('builtins.input', mock_input)
    sftpshellfuncs.commands["mget"](valfoo, args) #call copy directory
    monkeypatch.undo()
    #call remove dir remote
    y = ["rmd", "success1.txt"]
    sftpshellfuncs.commands["rmd"](valfoo, y) #Remove dir1
    z = ["rmd", "success2.txt"]
    sftpshellfuncs.commands["rmd"](valfoo, z) #Remove dir2
    assert "success1.txt" not in valfoo.pwd
    assert "success2.txt" not in valfoo.pwd

# Get file from remote server   
def test_get_file_remote(monkeypatch):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    valfoo.put('test.txt')
    rename1 = ["rename", "test.txt", "test1.txt"]
    sftpshellfuncs.commands["rename"](valfoo, rename1)
    assert valfoo.exists('test1.txt') == True 
    user_inputs = 'test1.txt' 
    def mock_input():
        return user_inputs 
    args = None
    monkeypatch.setattr('builtins.input', mock_input)
    sftpshellfuncs.commands["get_file"](valfoo, args) 
    monkeypatch.undo()
    y = ["rmd", "test1.txt"]
    sftpshellfuncs.commands["rmd"](valfoo, y)
    assert "test1.txt" not in valfoo.pwd

#rename file on local
def test_rename_local_file(tmpdir, monkeypatch, capsys):
    # Create a temporary directory for testing
    test_dir = tmpdir.mkdir("test_directory")

    # Create a temporary test file
    old_filename = 'testrename.txt'
    new_filename = 'new_test.txt'
    old_file_path = os.path.join(str(test_dir), old_filename)
    new_file_path = os.path.join(str(test_dir), new_filename)
    with open(old_file_path, 'w') as f:
        f.write('This is a test file.')

    # Mock user input for the new filename
    user_inputs = new_filename
    def mock_input():
        return user_inputs
    monkeypatch.setattr('builtins.input', mock_input)

    # Perform the renaming operation
    os.rename(old_file_path, new_file_path)

    # Assert that the file was renamed
    assert os.path.exists(new_file_path)
    assert not os.path.exists(old_file_path)

    # Clean up: remove the test directory
    test_dir.remove()



# testing put in remote server
def test_put_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    conn = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    # make sure "test_put.txt" doesn't already exist on remote
    assert conn.exists('test.txt') == False, 'test.txt already exists on remote server'

    # call put remote
    x = ['put', 'test_put.txt']
    sftpshellfuncs.commands['put'](conn, x)
    # check if the file got put
    assert conn.exists('test_put.txt') == True
    # clean up
    conn.execute('rm test_put.txt')
    assert conn.exists('test_put.txt') == False, "test_put_remote has failed cleanup, this will effect future tests"

    return # test_put_remote()


# testing put multiple in remote server
def test_put_multiple_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    conn = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)

    # make sure "test_put.txt" doesn't already exist on remote
    assert conn.exists('test.txt') == False, 'test_put.txt already exists on remote server'
    assert conn.exists('test_put.txt') == False, 'test_put.txt already exists on remote server'

    # call put remote
    x = ['put', 'test.txt', 'test_put.txt']
    sftpshellfuncs.commands['put'](conn, x)
    # check if the file got put
    assert conn.exists('test.txt') == True
    assert conn.exists('test_put.txt') == True
    # clean up
    conn.execute('rm test.txt test_put.txt')
    assert conn.exists('test.txt') == False, "test_put_multiple_remote has failed cleanup, this will effect future tests"
    assert conn.exists('test_put.txt') == False, "test_put_multiple_remote has failed cleanup, this will effect future tests"

    return # test_put_remote()

#using monkeypatch to mock the user input
#using capsys to capture the output printed

# Change the directory in local
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

# List of contents in local
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

# testing ls in remote server
def test_list_content_default():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username=usern, password=passwd, cnopts=cnopts)
    #call mkdir remote
    x = ["mkdir", "test_list_content_default"]
    sftpshellfuncs.commands["mkdir"](valfoo, x)
    #call ls to check if the directory is created
    y = ["ls"]
    sftpshellfuncs.commands["ls"](valfoo, y)
    assert valfoo.exists('test_list_content_default') == True
    #Clean up
    z = ["rmd" , "test_list_content_default"]
    sftpshellfuncs.commands["rmd"](valfoo, z)
    assert "test_list_content_default" not in valfoo.pwd

#testing chmod on remote server
def test_change_mode_remote(capsys):
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)

    #call mkdir remote
    x = ["mkdir", "testdir_chmod"]
    sftpshellfuncs.commands["mkdir"](valfoo, x) 
    #call ls to check if the directory is created
    y = ["ls"]
    sftpshellfuncs.commands["ls"](valfoo, y)
    assert valfoo.exists('testdir_chmod') == True

    #group and everyone else does not have any permissions to read, write or execute the directory testdir_chmod by default when created
    #call chmod to change the permissions to 777 for example
    x = ["chmod", "777", "testdir_chmod"]
    sftpshellfuncs.commands["chmod"](valfoo, x)

    # Capture and split the printed output
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split('\n')

    # check for success message in the output
    assert "Permission changed successfully for 'testdir_chmod'" in output_lines

    # Clean up
    z = ["rmd", "testdir_chmod"]
    sftpshellfuncs.commands["rmd"](valfoo, z)
    assert "test.txt" not in valfoo.pwd

# testing mkdir in remote server
def test_make_directory_remote():
    #setting the connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    valfoo = pysftp.Connection('linux.cs.pdx.edu', username= usern, password= passwd, cnopts=cnopts)
    #call mkdir remote
    x = ["mkdir", "test_mkdir"]
    sftpshellfuncs.commands["mkdir"](valfoo, x)
    #call ls to check if the directory is created
    y = ["ls"]
    sftpshellfuncs.commands["ls"](valfoo, y)
    assert valfoo.exists('test_mkdir') == True
    #Clean up
    z = ["rmd" , "test_mkdir"]
    sftpshellfuncs.commands["rmd"](valfoo, z)
    assert "test_mkdir" not in valfoo.pwd