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

// Set up event listener for when the DOM is fully loaded
$(document).ready(function() {
	// Select the provided event, or the first event as appropriate
	select(selected);
	
	$(".side-nav-item").click(function(e) {
		select($(this).attr('id').substring(3));
	});

	$("#btnAddPage").click(function(e) {
		$("#pagPageList, #pagPageEdit").animate({
			'left': '-=500vh'
		});
	});
	$("#btnBack").click(function(e) {
		savePage();
		$("#pagPageList, #pagPageEdit").animate({
			'left': '+=500vh'
		});
	});

	$("#txtPageName").click(clickPageName);
});