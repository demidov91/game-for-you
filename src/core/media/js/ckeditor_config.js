/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    CKEDITOR.on( 'dialogDefinition', function( ev )
       {
          var dialogName = ev.data.name;
          var dialogDefinition = ev.data.definition;
      
          if (dialogName == 'link') {
                var infoTab = dialogDefinition.getContents('info');
                infoTab.remove('browse');
                var targetTab = dialogDefinition.getContents('target');
                var targetField = targetTab.get('linkTargetType');
                targetField['default'] = '_blank';
            } else if (dialogName == 'image') {
                var infoTab = dialogDefinition.getContents('info');
                infoTab.remove('browse');
                infoTab.remove('txtHSpace');
                infoTab.remove('txtVSpace');
                infoTab.remove('txtAlt');
            }
       });
};
