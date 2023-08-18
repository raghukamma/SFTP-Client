''' main.py
Tazwell B. 7/14/2023
main
'''

import sftpclient

def main():
    client = sftpclient.SFTPClient()
    client.start()

if __name__=='__main__':
    main()