
function fetch_all_exam() {
    request_time = 0;
    var wait_message = "获取试卷中: ";
    document.getElementById("question-all-div").innerHTML = wait_message;
    wait_interval = setInterval(function() {
        request_time += 1;
        var new_wait_message = wait_message + request_time + "秒";
        document.getElementById("question-all-div").innerHTML = new_wait_message;
    }, 1000);

    $.ajax({
        url:"/exam/all",
        method:"GET",
        success:function(data) {
            clearInterval(wait_interval);
            var returned = JSON.parse(data);
            if (returned["status"] == 0) {
                document.getElementById("question-all-div").innerHTML = "获取成功";
            }
        },
        error:function(jqXHR, textStatus, errorThrown) {
            clearInterval(wait_interval);
            document.getElementById("question-all-div").innerHTML = "ajax error";
        }
    });
}


function fetch_new_exam() {
    request_time = 0;
    var wait_message = "获取试卷中:";
    document.getElementById("question-new-div").innerHTML = wait_message;
    wait_interval = setInterval(function() {
        request_time += 1;
        var new_wait_message = wait_message + request_time + "秒";
        document.getElementById("question-new-div").innerHTML = new_wait_message;
    }, 1000);

    $.ajax({
        url:"/exam/new",
        method:"GET",
        success:function(data) {
            clearInterval(wait_interval);
            var returned = JSON.parse(data);
            if (returned["status"] == 0) {
                document.getElementById("question-new-div").innerHTML = "获取成功";
            }
        },
        error:function(jqXHR, textStatus, errorThrown) {
            clearInterval(wait_interval);
            document.getElementById("question-new-div").innerHTML = "ajax error";
        }
    });
}