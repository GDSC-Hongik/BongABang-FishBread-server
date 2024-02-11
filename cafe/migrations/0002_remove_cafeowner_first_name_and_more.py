from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafeowner',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='cafeowner',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='cafeowner',
            name='username',
        ),
        migrations.AddField(
            model_name='cafeowner',
            name='cafe_image',
            field=models.ImageField(default='default_image.jpg', upload_to='menu_images'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('price_ice', models.IntegerField()),
                ('price_hot', models.IntegerField()),
                ('price_constant', models.IntegerField()),
                ('menu_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='menu_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.cafeowner')),
            ],
        ),
    ]
