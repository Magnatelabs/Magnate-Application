from forum.settings.base import Setting, SettingSet
from django.forms.widgets import Textarea
from django.core.urlresolvers import reverse
from forum.settings import APP_URL


MAGNATE_FUNDS = SettingSet('MAGNATE_FUNDS', 'Magnate Funds', "Setttings for Magnate Funds", 3000)

MAGNATE_FUND_TEMPLATES={}

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
			<div class="metric-amount1">
			<p>17</p>			
			</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-amount2">
			<p>$62,205</p>	
			</div>
			<div class="metric-text2">
			<p>New Asset Inflows</p>
			</div>
			</article>       
			</div>
			
			<div class="metric">
			<article>
			<div class="metric-amount2">
			<p>$32,603</p>	
			</div>
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
			<div class="metric-amount1 no_change">
			<p>00</p>			
			</div>
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
