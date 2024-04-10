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

def worker_generate_random_password(num_passwords):
    return [generate_random_password() for _ in range(num_passwords)]

key = "MBertini"

if __name__ == '__main__':
    num_workers = 0 #multiprocessing.cpu_count()
    num_passwords = 10000000

    if num_passwords <= 10000:
        num_workers = 1
    elif num_passwords <= 100000:
        num_workers = 2
    elif num_passwords <= 10000000:
        num_workers = 16
    elif num_passwords <= 9000000:
        num_workers = 10
    else:
        num_workers = multiprocessing.cpu_count()

    #Génération de mots de passe
    start_time_gen_pw = time.time()
    #passwords_to_encrypt = [generate_random_password() for _ in range(10000000)]

    # Divisez le nombre de mots de passe à générer par le nombre de processus
    chunk_size = num_passwords // num_workers

    # Créez une liste vide pour stocker les résultats de chaque processus
    results = []

    # Créez une piscine de processus
    pool = multiprocessing.Pool(processes=num_workers)

    # Mappez la fonction generate_random_passwords sur chaque processus avec le nombre de mots de passe à générer
    for _ in range(num_workers):
        results.append(pool.apply_async(worker_generate_random_password, args=(chunk_size,)))

    # Attendez que tous les processus se terminent et récupérez les résultats
    pool.close()
    pool.join()

    # Concaténez les résultats de chaque processus en une seule liste de mots de passe
    passwords_to_encrypt = []
    for result in results:
        passwords_to_encrypt.extend(result.get())

    end_time_gen_pw = time.time()
    pw_gen_time = end_time_gen_pw - start_time_gen_pw

    #print(passwords_to_encrypt)

    #print(f"Temps de generation de {len(passwords_to_encrypt)} mot de passe: {pw_gen_time}")

    start_crypt_time = time.time()
    print(num_workers)
    print("Nombre de mots de passe: ", num_passwords)
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

    print("Temps de decryptage:", exe_decryp_time)
