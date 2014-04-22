# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('relations_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.TextField')()),
            ('primary_team', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.SET_NULL, blank=True, null=True, to=orm['relations.Team'])),
        ))
        db.send_create_signal('relations', ['UserProfile'])

        # Adding model 'UserProfileRecordType'
        db.create_table('relations_userprofilerecordtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('relations', ['UserProfileRecordType'])

        # Adding model 'UserProfileRecordTypeName'
        db.create_table('relations_userprofilerecordtypename', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.UserProfileRecordType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('relations', ['UserProfileRecordTypeName'])

        # Adding model 'UserProfileRecord'
        db.create_table('relations_userprofilerecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.UserProfileRecordType'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('relations', ['UserProfileRecord'])

        # Adding model 'Team'
        db.create_table('relations_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ShareTree'])),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('relations', ['Team'])

        # Adding M2M table for field members on 'Team'
        m2m_table_name = db.shorten_name('relations_team_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm['relations.team'], null=False)),
            ('userprofile', models.ForeignKey(orm['relations.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['team_id', 'userprofile_id'])

        # Adding model 'Contact'
        db.create_table('relations_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('about', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.UserProfile'])),
        ))
        db.send_create_signal('relations', ['Contact'])

        # Adding model 'UserContact'
        db.create_table('relations_usercontact', (
            ('contact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['relations.Contact'], primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='known_people')),
        ))
        db.send_create_signal('relations', ['UserContact'])

        # Adding model 'TeamContact'
        db.create_table('relations_teamcontact', (
            ('contact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['relations.Contact'], primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.Team'])),
        ))
        db.send_create_signal('relations', ['TeamContact'])

        # Adding model 'KnownTeam'
        db.create_table('relations_knownteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('about', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.Team'])),
        ))
        db.send_create_signal('relations', ['KnownTeam'])

        # Adding model 'ContactRecord'
        db.create_table('relations_contactrecord', (
            ('userprofilerecord_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['relations.UserProfileRecord'], primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.Contact'])),
            ('is_encrypted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('relations', ['ContactRecord'])

        # Adding model 'OwnRecord'
        db.create_table('relations_ownrecord', (
            ('userprofilerecord_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['relations.UserProfileRecord'], primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User'], related_name='own_records')),
            ('shared_between', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('relations', ['OwnRecord'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('relations_userprofile')

        # Deleting model 'UserProfileRecordType'
        db.delete_table('relations_userprofilerecordtype')

        # Deleting model 'UserProfileRecordTypeName'
        db.delete_table('relations_userprofilerecordtypename')

        # Deleting model 'UserProfileRecord'
        db.delete_table('relations_userprofilerecord')

        # Deleting model 'Team'
        db.delete_table('relations_team')

        # Removing M2M table for field members on 'Team'
        db.delete_table(db.shorten_name('relations_team_members'))

        # Deleting model 'Contact'
        db.delete_table('relations_contact')

        # Deleting model 'UserContact'
        db.delete_table('relations_usercontact')

        # Deleting model 'TeamContact'
        db.delete_table('relations_teamcontact')

        # Deleting model 'KnownTeam'
        db.delete_table('relations_knownteam')

        # Deleting model 'ContactRecord'
        db.delete_table('relations_contactrecord')

        # Deleting model 'OwnRecord'
        db.delete_table('relations_ownrecord')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['core.ShareTree']"}),
            'shared_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'shared_to'"})
        },
        'relations.contact': {
            'Meta': {'object_name': 'Contact'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'relations.contactrecord': {
            'Meta': {'_ormbases': ['relations.UserProfileRecord'], 'object_name': 'ContactRecord'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Contact']"}),
            'is_encrypted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'userprofilerecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['relations.UserProfileRecord']", 'primary_key': 'True'})
        },
        'relations.knownteam': {
            'Meta': {'object_name': 'KnownTeam'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relations.ownrecord': {
            'Meta': {'_ormbases': ['relations.UserProfileRecord'], 'object_name': 'OwnRecord'},
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['auth.User']", 'related_name': "'own_records'"}),
            'shared_between': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'userprofilerecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['relations.UserProfileRecord']", 'primary_key': 'True'})
        },
        'relations.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['relations.UserProfile']", 'related_name': "'teams'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.teamcontact': {
            'Meta': {'_ormbases': ['relations.Contact'], 'object_name': 'TeamContact'},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['relations.Contact']", 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"})
        },
        'relations.usercontact': {
            'Meta': {'_ormbases': ['relations.Contact'], 'object_name': 'UserContact'},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['relations.Contact']", 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'known_people'"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'blank': 'True', 'null': 'True', 'to': "orm['relations.Team']"}),
            'status': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'relations.userprofilerecord': {
            'Meta': {'object_name': 'UserProfileRecord'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.UserProfileRecordType']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'relations.userprofilerecordtype': {
            'Meta': {'object_name': 'UserProfileRecordType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'relations.userprofilerecordtypename': {
            'Meta': {'object_name': 'UserProfileRecordTypeName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.UserProfileRecordType']"})
        }
    }

    complete_apps = ['relations']