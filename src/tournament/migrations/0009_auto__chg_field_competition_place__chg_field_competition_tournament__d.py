# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Competition.place'
        db.alter_column('tournament_competition', 'place_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.PlayField'], on_delete=models.PROTECT))

        # Changing field 'Competition.tournament'
        db.alter_column('tournament_competition', 'tournament_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.SET_NULL, to=orm['tournament.Tournament'], null=True))
        # Deleting field 'Tag.first_owners'
        db.delete_column('tournament_tag', 'first_owners_id')

        # Deleting field 'Tag.first_sharers'
        db.delete_column('tournament_tag', 'first_sharers_id')

        # Adding field 'Tag.first_owner'
        db.add_column('tournament_tag', 'first_owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='owner_tag_set', to=orm['core.ShareTree'], null=True),
                      keep_default=False)

        # Adding field 'Tag.first_sharer'
        db.add_column('tournament_tag', 'first_sharer',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='share_tag_set', to=orm['core.ShareTree'], null=True),
                      keep_default=False)

        # Adding M2M table for field owners on 'Tag'
        m2m_table_name = db.shorten_name('tournament_tag_owners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['tournament.tag'], null=False)),
            ('sharetree', models.ForeignKey(orm['core.sharetree'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'sharetree_id'])

        # Adding M2M table for field sharers on 'Tag'
        m2m_table_name = db.shorten_name('tournament_tag_sharers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['tournament.tag'], null=False)),
            ('sharetree', models.ForeignKey(orm['core.sharetree'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'sharetree_id'])


    def backwards(self, orm):

        # Changing field 'Competition.place'
        db.alter_column('tournament_competition', 'place_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.PlayField']))

        # Changing field 'Competition.tournament'
        db.alter_column('tournament_competition', 'tournament_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Tournament'], null=True))
        # Adding field 'Tag.first_owners'
        db.add_column('tournament_tag', 'first_owners',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags_owned', to=orm['core.ShareTree'], null=True),
                      keep_default=False)

        # Adding field 'Tag.first_sharers'
        db.add_column('tournament_tag', 'first_sharers',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags_to_publish', to=orm['core.ShareTree'], null=True),
                      keep_default=False)

        # Deleting field 'Tag.first_owner'
        db.delete_column('tournament_tag', 'first_owner_id')

        # Deleting field 'Tag.first_sharer'
        db.delete_column('tournament_tag', 'first_sharer_id')

        # Removing M2M table for field owners on 'Tag'
        db.delete_table(db.shorten_name('tournament_tag_owners'))

        # Removing M2M table for field sharers on 'Tag'
        db.delete_table(db.shorten_name('tournament_tag_sharers'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
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
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'symmetrical': 'False', 'to': "orm['relations.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"})
        },
        'relations.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'primary_team': ('django.db.models.fields.related.ForeignKey', [], {'on_delete': 'models.SET_NULL', 'blank': 'True', 'to': "orm['relations.Team']", 'null': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']", 'null': 'True'})
        },
        'tournament.competition': {
            'Meta': {'object_name': 'Competition'},
            'duration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'owners': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.PlayField']", 'on_delete': 'models.PROTECT'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'competitions'", 'symmetrical': 'False', 'to': "orm['tournament.Tag']"}),
            'team_accept_strategy': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team_limit': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'competitions'", 'on_delete': 'models.SET_NULL', 'blank': 'True', 'to': "orm['tournament.Tournament']", 'null': 'True'})
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
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['relations.Contact']", 'primary_key': 'True', 'unique': 'True'}),
            'participation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Participation']"})
        },
        'tournament.playfield': {
            'Meta': {'object_name': 'PlayField'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': "''", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''", 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'known_places'", 'to': "orm['auth.User']"})
        },
        'tournament.tag': {
            'Meta': {'object_name': 'Tag'},
            'first_owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_tag_set'", 'to': "orm['core.ShareTree']", 'null': 'True'}),
            'first_sharer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'share_tag_set'", 'to': "orm['core.ShareTree']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags_owned'", 'symmetrical': 'False', 'to': "orm['core.ShareTree']"}),
            'sharers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags_to_publish'", 'symmetrical': 'False', 'to': "orm['core.ShareTree']"}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribed_to'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True'})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'first_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ShareTree']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tournaments'", 'symmetrical': 'False', 'to': "orm['tournament.Tag']"})
        }
    }

    complete_apps = ['tournament']