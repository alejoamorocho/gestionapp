# Generated by Django 4.2.9 on 2025-01-22 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='categorias/')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('modelo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('especificaciones_tecnicas', models.TextField()),
                ('numero_serie', models.CharField(max_length=100, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('DISPONIBLE', 'Disponible'), ('VENDIDO', 'Vendido'), ('MANTENIMIENTO', 'En Mantenimiento'), ('RESERVADO', 'Reservado'), ('DESCONTINUADO', 'Descontinuado')], default='DISPONIBLE', max_length=20)),
                ('fecha_fabricacion', models.DateField()),
                ('fecha_adquisicion', models.DateField()),
                ('garantia_meses', models.IntegerField()),
                ('requiere_capacitacion', models.BooleanField(default=False)),
                ('notas', models.TextField(blank=True)),
                ('imagen_principal', models.ImageField(upload_to='equipos/')),
                ('manual_usuario', models.FileField(blank=True, upload_to='manuales/')),
                ('certificaciones', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='equipment.categoria')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='Fabricante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=50)),
                ('sitio_web', models.URLField(blank=True)),
                ('contacto_nombre', models.CharField(blank=True, max_length=100)),
                ('contacto_email', models.EmailField(blank=True, max_length=254)),
                ('contacto_telefono', models.CharField(blank=True, max_length=20)),
                ('notas', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Fabricante',
                'verbose_name_plural': 'Fabricantes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='ImagenEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='equipos/')),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('es_principal', models.BooleanField(default=False)),
                ('orden', models.IntegerField(default=0)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='equipment.equipo')),
            ],
            options={
                'verbose_name': 'Imagen de Equipo',
                'verbose_name_plural': 'Imágenes de Equipos',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='HistorialPrecio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('notas', models.TextField(blank=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_precios', to='equipment.equipo')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historial de Precio',
                'verbose_name_plural': 'Historial de Precios',
                'ordering': ['-fecha'],
            },
        ),
        migrations.AddField(
            model_name='equipo',
            name='fabricante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='equipment.fabricante'),
        ),
        migrations.CreateModel(
            name='DocumentoEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('MANUAL', 'Manual de Usuario'), ('CERTIFICADO', 'Certificado'), ('GARANTIA', 'Garantía'), ('SERVICIO', 'Historial de Servicio'), ('OTRO', 'Otro')], max_length=20)),
                ('titulo', models.CharField(max_length=200)),
                ('archivo', models.FileField(upload_to='documentos/')),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='equipment.equipo')),
            ],
            options={
                'verbose_name': 'Documento de Equipo',
                'verbose_name_plural': 'Documentos de Equipos',
                'ordering': ['-fecha_subida'],
            },
        ),
    ]
