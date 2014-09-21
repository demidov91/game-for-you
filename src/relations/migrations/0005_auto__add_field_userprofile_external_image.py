# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.external_image'
        db.add_column('relations_userprofile', 'external_image',
                      self.gf('django.db.models.fields.URLField')(blank=True, null=True, max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.external_image'
        db.delete_column('relations_userprofile', 'external_image')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['core.ShareTree']"}),
            'shared_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shared_to'", 'to': "orm['auth.User']"})
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
            'userprofilerecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['relations.UserProfileRecord']"})
        },
        'relations.knownteam': {
            'Meta': {'object_name': 'KnownTeam'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relations.ownrecord': {
            'Meta': {'_ormbases': ['relations.UserProfileRecord'], 'object_name': 'OwnRecord'},
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'own_records'", 'null': 'True', 'to': "orm['auth.User']"}),
            'shared_between': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'userprofilerecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['relations.UserProfileRecord']"})
        },
        'relations.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'symmetrical': 'False', 'to': "orm['relations.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.teamcontact': {
            'Meta': {'_ormbases': ['relations.Contact'], 'object_name': 'TeamContact'},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['relations.Contact']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"})
        },
        'relations.usercontact': {
            'Meta': {'_ormbases': ['relations.Contact'], 'object_name': 'UserContact'},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['relations.Contact']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'known_people'", 'to': "orm['auth.User']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'external_image': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '255', 'default': "'/media/upload/user_picks/owl.jpg'"}),
            'patronymic': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['relations.Team']"}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'unique': 'True', 'to': "orm['auth.User']"})
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