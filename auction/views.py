from django.shortcuts import render
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Item, Bid, Question
from .serializers import ItemSerializer, BidSerializer, QuestionSerializer, ReplySerializer

# -------------------------------------------------------------------------
# Custom Permissions
# -------------------------------------------------------------------------

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS requests are read-only so allowed.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

# -------------------------------------------------------------------------
# Item Views (List, Search, Create, Retrieve)
# -------------------------------------------------------------------------

class ItemListCreateView(generics.ListCreateAPIView):
    """
    GET: List all active items. Supports search via ?search=keyword
    POST: Create a new item (Authenticated users only)
    """
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Enable Searching
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        # Only show active items
        return Item.objects.filter(is_active=True).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve specific item details
    PUT/PATCH: Update item (Owner only)
    DELETE: Delete item (Owner only)
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

# -------------------------------------------------------------------------
# Bidding View
# -------------------------------------------------------------------------

class PlaceBidView(generics.CreateAPIView):
    """
    POST: Place a bid on a specific item.
    URL: /api/items/<item_id>/bid/
    """
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        item_id = self.kwargs['item_id']
        item = get_object_or_404(Item, id=item_id)
        
        # 1. Check if auction is active/not expired
        if not item.is_active or item.is_expired():
            raise ValidationError("This auction has ended.")

        # 2. Prevent owner from bidding on their own item
        if item.owner == self.request.user:
            raise ValidationError("You cannot bid on your own item.")

        # 3. Check bid amount logic
        bid_amount = serializer.validated_data['amount']
        
        # Check against starting price
        if bid_amount < item.starting_price:
            raise ValidationError(f"Bid must be at least {item.starting_price}")

        # Check against current highest bid
        highest_bid = item.bids.order_by('-amount').first()
        if highest_bid and bid_amount <= highest_bid.amount:
            raise ValidationError(f"Bid must be higher than current highest bid ({highest_bid.amount})")

        # If all checks pass, save the bid
        serializer.save(bidder=self.request.user, item=item)

# -------------------------------------------------------------------------
# Question & Reply Views
# -------------------------------------------------------------------------

class PostQuestionView(generics.CreateAPIView):
    """
    POST: Ask a question about an item.
    URL: /api/items/<item_id>/question/
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        item = get_object_or_404(Item, id=self.kwargs['item_id'])
        serializer.save(author=self.request.user, item=item)

class ReplyQuestionView(generics.UpdateAPIView):
    """
    PUT/PATCH: Reply to a question (Item owner only).
    URL: /api/questions/<question_id>/reply/
    """
    queryset = Question.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, serializer):
        question = self.get_object()
        # Ensure only the item owner can reply
        if question.item.owner != self.request.user:
            raise PermissionDenied("You do not have permission to reply to this question.")
        
        # Save the reply and automatically set the timestamp
        serializer.save(reply_timestamp=timezone.now())
