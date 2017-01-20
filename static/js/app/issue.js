$(function(){
	$("#commit").on('click', function(){
		var issue_id = $("#issue_id").val();
		var type_id = $("#sel").val();

		$.ajax({
			url: "/issue/"+issue_id,
			type: "post",
			data: {type_id: type_id},
			dataType: "json",
			success: function(data){
				if (data.errCode == 0){
					alert("提交成功");
				}else{
					alert(data.errMsg);
				}
			}			
		});	
	});
});
