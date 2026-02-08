#!/usr/bin/env python3
"""
Script to configure HashiCorp Vault with FastAPI secrets
"""
import hvac
import secrets
import os
import subprocess
import re
import time

def check_vault_installed():
    """Verifies that Vault is installed or Docker is available"""
    try:
        subprocess.run(['vault', '--version'], check=True, capture_output=True)
        return 'vault'
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['docker', '--version'], check=True, capture_output=True)
            print("✅ Using Docker to run Vault")
            return 'docker'
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Neither Vault nor Docker are available")
            return None

def start_vault_dev(method='vault'):
    """Starts Vault in development mode"""
    print("Starting Vault in development mode...")
    
    if method == 'docker':
        cmd = ['docker', 'run', '--rm', '-p', '8200:8200', '--cap-add=IPC_LOCK', 'vault:latest', 'vault', 'server', '-dev', '-dev-listen-address=0.0.0.0:8200']
    else:
        cmd = ['vault', 'server', '-dev']
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    root_token = None
    for line in process.stdout:
        print(line.strip())
        if "Root Token:" in line:
            token_match = re.search(r'Root Token:\s+([^\s]+)', line)
            if token_match:
                root_token = token_match.group(1)
                print(f"✅ Root Token captured: {root_token}")
                break
    
    if root_token:
        os.environ['VAULT_TOKEN'] = root_token
        save_env_file(root_token)
        return process, root_token
    
    process.terminate()
    return None, None

def save_env_file(token):
    """Creates/updates the .env file preserving existing configuration"""
    env_content = {}
    
    # Read existing .env file if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key] = value
    
    # Update Vault values
    env_content['VAULT_URL'] = 'http://localhost:8200'
    env_content['VAULT_TOKEN'] = token
    
    # Write updated file
    with open('.env', 'w') as f:
        f.write("# Database Configuration\n")
        f.write(f"DATABASE_URL={env_content.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/claims_manager')}\n\n")
        
        f.write("# FastAPI Configuration\n")
        f.write(f"DEBUG={env_content.get('DEBUG', 'True')}\n")
        f.write(f"SECRET_KEY={env_content.get('SECRET_KEY', 'your-secret-key-here')}\n\n")
        
        f.write("# HashiCorp Vault Configuration\n")
        f.write(f"VAULT_URL={env_content['VAULT_URL']}\n")
        f.write(f"VAULT_TOKEN={env_content['VAULT_TOKEN']}\n")
        f.write(f"VAULT_SECRET_PATH={env_content.get('VAULT_SECRET_PATH', 'secret/fastapi')}\n\n")
        
        f.write("# CORS Configuration\n")
        f.write(f"ALLOWED_ORIGINS={env_content.get('ALLOWED_ORIGINS', 'http://localhost:4200')}\n")
    
    print("✅ .env file updated")

def init_server():
    """Initialize a hvac client at http://localhost:8200 and
    prints out whether the client is authenticated.
    """
    client = hvac.Client(url='http://localhost:8200')
    return client

def setup_secrets(token):
    """Generates and stores SECRET_KEY in Vault and updates .env"""
    try:
        client = hvac.Client(url='http://localhost:8200', token=token)
        
        if not client.is_authenticated():
            return False
        
        secret_key = secrets.token_urlsafe(32)
        client.secrets.kv.v2.create_or_update_secret(
            path='fastapi',
            secret={'SECRET_KEY': secret_key}
        )
        
        # Verify
        response = client.secrets.kv.v2.read_secret_version(path='fastapi', raise_on_deleted_version=True)
        if response['data']['data']['SECRET_KEY'] == secret_key:
            print("✅ SECRET_KEY stored and verified in secret/fastapi")
            
            # Update SECRET_KEY in .env
            update_secret_key_in_env(secret_key)
            return True
        
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_secret_key_in_env(secret_key):
    """Updates SECRET_KEY in the .env file"""
    if not os.path.exists('.env'):
        return
    
    with open('.env', 'r') as f:
        content = f.read()
    
    # Replace SECRET_KEY
    import re
    content = re.sub(r'SECRET_KEY=.*', f'SECRET_KEY={secret_key}', content)
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ SECRET_KEY updated in .env")

def main():
    """Main function"""
    method = check_vault_installed()
    if not method:
        return
    
    vault_process, root_token = start_vault_dev(method)
    if not root_token:
        return
    
    time.sleep(3)
    
    # Verify server and authentication
    client = init_server()
    if not client.is_authenticated():
        print("❌ Error: Client not authenticated")
        vault_process.terminate()
        return
    
    print("✅ Server started and authentication successful")
    
    if setup_secrets(root_token):
        print("🎉 Configuration completed. Press Ctrl+C to stop Vault")
        try:
            vault_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping Vault...")
            vault_process.terminate()
    else:
        vault_process.terminate()

if __name__ == "__main__":
    main()