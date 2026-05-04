from __future__ import annotations

from types import TracebackType

import httpx

from .auth import AuthProvider, AuthType, Credentials
from .dispatcher import Dispatcher, RetryConfig
from .resources import (
    Account,
    BankAccounts,
    Events,
    Expenses,
    Generators,
    InboxFiles,
    InventoryItems,
    InventoryMoves,
    Invoices,
    NumberFormats,
    RecurringGenerators,
    Subjects,
    Todos,
    Users,
    Webhooks,
)
from .types import JsonValue


class FakturoidClient:
    """The main entry point for interacting with the Fakturoid API.

    This client provides a high-level, Pythonic interface to all Fakturoid resources.
    It handles authentication, request dispatching, and automatic retries.

    Attributes:
        auth: The authentication provider.
        dispatcher: The underlying request dispatcher.
        account: Account resource.
        bank_accounts: Bank accounts resource.
        events: Events resource.
        expenses: Expenses resource.
        generators: Generators resource.
        inbox_files: Inbox files resource.
        inventory_items: Inventory items resource.
        inventory_moves: Inventory moves resource.
        invoices: Invoices resource.
        number_formats: Number formats resource.
        recurring_generators: Recurring generators resource.
        subjects: Subjects (contacts) resource.
        todos: Todos resource.
        users: Users resource.
        webhooks: Webhooks resource.
    """

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        user_agent: str,
        account_slug: str | None = None,
        redirect_uri: str | None = None,
        credentials: Credentials | None = None,
        http_client: httpx.AsyncClient | None = None,
        base_url: str = Dispatcher.BASE_URL,
        retry: RetryConfig | None = None,
        close_http_client: bool | None = None,
    ) -> None:
        """Initializes the FakturoidClient.

        See: https://www.fakturoid.cz/api/v3#user-agent

        Args:
            client_id: The OAuth2 client ID.
            client_secret: The OAuth2 client secret.
            user_agent: The User-Agent string to identify the application.
            account_slug: The Fakturoid account slug. Required for most operations.
            redirect_uri: The OAuth2 redirect URI.
            credentials: Optional existing credentials to load.
            http_client: Optional custom HTTPX async client.
            base_url: The base URL for the API.
            retry: Optional retry configuration.
            close_http_client: Whether to close the http_client when aclose() is called.
                Defaults to True if http_client is not provided.
        """
        owns_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient()
        self._close_http_client = owns_client if close_http_client is None else close_http_client

        self.auth = AuthProvider(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            client=self._http_client,
            base_url=base_url,
        )
        self.auth.set_credentials(credentials)

        self.dispatcher = Dispatcher(
            authorization=self.auth,
            client=self._http_client,
            account_slug=account_slug,
            base_url=base_url,
            retry=retry,
            user_agent=user_agent,
        )

        # Resources
        self.account = Account(self.dispatcher)
        self.bank_accounts = BankAccounts(self.dispatcher)
        self.events = Events(self.dispatcher)
        self.expenses = Expenses(self.dispatcher)
        self.generators = Generators(self.dispatcher)
        self.inbox_files = InboxFiles(self.dispatcher)
        self.inventory_items = InventoryItems(self.dispatcher)
        self.inventory_moves = InventoryMoves(self.dispatcher)
        self.invoices = Invoices(self.dispatcher)
        self.number_formats = NumberFormats(self.dispatcher)
        self.recurring_generators = RecurringGenerators(self.dispatcher)
        self.subjects = Subjects(self.dispatcher)
        self.todos = Todos(self.dispatcher)
        self.users = Users(self.dispatcher)
        self.webhooks = Webhooks(self.dispatcher)

    def set_account_slug(self, account_slug: str) -> None:
        """Sets the account slug for the client.

        Args:
            account_slug: The Fakturoid account slug.
        """
        self.dispatcher.set_account_slug(account_slug)

    async def aclose(self) -> None:
        """Closes the underlying HTTP client."""
        if self._close_http_client:
            await self._http_client.aclose()

    async def __aenter__(self) -> FakturoidClient:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        await self.aclose()


__all__ = [
    "AuthType",
    "FakturoidClient",
    "JsonValue",
    "RetryConfig",
]
