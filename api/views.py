from django.db.models.functions import Coalesce
from django_tables2 import SingleTableView, LazyPaginator
from django_filters.views import FilterView
from django.db.models import Value, Sum, Q, Max
from api.tables import AccountTable, RootTable, AccountActiveTable, AccountTopTable, OperationTable
from api.models import Account, Operation, Root
from datetime import datetime, timedelta


class AccountGeneralView(SingleTableView, FilterView):
    """
    Main view for account data display
    Allows optional filtering with query args
    """
    model = Account
    table_class = AccountTable
    paginator_class = LazyPaginator
    template_name = 'api/accounts.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 15  # defines default pagesize

    def get_table_pagination(self, table):
        return {'per_page': self.page}

    def get_queryset(self):
        """
        Defines DB query
        Filters the query against params
        """
        queryset = Account.objects.all()
        recent = self.request.GET.get('recent')
        active = self.request.GET.get('active')
        search = self.request.GET.get('search')
        limit = self.request.GET.get('limit')
        top = self.request.GET.get('top')
        put_sum = Sum('operation__amount', filter=Q(operation__type='PUT'))
        wtd_sum = Coalesce(Sum('operation__amount', filter=Q(operation__type='WITHDRAW')), Value(0))
        if recent:
            queryset = queryset.filter(register_date__week=datetime.today().isocalendar()[1])
        if active:
            self.table_class = AccountActiveTable
            queryset = queryset.filter(operation__date__gte=datetime.today() - timedelta(days=3)).\
                annotate(last_operation=Max('operation__date'))
        if limit:
            self.page = int(limit)
        if top:
            self.table_class = AccountTopTable
            queryset = queryset[:100]
            queryset = Account.objects. \
                filter(id__in=queryset). \
                annotate(balance=(put_sum - wtd_sum), last_operation=Max('operation__date'))\
                .order_by('-balance')
            if not limit:
                self.page = 25
        if search:
            queryset = queryset.filter(number__icontains=search)
        return queryset


class OperationGeneralView(SingleTableView, FilterView):
    model = Operation
    table_class = OperationTable
    paginator_class = LazyPaginator
    template_name = 'api/operations.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 15  # defines default pagesize

    def get_table_pagination(self, table):
        return {'per_page': self.page}

    def get_queryset(self):
        """
        Defines DB query
        Filters the query against params
        """
        queryset = Operation.objects.all()
        recent = self.request.GET.get('recent')
        search = self.request.GET.get('search')
        limit = self.request.GET.get('limit')
        if recent:
            queryset = queryset.filter(date__week=datetime.today().isocalendar()[1])
        if search:
            queryset = queryset.filter(account__number__icontains=search)
        if limit:
            self.page = int(limit)
        return queryset


class RootView(SingleTableView, FilterView):
    """
    Displays all views available
    Format - view:path
    """

    model = Root
    table_class = RootTable
    template_name = 'api/root.html'
