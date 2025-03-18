from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ['id', 'user', 'created', 'updated']

    def validate_category(self, category):
        """
        Validate that the category belongs to the current user.
        """
        if category and category.user != self.context['request'].user:
            raise ValidationError("You can only use your own categories.")
        return category

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)