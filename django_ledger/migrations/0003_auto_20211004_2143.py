# pylint: skip-file
# Generated by Django 3.2.7 on 2021-10-05 01:43

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_ledger', '0002_auto_20210911_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemthroughmodel',
            name='po_quantity',
            field=models.FloatField(default=0.0, help_text='Authorized item quantity for purchasing.',
                                    validators=[django.core.validators.MinValueValidator(0)],
                                    verbose_name='PO Quantity'),
        ),
        migrations.AddField(
            model_name='itemthroughmodel',
            name='po_total_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'),
                                      help_text='Maximum authorized cost per Purchase Order.', max_digits=20,
                                      validators=[django.core.validators.MinValueValidator(0)],
                                      verbose_name='Authorized maximum item cost per Purchase Order'),
        ),
        migrations.AddField(
            model_name='itemthroughmodel',
            name='po_unit_cost',
            field=models.FloatField(default=0.0, help_text='Purchase Order unit cost.',
                                    validators=[django.core.validators.MinValueValidator(0)],
                                    verbose_name='PO Unit Cost'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='inventory_received',
            field=models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=20,
                                      verbose_name='Total inventory received.'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='inventory_received_value',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20,
                                      verbose_name='Total value of inventory received.'),
        ),
    ]
