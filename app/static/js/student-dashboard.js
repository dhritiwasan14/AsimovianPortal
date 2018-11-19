var selected = 'Dashboard';
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

function clickPageName(e) {
	var editableText = $("<input type=\"text\" name=\"edtPageName\" id=\"txtPageName\" class=\"form-control\"  style=\"line-height: 55px; height: 55px; vertical-align: middle; font-size:24px;\">");
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
	$.get('/student-dashboard/get-page/' + id, function(response) {
		if(response.success) {

		}
	});
}

function loadPages() {
	$.get(window.location.href  + '/get-pages', function(response) {
		if(response.success) {
			var pageHTML = "";

			for(var i = 0; i < response.pages.length; i++) {
				pageHTML += "<tr>";
				pageHTML += "<td>" + (i + 1) + "</td>";
				pageHTML += "<td>" + response.pages[i].name + "</td>";
				pageHTML += "<td>" + response.pages[i].last_update + "</td>";
				if(response.pages[i].is_main) {
					pageHTML += "<td><span class=\"text-success\">Main Page</span></td>";
				}
				else {
					pageHTML += "<td><button class=\"btn btn-success main-button\" id=\"" + response.pages[i].id + "\">Set As Main</button></td>";
				}
				pageHTML += "<td><a href=\"#\" class=\"edit-page\" id=\"" + response.pages[i].id + "\"><i class=\"fas fa-edit\"></i></a></td>";
				pageHTML += "<td><a href=\"#\" class=\"delete-page\" id=\"" + response.pages[i].id + "\"><i class=\"fas fa-trash-alt\"></i></a></td>";
				pageHTML += "</tr>";
			}

			if(response.pages.length == 0) {
				pageHTML = "<tr><td colspan=6>You have not added any pages!</td></tr>"
			}
			$("#tblPages").html(pageHTML);
		}
	});
}

// Set up event listener for when the DOM is fully loaded
$(document).ready(function() {
	// Select the provided event, or the first event as appropriate
	select(selected);
	loadPages();

	$(".side-nav-item").click(function(e) {
		select($(this).attr('id').substring(3));
	});

	$("#txtPageName").click(clickPageName);
});