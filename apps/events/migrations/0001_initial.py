# Generated by Django 4.2.9 on 2025-01-22 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0002_equipo_capacitacion_realizada_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('REGISTRADO', 'Registrado'), ('CONFIRMADO', 'Confirmado'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado'), ('NO_ASISTIO', 'No Asistió')], default='REGISTRADO', max_length=20)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_confirmacion', models.DateTimeField(blank=True, null=True)),
                ('asistio', models.BooleanField(default=False)),
                ('calificacion', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('comentarios', models.TextField(blank=True)),
                ('certificado_emitido', models.BooleanField(default=False)),
                ('fecha_certificado', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Asistente',
                'verbose_name_plural': 'Asistentes',
                'ordering': ['evento', 'fecha_registro'],
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('tipo', models.CharField(choices=[('CAPACITACION', 'Capacitación Técnica'), ('DEMOSTRACION', 'Demostración de Equipo'), ('CERTIFICACION', 'Certificación'), ('SEMINARIO', 'Seminario'), ('OTRO', 'Otro')], max_length=20)),
                ('descripcion', models.TextField()),
                ('modalidad', models.CharField(choices=[('PRESENCIAL', 'Presencial'), ('VIRTUAL', 'Virtual'), ('HIBRIDO', 'Híbrido')], max_length=20)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('ubicacion', models.CharField(blank=True, max_length=200)),
                ('link_virtual', models.URLField(blank=True)),
                ('capacidad_maxima', models.IntegerField()),
                ('requisitos', models.TextField(blank=True)),
                ('materiales', models.TextField(blank=True)),
                ('costo', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('activo', models.BooleanField(default=True)),
                ('notas', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('equipos', models.ManyToManyField(blank=True, related_name='eventos', to='equipment.equipo')),
                ('instructor', models.ForeignKey(limit_choices_to={'tipo': 'TECNICO'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eventos_como_instructor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='MaterialEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('archivo', models.FileField(upload_to='eventos/materiales/')),
                ('publico', models.BooleanField(default=False, help_text='Si es público, estará disponible antes del evento')),
                ('orden', models.IntegerField(default=0)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiales_adjuntos', to='events.evento')),
            ],
            options={
                'verbose_name': 'Material de Evento',
                'verbose_name_plural': 'Materiales de Eventos',
                'ordering': ['evento', 'orden', 'titulo'],
            },
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_evaluacion', models.DateTimeField(auto_now_add=True)),
                ('calificacion_teorica', models.DecimalField(decimal_places=2, max_digits=5)),
                ('calificacion_practica', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('observaciones', models.TextField(blank=True)),
                ('aprobado', models.BooleanField(default=False)),
                ('asistente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='evaluacion', to='events.asistente')),
                ('evaluador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluaciones_realizadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evaluación',
                'verbose_name_plural': 'Evaluaciones',
                'ordering': ['-fecha_evaluacion'],
            },
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_certificado', models.CharField(max_length=100, unique=True)),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
                ('archivo', models.FileField(upload_to='eventos/certificados/')),
                ('notas', models.TextField(blank=True)),
                ('asistente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='certificado', to='events.asistente')),
                ('firmado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='certificados_firmados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Certificado',
                'verbose_name_plural': 'Certificados',
                'ordering': ['-fecha_emision'],
            },
        ),
        migrations.AddField(
            model_name='asistente',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistentes', to='events.evento'),
        ),
        migrations.AddField(
            model_name='asistente',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_registrados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='asistente',
            unique_together={('evento', 'usuario')},
        ),
    ]
