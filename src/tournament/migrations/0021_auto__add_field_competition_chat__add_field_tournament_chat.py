# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Competition.chat'
        db.add_column('tournament_competition', 'chat',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['chat.Chat']),
                      keep_default=False)

        # Adding field 'Tournament.chat'
        db.add_column('tournament_tournament', 'chat',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['chat.Chat']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Competition.chat'
        db.delete_column('tournament_competition', 'chat_id')

        # Deleting field 'Tournament.chat'
        db.delete_column('tournament_tournament', 'chat_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'chat.chat': {
            'Meta': {'object_name': 'Chat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.sharetree': {
            'Meta': {'object_name': 'ShareTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['core.ShareTree']", 'null': 'True'}),
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
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'to': "orm['relations.UserProfile']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'external_image': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'default': "'/media/upload/user_picks/owl.jpg'", 'max_length': '255'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['relations.Team']", 'null': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']", 'null': 'True'})
        },
        'tournament.competition': {
            'Meta': {'object_name': 'Competition'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime(2014, 9, 28, 0, 0)', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.PROTECT', 'to': "orm['tournament.PlayField']"}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'competitions'", 'to': "orm['tournament.Tag']", 'symmetrical': 'False', 'null': 'True'}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'competition_requests'", 'to': "orm['tournament.Tag']", 'symmetrical': 'False', 'null': 'True'}),
            'team_accept_strategy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team_limit': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'on_delete': 'models.SET_NULL', 'related_name': "'competitions'", 'to': "orm['tournament.Tournament']", 'null': 'True'})
        },
        'tournament.competitionownerstree': {
            'Meta': {'object_name': 'CompetitionOwnersTree', '_ormbases': ['core.ShareTree']},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['tournament.Competition']"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['core.ShareTree']", 'primary_key': 'True'})
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
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['relations.Contact']", 'primary_key': 'True'}),
            'participation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Participation']"})
        },
        'tournament.playfield': {
            'Meta': {'object_name': 'PlayField'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'known_places'", 'to': "orm['auth.User']"})
        },
        'tournament.tag': {
            'Meta': {'object_name': 'Tag'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['chat.Chat']", 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'has_chat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscribed_to'", 'to': "orm['auth.User']", 'symmetrical': 'False', 'null': 'True'})
        },
        'tournament.tagmanagementtree': {
            'Meta': {'object_name': 'TagManagementTree', '_ormbases': ['core.ShareTree']},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'managers'", 'to': "orm['tournament.Tag']"}),
            'permissions': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['core.ShareTree']", 'primary_key': 'True'})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime(2014, 9, 28, 0, 0)', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'first_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tournaments'", 'to': "orm['tournament.Tag']", 'symmetrical': 'False', 'null': 'True'}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tournament_requests'", 'to': "orm['tournament.Tag']", 'symmetrical': 'False', 'null': 'True'})
        },
        'tournament.tournamentownerstree': {
            'Meta': {'object_name': 'TournamentOwnersTree', '_ormbases': ['core.ShareTree']},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': "orm['tournament.Tournament']"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['core.ShareTree']", 'primary_key': 'True'})
        }
    }

    complete_apps = ['tournament']