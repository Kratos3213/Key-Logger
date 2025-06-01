from cryptography.fernet import Fernet

# Replace with your actual key and message
key = b"aoQ3jAqx608GypyRz_vSPMFh9h1VaYtObv5xgXPz-rM="
encrypted_message = b"gAAAAABoPCm4NgPmOT45hYN88WAJ_3NSHi4UuoevAhUI1Fv8Ri05euqBP7Tcn8C4HGxw9_A3_Z_HBMkuL0fmB9jh_DF1MKNhsCzvuCPS11qi_-wFJrqAuVQ="

fernet = Fernet(key)
decrypted = fernet.decrypt(encrypted_message)

print(decrypted.decode())
