from Crypto.Cipher import DES
import base64
import random
import string
import time

def generate_random_password():
    # Définir l'ensemble des caractères autorisés
    allowed_chars = string.ascii_letters + string.digits + "./"

    # Générer un mot de passe aléatoire de longueur 8
    password = ''.join(random.choice(allowed_chars) for _ in range(8))
    return password

# Fonction pour crypter un mot de passe
def encrypt_password(password, key):
    if len(password) >= 8:
        password = password[:8]  # Si le mot de passe est plus long que 8 caractères, prenez les 8 premiers caractères
    else:
        password = password.ljust(8)  # Si le mot de passe est plus court que 8 caractères, ajoutez un remplissage
    
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    encrypted_password = cipher.encrypt(password.encode())
    return base64.b64encode(encrypted_password).decode()

# Fonction pour déchiffrer un mot de passe crypté
def decrypt_password(encrypted_password, key):
    cipher = DES.new(key.encode(), DES.MODE_ECB)
    decrypted_password = cipher.decrypt(base64.b64decode(encrypted_password))
    return decrypted_password.decode().rstrip('\0')


# Generation de la liste des mots de passe à crypter
passwords_to_encrypt = [generate_random_password() for _ in range(10000000)]  # Liste des mots de passe à crypter
#print("Mot de passe genere:", passwords_to_encrypt)

# Clé de chiffrement
key = "MBertini"  # Clé de chiffrement utilisée pour le cryptage

# Cryptage des mots de passe
start_crypt_time = time.time()
encrypted_passwords = [encrypt_password(password, key) for password in passwords_to_encrypt]
end_crypt_time = time.time()
exe_cryp_time = round(end_crypt_time - start_crypt_time, 4)

print("Temps du cryptage:", exe_cryp_time)
# Affichage des mots de passe cryptés
#for encrypted_password in encrypted_passwords:
#    print(encrypted_password)

# Déchiffrement des mots de passe cryptés
start_decrypt_time = time.time()
decrypted_passwords = [decrypt_password(password, key) for password in encrypted_passwords]
end_decrypt_time = time.time()
exe_decryp_time = round(end_decrypt_time - start_decrypt_time, 4)

print("\nTemps de decryptage:", exe_decryp_time)

# Affichage des mots de passe déchiffrés
#for decrypted_password in decrypted_passwords:
#    print(decrypted_password)
