# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tag.is_private'
        db.add_column('tournament_tag', 'is_private',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Tag.show_calendar'
        db.add_column('tournament_tag', 'show_calendar',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tag.is_private'
        db.delete_column('tournament_tag', 'is_private')

        # Deleting field 'Tag.show_calendar'
        db.delete_column('tournament_tag', 'show_calendar')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'chat.chat': {
            'Meta': {'object_name': 'Chat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
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
        'relations.team': {
            'Meta': {'object_name': 'Team'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['relations.UserProfile']", 'related_name': "'teams'", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'external_image': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'/media/upload/user_picks/owl.jpg'", 'max_length': '255', 'blank': 'True'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']", 'null': 'True', 'blank': 'True', 'on_delete': 'models.SET_NULL'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'tournament.competition': {
            'Meta': {'object_name': 'Competition'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.PlayField']", 'on_delete': 'models.PROTECT'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournament.Tag']", 'null': 'True', 'related_name': "'competitions'", 'symmetrical': 'False', 'blank': 'True'}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournament.Tag']", 'null': 'True', 'related_name': "'competition_requests'", 'symmetrical': 'False', 'blank': 'True'}),
            'team_accept_strategy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tournament']", 'null': 'True', 'related_name': "'competitions'", 'blank': 'True', 'on_delete': 'models.SET_NULL'})
        },
        'tournament.competitionownerstree': {
            'Meta': {'_ormbases': ['core.ShareTree'], 'object_name': 'CompetitionOwnersTree'},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Competition']", 'related_name': "'owners'"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.ShareTree']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tournament.participation': {
            'Meta': {'object_name': 'Participation'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Competition']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'greeting_words': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.Team']", 'related_name': "'participations'"})
        },
        'tournament.playerparticipation': {
            'Meta': {'_ormbases': ['relations.Contact'], 'object_name': 'PlayerParticipation'},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['relations.Contact']", 'unique': 'True', 'primary_key': 'True'}),
            'participation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Participation']"})
        },
        'tournament.playfield': {
            'Meta': {'object_name': 'PlayField'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'known_places'"})
        },
        'tournament.tag': {
            'Meta': {'object_name': 'Tag'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_chat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'show_calendar': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'related_name': "'subscribed_to'", 'symmetrical': 'False', 'blank': 'True'})
        },
        'tournament.tagmanagementtree': {
            'Meta': {'_ormbases': ['core.ShareTree'], 'object_name': 'TagManagementTree'},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tag']", 'related_name': "'managers'"}),
            'permissions': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.ShareTree']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'chat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 22, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournament.Tag']", 'null': 'True', 'related_name': "'tournaments'", 'symmetrical': 'False', 'blank': 'True'}),
            'tags_request': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournament.Tag']", 'null': 'True', 'related_name': "'tournament_requests'", 'symmetrical': 'False', 'blank': 'True'})
        },
        'tournament.tournamentownerstree': {
            'Meta': {'_ormbases': ['core.ShareTree'], 'object_name': 'TournamentOwnersTree'},
            'managed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tournament']", 'related_name': "'owners'"}),
            'sharetree_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.ShareTree']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tournament']