# Generated by Django 2.2.3 on 2019-09-17 14:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("youths", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="youthprofile", name="approved_by"),
        migrations.AddField(
            model_name="youthprofile",
            name="approval_notification_timestamp",
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="youthprofile",
            name="approval_token",
            field=models.CharField(
                blank=True, default=uuid.uuid4, editable=False, max_length=36
            ),
        ),
        migrations.AddField(
            model_name="youthprofile",
            name="approver_email",
            field=models.EmailField(default="dummy@example.com", max_length=254),
            preserve_default=False,
        ),
    ]
