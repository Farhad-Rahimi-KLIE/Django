# customers/views.py
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Customer, Account
from .forms import CustomerForm, AccountForm
from django_filters import FilterSet, DateFilter, DateRangeFilter, NumberFilter
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

class CustomerFilter(FilterSet):
    date = DateFilter(field_name='accounts__date', lookup_expr='exact', label='Single Day')
    date_range = DateRangeFilter(field_name='accounts__date', label='Date Range')
    data_used = NumberFilter(field_name='accounts__data_used', lookup_expr='gte', label='Min Data Used (GB)')
    
    class Meta:
        model = Customer
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['date_range'].extra['choices'] = [
    ('today', 'Today'),
    ('yesterday', 'Yesterday'),
    ('this_month', 'This Month'),
    ('last_month', 'Last Month'),
]


    def date_range_filter(self, queryset, name, value):
        today = timezone.now().date()
        if value == 'today':
            return queryset.filter(accounts__date__date=today)
        elif value == 'yesterday':
            yesterday = today - timedelta(days=1)
            return queryset.filter(accounts__date__date=yesterday)
        elif value == 'this_month':
            return queryset.filter(accounts__date__month=today.month, accounts__date__year=today.year)
        elif value == 'last_month':
            last_month = today - timedelta(days=30)
            return queryset.filter(accounts__date__month=last_month.month, accounts__date__year=last_month.year)
        return queryset

class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CustomerFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_form.html'
    success_url = reverse_lazy('customers:customer_list')

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer_detail.html'
    context_object_name = 'customer'

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'account_form.html'

    def form_valid(self, form):
        form.instance.customer_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.kwargs['pk']})