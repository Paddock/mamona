from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from mamona import signals

def return_urls_query_listener(sender, urls, **kwargs):
	url = 'http://%s%s' % (
			Site.objects.get_current().domain,
			reverse('cashier-show-order', kwargs={'order_id': sender.order.id})
			)
	urls.update({'success': url, 'failure': url})

def order_items_query_listener(sender, items, **kwargs):
	items.append({'name': sender.order.name})

def payment_status_changed_listener(sender, old_status, new_status, **kwargs):
	if new_status == 'paid':
		sender.order.status = 's'
		sender.order.save()
	elif new_status == 'failed':
		sender.order.status = 'f'
		sender.order.save()

signals.return_urls_query.connect(return_urls_query_listener)
signals.order_items_query.connect(order_items_query_listener)
signals.payment_status_changed.connect(payment_status_changed_listener)
