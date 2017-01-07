var rulot = []; var rulotsj = [];
var piaoshu = []; var piaoshusj = []; var huoliang = [];
var shijian = []; var piaoshu3 = []; var huoliang3 = [];
var jsonData;
var k;

$(function () {
    funJson();
    // funJson2();
    // funJson3();

    GetBar();
    GetLin();
    fungv();
    randomData();

    //setInterval(GetState, 30000);
    setInterval(funJson, 30000);

    // setInterval(funJson3, 30000);

    // setInterval(funJson2, 6000);

    //setInterval(fungv, 6000);

    setInterval(GetDg, 1000);

    CollectGarbage();
});

function GetBar() {
    var myChart = echarts.init(document.getElementById('echartbarA'), 'dark');
    option = {
        title: {
            text: 'Trigger Rank',
            right: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: ['搜索引擎']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: rulot
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'Count'
            }
        ],
        series: [
            {
                name: '',
                type: 'bar',
                barWidth: 50,
                data: rulotsj,
                //markLine: {
                //    itemStyle: {
                //        normal: {
                //            lineStyle: {
                //                type: 'dashed'
                //            }
                //        }
                //    },

                //}
            }
        ]
    };
    myChart.setOption(option);
}

//折线图（7天）
function GetLin() {
    //折线图（7天）
    var myChart = echarts.init(document.getElementById('echartbarB'), 'dark');
    option = {
        title: {
            text: '近7天货量排名 ',
            right: 'center'
        },

        tooltip: {
            trigger: 'axis'
        },

        legend: {
            left: '60%',
            top:'1.5%',
            data: ['货量', '票数']
        },

        //toolbox: {
        //    show: false,
        //    feature: {
        //        mark: { show: true },
        //        dataView: { show: true, readOnly: false },
        //        magicType: { show: true, type: ['line', 'bar'] },
        //        restore: { show: true },
        //        saveAsImage: { show: true }
        //    }
        //},

        grid: {
            left: '3%',
            right:'0%',
            bottom: '3%',
            containLabel: true
        },

        calculable: true,

        xAxis: [
            {
                type: 'category',
                data: piaoshu
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '票数(票)',
                //min: 0,
                //max: 350,
                //interval: 50,
                axisLabel: {
                    formatter: '{value}'
                }
            },

            {
                type: 'value',
                name: '货量(吨)',
                //min: 0,
                //max: 25,
                //interval: 5,
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [

            {
                name: '票数',
                type: 'line',
                smooth:true,
                data: piaoshusj,

                lineStyle: {
                    normal: {
                        width: 4
                    }
                }
            },
            {
                name: '货量',
                type: 'bar',
                barWidth:60,
                yAxisIndex: 1,
                data: huoliang
            },
        ]
    };
    myChart.setOption(option);
}

//折线图(24小时)
function randomData() {
    var myChart = echarts.init(document.getElementById('echartbarC'), 'dark');
    option = {
        title: {
            text: '近24时货量排名 ',
            right: 'center'
        },

        tooltip: {
            trigger: 'axis'
        },

        toolbox: {
            show: false,
            feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: false },
                magicType: { show: true, type: ['line', 'bar'] },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },

        grid: {
            left: '4%',
            right: '0%',
            bottom: '2%',
            containLabel: true
        },

        calculable: true,

        legend: {
            left: '60%',
            top:'2%',
            data: ['货量', '票数']
        },
        xAxis: [
            {
                type: 'category',
                data: shijian
            }
        ],


        yAxis: [
           {
               type: 'value',
               name: '货量(吨)',
               //min: 0,
               //max: 350,
               //interval: 50,
               axisLabel: {
                   formatter: '{value}'
               }
           },

           {
               type: 'value',
               name: '票数(票)',
               //min: 0,
               //max: 25,
               //interval: 5,
               axisLabel: {
                   formatter: '{value}'
               }
           }
        ],
        series: [

            {
                name: '货量',
                type: 'line',
                smooth: true,
                data: huoliang3,

                lineStyle: {
                    normal: {
                        width: 4
                    }
                }
            },
             {
                 name: '票数',
                 type: 'line',
                 smooth: true,
                 yAxisIndex: 1,
                 data: piaoshu3,

                 lineStyle: {
                     normal: {
                         width: 4
                     }
                 }
             },
        ]
    };
    myChart.setOption(option);
}

function funJson() {
    $.ajax({
		url: 'http://alert.ane56.com/trigger',
        type: 'POST',
        cache: false,
        async: false,
        dataType: 'json',

        success: function (data) {
            if (data) {
                for (var k in data) {
                    rulot.push(k);
                    rulotsj.push(data[k]);
                }
                console.log(rulot);
                console.log(rulotsj);
                GetBar();
                GetLin(); 
            }
        },
        error: function (msg) {
            //alert(msg);
            GetBar();
            GetLin(); 
        }
    });

}

function funJson2() {
    $.ajax({
		url: '',
		type: 'POST',
        cache: false,
        async: false,
        dataType: 'json',

        success: function (data) {
            if (data) {

                jsonData = data;
                //fungv();
                k = 0;
            }
        },
        error: function (msg) {
            //alert(msg);
		k = 0;
        }
    });

}

function funJson3() {
    $.ajax({
		url: '',
		type: 'POST',
        cache: false,
        async: false,
        dataType: 'json',

        success: function (data) {
            if (data) {

                for (var i = 0; i < data.length; i++) {
                    shijian[i] = data[i].time;
                    piaoshu3[i] = data[i].count;
                    huoliang3[i] = data[i].weight;

                }

                randomData();
            }
        },
        error: function (msg) {
            //alert(msg);
		randomData();
        }
    });

}

//获得表格数据
function fungv() {
    $('#tdg').datagrid({
        data: jsonData.list,
        //fit: true,
        //scrollbarSize:0,
        nowrap: true,
        //autoRowHeight: true,
        //fitColumns: true,
        striped: true,
        rownumbers: false,
        singleSelect: false,
        pagination: false,
        //data:
        columns: [[
             { field: 'orderNo', title: '运单号', align: 'center', width: '20%' },
             { field: 'siteName', title: '网点名称', align: 'center', width: '20%' },
             { field: 'outTime', title: '开单时间', align: 'center', width: '22.5%' },
             { field: 'weight', title: '开单重量', align: 'center', width: '20%' },
             { field: 'piece', title: '开单票数', align: 'center', width: '20%' },   
        ]],

        onLoadSuccess: function (data) {
            $('#tdg').datagrid('loaded');

             //k = 0;
        },

        onExpandRow: function (index, row) {
            //$(".num").addClass("easyui-numberbox");
            //$.parser.parse("#divhide" + index);
        },
        rowStyler: function (index, row) {
            if (index % 2 == 0) {
                return 'background-color:#333333;color:white;font-weight:500;';
            }
            else {
                return 'background-color:rgba(0,0,0,0.7);color:white;font-weight:500;';
            }
        }
    });

    $(".datagrid-header-row td div span").each(function (i, th) {
        var val = $(th).text();
        $(th).html("<label style='font-size: 18px;'>" + val + "</label>");
    });

}

//页面刷新
function GetState() {
    window.location.reload();
}

//滚动插入数据
function GetDg()
{
    if (k < 6) {
        $('#tdg').datagrid('insertRow', {
            row: {
                orderNo: jsonData.list[k].orderNo,
                siteName: jsonData.list[k].siteName,
                outTime: jsonData.list[k].outTime,
                weight: jsonData.list[k].weight,
                piece: jsonData.list[k].piece
            }
        });

        var data = $('#tdg').datagrid('getData');
        $('#tdg').datagrid({
            rowStyler: function (index, row) {
                if (index % 2 == 0) {
                    return 'background-color:#333333;color:white;font-weight:500;';
                }
                else {
                    return 'background-color:rgba(0,0,0,0.7);color:white;font-weight:500;';
                }
            }
        });
        // alert('总数据量:' + data.total)//注意你的数据源一定要定义了total，要不会为undefined，datagrid分页就是靠这个total定义
        //alert('当前页数据量:' + data.rows.length)
        $('#tdg').datagrid('deleteRow', 0);
        $('#tdg').datagrid('scrollTo', data.rows.length - 2);



        k = k + 1;
    }
    else {
        //k = 0;
    }
      $(".datagrid-header-row td div span").each(function (i, th) {
          var val = $(th).text();
          $(th).html("<label style='font-size: 18px;'>" + val + "</label>");
      });
}
