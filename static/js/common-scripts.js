    function OnEnterButton(evt, inputId)
    {
        evt = (evt) ? evt : window.event;
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if(charCode == 13)
        {
            checkInput(inputId);
            return false;
        }
    }

    function checkInput(inputId)
    {
        if(document.getElementById(inputId).value =='')
        {
            alert("Please, insert a Name of project!");
            return false;
        }
        else
        {
            editUrl(inputId)
        }
    }

    function editUrl(inputId)
    {
        url = '/ajax/' + inputId + '/';
        document.getElementById('create_proj').action = url;
        create_proj.submit();   
    }


    function delProject(proj_id, proj)
    {
        if(confirm("Вы уверены, что хотите удалить проект '" + proj() +"'"))
        {
            document.getElementById('del_proj').action+= proj_id+'/'
            del_proj.submit()
        }
    }

    function checkLength(string , numId)
    {
        if(string.length >= 35)
        {
            document.getElementById('projName_'+ numId).innerHTML = string.substr(0,32) + '...';
        }
    }

    function setProjName()
    {
        curr_date = new Date();
        document.getElementById('addproject').value = 'Project_'+ curr_date.getDate()+ '.' + (curr_date.getMonth()+1) + '.' + curr_date.getFullYear() + '_' + curr_date.getHours() + ":" + curr_date.getMinutes() + ':'+ curr_date.getSeconds();
    }

    function paginator_url(string)
    {
        document.getElementById(string).href='';
    }