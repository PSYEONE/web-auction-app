from rest_framework import serializers
from .models import Item, Bid, Question
from django.contrib.auth import get_user_model

# Get the User model dynamically (from your 'api' folder)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Used to nest user info inside Items/Bids so we see names, not just IDs"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_image']

class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)  # Read-only: server sets this based on who is logged in

    class Meta:
        model = Bid
        fields = ['id', 'item', 'bidder', 'amount', 'timestamp']
        read_only_fields = ['item', 'timestamp']

    def validate_amount(self, value):
        """Check that the bid is higher than the starting price and current highest bid."""
        # Note: We need the context to access the specific item being bid on
        # We will pass the item in the View later, or access it via self.instance if updating
        # For simple creation validation, we usually do this in the View or 'validate' method below.
        return value

class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'item', 'author', 'question_text', 'timestamp', 'reply_text', 'reply_timestamp']
        read_only_fields = ['item', 'author', 'timestamp', 'reply_timestamp']

class ReplySerializer(serializers.ModelSerializer):
    """Serializer for the owner to update the reply_text"""
    class Meta:
        model = Question
        fields = ['reply_text']

class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True) 
    # Nesting serializers: When we fetch an item, we want to see the list of bids and questions too
    bids = BidSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    
    # Custom field to get the highest bid currently
    highest_bid = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'owner', 'title', 'description', 'starting_price', 
            'image', 'end_date', 'is_active', 'bids', 'questions', 'highest_bid'
        ]
        read_only_fields = ['owner', 'is_active']

    def get_highest_bid(self, obj):
        # Efficiently get the highest bid amount
        highest = obj.bids.order_by('-amount').first()

        return highest.amount if highest else None
