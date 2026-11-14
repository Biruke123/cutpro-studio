import os
import zipfile
from file_crypto import is_encrypted, decrypt_file

folder = r"D:\SecureBoxAI\uploads"

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    if not os.path.isfile(path):
        continue
    
    print(f"\n📄 File: {filename}")
    print(f"   Size: {os.path.getsize(path)} bytes")
    
    # Check magic header
    with open(path, 'rb') as f:
        header = f.read(4)
    print(f"   Header: {header} ({header.hex()})")
    
    # Is it encrypted?
    if is_encrypted(path):
        print(f"   ✅ ENCRYPTED (SBXF magic found)")
    else:
        print(f"   ❌ NOT encrypted!")
        continue
    
    # Try to open as zip (all .docx/.xlsx are zips)
    try:
        with zipfile.ZipFile(path) as z:
            print(f"   ❌ ZIP opened — NOT encrypted!")
            print(f"   Contents: {z.namelist()[:3]}")
    except zipfile.BadZipFile:
        print(f"   ✅ Cannot open as ZIP — truly encrypted")
    except Exception as e:
        print(f"   ✅ Cannot open — {type(e).__name__}")
    
    # Decrypt and verify content
    try:
        decrypted = decrypt_file(path)
        print(f"   ✅ Decryption works! Plaintext size: {len(decrypted)} bytes")
        
        # Check if it's a valid ZIP after decrypt
        import io
        try:
            with zipfile.ZipFile(io.BytesIO(decrypted)) as z:
                print(f"   ✅ Decrypted content is valid DOCX/ZIP: {z.namelist()[:3]}")
        except zipfile.BadZipFile:
            print(f"   ⚠️  Decrypted content is not a ZIP (could be image/pdf/etc)")
    except Exception as e:
        print(f"   ❌ Decryption failed: {e}")
