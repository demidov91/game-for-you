# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for tag in orm.Tag.objects.filter(has_chat=True):
            chat = orm['chat.Chat']()
            chat.save()
            tag.chat = chat
            tag.save()
            for message in orm['chat.TagMessage'].objects.filter(tag=tag):
                new_message = orm['chat.Message'](
                    author=message.author, text=message.text, create_time=message.create_time, chat=chat)
                new_message.save()

    def backwards(self, orm):
        for tag in orm.Tag.objects.filter(chat__isnull=False):
            for message in tag.chat.message_set.filter(chat=tag.chat):
                old_message = orm['chat.TagMessage'](
                    author=message.author, create_time=message.create_time, tag=tag, text=message.text)
                old_message.save()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'chat.chat': {
            'Meta': {'object_name': 'Chat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'chat.message': {
            'Meta': {'ordering': "('create_time',)", 'object_name': 'Message'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'chat.tagmessage': {
            'Meta': {'ordering': "('create_time',)", 'object_name': 'TagMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tag']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['core.ShareTree']", 'blank': 'True'}),
            'shared_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shared_to'", 'to': "orm['auth.User']"})
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
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'symmetrical': 'False', 'to': "orm['relations.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'external_image': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'/media/upload/user_picks/owl.jpg'", 'max_length': '255', 'blank': 'True'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'null': 'True', 'to': "orm['relations.Team']", 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']", 'null': 'True'})
        },
        'tournament.competition': {
            'Meta': {'object_name': 'Competition'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.PROTECT', 'to': "orm['tournament.PlayField']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'competitions'", 'symmetrical': 'False', 'null': 'True', 'to': "orm['tournament.Tag']", 'blank': 'True'}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'competition_requests'", 'symmetrical': 'False', 'null': 'True', 'to': "orm['tournament.Tag']", 'blank': 'True'}),
            'team_accept_strategy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'related_name': "'competitions'", 'null': 'True', 'to': "orm['tournament.Tournament']", 'blank': 'True'})
        },
        'tournament.competitionownerstree': {
            'Meta': {'object_name': 'CompetitionOwnersTree', '_ormbases': ['core.ShareTree']},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['tournament.Competition']"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['core.ShareTree']"})
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
            'Meta': {'object_name': 'PlayerParticipation', '_ormbases': ['relations.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['relations.Contact']"}),
            'participation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Participation']"})
        },
        'tournament.playfield': {
            'Meta': {'object_name': 'PlayField'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'known_places'", 'to': "orm['auth.User']"})
        },
        'tournament.tag': {
            'Meta': {'object_name': 'Tag'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['chat.Chat']", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_chat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribed_to'", 'symmetrical': 'False', 'null': 'True', 'to': "orm['auth.User']", 'blank': 'True'})
        },
        'tournament.tagmanagementtree': {
            'Meta': {'object_name': 'TagManagementTree', '_ormbases': ['core.ShareTree']},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'managers'", 'to': "orm['tournament.Tag']"}),
            'permissions': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['core.ShareTree']"})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tournaments'", 'symmetrical': 'False', 'null': 'True', 'to': "orm['tournament.Tag']", 'blank': 'True'}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tournament_requests'", 'symmetrical': 'False', 'null': 'True', 'to': "orm['tournament.Tag']", 'blank': 'True'})
        },
        'tournament.tournamentownerstree': {
            'Meta': {'object_name': 'TournamentOwnersTree', '_ormbases': ['core.ShareTree']},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['tournament.Tournament']"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['core.ShareTree']"})
        }
    }

    complete_apps = ['chat', 'tournament']
    symmetrical = True
