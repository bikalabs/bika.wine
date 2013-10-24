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
					$("#ar_"+column+"_Contact").val(ar_data['Contact']);
					$("#ar_"+column+"_Contact_uid").val(ar_data['Contact_uid']);
					// $("#ar_"+column+"_CCContact").val(ar_data['CCContact']);
					// $("#ar_"+column+"_CCContact_uid").val(ar_data['CCContact_uid']);
					$("#ar_"+column+"_CCEmails").val(ar_data['CCEmails']);
					$("#ar_"+column+"_Client").val(ar_data['Client']);
					$("#ar_"+column+"_Client_uid").val(ar_data['Client_uid']);
					$("#ar_"+column+"_SubGroup").val(ar_data['SubGroup']);
					$("#ar_"+column+"_SubGroup_uid").val(ar_data['SubGroup_uid']);
					$("#ar_"+column+"_Template").val(ar_data['Template']);
					$("#ar_"+column+"_Template_uid").val(ar_data['Template_uid']);
					$("#ar_"+column+"_Profile").val(ar_data['Profile']);
					$("#ar_"+column+"_Profile_uid").val(ar_data['Profile_uid']);
					$("#ar_"+column+"_SampleType").val(ar_data['SampleType']);
					$("#ar_"+column+"_SampleType_uid").val(ar_data['SampleType_uid']);
					$("#ar_"+column+"_SamplePoint").val(ar_data['SamplePoint']);
					$("#ar_"+column+"_SamplePoint_uid").val(ar_data['SamplePoint_uid']);
					$("#ar_"+column+"_ClientOrderNumber").val(ar_data['ClientOrderNumber']);
					$("#ar_"+column+"_ClientReference").val(ar_data['ClientReference']);
					$("#ar_"+column+"_ClientSampleID").val(ar_data['ClientSampleID']);

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
