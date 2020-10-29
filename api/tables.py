import itertools

import django_tables2 as tables
from api.models import Account


class AccountTable(tables.Table):
    class Meta:
        model = Account
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('id', 'number', 'name', 'date')


class AccountTopTable(AccountTable):
    place = tables.Column(empty_values=(), orderable=False)
    balance = tables.Column()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = itertools.count(start=1)

    def order_balance(self, queryset, is_descending):
        queryset = queryset.order_by(("-" if is_descending else "") + "balance")
        return (queryset, True)


    def render_place(self):
        return "%d" % next(self.counter)

    def value_place(self):
        return "%d" % next(self.counter)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['place']