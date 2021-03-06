from django.db.models.signals import pre_delete,post_delete
from django.dispatch import receiver
import stockapp.models as stkmd

@receiver(post_delete, sender=stkmd.StockGroupIndex, dispatch_uid='stockgroupindex_delete_signal')
def log_deleted_question(sender, instance, using, **kwargs):
	print "Sgnal received to delete Stockmeta data for symbol ",instance.Symbol
	instance.Symbol.delete()
