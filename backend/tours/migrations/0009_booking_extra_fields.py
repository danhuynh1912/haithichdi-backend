from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0008_location_quotation_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="medal_name",
            field=models.CharField(
                max_length=200,
                null=True,
                blank=True,
                help_text="Tên in trên huy chương",
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="dob",
            field=models.DateField(
                null=True, blank=True, help_text="Ngày tháng năm sinh"
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="citizen_id",
            field=models.CharField(
                max_length=50,
                null=True,
                blank=True,
                help_text="Căn cước công dân",
            ),
        ),
    ]
