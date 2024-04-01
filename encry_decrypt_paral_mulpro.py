from Crypto.Cipher import DES
import base64
import random
import string
import time
import multiprocessing

# Fonction pour générer un mot de passe aléatoire
def generate_random_password():
    allowed_chars = string.ascii_letters + string.digits + "./"
    password = ''.join(random.choice(allowed_chars) for _ in range(8))
    return password

# Fonction pour crypter un mot de passe
def encrypt_password(password, key):
    if len(password) >= 8:
        password = password[:8]
    else:
        password = password.ljust(8)
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    encrypted_password = cipher.encrypt(password.encode())
    return base64.b64encode(encrypted_password).decode()

# Fonction pour déchiffrer un mot de passe crypté
def decrypt_password(encrypted_password, key):
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    decrypted_password = cipher.decrypt(base64.b64decode(encrypted_password))
    return decrypted_password.decode().rstrip('\0')

# Fonction exécutée par chaque processus pour le cryptage en parallèle
def worker_encrypt(password):
    global key
    return encrypt_password(password, key)

# Fonction exécutée par chaque processus pour le déchiffrement en parallèle
def worker_decrypt(encrypted_password):
    global key
    return decrypt_password(encrypted_password, key)
key = "MBertini"
if __name__ == '__main__':
    passwords_to_encrypt = [generate_random_password() for _ in range(1000000)]

    start_crypt_time = time.time()
    num_workers = multiprocessing.cpu_count()
    print(num_workers)
    pool = multiprocessing.Pool(processes=num_workers)
    encrypted_passwords = pool.map(worker_encrypt, passwords_to_encrypt)
    pool.close()
    pool.join()
    end_crypt_time = time.time()
    exe_cryp_time = round(end_crypt_time - start_crypt_time, 4)

    print("Temps du cryptage:", exe_cryp_time)

    start_decrypt_time = time.time()
    pool = multiprocessing.Pool(processes=num_workers)
    decrypted_passwords = pool.map(worker_decrypt, encrypted_passwords)
    pool.close()
    pool.join()
    end_decrypt_time = time.time()
    exe_decryp_time = round(end_decrypt_time - start_decrypt_time, 4)

    print("\nTemps de decryptage:", exe_decryp_time)
