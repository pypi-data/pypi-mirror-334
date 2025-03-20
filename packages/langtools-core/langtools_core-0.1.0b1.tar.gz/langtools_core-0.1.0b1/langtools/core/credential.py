import os, base64, platform
from azure.core.credentials import TokenCredential
from azure.identity import (
    SharedTokenCacheCredential,
    CertificateCredential,
    DefaultAzureCredential,
    ManagedIdentityCredential,
    OnBehalfOfCredential
)
from azure.keyvault.secrets import SecretClient
from typing import Mapping, Optional, Dict, Callable, Union
from dotenv import load_dotenv
from enum import Enum
from .identity import LongRunningOBOTokenCredential

class CredentialType(Enum):
    Default = "default"
    ManagedIdentity = "managedidentity"
    Certificate = "certificate"
    Shared = "shared"
    OnBehalfOf = "onbehalfof"
    LongRunningOnBehalfOf = "longrunningonbehalfof"

class Credential:
    """A class to manage Azure credentials and authentication."""

    def __init__(self,
                 tenant_id: Optional[str] = None,
                 client_id: Optional[str] = None
    ) -> None:
        """
        Initialize Credential with configuration from parameters or environment variables.

        Args:
            tenant_id: Azure tenant ID (overrides AZURE_TENANT_ID)
            client_id: Azure client/application ID (overrides AZURE_CLIENT_ID)
        """
        # Load environment variables first
        load_dotenv()

        # Set configuration with parameter priority over environment variables
        self.tenant_id = tenant_id or os.getenv('AZURE_TENANT_ID', None)
        self.client_id = client_id or os.getenv('AZURE_CLIENT_ID', None)
        self.cert_name = os.getenv('AZURE_CERT_NAME', None)
        self.vault_url = os.getenv('AZURE_KEY_VAULT_URL', None)
        
        self.OBO_client_id = "a5a4de99-713c-42c4-a09b-7553cebbe1d7"
        self.OBO_tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"

        self._credential_types: Dict[CredentialType, Callable] = {
            CredentialType.Default: self._get_default_credential,
            CredentialType.ManagedIdentity: self._get_managed_identity_credential,
            CredentialType.Certificate: self._get_certificate_credential,
            CredentialType.Shared: self._get_shared_token_credential,
            CredentialType.OnBehalfOf: self._get_obo_credential,
            CredentialType.LongRunningOnBehalfOf: self._get_long_running_obo_credential,
        }

    def _is_wsl(self) -> bool:
        """Check if running in Windows Subsystem for Linux."""
        return 'microsoft-standard' in platform.release().lower()

    def _get_user_assertion(self) -> str:
        """Get user assertion from file."""
        user_assertion = os.getenv('OBO_USER_ASSERTION', '')
        return user_assertion

    def _get_managed_identity_assertion(self) -> str:
        """Get managed identity assertion."""
        miCred = self._get_default_credential()
        # Use the correct scope for token exchange
        mi_token = miCred.get_token("api://AzureADTokenExchange/.default")
        return mi_token.token

    def get_cert(self,
                credential: TokenCredential,
                cert_name,
                vault_url,
    ) -> bytes:
        """Get certificate from Key Vault."""
        # Get certificate from Key Vault
        secret_client = SecretClient(vault_url, credential)
        cert_secret = secret_client.get_secret(cert_name)
        cert_bytes = base64.b64decode(cert_secret.value)
        
        # Return certificate bytes
        return cert_bytes

    def _get_managed_identity_credential(self, 
                                     client_id: Optional[str] = None,
                                     identity_config: Optional[Mapping[str, str]] = None,
                                     **kwargs) -> ManagedIdentityCredential:
        """Get a Managed Identity credential for Azure services."""
        return ManagedIdentityCredential(
            client_id=client_id,
            identity_config=identity_config,
            **kwargs
        )

    def _get_certificate_credential(
        self,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        cert_bytes: Optional[bytes] = None,
        vault_url: Optional[str] = None,
        cert_name: Optional[str] = None,
        credential_type_kv: Optional[CredentialType] = None,
        **kwargs
    ) -> CertificateCredential:
        """
        Get a certificate-based credential for Azure services.
        
        Note on credential_type_kv:
        Certificate storage differs between Windows and WSL:
        Windows: Certificates are stored in the Windows Certificate Store (needs CredentialType.Shared)
        WSL: Certificates are accessed through environment-based configuration (needs CredentialType.Default)
        """
        # Use provided values or fall back to instance defaults
        tenant_id = tenant_id or self.tenant_id
        client_id = client_id or self.client_id

        # Determine appropriate credential type for key vault access
        if credential_type_kv is None:
            credential_type_kv = CredentialType.Default if self._is_wsl() else CredentialType.Shared

        # Get certificate from Key Vault
        if not cert_bytes:
            vault_url = vault_url or self.vault_url
            cert_name = cert_name or self.cert_name
            if not vault_url or not cert_name:
                raise ValueError("Missing required certificate configuration.")
            
            credential = self.get_credential(credential_type_kv)
            cert_bytes = self.get_cert(credential=credential, cert_name=cert_name, vault_url=vault_url)

        # Create certificate credential
        return CertificateCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            certificate_data=cert_bytes,
            send_certificate_chain=True,
            **kwargs
        )

    def _get_shared_token_credential(self, **kwargs) -> SharedTokenCacheCredential:
        """Get a shared token cache credential for Azure services."""
        return SharedTokenCacheCredential(additionally_allowed_tenants=["*"])

    def _get_default_credential(self, **kwargs) -> DefaultAzureCredential:
        """Get a DefaultAzureCredential for Azure services."""
        return DefaultAzureCredential(**kwargs)
    
    def _get_obo_credential(self, **kwargs) -> OnBehalfOfCredential:
        """Get an OnBehalfOfCredential for Azure services."""
        user_assertion = self._get_user_assertion()
        
        # Get the client assertion token first
        credential = OnBehalfOfCredential(
            tenant_id=self.OBO_tenant_id, 
            client_id=self.OBO_client_id, 
            user_assertion=user_assertion, 
            client_assertion_func=self._get_managed_identity_assertion,
        )
        return credential
    
    def _get_long_running_obo_credential(self, **kwargs) -> LongRunningOBOTokenCredential:
        user_assertion = self._get_user_assertion()
        miCred = self._get_default_credential()

        lrobo = LongRunningOBOTokenCredential(
            tenant_id=self.OBO_tenant_id,
            client_id=self.OBO_client_id,
            initial_access_token=user_assertion,
            client_credential=miCred,
            scopes=["https://vault.azure.net/user_impersonation"]
        )
        return lrobo

    def get_credential(
        self,
        credential_type: Union[CredentialType, str] = CredentialType.Default,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        **kwargs
    ) -> TokenCredential:
        """
        Get a token credential based on the specified type.

        Args:
            credential_type: Type of credential to return (CredentialType or str)
            tenant_id: Azure tenant ID (defaults to instance's tenant_id)
            client_id: Azure client/application ID (defaults to instance's client_id)
            **kwargs: Additional arguments specific to the credential type.
                     For CredentialType.Certificate:
                     - credential_type_kv: Optional override for key vault access credential type
                       (automatically set based on environment: Default for WSL, Shared for Windows)

        Returns:
            TokenCredential: The configured credential object
            
        Raises:
            ValueError: If credential_type is not recognized
        """
        # Convert string to CredentialType if needed
        if isinstance(credential_type, str):
            try:
                credential_type = next(ct for ct in CredentialType if ct.value == credential_type)
            except StopIteration:
                valid_types = [ct.value for ct in CredentialType]
                raise ValueError(f"Invalid credential type. Must be one of: {', '.join(valid_types)}")

        if credential_type not in self._credential_types:
            valid_types = [ct.value for ct in CredentialType]
            raise ValueError(f"Invalid credential type. Must be one of: {', '.join(valid_types)}")

        if credential_type == CredentialType.Certificate:
            return self._credential_types[credential_type](
                tenant_id=tenant_id or self.tenant_id,
                client_id=client_id or self.client_id,
                **kwargs
            )
        elif credential_type == CredentialType.ManagedIdentity:
            return self._credential_types[credential_type](client_id=client_id, **kwargs)
        else:
            return self._credential_types[credential_type](**kwargs)