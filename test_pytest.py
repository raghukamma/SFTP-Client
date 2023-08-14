#from client.sftpclient import sftpclient
import pysftp
import sftpshellfuncs 
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



