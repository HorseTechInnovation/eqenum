# Generated by Django 2.0.8 on 2019-02-15 14:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markupfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries_plus', '0005_auto_20160224_1804'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('languages_plus', '0004_auto_20171214_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='countries_plus.Country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='languages_plus.Language')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('ref', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('notes', markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True)),
                ('notes_markup_type', models.CharField(choices=[('', '--'), ('markdown', 'markdown')], default='markdown', editable=False, max_length=30)),
                ('_notes_rendered', models.TextField(editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date')),
                ('updated', models.DateTimeField(blank=True, db_index=True, editable=False, null=True, verbose_name='Updated Date')),
                ('ref', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=60)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Incomplete'), (1, 'Proposed'), (3, 'Draft'), (6, 'Approved')], default=1)),
                ('ordering', models.CharField(default='0', max_length=10)),
                ('notes', markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True)),
                ('notes_markup_type', models.CharField(choices=[('', '--'), ('markdown', 'markdown')], default='markdown', editable=False, max_length=30)),
                ('_notes_rendered', models.TextField(editable=False, null=True)),
                ('authority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Authority')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='web_enum_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['ordering', 'ref'],
                'verbose_name': 'Enum Item',
            },
        ),
        migrations.CreateModel(
            name='EnumDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date')),
                ('updated', models.DateTimeField(blank=True, db_index=True, editable=False, null=True, verbose_name='Updated Date')),
                ('display', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(blank=True, max_length=10, null=True)),
                ('symbol', models.CharField(blank=True, max_length=10, null=True)),
                ('notes', markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True)),
                ('notes_markup_type', models.CharField(choices=[('', '--'), ('markdown', 'markdown')], default='markdown', editable=False, max_length=30)),
                ('_notes_rendered', models.TextField(editable=False, null=True)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='web_enumdisplay_creator', to=settings.AUTH_USER_MODEL)),
                ('culture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='languages_plus.CultureCode')),
                ('enum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Enum')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='languages_plus.Language')),
                ('updator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='web_enumdisplay_updator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Enum Output/Display',
            },
        ),
        migrations.CreateModel(
            name='EnumType',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Date')),
                ('updated', models.DateTimeField(blank=True, db_index=True, editable=False, null=True, verbose_name='Updated Date')),
                ('ref', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deprecated'), (1, 'Proposed'), (3, 'Draft'), (6, 'Approved')], default=1)),
                ('notes', markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True)),
                ('notes_markup_type', models.CharField(choices=[('', '--'), ('markdown', 'markdown')], default='markdown', editable=False, max_length=30)),
                ('_notes_rendered', models.TextField(editable=False, null=True)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='web_enumtype_creator', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.EnumType')),
                ('updator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='web_enumtype_updator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Enum Grouping',
            },
        ),
        migrations.AddField(
            model_name='enum',
            name='enumtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.EnumType'),
        ),
        migrations.AddField(
            model_name='enum',
            name='updator',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='web_enum_updator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='enum',
            unique_together={('enumtype', 'authority', 'ref')},
        ),
    ]