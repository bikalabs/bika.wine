/*global jQuery:false */
(function( $ ) {
"use strict";

function fill_column(data) {
	if(data.objects.length > 0) {
		var obj = data.objects[0];
		var col = window.bika.ar_copy_from_col;
		$("#ar_"+col+"_Contact").val(obj.Contact);
		$("#ar_"+col+"_Contact_uid").val(obj.Contact_uid);
		// $("#ar_"+col+"_CCContact").val(obj.CCContact);
		// $("#ar_"+col+"_CCContact_uid").val(obj.CCContact_uid);
		$("#ar_"+col+"_CCEmails").val(obj.CCEmails);
		$("#ar_"+col+"_Client").val(obj.Client);
		$("#ar_"+col+"_Client_uid").val(obj.Client_uid);
		$("#ar_"+col+"_SubGroup").val(obj.SubGroup);
		$("#ar_"+col+"_SubGroup_uid").val(obj.SubGroup_uid);
		$("#ar_"+col+"_Template").val(obj.Template);
		$("#ar_"+col+"_Template_uid").val(obj.Template_uid);
		$("#ar_"+col+"_Profile").val(obj.Profile);
		$("#ar_"+col+"_Profile_uid").val(obj.Profile_uid);
		$("#ar_"+col+"_SampleType").val(obj.SampleType);
		$("#ar_"+col+"_SampleType_uid").val(obj.SampleType_uid);
		$("#ar_"+col+"_SamplePoint").val(obj.SamplePoint);
		$("#ar_"+col+"_SamplePoint_uid").val(obj.SamplePoint_uid);
		$("#ar_"+col+"_ClientOrderNumber").val(obj.ClientOrderNumber);
		$("#ar_"+col+"_ClientReference").val(obj.ClientReference);
		$("#ar_"+col+"_ClientSampleID").val(obj.ClientSampleID);

		var services = {};
		var specs = {};
		var cat_uid, service_uid;
		var i;

		for (i = obj.Analyses.length - 1; i >= 0; i--) {
			var analysis = obj.Analyses[i];
			cat_uid = analysis.CategoryUID;
			service_uid = analysis.ServiceUID;
			if(!(analysis.CategoryUID in services)){
				services[analysis.CategoryUID] = [];
			}
			services[analysis.CategoryUID].push(service_uid);
			specs[service_uid] = analysis.specification;
		}

		for(cat_uid in services){
			if(!services.hasOwnProperty(cat_uid)){ continue; }
			var service_uids = services[cat_uid];
			window.toggleCat("lab", cat_uid, col, service_uids, true);
			for (i = 0; i < service_uids.length; i++) {
				service_uid = service_uids[i];
				// $("[column="+col+"]").filter("#"+service_uid).click(); // toggleCat does this.
				var spec = specs[service_uid];
				if(spec){
					$("[name^='ar."+col+".min']").filter("[uid='"+service_uid+"']").val(spec.min);
					$("[name^='ar."+col+".max']").filter("[uid='"+service_uid+"']").val(spec.max);
					$("[name^='ar."+col+".error']").filter("[uid='"+service_uid+"']").val(spec.error);
				}
			}
		}
	}
}

$(document).ready(function(){
	var copy_from = window.location.href.split("copy_from=");
	if(copy_from.length > 1){
		copy_from = copy_from[1].split("&")[0];
		copy_from = copy_from.split(",");
		for (var column = 0; column < copy_from.length; column++) {
			window.bika.ar_copy_from_col = column;
			$.ajaxSetup({async:false});
			window.bika.lims.jsonapi_read({
				catalog_name: "uid_catalog",
				UID: copy_from[column]
			}, fill_column);
			$.ajaxSetup({async:true});
		}
	}

});
}(jQuery));
