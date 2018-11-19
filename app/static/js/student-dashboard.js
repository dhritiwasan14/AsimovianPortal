var selected = 'Dashboard';
new ClipboardJS('.get-link');
var simplemde = new SimpleMDE(
	{
		element: document.getElementById('page'),
		previewRender: function (plaintext, preview) {
			setTimeout(function() {
				preview.innerHTML = converter.makeHtml(plaintext);
			}, 250);
			return 'Loading...';
		}
	}
);
		// Function that loads the appropriate event when selected and updates the UI to reflect it
function select(pane) {
	$("#nav" + selected).removeClass('selected'); // "De-select" the row of the previously selected event
	selected = pane; // Set the selected event to the event that was clicked
	$("#nav" + pane).addClass('selected'); // "Select" the row of the clicked event
	// Load the event data into the page
	loadPane('pan' + pane);
}

function loadPane(paneId) {
	$(".pane").hide();
	$("#" + paneId).show();
}


function set_new_image(image_url) {
	$('#lightgallery').append('<li class="col-xs-6 col-sm-4 col-md-2" style="background-color: white;"><img class="img-responsive get-link" src="'+image_url+'" data-clipboard-text="localhost:5000'+image_url+'" alt="Thumb-1"></li>')
	
	lightGallery(document.getElementById('demo-gallery'), {
		thumbnail: true,
		cssEasing:'cubic-bezier(0.680, -0.550, 0.265, 1.550)',
		closable:false,
		enableTouch: false,
		enableDrag: false,
		loop:true,
		speed:1500
	});
	new ClipboardJS('.get-link');
	$(".get-link").click(function(e) {
		alert("URL has been copied. ")
	});
}


var editableText = $("<input type=\"text\" name=\"edtPageName\" id=\"txtPageName\" class=\"form-control\"  style=\"line-height: 55px; height: 55px; vertical-align: middle; font-size:24px;\">");

function clickPageName(e) {
	var original = $(this);
	editableText.val($(this).html())
	$(this).replaceWith(editableText);
	editableText.focus();
	editableText.keypress(function(e) {
		if(e.keyCode == 13) {
			original.html($(this).val());
			$(this).replaceWith(original);
			$(this).val("");

			savePage();

			original.click(clickPageName);

			return false;
		}

		return true;
	});
}

function savePage() {
	// POST page data to backend
	// Reload page list table
}

function loadPage(id) {
	$.get(window.location.href  + '/get-page/' + id, function(response) {
		if(response.success) {
			$("#txtPageName").html(response.page.name);
			editableText.val(response.page.name);
			simplemde.value(response.page.content);
			$("#pagPageList, #pagPageCreate").animate({
				'left': "-=" + ($(".sliding-content").width() * 0.51) + "px"
			});
		}
	});
}

function loadPages() {
	$.get(window.location.href  + '/get-pages', function(response) {
		if(response.success) {
			var pageHTML = "";

			for(var i = 0; i < response.pages.length; i++) {
				pageHTML += "<tr>";
				pageHTML += "<td style=\"vertical-align: middle\">" + (i + 1) + "</td>";
				pageHTML += "<td style=\"vertical-align: middle\">" + response.pages[i].name + "</td>";
				pageHTML += "<td style=\"vertical-align: middle\">" + response.pages[i].last_update + "</td>";
				if(response.pages[i].is_main) {
					pageHTML += "<td><span class=\"text-success\">Main Page</span></td>";
				}
				else {
					pageHTML += "<td><button class=\"btn btn-success main-button\" id=\"" + response.pages[i].id + "\">Set As Main</button></td>";
				}
				pageHTML += "<td style=\"vertical-align: middle\"><a href=\"#\" class=\"edit-page\" id=\"" + response.pages[i].id + "\"><i class=\"fas fa-edit\"></i></a></td>";
				pageHTML += "<td style=\"vertical-align: middle\"><a href=\"#\" class=\"delete-page\" id=\"" + response.pages[i].id + "\"><i class=\"fas fa-trash-alt\"></i></a></td>";
				pageHTML += "</tr>";
			}

			if(response.pages.length == 0) {
				pageHTML = "<tr><td colspan=6>You have not added any pages!</td></tr>"
			}
			$("#tblPages").html(pageHTML);

			$(".edit-page").click(function(e) {
				e.preventDefault();

				var id = $(this).attr('id');
				loadPage(id);
			});

			$(".delete-page").click(function(e) {
				e.preventDefault();

				$("#hdnDeletePage").val($(this).attr('id'));
				$("#mdlDeletePage").modal();
			})
		}
	});
}

// Set up event listener for when the DOM is fully loaded
$(document).ready(function() {
	// Select the provided event, or the first event as appropriate
	select(selected);
	loadPages();

	$("#btnAddPage").click(function(e) {
		$("#pagPageList, #pagPageCreate").animate({
			'left': "-=" + ($(".sliding-content").width() * 0.51) + "px"
		});
	});
	$("#btnBack").click(function(e) {
		$("#pagPageList, #pagPageCreate").animate({
			'left': "+=" + ($(".sliding-content").width() * 0.51) + "px"
		});
		$("#txtPageName").html("New Page");
		editableText.val("New Page");
		simplemde.value("");
	});

	$("#btnViewWiki").click(function(e) {
		var pathArray = window.location.href.split('/');
		window.open(
			"/wiki/" + pathArray[pathArray.length - 1] + "/",
			'_blank'
		);
	});

	$(".side-nav-item").click(function(e) {
		select($(this).attr('id').substring(3));
	});

	$("#txtPageName").click(clickPageName);

	$("#btnConfirmDeletePage").click(function(e) {
		e.preventDefault();

		var id = $("#hdnDeletePage").val();
		$(this).html('<i class=\"fas fa-sync-alt spinning\"></i> Deleting').attr('disabled', true);
		$.post(window.location.href + "/delete-page", {id: id}, function(response) {
			if(response.success) {
				$("#btnConfirmDeletePage").html("Delete Page").removeAttr('disabled');
				$("#mdlDeletePage").modal('hide');
				loadPages();
			}
		});
	});

	lightGallery(document.getElementById('demo-gallery'), {
		thumbnail: true,
		cssEasing: 'cubic-bezier(0.680, -0.550, 0.265, 1.550)',
		closable: false,
		enableTouch: false,
		enableDrag: false,
		loop: true,
		speed: 1500
	});

	$('input').change(function(e) {
		var filename = this.files[0].name;
		console.log(filename);
		$('.custom-file-label').text(filename);
	});

	$('.upload-image').click(function(e) {
		e.preventDefault();

		var image = $('input')[0];
		var file = image.files[0];
		var formData = new FormData();
		formData.append('image', file);
		$.ajax({
			url: '/upload-image/{{username}}',
			data: formData,
			cache: false,
			contentType: false,
			processData: false,
			type: 'POST',
			success: function(data){
				alert(data);
			}
		});	
	});

	$('#btnSave').click(function(e) {
		e.preventDefault();
		var formData = new FormData();
		// need to get it from every CodeMirror-line
		var content = simplemde.value();
		
		formData.append('content', content);
		formData.append('title', editableText.val());

		$(this).html("<i class=\"fas fa-sync-alt spinning\"></i> Saving").attr('disabled', true);
		$.ajax({url: window.location.href + "/add-page",
	        data: formData,
	        contentType: false,
	        processData: false,
	        type: 'POST',
	        success: function (response) {
	            if(response.success) {
	            	$("#btnSave").html("Save Page").removeAttr('disabled');
	            	loadPages();
	            	$("#pagPageList, #pagPageCreate").animate({
						'left': "+=" + ($(".sliding-content").width() * 0.51) + "px"
					});
	            }
	        }
	    });
    });
});