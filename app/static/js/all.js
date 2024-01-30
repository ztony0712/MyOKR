$(document).ready(function() {

    // right side bar
    $(function() {
        $('.sidebarCollapse').on('click', function(event) {
            $('#sidebar, #content').addClass('active');
        });
        // need modification
        $('.close').on('click', function(event) {
            $('#sidebar, #content').removeClass('active');
        });
    });


    // left side bar
    let btn = document.querySelector("#btn");
    let left_sidebar = document.querySelector(".left_sidebar");
    let searchBtn = document.querySelector(".bx-search");

    btn.onclick = function() {
        left_sidebar.classList.toggle("active2");
    }
    searchBtn.onclick = function() {
        left_sidebar.classList.toggle("active2");
    }

    // pop up js
    let specifiedBtns = [...document.querySelectorAll(".button")];
    specifiedBtns.forEach(function(btn) {
        btn.onclick = function() {
            $('.specified').css('display', 'none');
            let correspond = btn.getAttribute('id');
            document.getElementById(correspond)
                .style.display = "block";
        }
    });

    // circle progress
    $(".progress-bar").loading();

    // flash message fade out
    $('.alert').fadeOut(3000);


});

// live search box

jQuery(document).ready(function($) {
    $('.live-search-list .button').each(function() {
        var widgetText = $(this).find('.widget-heading').text().toLowerCase();
        $(this).attr('data-search-term', widgetText);
    });

    $('.live-search-box').on('keyup', function() {
        var searchTerm = $(this).val().toLowerCase();

        $('.live-search-list .button').each(function() {
            if (searchTerm.length < 1 || $(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
        

    });

});


$.ajax({
    async: true,
    beforeSend: function() {
        ShowDiv();
    },
    complete: function() {
        HiddenDiv();
    },
    type: 'GET',
    url: '',
    data: {

    },
    success: function(data) {
        //var obj = JSON.parse(data);
        //var str = JSON.stringify(obj);
    }
});

function ShowDiv() {
    $("#loading").show();
}

function HiddenDiv() {
    $("#loading").hide();
}

function make_clock() {
    
    var canvas = document.getElementById("canvasID");
    var circle = canvas.getContext("2d");
    var width = circle.canvas.width;
    var height = circle.canvas.height;
    var r = width / 2;
    circle.translate(r, r)

    // draw clock Plate
    function drawPlate() {
        circle.save();
        circle.beginPath();
        circle.arc(0, 0, r - 5, 0, 2 * Math.PI);
        circle.lineWidth = 10;
        circle.stroke();

        var hourScales = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2];
        circle.font = '22px Arial';
        circle.textAlign = 'center';
        circle.textBaseline = 'middle';

        // draw scals
        hourScales.forEach(function(scale, index) {
            var rad = 2 * Math.PI / 12 * index;
            var x = Math.cos(rad) * (r - 35);
            var y = Math.sin(rad) * (r - 35);
            circle.fillText(scale, x, y);
        });
        // draw points
        for (var i = 0; i < 60; i++) {
            var rad = 2 * Math.PI / 60 * i;
            var x = Math.cos(rad) * (r - 18);
            var y = Math.sin(rad) * (r - 18);
            circle.beginPath();
            if (i % 5 == 0) {
                circle.fillStyle = 'black';
                circle.arc(x, y, 3, 0, 2 * Math.PI);
            } else {
                circle.fillStyle = 'grey';
                circle.arc(x, y, 2, 0, 2 * Math.PI);
            }
            circle.fill();
        }
    }

    // draw hands on plante
    function hourHand(hour, minute) {
        circle.save();
        circle.beginPath();
        var hrad = 2 * Math.PI / 12 * hour;
        var mrad = 2 * Math.PI / 12 / 60 * minute;
        circle.rotate(hrad + mrad);
        circle.lineWidth = 8;
        circle.lineCap = 'round';
        circle.moveTo(0, 0);
        circle.lineTo(0, -r / 2);
        circle.stroke();
        circle.restore();
    }

    function minuteHand(minute, second) {
        circle.save();
        circle.beginPath();
        var mrad = 2 * Math.PI / 60 * minute;
        var srad = 2 * Math.PI / 60 /60 * second;
        circle.rotate(mrad + srad);
        circle.lineWidth = 4;
        circle.lineCap = 'round';
        circle.moveTo(0, 0);
        circle.lineTo(0, -2 * r / 3);
        circle.stroke();
        circle.restore();
    }

    function secondHand(second) {
        circle.save();
        circle.beginPath();
        var rad = 2 * Math.PI / 60 * second;
        circle.rotate(rad);
        circle.lineWidth = 2;
        circle.lineCap = 'round';
        circle.moveTo(0, 30);
        circle.lineTo(0, -4 * r / 5);
        circle.strokeStyle = 'red'
        circle.stroke();
        circle.restore();
    }

    function middlePoint() {
        circle.beginPath();
        circle.fillStyle = "white";
        circle.arc(0, 0, 5, 0, 2 * Math.PI)
        circle.fill();
    }

    // access time and draw the whole clock
    function draw() {
        circle.clearRect(-r, -r, width, height);
        var time = new Date();
        var hour = time.getHours();
        var minute = time.getMinutes();
        var second = time.getSeconds();
        drawPlate();
        hourHand(hour, minute);
        minuteHand(minute, second);
        secondHand(second);
        middlePoint();
        circle.restore();
    }

    draw();
    setInterval(draw, 1000);

}
make_clock();