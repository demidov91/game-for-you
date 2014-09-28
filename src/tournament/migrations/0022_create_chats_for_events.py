# -*- coding: utf-8 -*-
from itertools import chain

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for event in chain(orm.Competition.objects.all(), orm.Tournament.objects.all()):
            event.chat = orm['chat.Chat'].objects.create()
            event.save()

    def backwards(self, orm):
        for event in chain(orm.Competition.objects.all(), orm.Tournament.objects.all()):
            event.chat.delete()


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'chat.chat': {
            'Meta': {'object_name': 'Chat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['core.ShareTree']"}),
            'shared_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shared_to'", 'to': "orm['auth.User']"})
        },
        'relations.contact': {
            'Meta': {'object_name': 'Contact'},
            'about': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'relations.team': {
            'Meta': {'object_name': 'Team'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'teams'", 'to': "orm['relations.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'external_image': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'default': "'/media/upload/user_picks/owl.jpg'", 'blank': 'True'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'null': 'True', 'blank': 'True', 'to': "orm['relations.Team']"}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'to': "orm['auth.User']", 'unique': 'True'})
        },
        'tournament.competition': {
            'Meta': {'object_name': 'Competition'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 28, 0, 0)', 'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.PROTECT', 'to': "orm['tournament.PlayField']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'competitions'", 'blank': 'True', 'to': "orm['tournament.Tag']"}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'competition_requests'", 'blank': 'True', 'to': "orm['tournament.Tag']"}),
            'team_accept_strategy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'null': 'True', 'related_name': "'competitions'", 'blank': 'True', 'to': "orm['tournament.Tournament']"})
        },
        'tournament.competitionownerstree': {
            'Meta': {'_ormbases': ['core.ShareTree'], 'object_name': 'CompetitionOwnersTree'},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['tournament.Competition']"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['core.ShareTree']", 'unique': 'True'})
        },
        'tournament.participation': {
            'Meta': {'object_name': 'Participation'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Competition']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'greeting_words': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': "orm['relations.Team']"})
        },
        'tournament.playerparticipation': {
            'Meta': {'_ormbases': ['relations.Contact'], 'object_name': 'PlayerParticipation'},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['relations.Contact']", 'unique': 'True'}),
            'participation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Participation']"})
        },
        'tournament.playfield': {
            'Meta': {'object_name': 'PlayField'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "''", 'max_length': '100', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'known_places'", 'to': "orm['auth.User']"})
        },
        'tournament.tag': {
            'Meta': {'object_name': 'Tag'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['chat.Chat']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_chat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'subscribed_to'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'tournament.tagmanagementtree': {
            'Meta': {'_ormbases': ['core.ShareTree'], 'object_name': 'TagManagementTree'},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'managers'", 'to': "orm['tournament.Tag']"}),
            'permissions': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['core.ShareTree']", 'unique': 'True'})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 28, 0, 0)', 'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'first_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'tournaments'", 'blank': 'True', 'to': "orm['tournament.Tag']"}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'related_name': "'tournament_requests'", 'blank': 'True', 'to': "orm['tournament.Tag']"})
        },
        'tournament.tournamentownerstree': {
            'Meta': {'_ormbases': ['core.ShareTree'], 'object_name': 'TournamentOwnersTree'},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['tournament.Tournament']"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['core.ShareTree']", 'unique': 'True'})
        }
    }

    complete_apps = ['tournament']
    symmetrical = True
