window.onload = function() {
    var converter = new showdown.Converter();
    var pad = document.getElementById('pad');
    var markdownArea = document.getElementById('markdown');   

    var convertTextAreaToMarkdown = function(){
        var markdownText = pad.value;
        html = converter.makeHtml(markdownText);
        markdownArea.innerHTML = html;
    };

    pad.addEventListener('input', convertTextAreaToMarkdown);

    convertTextAreaToMarkdown();
};

function myFunction() {
    var x = document.getElementById("myFile");
    x.disabled = true;
}

$('.image').change(function() {
    var urlString = $.ajax({
        type: "POST",
        url: '/student-editor/{{username}}',
        success: setURLString,
        dataType: 'json'
    });
    
})