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
        $(this).attr('data-search-term', $(this).text().toLowerCase());
    });

    $('.live-search-box').on('keyup', function() {

        var searchTerm = $(this).val().toLowerCase();

        $('.live-search-list .button').each(function() {

            if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
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