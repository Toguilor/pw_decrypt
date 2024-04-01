# PASSWORD DECRYPTION
 
Implementation of a sequential and a parallel Program for password decrtpting.
 
The program generates numbers of passwords needed by the user. 

Each password consider 8 characters lengths in the set [a-zA-Z0-9./]

After generating passwords, the program encryptes them using crypt (DES), and decrypt the password encrypted still using crypt (DES)

Both programs consider only dates or common 8-chars passwords

At the end we compute the execution time of the sequential and parallel program for the decryption to calculate the speedup.
