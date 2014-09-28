# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for team in orm.Team.objects.all():
            team.chat = orm['chat.Chat'].objects.create()
            team.save()

    def backwards(self, orm):
        for team in orm.Team.objects.all():
            team.chat.delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'chat.chat': {
            'Meta': {'object_name': 'Chat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'chat.message': {
            'Meta': {'object_name': 'Message', 'ordering': "('create_time',)"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'default': 'datetime.datetime(2014, 9, 28, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']", 'null': 'True', 'blank': 'True'}),
            'shared_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'shared_to'"})
        },
        'relations.contact': {
            'Meta': {'object_name': 'Contact'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'relations.contactrecord': {
            'Meta': {'object_name': 'ContactRecord', '_ormbases': ['relations.UserProfileRecord']},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Contact']"}),
            'is_encrypted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'userprofilerecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['relations.UserProfileRecord']", 'primary_key': 'True', 'unique': 'True'})
        },
        'relations.knownteam': {
            'Meta': {'object_name': 'KnownTeam'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relations.ownrecord': {
            'Meta': {'object_name': 'OwnRecord', '_ormbases': ['relations.UserProfileRecord']},
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'related_name': "'own_records'"}),
            'shared_between': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'userprofilerecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['relations.UserProfileRecord']", 'primary_key': 'True', 'unique': 'True'})
        },
        'relations.team': {
            'Meta': {'object_name': 'Team'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['relations.UserProfile']", 'symmetrical': 'False', 'related_name': "'teams'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.teamcontact': {
            'Meta': {'object_name': 'TeamContact', '_ormbases': ['relations.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['relations.Contact']", 'primary_key': 'True', 'unique': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"})
        },
        'relations.usercontact': {
            'Meta': {'object_name': 'UserContact', '_ormbases': ['relations.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['relations.Contact']", 'primary_key': 'True', 'unique': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'known_people'"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'external_image': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True', 'default': "'/media/upload/user_picks/owl.jpg'"}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'default': "''"}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'null': 'True', 'unique': 'True'})
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

    complete_apps = ['chat', 'relations']
    symmetrical = True
