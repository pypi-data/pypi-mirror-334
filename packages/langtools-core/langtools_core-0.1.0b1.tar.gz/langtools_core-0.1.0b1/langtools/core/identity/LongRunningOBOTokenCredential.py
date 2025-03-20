import time
import logging
from typing import Optional, Any, Union
import msal
from azure.core.credentials import AccessToken, TokenCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

logger = logging.getLogger(__name__)

class LongRunningOBOTokenCredential(TokenCredential):
    """
    A credential that implements the long-running On-Behalf-Of flow using refresh tokens.
    This allows for token refresh in long-running processes without requiring user interaction.
    """
    
    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_credential: Union[DefaultAzureCredential, ManagedIdentityCredential],
        initial_access_token: str,
        scopes: list[str],
    ) -> None:
        """
        Initialize the LongRunningOBOTokenCredential.
        
        :param tenant_id: Azure AD tenant ID
        :param client_id: Application (client) ID
        :param client_credential: DefaultAzureCredential or ManagedIdentityCredential instance
        :param initial_access_token: Initial access token to exchange for refresh token
        :param scopes: List of scopes to request for refresh token and access token
        """
        self._tenant_id = tenant_id
        self._client_id = client_id
        self._initial_access_token = initial_access_token
        self._scopes = scopes
        
        # Get client assertion token
        token = client_credential.get_token("api://AzureADTokenExchange/.default")
        
        # Initialize MSAL confidential client with client assertion and default token cache
        self._app = msal.ConfidentialClientApplication(
            client_id=self._client_id,
            authority=f"https://login.microsoftonline.com/{self._tenant_id}",
            client_credential={
                "client_assertion": token.token
            }
        )
        
        self._refresh_token: Optional[str] = None
        
        # Cache for user assertion (access token)
        self._user_assertion: Optional[AccessToken] = None
        
        # Initialize refresh token using OBO flow
        self._initialize_refresh_token()

    def _initialize_refresh_token(self) -> None:
        """
        Initialize the refresh token by exchanging the initial access token using OBO flow.
        Uses the scopes provided in constructor for the refresh token flow.
        """
        try:
            result = self._app.acquire_token_on_behalf_of(
                user_assertion=self._initial_access_token,
                scopes=self._scopes
            )
            
            if "error" in result:
                raise ClientAuthenticationError(
                    message=f"Error in OBO flow: {result.get('error_description', result['error'])}"
                )
            
            if "refresh_token" not in result:
                raise ClientAuthenticationError(
                    message="Failed to obtain refresh token from initial access token"
                )
            
            self._refresh_token = result["refresh_token"]
            # Cache the initial access token as AccessToken
            self._user_assertion = AccessToken(
                result["access_token"],
                int(result["expires_in"] + time.time())
            )
            
        except Exception as ex:
            raise ClientAuthenticationError(
                message=f"Failed to initialize refresh token: {str(ex)}"
            ) from ex

    def _ensure_valid_user_assertion(self) -> str:
        """
        Ensure we have a valid access token to use as user assertion.
        If expired, gets a new one using the refresh token.
        
        :return: Valid access token to use as user assertion
        :raises ClientAuthenticationError: If token acquisition fails
        """
        # Check if current user assertion is valid
        if (self._user_assertion and 
            self._user_assertion.expires_on > time.time() + 300):  # 5 minute buffer
            return self._user_assertion.token
            
        if not self._refresh_token:
            raise ClientAuthenticationError("No refresh token available")
            
        try:
            # Get new access token using refresh token with constructor scopes
            result = self._app.acquire_token_by_refresh_token(
                refresh_token=self._refresh_token,
                scopes=self._scopes
            )
            
            if "error" in result:
                raise ClientAuthenticationError(
                    f"Error refreshing token: {result.get('error_description', result['error'])}"
                )
            
            # Update refresh token if provided
            if "refresh_token" in result:
                self._refresh_token = result["refresh_token"]
            
            # Cache the new access token as AccessToken
            self._user_assertion = AccessToken(
                result["access_token"],
                int(result["expires_in"] + time.time())
            )
            
            return self._user_assertion.token
            
        except Exception as ex:
            raise ClientAuthenticationError(
                message=f"Failed to acquire new user assertion: {str(ex)}"
            ) from ex

    def get_token(self, *scopes: str, **kwargs: Any) -> AccessToken:
        """
        Get an access token.
        Returns the cached user assertion token that was obtained with constructor scopes.
        
        :param scopes: Ignored as we use constructor scopes
        :param kwargs: Additional keyword arguments
        :return: An AccessToken instance
        :raises ClientAuthenticationError: If token acquisition fails
        """
        try:
            # Get valid user assertion (refreshes if needed)
            self._ensure_valid_user_assertion()
            
            if not self._user_assertion:
                raise ClientAuthenticationError("No valid user assertion available")
                
            return self._user_assertion
            
        except Exception as ex:
            raise ClientAuthenticationError(
                message=f"Failed to acquire token: {str(ex)}"
            ) from ex