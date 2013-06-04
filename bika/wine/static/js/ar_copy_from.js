(function( $ ) {
$(document).ready(function(){

	_p = jarn.i18n.MessageFactory('plone');
	_b = jarn.i18n.MessageFactory('bika');
	_ = jarn.i18n.MessageFactory('bika.wine');

	var copy_from = window.location.href.split("copy_from=");
	var arinfourl = window.location.href.split("/portal_factory")[0] + "/getarinfo"
	if(copy_from.length > 1){
		copy_from = copy_from[1].split("&")[0]
		copy_from = copy_from.split(",")
		for (var col = 0; col < copy_from.length; col++) {
			jQuery.ajaxSetup({async:false});
			$.getJSON(arinfourl,
				{'ar_uid': copy_from[col],
				 'column': col,
				 '_authenticator': $('input[name="_authenticator"]').val(),},
				function(ar_data, textStatus){
					column = ar_data['column'];
					$("#ar_"+column+"_Client").val(ar_data['Client']);
					$("#ar_"+column+"_Client_uid").val(ar_data['Client_uid']);
					$("#ar_"+column+"_SampleType").val(ar_data['SampleType']);
					$("#ar_"+column+"_SampleType_uid").val(ar_data['SampleType_uid']);
					for (var i = ar_data['categories'].length - 1; i >= 0; i--) {
						var cat_uid = ar_data['categories'][i];
						var services = ar_data['services'][cat_uid];
						window.toggleCat('lab', cat_uid, column, [], true);
						for (var s = 0; s < services.length; s++) {
							$("[column="+column+"]").filter("#"+services[s]).attr('checked', 'checked');
						};
					};
					window.calculate_parts(column);
				}
			);
			jQuery.ajaxSetup({async:true});
		};
	}

});
}(jQuery));
