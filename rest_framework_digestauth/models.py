
from django.db import models


class DigestAuthCounter(models.Model):
    server_nonce = models.CharField(max_length=255)
    client_nonce = models.CharField(max_length=255)
    client_counter = models.IntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('server_nonce', 'client_nonce')
