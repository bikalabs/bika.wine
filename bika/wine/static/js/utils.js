(function( $ ) {
$(document).ready(function(){

    var millis = 300000;

    _p = jarn.i18n.MessageFactory('plone');
    _b = jarn.i18n.MessageFactory('bika');
    _ = jarn.i18n.MessageFactory('bika.wine');

    var pu = window.portal_url;
    $('<audio id="alert_beep">' +
      '<source src="'+pu+'/++resource++beep.wav" type="audio/wav">' +
      '<source src="'+pu+'/++resource++beep.mp3" type="audio/mp3">' +
      '</audio>').appendTo('body');

    var alerturl = window.portal_url + "/@@wine_alerts";
    function alerts() {
        $.getJSON(alerturl,
            {'_authenticator': $('input[name="_authenticator"]').val(),},
            function(alert_data, textStatus){
                var msgtitle = _b("Attention");
                var msgtext = _b("The following items are not yet received, and their sampling date has past.");
                var title = _b("Title");
                var description = _b("Description");
                if(alert_data.length > 0){
                    $("#alert_dialog").remove();
                    if(alert_data['error'] != undefined){
                        return;
                    }
                    var dt = "<div id='alert_dialog' title='"+msgtitle+"'>";
                    dt = dt + "<p>"+msgtext+"</p><br/>";
                    dt = dt + "<table class='alert_table' width='100%'><tr><th>"+title+"</th><th>"+description+"</th></tr>"
                    dt = dt + "<tr></tr>"
                    for (var i = 0; i < alert_data.length; i++) {
                        dt = dt + "<tr>";
                        dt = dt + "<td>"+alert_data[i]['Title']+"</td>";
                        dt = dt + "<td>"+alert_data[i]['Description']+"</td>";
                        dt = dt + "</tr>";
                    };
                    dt = dt + "</table>"
                    dt = dt + "</div>";
                    $('body').append(dt);
                    $('#alert_dialog').dialog();
                    $('#alert_beep')[0].play();
                }
            }
        );
    }
    var alertIntervalID = setInterval(alerts, millis);

});
}(jQuery));
