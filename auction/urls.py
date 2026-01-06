from django.urls import path
from .views import (
    ItemListCreateView, 
    ItemDetailView, 
    PlaceBidView, 
    PostQuestionView
)

urlpatterns = [
    # List all items & Create new item
    path('items/', ItemListCreateView.as_view(), name='item-list'),
    
    # Get details, update, or delete a specific item
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    
    # Place a bid on a specific item
    path('items/<int:item_id>/bid/', PlaceBidView.as_view(), name='place-bid'),
    
    # Ask a question
    path('items/<int:item_id>/question/', PostQuestionView.as_view(), name='post-question'),
]