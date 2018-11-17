var selected = 'Dashboard';

// Function that loads the appropriate event when selected and updates the UI to reflect it
function select(pane) {
	$("#nav" + selected).removeClass('selected'); // "De-select" the row of the previously selected event
	$("#nav" + selected).find(".nav-item-icon").attr('src', '/static/img/' + selected.toLowerCase() + '-24px.png');
	selected = pane; // Set the selected event to the event that was clicked
	$("#nav" + pane).addClass('selected'); // "Select" the row of the clicked event
	$("#nav" + selected).find(".nav-item-icon").attr('src', '/static/img/selected-' + selected.toLowerCase() + '-24px.png');
	// Load the event data into the page
	loadPane('pan' + pane);
}

function loadPane(paneId) {
	$(".pane").hide();
	$("#" + paneId).show();
}

function saveClass() {
	var className = $("#edtClassName").val();
	var deadline = $("#edtDeadline").val();
	var groupJSON = $("#hdnGroupJSON").val();
	
	// TODO: Check if empty inputs

	deadline = moment(deadline).format('YYYY-MM-DD HH:mm:ss');
	
	$.post("/dashboard/create-class", {class_name: className, deadline: deadline, groupJSON: groupJSON}, function(data) {
		console.log(data);
		$("#btnBack").click();
		reloadClasses();
	});
}

function viewClass(id) {
	$.get('/dashboard/get-class/' + id, function(response) {
		$("#edtViewClassName").val(response.class.name);
		$("#edtViewDeadline").val(moment(response.class.deadline).format('YYYY-MM-DDTHH:mm'));

		var groupHTML = "";

        for(var i = 0; i < response.class.groups.length; i++) {
        	groupHTML += "<tr>";
        	groupHTML += "<td>" + (i + 1) + "</td>";
        	groupHTML += "<td>" + response.class.groups[i].username + "</td>";
        	groupHTML += "<td>" + response.class.groups[i].members + "</td>";
        	groupHTML += "<td><button class=\"reset-group-password btn btn-danger\" id=\"" + response.class.groups[i].username + "\">Reset Password</button></td>"
        	groupHTML += "<td><a href=\"/" + response.class.groups[i].username + "\" target=\"_blank\"><i class=\"fas fa-eye\" title=\"View group's wiki\"></i></a></td>";
        	groupHTML += "<td><a href=\"/student-dashboard/" + response.class.groups[i].username +"\" target=\"_blank\"><i class=\"fas fa-columns\" title=\"View group's dashboard\"></i></a></td>";
        	groupHTML += "<td><a href=\"#\"><i class=\"fas fa-edit\" title=\"Edit group's settings\"></a></td>";
        	groupHTML += "<td><a href=\"#\"><i class=\"fas fa-trash-alt\" title=\"Delete group\"></a></td>";
        	groupHTML += "</tr>";
        }

        $("#tblViewGroups").html(groupHTML);
        $("#hdnViewGroupJSON").val(JSON.stringify(response.class.groups));

		$(".reset-group-password").click(function(e) {
			e.preventDefault();
			
			var username = $(this).attr('id');
			$.post('/dashboard/reset-group-password', {username: username}, function(response) {
				if(response.success) {
					// TODO: Display succesful reset message
				}
			});
		});
	})
	$("#pagClassView, #pagClassList, #pagClassCreate").animate({
		'left': "+=" + ($(".sliding-content").width() * 0.335) + "px"
	});
}

function reloadClasses() {
	$.get('/dashboard/get-classes', function(response) {
		var classHTML = "";

		for(var i = 0; i < response.classes.length; i++) {
			classHTML += "<tr>";
			classHTML += "<td>" + (i + 1) + "</td>";
			classHTML += "<td>" + response.classes[i].name + "</td>";
			classHTML += "<td>0</td>";
			classHTML += "<td class=\"date-cell\">" + response.classes[i].deadline + "</td>";
			classHTML += "<td><a href=\"#\"><i class=\"fas fa-edit edit-class\" id=\"" + response.classes[i].id + "\"></i></a></td>";
			classHTML += "<td><a href=\"#\"><i class=\"fas fa-trash-alt delete-class\" id=\"" + response.classes[i].id + "\"></i></a></td>";
			classHTML += "</tr>";
		}

		if(response.classes.length == 0) {
			classHTML = "<tr colspan=6><td>You have not created any classes!</td></tr>";
		}

		$("#tblClasses").html(classHTML);

		$(".date-cell").each(function() {
			$(this).html(moment($(this).html()).format('MMMM Do YYYY, h:mm:ss a'));
		});

		$('.edit-class').click(function(e) {
			e.preventDefault();

			var id = $(this).attr('id');
			viewClass(id);
		});
		
		$('.delete-class').click(function(e) {
			e.preventDefault();

			var id = $(this).attr('id');
			$("#hdnDeleteClass").val(id);
			$("#mdlDeleteClass").modal();
		});
	});
}
// Set up event listener for when the DOM is fully loaded
$(document).ready(function() {
	// Select the provided event, or the first event as appropriate
	select(selected);
	reloadClasses();

	$("#pagClassView, #pagClassList, #pagClassCreate").animate({
		'left': "-=" + ($(".sliding-content").width() * 0.335) + "px"
	}, 0);
	
	$(".side-nav-item").click(function(e) {
		select($(this).attr('id').substring(3));
	});

	$("#btnAddClass").click(function(e) {
		$("#pagClassList, #pagClassCreate").animate({
			'left': "-=" + ($(".sliding-content").width() * 0.335) + "px"
		});
	});
	$("#btnBack").click(function(e) {
		$("#pagClassList, #pagClassCreate").animate({
			'left': "+=" + ($(".sliding-content").width() * 0.335) + "px"
		});
	});

	$("#btnViewBack").click(function(e) {
		$("#pagClassView, #pagClassList, #pagClassCreate").animate({
			'left': "-=" + ($(".sliding-content").width() * 0.335) + "px"
		});
	})

	$("#btnUploadGroups").click(function(e) {
		e.preventDefault();	
		$("#group-file").click();
	});

	$("#btnAddGroup").click(function(e) {
		e.preventDefault();
	})

	$("#group-file").change(function(e) {
		e.preventDefault();

		var formData = new FormData();
		formData.append("group-file", $("#group-file")[0].files[0]);

		$.ajax({
	        url: '/dashboard/add-groups',
	        data: formData,
	        contentType: false,
	        processData: false,
	        type: 'POST',
	        success: function ( data ) {
	            response = data;

	            var groupHTML = "";

	            for(var i = 0; i < response.length; i++) {
	            	groupHTML += "<tr>";
	            	groupHTML += "<td>" + (i + 1) + "</td>";
	            	groupHTML += "<td>" + response[i].username + "</td>";
	            	groupHTML += "<td>" + response[i].members + "</td>";
	            	groupHTML += "<td>---</td>"
	            	groupHTML += "<td><a href=\"#\"><i class=\"fas fa-edit\"></a></td>";
	            	groupHTML += "<td><a href=\"#\"><i class=\"fas fa-trash-alt\"></a></td>";
	            	groupHTML += "</tr>";
	            }

	            $("#tblGroups").html(groupHTML);
	            $("#hdnGroupJSON").val(JSON.stringify(response));
	        }
	    });
	});

	$("#btnSaveClass").click(function(e) {
		e.preventDefault();

		saveClass();
	});

	$('.add-member').click(function(e) {
		e.preventDefault();
		$('.modal-form').append('<br><div class="row"><div class="col-4"><label>Member Student ID:</label></div><div class="col-8"><input type="text" class="form-control member-id-input"></div></div>');
	});

	$("#btnConfirmDeleteClass").click(function(e) {
		e.preventDefault();

		var id = $("#hdnDeleteClass").val();

		$.post('/dashboard/delete-class', {id: id}, function(response) {
			if(response.success) {
				reloadClasses();
				$("#mdlDeleteClass").modal('hide');
			}
		})
	});
});