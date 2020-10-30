import itertools

import django_tables2 as tables
from api.models import Account, Root, Operation


class AccountTable(tables.Table):
    """Table class for account display"""

    class Meta:
        model = Account
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'number', 'name', 'register_date',)


class AccountActiveTable(AccountTable):
    """Displays active accounts"""
    last_operation = tables.Column()

    def order_balance(self, queryset, is_descending):
        queryset = queryset.order_by(("-" if is_descending else "") + "balance")
        return (queryset, True)

    def order_last_operation(self, queryset, is_descending):
        queryset = queryset.order_by(("-" if is_descending else "") + "last_operation")
        return (queryset, True)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'


class AccountTopTable(AccountActiveTable):
    """Displays top accounts"""
    balance = tables.Column()

    def order_balance(self, queryset, is_descending):
        queryset = queryset.order_by(("-" if is_descending else "") + "balance")
        return (queryset, True)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'


class OperationTable(tables.Table):
    account_number = tables.Column(verbose_name='Acc_number', accessor='account__number')
    class Meta:
        model = Operation
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['id', 'amount', 'type', 'date',  'account_number',]


class RootTable(tables.Table):
    """
    Lists all available views in a table
    """

    class Meta:
        model = Root
        template_name = 'django_tables2/bootstrap4.html'
        exclude = ['id']