#-------------------------------------------------------------------------------
# Name:        Crippter
# Purpose:     Simple password obfuscation for strings and files.
#
# Author:      werwath
#
# Created:     12/07/2011
# Copyright:   (c) werwath 2011
# Licence:     Lifted most of this from Pyro.699
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import base64
import filecmp
class Crippter:

    def __init__(self,p):
        self.password = p
        self.c=""
        for x in range(32,127): self.c+=chr(x)

    def encryptFile(self,fin,fout):
        #Let any exceptions go up to caller
        stringContents = open(fin, 'rb').read()
        encryptedStringContents = self.encryptString(stringContents)
        open(fout,'wb').write(encryptedStringContents)

    def encryptString(self,s):
        k = self.password
        s = base64.b64encode(s)
        s2=[self.c.find(v) for v in s]
        k2=[]
        i=0
        while len(k2) != len(s):
            if i >= len(k):
                i = 0
            k2.append(self.c.find(k[i]))
            i+=1
        r=[self.c[(j+k)%len(self.c)] for j,k in zip(s2,k2)]
        return  "".join(r)

    def decryptFile(self,fin,fout):
        #Let any exceptions go up to caller
        s = open(fin, 'rb').read()
        decryptedStringContents = self.decryptString(s)
        open(fout,'wb').write(decryptedStringContents)

    def decryptString(self,r):
        k = self.password
        r2=[self.c.find(v) for v in r]
        k2=[]
        i=0
        while len(k2) != len(r):
            if i >= len(k):
                i = 0
            k2.append(self.c.find(k[i]))
            i+=1
        s=[self.c[(j-k)%len(self.c)] for j,k in zip(r2,k2)]
        return base64.b64decode("".join(s))


def main():
    #FIXME - Make this a real unit test.
    password = "secret"
    message = "This is a secret for jo jo bolonga!!!!"
    crippter = Crippter(password)
    encoded_message = crippter.encryptString(message)
    print "GOT:"+encoded_message
    decoded_message = Crippter(password).decryptString(encoded_message)
    print "Original String: %s\nKey: %s\nHash: %s\nDecrypted String: %s\nEqual?: %s"%(message, password, encoded_message, decoded_message, message==decoded_message)

    crippter.encryptFile('pain.mp3','encrypted_pain.mp3')
    crippter.decryptFile('encrypted_pain.mp3','decrypted_pain.mp3')
    print "Equal %s\n"%(filecmp.cmp('decrypted_pain.mp3','pain.mp3'))




if __name__ == '__main__':
    main()
