$(document).ready(function() {

	var host = window.location.host;

	var ws = new ReconnectingWebSocket('ws://' + host + '/ws');
	ws.debug = true;
	ws.timeoutInterval = 3000;

	var $message = $('#ws_status');

	tbl = $('#eventList').DataTable({
		"columnDefs": [{"targets":0, "visible": false}, {"targets":1, "width":"20%"}, 
					   {"targets":2, "width":"20%"},{"targets":3, "width":"50%"},
					   {"targets":-1, "width":"10%", "data":null, "defaultContent": "<button>删除</button>"}],
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
			if (data.is_sound == 1){
				audio4new(data);
			}
			// responsiveVoice.speak("收到新的告警 请查看", "Chinese Female");
		}
		$message.text('waiting message');
	}

	$('#eventList tbody').on( 'click', 'button', function () {
		var tr = tbl.row( $(this).parents('tr') )
		var tdata = tr.data();
		$.ajax({
			url: "/pushAlert",
			data: {eventid: tdata[0]},
			type: "post",
			dataType: "json",
			success: function(data){
				if (data.errCode == 0){
					tr.remove().draw();
				}else{
					alertDiag(data.errMsg);
				}
			}	
		});
	});

	ws.onclose = function(ev) {
		$message.attr("class", 'label label-important');
		$message.text('closed');
	}

	ws.onerror = function(ev) {
		$message.attr("class", 'label label-warning');
		$message.text('error occurred');
	}

	
	$.ajax({
		url: "/pushAlert",
		type: "get",
		dataType: "json",
		success: function(data){
			for (var i = 0; i < data.length; i++){
				var d = data[i]
				tbl.row.add([d.eventid, d.dt, d.host, d.content]).draw(false);
			}	
		}		
	});

	var fnDeleteRows = function (table, eventid){
		var indexes = table.rows().eq( 0 ).filter( function (rowIdx) {
			return table.cell( rowIdx, 0).data() == eventid ? true : false;
		});

		table.rows(indexes).remove().draw();
	}

	var audio4new = function(data){
		var text = "收到新的告警请查看";
		text = encodeURI(text);
		
		var s = '<audio autoplay="autoplay">';
		s += '<source src="http://tsn.baidu.com/text2audio?lan=zh&ctp=1&per=0&cuid=1&tok='+ data.tok +'&tex='+ text +'"  type="audio/mpeg">';
		s += '<embed height="0" width="0" src="http://tsn.baidu.com/text2audio?lan=zh&per=0&ctp=1&cuid=1&tok='+ data.tok +'&tex='+ text+'">';
		s += '</audio>';
		
		$("#audio4new").html(s);
	}

	var alertDiag = function(data) {
		$("#modal-alert-text").text(data);
		$('#modal-alert').modal('show');
	};
});
