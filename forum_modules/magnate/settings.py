from forum.settings.base import Setting, SettingSet
from django.forms.widgets import Textarea
from django.core.urlresolvers import reverse
from forum.settings import APP_URL


MAGNATE_FUNDS = SettingSet('MAGNATE_FUNDS', 'Magnate Funds', "Setttings for Magnate Funds", 3000)
MAGNATE_LOBBIES = SettingSet('MAGNATE_LOBBY', 'Magnate Lobbies', "Settings for Magnate Lobbies", 3000)

MAGNATE_FUND_TEMPLATES={}
MAGNATE_LOBBY_TEMPLATES={}

# In case the table for MagnateFund has not been created yet...
from django.db.utils import ProgrammingError, OperationalError

from donations.models import MagnateFund
try:
	for fund in MagnateFund.objects.all():
		FUND_METRICS_TEMPLATE = Setting('FUND_%d_METRICS_TEMPLATE' % (fund.pk),
		"""        <div class="fund_metrics-container">
        <div class="metrics-contentinner">
			<div class="metric">
			<article>
			<div class="metric-text">
			<p>Number of new Investments</p>
			</div>
			<div class="metric-amount1 metric-resize">17</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-amount2 metric-resize">$62,205</div>
			<div class="metric-text2">
			<p>New Asset Inflows</p>
			</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-amount2 metric-resize">$32,603</div>
			<div class="metric-text2">
			<p>Number of Participants</p>
			</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-text">
			<p>Number of new Investments</p>
			</div>
			<div class="metric-amount1 no_change metric-resize">00</div>
			</article>       
			</div>
		</div>	
			<div class="fundbtn"><a href="#" class="btn disabled" id="dashbtn_fix">Detailed View</a></div>	
        </div>

	""", MAGNATE_FUNDS, dict(
	label = "Template for statistics for %s" % (fund.name),
	help_text = """
	Template for statistics for %s 
	""" % (fund.name),
	widget=Textarea(attrs={'rows': '20'})))
		MAGNATE_FUND_TEMPLATES[fund.pk] = FUND_METRICS_TEMPLATE
except (ProgrammingError, OperationalError) as e:
	pass


from zinnia.models import Category
try:
	for category in Category.objects.all():
		LOBBY_METRICS_TEMPLATE = Setting('LOBBY_%d_METRICS_TEMPLATE' % (category.pk),
		"""        <div class="fund_metrics-container">
        <div class="metrics-contentinner">
			<div class="metric">
			<article>
			<div class="metric-text">
			<p>Number of new Investments</p>
			</div>
			<div class="metric-amount1 dollar">17</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-amount2 dollar">$62,205</div>
			<div class="metric-text2">
			<p>New Asset Inflows</p>
			</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-amount2 dollar">$32,603</div>
			<div class="metric-text2">
			<p>Number of Participants</p>
			</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-text">
			<p>Number of new Investments</p>
			</div>
			<div class="metric-amount1 dollar">00</div>
			</article>       
			</div>
		</div>	
			<div class="fundbtn"><a href="#" class="btn disabled" id="dashbtn_fix">Detailed View</a></div>	
        </div>

	""", MAGNATE_LOBBIES, dict(
	label = "Template for statistics for %s" % (category.title),
	help_text = """
	Template for statistics for %s 
	""" % (category.title),
	widget=Textarea(attrs={'rows': '20'})))
		MAGNATE_LOBBY_TEMPLATES[category.pk] = LOBBY_METRICS_TEMPLATE
except (ProgrammingError, OperationalError) as e:
	pass




