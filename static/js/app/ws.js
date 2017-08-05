$(document).ready(function() {

	$("#menu_event").click(function(){
		$("#event_dashboard").show();
		$("#busi_dashboard").hide();
	});

	$("#menu_busi").click(function(){
		$("#busi_dashboard").show();
		$("#event_dashboard").hide();
	});


	var host = window.location.host;

	var ws = new ReconnectingWebSocket('ws://' + host + '/ws');
	ws.debug = true;
	ws.timeoutInterval = 3000;

	var $message = $('#event_total');

	tbl = $('#eventList').DataTable({
		"columnDefs": [{"targets":0, "visible": false}, {"targets":1, "width":"20%"}, {"targets":2, "width":"20%"},{"targets":3, "width":"60%"}],
		"order": [[ 1, "desc" ]],
		"oLanguage": {"sEmptyTable": "暂无告警信息"},
	});

	ws.onopen = function() {
		$message.attr("class", 'label label-success');
		$message.text('open');
	};

	ws.onmessage = function(ev) {
		$message.attr("class", 'label label-info');
		$message.text('recieved message');

		$message.fadeIn("slow");

		data = JSON.parse(ev.data);
		if (data.status == 1) {
			fnDeleteRows(tbl, data.eventid)
		}else{
			tbl.row.add([data.eventid, data.dt, data.host, data.content]).draw( false );
		}
	}

	ws.onclose = function(ev) {
		$message.attr("class", 'label label-important');
		$message.text('closed');
	}

	ws.onerror = function(ev) {
		$message.attr("class", 'label label-warning');
		$message.text('error occurred');
	}


	var fnDeleteRows = function (table, eventid){
		var indexes = table.rows().eq( 0 ).filter( function (rowIdx) {
			return table.cell( rowIdx, 0).data() == eventid ? true : false;
		});

		table.rows(indexes).remove().draw();
	}
});