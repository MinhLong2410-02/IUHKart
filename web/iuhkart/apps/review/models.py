from django.db import models
from django.utils import timezone
# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, related_name='reviews'
    )
    customer = models.ForeignKey(
        'account.Customer', on_delete=models.CASCADE, related_name='customer_review'
    )
    review_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_date = models.DateField(default=timezone.now)
    review_content = models.TextField()
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['product', 'customer']
        verbose_name_plural = 'Reviews'
        ordering = ['review_date']