$(document).ready(function() {

    $(".js-pr-create").on('click', function(){
        var $popup = $('#createProject');
        $('.js-clean', $popup).each(function() {
            $(this).val('');
        });
        $popup.modal()
        return false;
    });

    $(".js-pr-submit").on('click', function(){
        $form = $('form#create_form');
        $.ajax({
            type: "POST",
            url: "/ajax/project/create/",
            data: $form.serialize(),
            success: function(data) {
                if (data && data.status == 'ok') {
                    $("#createProject").modal('hide');
                    location.reload();
                }
                else {
                    $("input[name='name']", $form).closest('.control-group').addClass("error");
                }
           }
        });

        return false;
    });


    $(".js-pr-delete").on('click', function(){
        $elem = $(this);
        $.ajax({
            type: "GET",
            url: "/ajax/project/delete/" + $elem.data('pr_id') + "/",
            success: function(data) {
                if(data && data.status == 'ok') {
                   $elem.closest('tr').remove();
                }
                else {
                    $elem.closest('tr').addClass("error");
                }
           }
         });
        return false;
    });

    $(".js-pr-edit").on('click', function(){
        $btn  = $(this);
        $form = $('form#edit_form');
        $tr = $btn.closest('tr');
        $("input[name='name']",  $form).val($(".js-pr-name a", $tr).text());
        $("textarea[name='descr']", $form).val($(".js-pr-descr", $tr).prop('title'));
        $(".js-pr-edit-submit").data('pr_id', $btn.data('pr_id'));
        console.log($(".js-pr-descr", $tr).prop('title'));
        $('#editProject').modal()
        return false;
    });

    $(".js-pr-edit-submit").on('click', function(){
        $btn  = $(this);
        $form = $('form#edit_form');
        $.ajax({
            type: "POST",
            url: "/ajax/project/edit/" + $btn.data('pr_id') +"/",
            data: $form.serialize(),
            success: function(data) {
                if (data && data.status == 'ok') {
                    $("#editProject").modal('hide');
                    location.reload();
                }
                else {
                    $("input[name='name']", $form).closest('.control-group').addClass("error");
                }
           }
        });

        return false;
    });

    document.PARETO = {
        page: 1,
        per_page: 20,
        total: parseInt($("#js-total").data("num"))
    };
    $(".js-more").on('click', function(){
        var $btn = $(this);
        $.ajax({
            type: "GET",
            url: "/ajax/project_row/",
            data: { page: document.PARETO.page + 1 },
            success: function(data) {
                if (data) {
                    $('tbody').append(data);
                    document.PARETO.page++;
                    if (document.PARETO.page * document.PARETO.per_page
                        > document.PARETO.total) {
                        $btn.hide();
                    }
                }
           }
        });

        return false;
    });

    $(".js-search").on('click', function(){
        var $btn  = $(this);
        var $form = $btn.closest("form");

        $.ajax({
            type: "POST",
            url: "/ajax/project_search/",
            data: $form.serialize(),
            success: function(data) {
                if (data) {
                    $('tbody').empty().append(data);
                }
           }
        });

        return false;
    });

});
