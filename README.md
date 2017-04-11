# rsaProject
implementation of RSA in Python3

The functions in this project encrypt and decrypt by BLOCKS, not
by individual letters.
Also please note that the ASCII codes per character are three-digits long, not two.
This program requires a list of primes named 'primes.txt' which is provided.
It also requires a 'privateKey.txt' where n and d are stored, and 'publicKey.txt' where
n and e are stored. n is stored in the first line, d/e are stored in the second line.
During the first execution of this program, the user should either 
provide their own keys by creating and editing the text files, or generate the keys 
so that the text files are created if the text files are missing.
