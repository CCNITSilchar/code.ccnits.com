var editor = ace.edit("editor");
    var input_editor = ace.edit("input_editor");
    var output_editor = ace.edit("output_editor");
    var EDITED = false;
    var SAVE_LOCK = false;
    editor.setTheme("ace/theme/twilight");
    input_editor.setTheme("ace/theme/iplastic");
    output_editor.setTheme("ace/theme/iplastic");
    input_editor.getSession().setMode("ace/mode/plain_text");
    output_editor.getSession().setMode("ace/mode/plain_text");
    document.getElementById('editor').style.fontSize='14px';
    document.getElementById('input_editor').style.fontSize='12px';
    document.getElementById('output_editor').style.fontSize='12px';
    editor.getSession().setUseWrapMode(true);
    editor.setReadOnly(true);  // false to make it editable
    output_editor.setReadOnly(true);
    input_editor.setReadOnly(false);
    editor.$blockScrolling = Infinity;
    input_editor.$blockScrolling = Infinity;
    output_editor.$blockScrolling = Infinity;

    $("#compile").click(function(){
        compile_code();
    });
    $("#run").click(function(){
        run_code();
    });
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