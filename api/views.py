from django.db.models.functions import Coalesce
from django_tables2 import SingleTableView, LazyPaginator
from django_filters.views import FilterView
from django.db.models import Value, Sum, Q
from api.tables import *
from datetime import datetime, timedelta


# Create your views here.

class AccountGeneralView(SingleTableView, FilterView):
    model = Account
    table_class = AccountTable
    paginator_class = LazyPaginator
    template_name = 'api/accounts.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 25

    def get_table_pagination(self, table):
        return {'per_page': self.page}

    def get_queryset(self):
        queryset = Account.objects.all()
        recent = self.request.GET.get('recent')
        active = self.request.GET.get('active')
        search = self.request.GET.get('search')
        page = self.request.GET.get('limit')
        print(search)
        if recent:
            queryset = queryset.filter(date__week=datetime.today().isocalendar()[1])
        if active:
            queryset = queryset.filter(date__gte=datetime.today() - timedelta(days=3))
        if page:
            self.page = int(page)
        if search:
            queryset = queryset.filter(Q(number__icontains=search) |
                                       Q(name__icontains=search))
        return queryset


class AccountTopView(SingleTableView, FilterView):
    model = Account
    table_class = AccountTopTable
    template_name = 'api/accounts_top.html'
    table_pagination = False

    def get_queryset(self):
        recent = self.request.GET.get('recent')
        active = self.request.GET.get('active')
        search = self.request.GET.get('search')
        put_sum = Sum('operation__amount', filter=Q(operation__type='PUT'))
        wtd_sum = Coalesce(Sum('operation__amount', filter=Q(operation__type='WITHDRAW')), Value(0))
        queryset = Account.objects.annotate(balance=(put_sum - wtd_sum))
        date = datetime.today() - timedelta(days=3)
        if search:
            queryset = queryset.filter(Q(number__icontains=search) |
                                       Q(name__icontains=search))
        if recent:
            queryset = queryset.filter(date__week=datetime.today().isocalendar()[1])
        if active:
            queryset = queryset.filter(date__gte=date)
        queryset = queryset[:100]
        qs = Account.objects.filter(id__in=queryset).annotate(balance=(put_sum-wtd_sum)).order_by('-balance')
        return qs
