# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuthorizeAIMResponse'
        db.create_table(u'billing_authorizeaimresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response_code', self.gf('django.db.models.fields.IntegerField')()),
            ('response_reason_code', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('response_reason_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('authorization_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('address_verification_response', self.gf('django.db.models.fields.CharField')(max_length='8')),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('customer_id', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('shipping_first_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_last_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_company', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_address', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_city', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_state', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_zip_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('shipping_country', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('card_code_response', self.gf('django.db.models.fields.CharField')(max_length='8')),
        ))
        db.send_create_signal('billing', ['AuthorizeAIMResponse'])

        # Adding model 'GCNewOrderNotification'
        db.create_table(u'billing_gcnewordernotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notify_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('google_order_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('buyer_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('private_data', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_contact_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_address1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_country_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('shipping_company_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_fax', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shipping_phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_contact_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_address1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_region', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_country_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('billing_company_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_fax', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('billing_phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('marketing_email_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_cart_items', self.gf('django.db.models.fields.IntegerField')()),
            ('cart_items', self.gf('django.db.models.fields.TextField')()),
            ('total_tax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('total_tax_currency', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('adjustment_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('adjustment_total_currency', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('order_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=2, blank=True)),
            ('order_total_currency', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('financial_order_state', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('fulfillment_order_state', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('billing', ['GCNewOrderNotification'])

        # Adding model 'WorldPayResponse'
        db.create_table(u'billing_worldpayresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('installation_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cart_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('amount_string', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('auth_mode', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('test_mode', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('transaction_status', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('transaction_time', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('auth_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('auth_currency', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('auth_amount_string', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('raw_auth_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('raw_auth_code', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('future_pay_id', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('card_type', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('billing', ['WorldPayResponse'])

        # Adding model 'AmazonFPSResponse'
        db.create_table(u'billing_amazonfpsresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyerEmail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('buyerName', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('callerReference', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('notificationType', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('paymentMethod', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('recipientEmail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('recipientName', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('statusCode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('statusMessage', self.gf('django.db.models.fields.TextField')()),
            ('transactionAmount', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('transactionDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('transactionId', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('transactionStatus', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('customerEmail', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('customerName', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('addressFullName', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('addressLine1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('addressLine2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('addressState', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('addressZip', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('addressCountry', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('addressPhone', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('billing', ['AmazonFPSResponse'])

        # Adding model 'PaylaneTransaction'
        db.create_table(u'billing_paylanetransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('customer_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('customer_email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error_code', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('error_description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('acquirer_error', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('acquirer_description', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('billing', ['PaylaneTransaction'])

        # Adding model 'PaylaneAuthorization'
        db.create_table(u'billing_paylaneauthorization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sale_authorization_id', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('first_authorization', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transaction', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['billing.PaylaneTransaction'], unique=True)),
        ))
        db.send_create_signal('billing', ['PaylaneAuthorization'])

        # Adding model 'PinCard'
        db.create_table(u'billing_pincard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('display_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('expiry_month', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('expiry_year', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('scheme', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address_city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_postcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address_state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pin_cards', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('billing', ['PinCard'])

        # Adding model 'PinCustomer'
        db.create_table(u'billing_pincustomer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customers', to=orm['billing.PinCard'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='pin_customer', unique=True, null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('billing', ['PinCustomer'])

        # Adding model 'PinCharge'
        db.create_table(u'billing_pincharge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='charges', to=orm['billing.PinCard'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='customers', null=True, to=orm['billing.PinCustomer'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('status_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pin_charges', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('billing', ['PinCharge'])

        # Adding model 'PinRefund'
        db.create_table(u'billing_pinrefund', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='refunds', to=orm['billing.PinCharge'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('status_message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pin_refunds', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('billing', ['PinRefund'])


    def backwards(self, orm):
        # Deleting model 'AuthorizeAIMResponse'
        db.delete_table(u'billing_authorizeaimresponse')

        # Deleting model 'GCNewOrderNotification'
        db.delete_table(u'billing_gcnewordernotification')

        # Deleting model 'WorldPayResponse'
        db.delete_table(u'billing_worldpayresponse')

        # Deleting model 'AmazonFPSResponse'
        db.delete_table(u'billing_amazonfpsresponse')

        # Deleting model 'PaylaneTransaction'
        db.delete_table(u'billing_paylanetransaction')

        # Deleting model 'PaylaneAuthorization'
        db.delete_table(u'billing_paylaneauthorization')

        # Deleting model 'PinCard'
        db.delete_table(u'billing_pincard')

        # Deleting model 'PinCustomer'
        db.delete_table(u'billing_pincustomer')

        # Deleting model 'PinCharge'
        db.delete_table(u'billing_pincharge')

        # Deleting model 'PinRefund'
        db.delete_table(u'billing_pinrefund')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'billing.amazonfpsresponse': {
            'Meta': {'object_name': 'AmazonFPSResponse'},
            'addressCountry': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'addressFullName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'addressLine1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'addressLine2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'addressPhone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'addressState': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'addressZip': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'buyerEmail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'buyerName': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'callerReference': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'customerEmail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'customerName': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notificationType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'paymentMethod': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'recipientEmail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'recipientName': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'statusCode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'statusMessage': ('django.db.models.fields.TextField', [], {}),
            'transactionAmount': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transactionDate': ('django.db.models.fields.DateTimeField', [], {}),
            'transactionId': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'transactionStatus': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'billing.authorizeaimresponse': {
            'Meta': {'object_name': 'AuthorizeAIMResponse'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'address_verification_response': ('django.db.models.fields.CharField', [], {'max_length': "'8'"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'authorization_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'card_code_response': ('django.db.models.fields.CharField', [], {'max_length': "'8'"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {}),
            'response_reason_code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'response_reason_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_company': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_state': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'shipping_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'billing.gcnewordernotification': {
            'Meta': {'object_name': 'GCNewOrderNotification'},
            'adjustment_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'adjustment_total_currency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_country_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'billing_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'billing_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'buyer_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cart_items': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'financial_order_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fulfillment_order_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'google_order_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marketing_email_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notify_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'num_cart_items': ('django.db.models.fields.IntegerField', [], {}),
            'order_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'order_total_currency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'private_data': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shipping_address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_country_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'shipping_fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shipping_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'total_tax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'total_tax_currency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'billing.paylaneauthorization': {
            'Meta': {'object_name': 'PaylaneAuthorization'},
            'first_authorization': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sale_authorization_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'}),
            'transaction': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['billing.PaylaneTransaction']", 'unique': 'True'})
        },
        'billing.paylanetransaction': {
            'Meta': {'object_name': 'PaylaneTransaction'},
            'acquirer_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'acquirer_error': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'customer_email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'error_code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'error_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'billing.pincard': {
            'Meta': {'object_name': 'PinCard'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_postcode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'address_state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'expiry_month': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'expiry_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pin_cards'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        'billing.pincharge': {
            'Meta': {'object_name': 'PinCharge'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'charges'", 'to': "orm['billing.PinCard']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'customers'", 'null': 'True', 'to': "orm['billing.PinCustomer']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'status_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pin_charges'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        'billing.pincustomer': {
            'Meta': {'object_name': 'PinCustomer'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customers'", 'to': "orm['billing.PinCard']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'pin_customer'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        },
        'billing.pinrefund': {
            'Meta': {'object_name': 'PinRefund'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'refunds'", 'to': "orm['billing.PinCharge']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pin_refunds'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        'billing.worldpayresponse': {
            'Meta': {'object_name': 'WorldPayResponse'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'amount_string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'auth_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '2'}),
            'auth_amount_string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'auth_currency': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'auth_mode': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'cart_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'future_pay_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installation_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'raw_auth_code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'raw_auth_message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'test_mode': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_status': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'transaction_time': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['billing']