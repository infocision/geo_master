from report import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('login/', views.product_view, name='login'),
    path('index/', views.index, name='index'),
    path('index/primary_sales/', views.primary_sales, name='primary_sales'),
    path('index/primary_sales/prm/', views.prm, name='prm'),
    path('index/primary_sales/spm/', views.spm, name='spm'),
    path('index/primary_sales/cup/', views.cup, name='cup'),
    path('index/primary_sales/cvp/', views.cvp, name='cvp'),
    path('index/primary_sales/msgu/', views.msgu, name='msgu'),
    path('index/primary_sales/msgv/', views.msgv, name='msgv'),
    path('index/primary_sales/dsu/', views.dsu, name='dsu'),
    path('index/primary_sales/dsv/', views.dsv, name='dsv'),
]


# urlpatterns = patterns('',
#     # ... the rest of your URLconf goes here ...
# ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)