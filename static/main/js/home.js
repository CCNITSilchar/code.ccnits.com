    var editor = ace.edit("editor");
    var input_editor = ace.edit("input_editor");
    var output_editor = ace.edit("output_editor");
    var EDITED = false;
    var SAVE_LOCK = false;
    editor.setTheme("ace/theme/twilight");
    input_editor.setTheme("ace/theme/iplastic");
    output_editor.setTheme("ace/theme/iplastic");
    editor.getSession().setMode("ace/mode/c_cpp");
    input_editor.getSession().setMode("ace/mode/plain_text");
    output_editor.getSession().setMode("ace/mode/plain_text");
    document.getElementById('editor').style.fontSize='14px';
    document.getElementById('input_editor').style.fontSize='12px';
    document.getElementById('output_editor').style.fontSize='12px';
    editor.getSession().setUseWrapMode(true);
    editor.setReadOnly(false);  // false to make it editable
    output_editor.setReadOnly(true);
    input_editor.setReadOnly(false);
    editor.$blockScrolling = Infinity;
    input_editor.$blockScrolling = Infinity;
    output_editor.$blockScrolling = Infinity;
    $("#save").click(function(){
        EDITED = true;
        $("#save").html("Saving...");
        save_code();
    });
    editor.commands.addCommand({
         name: 'saveCommand',
         bindKey: {win: 'Ctrl-S',  mac: 'Command-S'},
         exec: function(editor) {
             $("#save").html("Saving...");
             save_code();
         },
    });
    $("#editor").bind("keyup change", function(e) {
        EDITED = true;
        $("#save").html("Saving...");
        save_code();
    });

    $("#language_select").change(function(){
        var item = $(this).val();
        set_language(item);
    });
    $("#compile").click(function(){
        save_code_compile();
    });
    $("#run").click(function(){
        save_code()
        run_code();
    });
    function set_language(item){
        $.ajax({
            type:'GET',
            url:'/sample/',
            data:"lang_id="+item,
            success:function(response){
                if(response.success){
                    if(!EDITED){
                        editor.setValue(response.sample);
                        editor.getSession().setMode("ace/mode/"+response.ace_mode);
                    }else{
                        editor.getSession().setMode("ace/mode/"+response.ace_mode);
                    }
                }
            }
        });
    }
    function save_code(){
        if(!SAVE_LOCK){
            SAVE_LOCK = true;
            $.ajax({
                type:'POST',
                url:'/save_code/',
                dataType:"json",
                data:{"lang_id":$("#language_select").val(),"code":editor.getSession().getValue(), "slug":$("#hidden_slug").val()},
                success:function(response){
                    if(response.success){
                        $("#hidden_slug").val(response.slug);
                        $("#save").html("Saved");
                        SAVE_LOCK = false;
                        $("#code_url_field").html("Code URL : <a href='http://localhost/"+response.slug+"' target='_blank'>http://localhost/"+response.slug+"</a>");
                        $("#downloadLink").attr('href', 'http://localhost/download/'+response.slug+'/');
                    }
                }
            });
        }

    }
    function save_code_compile(){
        if(!SAVE_LOCK){
            SAVE_LOCK = true;
            $.ajax({
                type:'POST',
                url:'/save_code/',
                dataType:"json",
                data:{"lang_id":$("#language_select").val(),"code":editor.getSession().getValue(), "slug":$("#hidden_slug").val()},
                success:function(response){
                    if(response.success){
                        $("#hidden_slug").val(response.slug);
                        $("#save").html("Saved");
                        SAVE_LOCK = false;
                        $("#code_url_field").html("Code URL : <a href='http://localhost/"+response.slug+"' target='_blank'>http://localhost/"+response.slug+"</a>");
                        $("#downloadLink").attr('href', 'http://localhost/download/'+response.slug+'/');
                        compile_code();
                    }
                }
            });
        }

    }
    function compile_code(){
        $("#compile").html("Compiling");
        $.ajax({
            type:'POST',
            url:'/compile/',
            dataType:"json",
            data:{"slug":$("#hidden_slug").val()},
            success:function(response){
                if(response.success){
                    //$("#hidden_slug").val(response.slug);
                    $("#compile").html("<i class='fa fa-rocket'> Compile </i>");
                    output_editor.setValue(response.output, 1);
                }
            }
        });
    }
    function run_code(){
        $("#run").html("Running");
        $.ajax({
            type:'POST',
            url:'/run/',
            dataType:"json",
            data:{"slug":$("#hidden_slug").val(), "custom_input":input_editor.getValue()},
            success:function(response){
                if(response.success){
                    //$("#hidden_slug").val(response.slug);
                    $("#run").html("<i class='fa fa-play'> Run </i>");
                    output_editor.setValue(response.output, 1);
                    $("#time_taken").html(response.time_taken);
                    $("#memory_taken").html(response.memory_taken);
                }
            }
        });
    }