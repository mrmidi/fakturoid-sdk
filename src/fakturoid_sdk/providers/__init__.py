"""Raw API providers for Fakturoid resources."""

from .account import AccountProvider
from .bank_accounts import BankAccountsProvider
from .events import EventsProvider
from .expenses import ExpensesProvider
from .generators import GeneratorsProvider
from .inbox_files import InboxFilesProvider
from .inventory_items import InventoryItemsProvider
from .inventory_moves import InventoryMovesProvider
from .invoices import InvoicesProvider
from .number_formats import NumberFormatsProvider
from .recurring_generators import RecurringGeneratorsProvider
from .subjects import SubjectsProvider
from .todos import TodosProvider
from .users import UsersProvider
from .webhooks import WebhooksProvider

__all__ = [
	"AccountProvider",
	"BankAccountsProvider",
	"EventsProvider",
	"ExpensesProvider",
	"GeneratorsProvider",
	"InboxFilesProvider",
	"InventoryItemsProvider",
	"InventoryMovesProvider",
	"InvoicesProvider",
	"NumberFormatsProvider",
	"RecurringGeneratorsProvider",
	"SubjectsProvider",
	"TodosProvider",
	"UsersProvider",
	"WebhooksProvider",
]
