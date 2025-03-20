from dentity.access_management_service import AccessManagementService
from dentity.connect_service import ConnectService
from dentity.credential_service import CredentialService
from dentity.file_management_service import FileManagementService
from dentity.proto.sdk.options.v1 import DentityOptions
from dentity.provider_service import ProviderService

from dentity.service_base import ServiceBase
from dentity.template_service import TemplateService
from dentity.trustregistry_service import TrustRegistryService
from dentity.wallet_service import WalletService


class DentityService(ServiceBase):
    def __init__(
        self,
        *,
        server_config: DentityOptions = None,
    ):
        super().__init__(server_config)

        self._access_management: AccessManagementService = AccessManagementService(
            server_config=self._channel
        )
        self._connect: ConnectService = ConnectService(server_config=self._channel)
        self._credential: CredentialService = CredentialService(
            server_config=self._channel
        )
        self._file_management: FileManagementService = FileManagementService(
            server_config=self._channel
        )
        self._template: TemplateService = TemplateService(server_config=self._channel)
        self._provider: ProviderService = ProviderService(server_config=self._channel)
        self._trust_registry: TrustRegistryService = TrustRegistryService(
            server_config=self._channel
        )
        self._wallet: WalletService = WalletService(server_config=self._channel)

    def __del__(self):
        self.close()

    def close(self):
        self._access_management.close()
        self._credential.close()
        self._file_management.close()
        self._template.close()
        self._provider.close()
        self._trust_registry.close()
        self._wallet.close()
        super().close()

    @property
    def access_management(self) -> AccessManagementService:
        self._access_management.service_options = self.service_options
        return self._access_management

    @property
    def connect(self) -> ConnectService:
        self._connect.service_options = self.service_options
        return self._connect

    @property
    def credential(self) -> CredentialService:
        self._credential.service_options = self.service_options
        return self._credential

    @property
    def file_management(self) -> FileManagementService:
        self._file_management.service_options = self.service_options
        return self._file_management

    @property
    def template(self) -> TemplateService:
        self._template.service_options = self.service_options
        return self._template

    @property
    def provider(self) -> ProviderService:
        self._provider.service_options = self.service_options
        return self._provider

    @property
    def trust_registry(self) -> TrustRegistryService:
        self._trust_registry.service_options = self.service_options
        return self._trust_registry

    @property
    def wallet(self) -> WalletService:
        self._wallet.service_options = self.service_options
        return self._wallet
