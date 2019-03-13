$( function() {
  // var invite_link_str = '&lt;&lt;Invite Link&gt;&gt;';
  // Upload resume
  var csrf_token = $( 'input[name=\'csrfmiddlewaretoken\']' ).val();
  $( 'input:file' ).change( function() {
    var fileName = $( this )[ 0 ].files[ 0 ];
    var url = $( this ).data( 'url' );
    var form = new FormData();
    form.append( 'csrfmiddlewaretoken', csrf_token );
    form.append( 'resume', fileName );
    var btn = $( this );
    $.ajax( {
      url: url,
      data: form,
      cache: false,
      contentType: false,
      processData: false,
      type: 'POST',
      success: function() {
        btn.attr( 'disabled', 'disabled' );
        btn.parent( 'label' ).attr( 'disabled', 'disabled' );
      },
    } );
  } );

  var maxQuestionsCount = 10;

  function getValue( object, path, defaultValue ) {
    const pathParts = path instanceof Array ? path : path.split( '.' );

    if ( !pathParts.length || typeof object !== 'object' ) return defaultValue;

    const currentPathPart = pathParts[ 0 ];
    const restPath = pathParts.slice( 1 );

    if ( pathParts.length === 1 ) return object[ currentPathPart ];

    return getValue( object[ currentPathPart ], restPath, defaultValue );
  }

  function getPositionsSuggestions( { value, cb } ) {
    $.ajax( {
      url: urlPositionsSuggestions + '?position=' + value,
      cache: false,
      success: function( result ) {
        cb(
          result.map( function( pos ) {
            return getValue( pos, 'fields.name', '' );
          } ).filter( function( pos ) {
            return pos;
          } )
        );
      },
    } );
  }

  function getPositionsQuestions( { value, cb } ) {
    $.ajax( {
      url: urlPositionQuestions + '?position=' + value,
      cache: false,
      success: function( result ) {
        cb(
          result.map( function( pos ) {
            var question = getValue( pos, 'fields.content', '' );
            var limit = getValue( pos, 'fields.limit', '2' );
            return { [ question ]: limit };
          } ).filter( function( pos ) {
            return pos;
          } )
        );
      },
    } );
  }

  function getCompetenciesSuggestions( { value, cb } ) {
    $.ajax( {
      url: urlCompetenciesSuggestions + '?competency=' + value,
      cache: false,
      success: function( result ) {
        cb(
          result.map( function( pos ) {
            return getValue( pos, 'fields.name', '' );
          } ).filter( function( pos ) {
            return pos;
          } )
        );
      },
    } );
  }

  function getCompetencyQuestions( { value, cb } ) {
    $.ajax( {
      url: urlCompetencyQuestions + '?competency=' + value,
      cache: false,
      success: function( result ) {
        cb(
          result.map( function( pos ) {
            return getValue( pos, 'fields.content', '' );
          } ).filter( function( pos ) {
            return pos;
          } )
        );
      },
    } );
  }

  function appendQuestion( currentIdx, { text, timeLimit } ) {
    $( '.question-group' ).append(
      '<div class="question-wrapper' + currentIdx + '">' +
      '<div class="form-group question' + currentIdx + '">' +
      '<div class="col-lg-1"><a class="btn btn-default btn-xs del-question" index="' +
      currentIdx + '"><i class="fa fa-minus"></i></a></div>' +
      '<label class="control-label col-lg-3">Question' + currentIdx +
      '</label>' +
      '<div class="col-lg-8">' +
      '<textarea class="form-control" name="question' + currentIdx +
      '" required>' + text + '</textarea>' +
      '</div>' +
      '</div>' +
      '<div class="form-group time-limit' + currentIdx + '">' +
      '<div class="col-lg-8 col-lg-offset-4">' +
      '<label for="time-limit" class="control-label col-lg-4">Time limit</label>' +
      '<input type="text" class="form-control time-limit" name="limit' +
      currentIdx + '" value="' + timeLimit + '" required>' +
      '</div>' +
      '</div>' +
      '</div>'
    );
  }

  function setPositionQuestions( questions ) {
    if ( !( questions instanceof Array ) || !questions.length ) return;

    const addBtn = $( '.add-question' );
    let allQuestions = [];
    const oldQuestions = $( '.question-group' ).
      find( '[class^="question-wrapper"]' );

    oldQuestions.each( function( j, elem ) {
      const text = $( elem ).find( 'textarea' ).val();
      const timeLimit = $( elem ).find( '.time-limit' ).val();
      if ( text ) allQuestions.push( { text, timeLimit } );
    } );

    oldQuestions.remove();
    questions.forEach( function( text ) {
      for ( var property in text ) {
        allQuestions.push( { text:property, timeLimit: text[property] } );
      }
    } );
    // allQuestions = allQuestions.slice(0, maxQuestionsCount); // think it's not needed in that case

    allQuestions.forEach( function( questionData, index ) {
      const currentIdx = index + 1;
      appendQuestion( currentIdx, questionData );
    } );
    addBtn.attr( 'index', allQuestions.length );
  }

  $( 'body' ).on( 'change keyup blur input', '#first_name', function( e ) {
    const newValue = e.target.value || 'Applicant';
    const currentTemplateId = $( '#cur_invite_template' ).attr( 'template_id' );

    $( '.editor-candidate-name' ).html( newValue ); // to change showed in editor data
    $( 'body' ).
      find( 'textarea[id^="invite_template"]' ).
      each( function( index, el ) {
        $( el ).val( ( $( el ).val() || '' ).replace(
          /<span class="editor-candidate-name">[^<]*<\/span>/,
          '<span class="editor-candidate-name">' +
          newValue + '</span>' ) );
      } )
    ;

    $( '#cur_invite_template' ).
      val(
        $( 'textarea[id^="invite_template"][template_id="' + currentTemplateId +
          '"]' ).val() );
  } );

  var invite_link_str = '%3C%3CInvite%20Link%3E%3E';
  $( '#inviteModal' ).on( 'shown.bs.modal', function( e ) {
    if ( $( e.relatedTarget ).hasClass( 'resend-btn' ) ) {
      $( this ).addClass( 'resend' );
      var candidate_id = $( e.relatedTarget ).attr( 'candidate_id' );
      $.ajax( {
        url: urlGetCandidateInfo,
        type: 'post',
        data: { candidate_id: candidate_id },
        success: function( data ) {
          const oldQuestions = $( '.question-group' ).
            find( '[class^="question-wrapper"]' );
          oldQuestions.remove();
          $( '#invite_email' ).val( data.email );
          $( '#invite_position' ).val( data.position );
          for ( var i = 0; i < data.questions.length; i++ ) {
            appendQuestion( i + 1,
              { text: data.questions[ i ], timeLimit: data.limits[ i ] } );
          }
          $( '.add-question' ).attr( 'index', data.questions.length );
        },
      } );
    } else if ( $( e.relatedTarget ).hasClass( 'invite-btn' ) ) {
      $( this ).removeClass( 'resend' );
      $( '#invite_email' ).val( '' );
      $( '#invite_position' ).val( '' );
      $( '.question-group textarea' ).val( '' );
    }
    $( '#invite_note' ).empty();
    monkeyPatchAutocomplete();
    $( '.question-group textarea' ).autocomplete( {
      source: function( req, responseFn ) {
        var re = $.ui.autocomplete.escapeRegex( req.term );
        var matcher = new RegExp( '\\b' + re, 'i' );
        var a = $.grep( phraselist, function( item, index ) {
          return matcher.test( item );
        } );
        responseFn( a );
      },
    } );
    $( '#invite_position' ).on( 'change', function() {
      var selectedPosition = this.value;

      if ( selectedPosition ) {
        getPositionsQuestions( {
          value: selectedPosition,
          cb: setPositionQuestions,
        } );
      }
    } );
    $( '.slider_invite_template' ).slick( {
      dots: true,
      arrows: false,
      accessibility: false,
    } );
    $( '.slider_invite_template' ).
      on( 'beforeChange', function( event, slick, currentSlide, nextSlide ) {
        $( '#cur_invite_template' ).
          val( $( '#invite_template' + nextSlide ).val() );
        $( '#cur_invite_template' ).
          attr( 'template_id',
            $( '#invite_template' + nextSlide ).attr( 'template_id' ) );
      } );
    $( '#cur_invite_template' ).val( $( '#invite_template0' ).val() );
    $( '#cur_invite_template' ).
      attr( 'template_id', $( '#invite_template0' ).attr( 'template_id' ) );
  } );

  $( '.question-group' ).on( 'DOMNodeInserted', '.form-group', function() {
    $( this ).find( 'textarea' ).autocomplete( {
      source: function( req, responseFn ) {
        var re = $.ui.autocomplete.escapeRegex( req.term );
        var matcher = new RegExp( '\\b' + re, 'i' );
        var a = $.grep( phraselist, function( item, index ) {
          return matcher.test( item );
        } );
        responseFn( a );
      },
    } );
  } );

  $( '.add-question' ).click( function() {
    var newIdx = parseInt( $( this ).attr( 'index' ) ) + 1;
    if ( newIdx > maxQuestionsCount ) {
      alert( 'You can not create over ' + maxQuestionsCount + ' questions' );
      return;
    }
    appendQuestion( newIdx, { text: '', timeLimit: 2 } );
    $( this ).attr( 'index', newIdx );
  } );

  $( '#save_template' ).click( function() {
    var template_id = $( '#cur_invite_template' ).attr( 'template_id' );
    var html = $( '#cur_invite_template' ).val();
    var invite_link = $( '#invite_link' ).val();
    $.ajax( {
      url: urlSaveTemlate,
      type: 'post',
      data: {
        'template_id': template_id,
        'html': html,
        'invite_link': invite_link,
      },
      success: function( data ) {
      },
    } );
  } );

  $( '.question-group' ).on( 'click', '.del-question', function( e ) {
    var count = parseInt( $( '.add-question' ).attr( 'index' ) );
    if ( count <= 1 ) {
      $( '#invite_note' ).html( 'You have to send at least 1 question.' );
      return;
    }
    $( '#invite_note' ).empty();
    var idx = parseInt( $( this ).attr( 'index' ) );
    $( '.question-group .question' + idx ).remove();
    $( '.question-group .time-limit' + idx ).remove();
    for ( var i = idx + 1; i <= count; i++ ) {
      $( '.question-group .question' + i + ' .del-question' ).
        attr( 'index', i - 1 );
      $( '.question-group .question' + i + ' label' ).
        html( 'Question' + ( i - 1 ) );
      $( '.question-group .question' + i + ' textarea' ).
        attr( 'name', 'question' + ( i - 1 ) );
      $( '.question-group .question' + i ).
        addClass( 'question' + ( i - 1 ) ).
        removeClass( 'question' + i );
      $( '.question-group .time-limit' + i + ' .time-limit' ).
        attr( 'name', 'limit' + ( i - 1 ) );
      $( '.question-group .time-limit' + i ).
        addClass( 'time-limit' + ( i - 1 ) ).
        removeClass( 'time-limit' + i );
      $( '#invite_question' + i ).attr( 'id', 'invite_question' + ( i - 1 ) );
    }
    $( '.add-question' ).attr( 'index', count - 1 );
  } );
  $( '#inviteForm' ).submit( function() {
    var rst = false,
      error;
    $.ajax( {
      url: urlIsCandidateExist,
      type: 'post',
      async: false,
      data: $( this ).serialize(),
      success: function( data ) {
        if ( data != 'false' ) {
          rst = true;
          error = data;
        }
      },
    } );
    $( '#invite_note' ).empty();
    if ( rst ) {
      $( '#invite_note' ).html( error );
      return false;
    } else {
      location.reload();
    }
  } );
  $( '#dataTable' ).on( 'click', '.del-btn', function( e ) {
    var url = $( this ).attr( 'del_id' );
    $( '#delForm' ).attr( 'action', url );
  } );

  var token = makeToken();
  var link = siteUrl + token;
  var froala_key = 'MmC-13E-11D5qC-7kgA-21xsE-11vmC-7ijtD-17hF4bmnH3ds==';
  $( '#invite_link' ).val( link );
  if ( invitesString == '[]' ) {
    $( '#invite_template0' ).
      text(
        '<p>Hello <span class="editor-candidate-name">Applicant</span>,</p><p>Please click on the link below to open the webpage for your anytime interview. Allow approximately 15 minutes this complete this task.</p><p>Interview link for you: <a href="' +
        link + '">Start Interview</a>&nbsp;</p>' );
    $( '#invite_template0' ).froalaEditor( {
      toolbarButtons: [
        'bold',
        'italic',
        'underline',
        'strikeThrough',
        'color',
        'emoticons',
        'insertFile',
        'html' ],
      key: froala_key,
    } );
  } else {
    invites.forEach( function( invite, index ) {
      var new_msg = oldMessages[ index ].replace( invite_link_str, link );
      $( '#invite_template' + index ).html( new_msg );
      $( '#invite_template' + index ).froalaEditor( {
        toolbarButtons: [
          'bold',
          'italic',
          'underline',
          'strikeThrough',
          'color',
          'emoticons',
          'insertFile',
          'html' ],
        key: froala_key,
      } ).on( 'froalaEditor.contentChanged', function( e, editor ) {
        $( '#cur_invite_template' ).val( editor.html.get() );
      } );
    } );
  }
} );

function monkeyPatchAutocomplete() {
  var oldFn = $.ui.autocomplete.prototype._renderItem;

  $.ui.autocomplete.prototype._renderItem = function( ul, item ) {
    var re = new RegExp( '\\b' + this.term, 'i' );
    var t = item.label.replace(
      re, '<span style=\'font-weight:bold;color:Blue;\'>' + this.term +
      '</span>' );
    return $( '<li></li>' ).
      data( 'item.autocomplete', item ).
      append( '<a>' + t + '</a>' ).
      appendTo( ul );
  };
}

function makeToken() {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for ( var i = 0; i < 32; i++ )
    text += possible.charAt( Math.floor( Math.random() * possible.length ) );
  return text;
}
