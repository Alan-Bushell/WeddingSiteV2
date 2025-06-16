# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User model to extend Django's default AbstractUser.
    This allows adding custom fields to the user profile without needing a separate profile model.
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True,
                                    help_text="Optional: Your phone number.")

    # Add unique related_name arguments to avoid clashes with auth.User's default related_names.
    # This is necessary when extending AbstractUser if you ever reference these relations directly.
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=("groups"),
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="customuser_groups", # Custom related_name for groups
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=("user permissions"),
        blank=True,
        help_text=("Specific permissions for this user."),
        related_name="customuser_user_permissions", # Custom related_name for user_permissions
        related_query_name="customuser",
    )

    def __str__(self):
        """
        Returns the username as the string representation of the user.
        """
        return self.username

    class Meta:
        """
        Meta options for the CustomUser model.
        """
        verbose_name = "User"
        verbose_name_plural = "Users"