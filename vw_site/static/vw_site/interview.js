$( function() {
  var question_order = 1;
  var token = $( '#token' ).val();
  var question_count = $( '#question_count' ).val();
  var urlSaveInterview = $( '#save-interview' ).val();

  var userAgent = navigator.userAgent || navigator.vendor || window.opera;
  var is_ios = ( /iPad|iPhone|iPod/.test( userAgent ) && !window.MSStream );
  var uploadingVideo = false;
  var progressBarWrapper = document.querySelector( '.progress-bar-section' );
  var progressBar = document.querySelector( '#progress-bar-progress' );
  // iOS detection from: http://stackoverflow.com/a/9039885/177710
  var is_webrtc_dont_work = is_ios;
  var current_answer_video;

  function getValue( object, path, defaultValue ) {
    const pathParts = path instanceof Array ? path : path.split( '.' );

    if ( !pathParts.length || typeof object !== 'object' ) return defaultValue;

    const currentPathPart = pathParts[ 0 ];
    const restPath = pathParts.slice( 1 );

    if ( pathParts.length === 1 ) return object[ currentPathPart ];

    return getValue( object[ currentPathPart ], restPath, defaultValue );
  }

  $( '#step1-next' ).click( function() {
    $( '#step2-name' ).html( 'Hi ' + $( '#first-name' ).val() );
    $( '#practice-start-record' ).removeAttr( 'disabled' );
    navigator.mediaDevices.enumerateDevices().then( function( devices ) {
      $( '#check_video' ).html( '<i class="fa fa-warning"></i> Not Found' );
      $( '#check_audio' ).html( '<i class="fa fa-warning"></i> Not Found' );
      var video = false, audio = false;
      devices.map( function( device ) {
        if ( device.kind == 'videoinput' ) {
          $( '#check_video' ).html( 'OK' );
          video = true;
        }
        if ( device.kind == 'audioinput' ) {
          $( '#check_audio' ).html( 'OK' );
          audio = true;
        }
      } );
    } ).catch( function( err ) {
      $( '#check_video' ).html( '<i class="fa fa-warning"></i> Not Found' );
      $( '#check_audio' ).html( '<i class="fa fa-warning"></i> Not Found' );
    } );
  } );
  $( '#step2-next' ).click( function() {
    practice_video.pause();
    preview( question_order );
  } );
  $( '.next-question' ).click( function() {
    if ( !is_webrtc_dont_work ) {
      $( '#interview-video' ).attr( 'status', 'end' );
      return;
    }
    $( 'video:visible' ).hide();
    const formData = new FormData();
    formData.append( 'first_name', $( '#first-name' ).val() );
    formData.append( 'last_name', $( '#last-name' ).val() );
    formData.append( 'video', current_answer_video );
    formData.append( 'token', token );
    formData.append( 'question_order', question_order );
    formData.append( 'question_count', question_count );
    if ( $( '#email' ).val() )
      formData.append( 'email', $( '#email' ).val() );
    if ( $( '#job_id' ).val() )
      formData.append( 'job_id', $( '#job_id' ).val() );

    if ( $( '#position' ).val() )
      formData.append( 'position', $( '#position' ).val() );
    $( '#question' + question_order + ' .next-question' ).attr( 'disabled' );
    uploadingVideo = true;

    // upload using jQuery
    $.ajax( {
      url: urlSaveInterview, // replace with your own server URL
      data: formData,
      cache: true,
      dataType: 'json',
      contentType: false,
      processData: false,
      type: 'POST',
      xhr: function() {
        $('.progress-bar-section').css("display",'inline-flex');
        $('#progress-bar-progress').css('width', '0%');
        $('#percent').text('0%');
        var xhr = new window.XMLHttpRequest(); // получаем объект XMLHttpRequest

        // progressBarWrapper.classList.remove( '-hidden' );
        // progressBar.style.width = '0';

        xhr.upload.addEventListener( 'progress', function( evt ) { // добавляем обработчик события progress (onprogress)
          if ( evt.lengthComputable ) { // если известно количество байт
            // высчитываем процент загруженного

            var percentComplete = evt.loaded / evt.total;

            console.log(evt.loaded);
            console.log(evt.total);

            // progressBar.style.width = percentComplete + '%';

            $('#progress-bar-progress').css ('width', (percentComplete)*100+'%');
            $('#percent').text(Math.floor((percentComplete)*100)+'%');

            if ( percentComplete === 100 && uploadingVideo ) {
              camera.getTracks().forEach( function( track ) {
                track.stop();
              } );
              onVideoUploadComplete();
            }
          }
        }, false );
        return xhr;
      },
      success: function( response ) {
        if ( response != 'success' ) {
          alert( "Uploading failed" );
          // alert( response ); // error/failure
        }
      },
      complete: function() {
        if ( uploadingVideo ) {
          current_answer_video = null;
          onVideoUploadComplete();
        }
      },
    } );
    if ( !is_webrtc_dont_work ) {
      $( '#interview-video' ).prop( 'muted', true );
    }
  } );
  $( '.next-question-ios input' ).on( 'change', function( e ) {
    const file = getValue( e, 'target.files', [] )[ 0 ];
    if ( !file || !file.type.match( 'video/' ) ) {
      $( '#question' + question_order + ' .next-question' ).attr( 'disabled' );
      current_answer_video = null;
      return;
    }
    $( '#interview-video' ).prop( 'muted', false );
    $( '#interview-video' ).show();
    current_answer_video = file;
    const interview_video = document.getElementById( 'interview-video' );
    interview_video.src = interview_video.srcObject = null;
    interview_video.src = URL.createObjectURL( file );
    const loadListener = function() {
      const time_limit = parseInt(
        $( '#question' + question_order ).attr( 'limit' ) );
      if ( Math.floor( interview_video.duration ) > time_limit * 60 ) {
        alert(
          'Your time limit has elapsed. Your answer is being saved and uploaded.' );
      }
      interview_video.removeEventListener( 'loadedmetadata', loadListener );
    };
    interview_video.addEventListener( 'loadedmetadata', loadListener );
    $( '#question' + question_order + ' .next-question' ).
      removeAttr( 'disabled' );
    $( '#question' + question_order + ' .next-question-ios' ).remove();
  } );
  $( '#practice-start-record-ios input' ).on( 'change', function( e ) {
    const file = getValue( e, 'target.files', [] )[ 0 ];
    if ( !file || !file.type.match( 'video/' ) ) {
      $( '#step2-next' ).attr( 'disabled' );
      return;
    }
    $( '#practice-video' ).prop( 'muted', false );
    $( '#step2-next' ).removeAttr( 'disabled' );
    $( '[data-action="practice-video"]' ).show();
    $( 'p.text-justify' ).hide();
    practice_video.src = practice_video.srcObject = null;
    practice_video.src = URL.createObjectURL( file );
    practice_video.play();
  } );
  $( '#practice-start-record-ios' ).click( function() {
    $( '#practice-explain' ).hide();
    $( '#practice-video' ).prop( 'muted', true );
  } );

  function onVideoUploadComplete() {
    setTimeout(
      function() 
      {
        //do something special
        uploadingVideo = false;
        alert("Uploaded Successfully");
        $('.progress-bar-section').css("display",'none');
        const interview_video = document.getElementById( 'interview-video' );
        try {
          interview_video.src = interview_video.srcObject = '';
        } catch ( err ) {
          interview_video.src = interview_video.srcObject = null;
        }

        if ( question_order >= question_count ) {
          $( '.f1-steps' ).hide();
          $( 'form.f1 fieldset' ).hide();
          $( 'form.f1>p' ).hide();
          $( 'form.f1' ).
            append( '<h4><strong>Thank you ' + $( '#first-name' ).val() +
              '</strong><p>You have completed your interview.<br>You may close your browser now.</p><p>Regards,<br>Anytime Interview</p></h4>' );
        } else {
          question_order++;
          preview( question_order );
        }
    }, 2000);
  }

  function preview( order ) {
    $( '.question' ).hide();
    $( '#question' + order ).show();
    $('#question-limit1').html($( '#question' + order ).attr('limit'))
    $('#question-limit').html($( '#question' + order ).attr('limit'))
    if ( is_ios ) {
      order === 1
        ? $( '#ios-flow-description' ).show()
        : $( '#ios-flow-description' ).hide();
    }

    if ( is_webrtc_dont_work ) {
      $( '#question' + order + ' .next-question-ios' ).show();
      return;
    }

    var time_limit = parseInt( $( '#question' + order ).attr( 'limit' ) );
    // capture camera and/or microphone
    navigator.mediaDevices.getUserMedia( { video: true, audio: true } ).
      then( function( camera ) {
        // preview camera during recording
        document.getElementById( 'interview-video' ).muted = true;
        setSrcObject( camera, document.getElementById( 'interview-video' ) );
        // start record in few seconds
        var secs = 10;
        $( '#note' ).
          html(
            '<div style="height:20px; float:left;">Record will be started in&nbsp;</div><strong style="color:red">' +
            secs + '</strong>' );
        $( '#note' ).height( 20 );
        var wait_timer = setInterval( function() {
          $( '#note strong' ).animate( {
            opacity: 0.25,
            fontSize: '2em',
          }, 500, function() {
            $( '#note strong' ).css( 'opacity', 1 );
            $( '#note strong' ).css( 'font-size', '1em' );
            $( '#note strong' ).text( secs );
          } );

          secs--;
          if ( secs === 0 ) {
            $( '#note strong' ).fadeOut( 'fast' );
            clearInterval( wait_timer );
            $( '#interview-video' ).attr( 'status', 'start' );
            record( camera, time_limit );
            $( '#question' + order + ' .next-question' ).
              removeAttr( 'disabled' );
          }
        }, 1000 );
      } );
  }

  function record( camera, time_limit ) {
    // recording configuration/hints/parameters
    var recordingHints = {
      type: 'video',
      bitsPerSecond: 128000,
    };
    // initiating the recorder
    var recorder = RecordRTC( camera, recordingHints );
    // starting recording here
    recorder.startRecording();

    // countdown timer
    var mins = time_limit;
    var secs = mins * 60;
    var currentSeconds = 0;
    var currentMinutes = 0;
    var timer = setInterval( function() {
      currentMinutes = Math.floor( secs / 60 );
      currentSeconds = secs % 60;
      if ( currentSeconds <= 9 ) currentSeconds = '0' + currentSeconds;
      secs--;
      $( '#note' ).
        html( '<span style=\'color: red;\'>Recording...&nbsp&nbsp</span>' +
          currentMinutes + ':' + currentSeconds ); //Set the element id you need the time put into.
      if ( secs === -1 || $( '#interview-video' ).attr( 'status' ) == 'end' ) {
        clearInterval( timer );
        // stop recording
        recorder.stopRecording( function() {

          // get recorded blob
          var blob = recorder.getBlob();
          // generating a random file name
          var fileName = getFileName( 'mp4' );
          // we need to upload "File" --- not "Blob"
          var fileObject = new File( [ blob ], fileName, {
            type: 'video/mp4',
          } );

          var formData = new FormData();
          formData.append( 'first_name', $( '#first-name' ).val() );
          formData.append( 'last_name', $( '#last-name' ).val() );
          formData.append( 'video', fileObject );
          formData.append( 'token', token );
          formData.append( 'question_order', question_order );
          formData.append( 'question_count', question_count );
          if ( $( '#email' ).val() )
            formData.append( 'email', $( '#email' ).val() );
          if ( $( '#job_id' ).val() )
            formData.append( 'job_id', $( '#job_id' ).val() );
          if ( $( '#position' ).val() )
            formData.append( 'position', $( '#position' ).val() );
          $( '#question' + question_order + ' .next-question' ).
            attr( 'disabled' );
          uploadingVideo = true;

          console.log("upload started");

          // upload using jQuery
          $.ajax( {
            url: urlSaveInterview, // replace with your own server URL
            data: formData,
            cache: true,
            dataType: 'json',
            contentType: false,
            processData: false,
            type: 'POST',
            xhr: function() {

              $('.progress-bar-section').css("display",'inline-flex');
              $('#progress-bar-progress').css('width', '0%');
              $('#percent').text('0%');
              var xhr = new window.XMLHttpRequest(); // получаем объект XMLHttpRequest

              // progressBarWrapper.classList.remove( '-hidden' );
              // progressBar.style.width = '0';

              xhr.upload.addEventListener( 'progress', function( evt ) { // добавляем обработчик события progress (onprogress)
                if ( evt.lengthComputable ) { // если известно количество байт
                  // высчитываем процент загруженного

                  var percentComplete = evt.loaded / evt.total;

                  console.log(evt.loaded);
                  console.log(evt.total);

                  // progressBar.style.width = percentComplete + '%';

                  $('#progress-bar-progress').css ('width', (percentComplete)*100+'%');
                  $('#percent').text(Math.floor((percentComplete)*100)+'%');

                  if ( percentComplete === 100 && uploadingVideo ) {
                    camera.getTracks().forEach( function( track ) {
                      track.stop();
                    } );
                    onVideoUploadComplete();
                  }
                }
              }, false );
              return xhr;
            },
            success: function( response ) {
              if ( response != 'success' ) {
                alert( response ); // error/failure
              }
            },
            complete: function() {
              if ( uploadingVideo ) {
                camera.getTracks().forEach( function( track ) {
                  track.stop();
                } );
                onVideoUploadComplete();
              }
            },
          } );
        } );
      }
    }, 1000 );
  }

  $( '[data-action="practice-video"]' ).hide();

  function getFileName( fileExtension ) {
    var d = new Date();
    var year = d.getUTCFullYear();
    var month = d.getUTCMonth();
    var date = d.getUTCDate();
    return 'RecordRTC-' + year + month + date + '-' + getRandomString() + '.' +
      fileExtension;
  }

  function getRandomString() {
    if ( window.crypto && window.crypto.getRandomValues &&
      navigator.userAgent.indexOf( 'Safari' ) === -1 ) {
      var a = window.crypto.getRandomValues( new Uint32Array( 3 ) ),
        token = '';
      for ( var i = 0, l = a.length; i < l; i++ ) {
        token += a[ i ].toString( 36 );
      }
      return token;
    } else {
      return ( Math.random() * new Date().getTime() ).toString( 36 ).
        replace( /\./g, '' );
    }
  }

  var practice_video = document.getElementById( 'practice-video' );
  $( '#practice-video' ).prop( 'muted', true );

  function captureCamera( callback ) {
    navigator.mediaDevices.getUserMedia( { audio: true, video: true } ).
      then( function( camera ) {
        $( '#step2-next' ).removeAttr( 'disabled' );
        callback( camera );
      } ).
      catch( function( error ) {
        alert( 'Unable to capture your camera. Please check console logs.' );
        console.error( error );
      } );
  }

  function stopRecordingCallback() {
    practice_video.src = practice_video.srcObject = null;
    practice_video.src = URL.createObjectURL( practice_recorder.getBlob() );
    practice_video.play();
    practice_recorder.camera.stop();
    practice_recorder.destroy();
    practice_recorder = null;
  }

  var practice_recorder; // globally accessible
  $('#practice-start-record').click(function() {
    $(this).hide();
    $('#practice-explain').hide();
    $('.video-wrapper').show();
    $('.pracetice_question').removeClass('col-sm-6');
    $('.pracetice_question').addClass('col-sm-12');
    $('fieldset:visible').find('.text-justify').remove();
    $('[data-action="practice-video"]').show();
    captureCamera(function(camera) {
      setSrcObject(camera, practice_video);
      practice_video.play();
      practice_recorder = RecordRTC( camera, {
        type: 'video',
      } );
      practice_recorder.startRecording();
      // release camera on stopRecording
      practice_recorder.camera = camera;
      $( '#practice-stop-record' ).show();
    } );
  } );
  $( '#practice-stop-record' ).click( function() {
    $( '#hello-section' ).hide();
    $( '#practice-explain' ).show();
    $( this ).hide();
    $( '#practice-start-record' + ( is_webrtc_dont_work ? '-ios' : '' ) ).
      show();
    $( '#practice-video' ).prop( 'muted', false );
    practice_recorder.stopRecording( stopRecordingCallback );
  } );
} );
