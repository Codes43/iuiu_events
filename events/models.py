from django.db import models
from django.utils import timezone

EVENT_CATEGORIES = [
    ('music', 'Music'),
    ('education', 'Education'),
    ('sports', 'Sports'),
    ('technology', 'Technology'),
    ('conference', 'Conference'),
    ('festival', 'Festival'),
    ('health', 'Health & Wellness'),
    ('other', 'Other'),
]

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    category = models.CharField(
        max_length=50,
        choices=EVENT_CATEGORIES,
        default='music'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_date >= timezone.now()

    def save(self, *args, **kwargs):
        """Automatically soft-delete event once it is finished."""
        now = timezone.now()

        # If event has an end_date
        if self.end_date:
            if self.end_date < now:
                self.is_deleted = True
        else:
            # If only start_date exists
            if self.start_date < now:
                self.is_deleted = True

        super().save(*args, **kwargs)
