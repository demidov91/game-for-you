# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Competition.name'
        db.add_column('tournament_competition', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, blank=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Competition.name'
        db.delete_column('tournament_competition', 'name')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']", 'null': 'True'}),
            'shared_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'shared_to'"})
        },
        'relations.contact': {
            'Meta': {'object_name': 'Contact'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'relations.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['relations.UserProfile']", 'symmetrical': 'False', 'related_name': "'teams'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'to': "orm['relations.Team']", 'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'tournament.competition': {
            'Meta': {'object_name': 'Competition'},
            'duration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.PlayField']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournament.Tag']", 'symmetrical': 'False', 'related_name': "'competitions'"}),
            'team_accept_strategy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team_limit': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tournament']", 'blank': 'True', 'null': 'True'})
        },
        'tournament.participation': {
            'Meta': {'object_name': 'Participation'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Competition']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'greeting_words': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']"})
        },
        'tournament.playerparticipation': {
            'Meta': {'object_name': 'PlayerParticipation', '_ormbases': ['relations.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['relations.Contact']", 'unique': 'True'}),
            'participation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Participation']"})
        },
        'tournament.playfield': {
            'Meta': {'object_name': 'PlayField'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sharers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'known_places'"})
        },
        'tournament.tag': {
            'Meta': {'object_name': 'Tag'},
            'first_owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'tags_owned'"}),
            'first_sharers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'related_name': "'tags_to_publish'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'related_name': "'subscribed_to'", 'symmetrical': 'False', 'blank': 'True', 'null': 'True'})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'first_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournament.Tag']", 'symmetrical': 'False', 'related_name': "'tournaments'"})
        }
    }

    complete_apps = ['tournament']