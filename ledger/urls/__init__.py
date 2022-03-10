

from django.urls import path, include

from ledger import views

app_name = 'ledger'

urlpatterns = [

    path('entity/', include('ledger.urls.entity')),
    path('unit/', include('ledger.urls.unit')),
    path('report/', include('ledger.urls.report')),
    path('chart-of-accounts/', include('ledger.urls.chart_of_accounts')),
    path('account/', include('ledger.urls.account')),
    path('ledger/', include('ledger.urls.ledger')),
    path('journal-entry/', include('ledger.urls.journal_entry')),
    path('transactions/', include('ledger.urls.transactions')),
    path('invoice/', include('ledger.urls.invoice')),
    path('bill/', include('ledger.urls.bill')),
    path('purchase_order/', include('ledger.urls.purchase_order')),
    path('customer/', include('ledger.urls.customer')),
    path('vendor/', include('ledger.urls.vendor')),
    path('item/', include('ledger.urls.item')),
    path('bank-account/', include('ledger.urls.bank_account')),
    path('data-import/', include('ledger.urls.data_import')),
    path('auth/', include('ledger.urls.auth')),
    path('feedback/', include('ledger.urls.feedback')),
    path('inventory/', include('ledger.urls.inventory')),
    path('home/', include('ledger.urls.home')),
    path('djl-api/v1/', include('ledger.urls.djl_api')),
    path('', views.RootUrlView.as_view(), name='root'),
]
