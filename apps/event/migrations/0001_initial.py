# Generated by Django 5.0.2 on 2024-03-07 14:17

import apps.event.models.event
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('semester', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('points', models.IntegerField(verbose_name='Puntos')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado el')),
            ],
            options={
                'verbose_name': 'Tipo Evento',
                'verbose_name_plural': 'Tipos de Eventos',
                'db_table': 'sumate_tipo_evento',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.event.models.event.event_image_file_path, verbose_name='Imagen')),
                ('start', models.DateTimeField(verbose_name='Fecha Inicio')),
                ('end', models.DateTimeField(verbose_name='Fecha Término')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('status', models.CharField(choices=[('enabled', 'Habilitado'), ('finished', 'Finalizado')], default='enabled', max_length=10, verbose_name='Estado')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester', to='semester.semester', verbose_name='Semestre')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_type', to='event.eventtype', verbose_name='Tipo Evento')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'db_table': 'sumate_evento',
            },
        ),
    ]