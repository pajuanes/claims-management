# Configuración de HashiCorp Vault para FastAPI

Este proyecto utiliza HashiCorp Vault para gestionar de forma segura la `SECRET_KEY` y otros secretos sensibles.

## Instalación y Configuración

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Vault (Desarrollo Local)

#### Opción A: Usando Docker
```bash
# Ejecutar Vault en modo desarrollo
docker run --cap-add=IPC_LOCK -d --name=dev-vault -p 8200:8200 -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' vault:latest

# El token de desarrollo será: myroot
```

#### Opción B: Instalación local
```bash
# Descargar e instalar Vault desde https://www.vaultproject.io/downloads
# Ejecutar en modo desarrollo
vault server -dev -dev-root-token-id="myroot"
```

### 3. Configurar variables de entorno

Copia `.env.example` a `.env` y configura:

```bash
cp .env.example .env
```

Edita `.env`:
```env
VAULT_URL=http://localhost:8200
VAULT_TOKEN=myroot
```

### 4. Configurar secretos en Vault

Ejecuta el script de configuración:

```bash
python setup_vault.py
```

Este script:
- Genera una `SECRET_KEY` segura automáticamente
- La almacena en Vault en el path `secret/fastapi`
- Verifica la conectividad con Vault

### 5. Verificar configuración

Tu aplicación FastAPI ahora:
1. Intentará obtener la `SECRET_KEY` desde Vault
2. Si Vault no está disponible, usará la variable de entorno `SECRET_KEY`
3. Como último recurso, usará una clave por defecto (solo para desarrollo)

## Uso en Producción

Para producción:

1. **Configura Vault con autenticación adecuada** (no uses el modo dev)
2. **Usa tokens con permisos limitados**
3. **Configura políticas de acceso restrictivas**
4. **Considera usar métodos de autenticación como AWS IAM, Kubernetes, etc.**

### Ejemplo de política de Vault para producción:

```hcl
path "secret/data/fastapi" {
  capabilities = ["read"]
}
```

## Comandos útiles de Vault

```bash
# Verificar estado de Vault
vault status

# Leer secreto
vault kv get secret/fastapi

# Escribir secreto manualmente
vault kv put secret/fastapi SECRET_KEY="tu-clave-secreta"

# Listar secretos
vault kv list secret/
```

## Troubleshooting

- **Error de conexión**: Verifica que Vault esté ejecutándose en `http://localhost:8200`
- **Error de autenticación**: Verifica que `VAULT_TOKEN` esté configurado correctamente
- **Secreto no encontrado**: Ejecuta `python setup_vault.py` para crear los secretos iniciales