function ReadForm() {
	var x = document.getElementById("cc-form");
	var dict1 = {
		"cc-email": {"type": "text", "regex": "^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,5})$"},
		"cc-adults-name": {"type": "text", "regex": "^([A-Za-z\\-]+)(\\s[A-Za-z\\-]+)+$"},
		"cc-childs-name": {"type": "text", "regex": "^[A-z\\-]+$"},
		"cc-childs-age": {"type": "number", "max": 11},
		"cc-image": {"type": "image"},
		"cc-tcs": {"type": "checkbox", "required": true},
		"cc-mail-list": {"type": "checkbox", "required": false}
	};
	var error_dict = {
		"cc-email": {"id": "email_error", "border-id": "cc-email", "message": "Please enter a valid email."},
		"cc-adults-name": {"id": "fullname_error", "border-id": "cc-adults-name", "message": "Please enter the Parent/Guardians full name."},
		"cc-childs-name": {"id": "firstname_error", "border-id": "cc-childs-name", "message": "Only enter the childs first name."},
		"cc-childs-age": {"id": "age_error", "border-id": "cc-childs-age", "message": "Childs age must be below 11 to enter."},
		"cc-image": {"id": "file_error", "border-id": "cc-file", "message": "Please select a png or jpg/jpeg image file."},
		"cc-tcs": {"id": "tcs_error", "border-id": "cc-adults-name", "message": "You must agree to the Terms and conditions to enter."}
	};

	var dict2 = {"valid": true};
	var error_out = [];
	var val;
	var element;

	for (let id in error_dict) {
		if (error_dict[id]["id"] !== null) {
			// console.log(error_dict[id]["id"])
			document.getElementById(error_dict[id]["border-id"]).classList.remove('cc-error-border');
			document.getElementById(error_dict[id]["id"]).innerHTML = "";
		}
	}

	for (let id in dict1) {
		element = document.getElementById(id);
		// checkbox
		if (dict1[id]["type"] == "checkbox") {
			if (element.checked) {
				val = true;
			} else {
				if (dict1[id]["required"]){
					dict2["valid"] = false;
					console.log(id);
					error_out.push(id);
				} else {
					val = false;
				}

			}
		} else if (dict1[id]["type"] == "text") {
			val = element.value;
			if (dict1[id]["regex"]) {
				var re = RegExp(dict1[id]["regex"]);
				if (!re.test(val)) {
					dict2["valid"] = false;
					console.log(id);
					error_out.push(id);
				}
			}

		} else if (dict1[id]["type"] == "number") {
			val = Number(element.value);
			if (val > dict1[id]["max"] || element.value == "") {
				dict2["valid"] = false;
				console.log(id);
				error_out.push(id);
			}
		} else if (dict1[id]["type"] == "image"){
			val = element.value;
			var sub = val.substring(0, 12);
			console.log(sub)
			if (sub == "data:image/p" || sub == "data:image/j") {
				console.log("valid image")
			} else {
				dict2["valid"] = false;
				console.log(id);
				error_out.push(id);
			}

		}
		dict2[id] = val;
	}
	if (dict2["valid"]) {
		console.log(dict2);
		window.location.replace(document.getElementById("cc-success-url").value);
	} else {
		console.log("Not Valid")
		for (var id in error_out) {
			console.log(error_out[id]);
			document.getElementById(error_dict[error_out[id]]["border-id"]).classList.add('cc-error-border');
			document.getElementById(error_dict[error_out[id]]["id"]).innerHTML = error_dict[error_out[id]]["message"];
		}
	}
	// alert('test');
	// window.location.replace("/testing/submitted.html");
}

function encodeImageFileAsURL(element) {
	var file = element.files[0];
	var reader = new FileReader();
	reader.onloadend = function() {
		document.getElementById("cc-image").value = reader.result
		console.log('RESULT', reader.result)
	}
	reader.readAsDataURL(file);
}

document.addEventListener("DOMContentLoaded", function() {removeBR()});

function removeBR() {
	console.log("remove br")
	var formElement = document.getElementById("cc-form");
	var collection = formElement.getElementsByTagName("br");
	var list = Array.from(collection)
	console.log(list.length)
	console.log(list)
	for (var element of list) {
		if (element.className !== "") {
			var index = list.indexOf(element);
			if (index > -1) {
				list.splice(index, 1);
			}
		}
	}
	console.log(list.length);
	for (var element of list) {
		console.log(element);
		element.remove();
	}

	var collection = formElement.getElementsByTagName("br");
	var list = Array.from(collection)

	for (var element of list) {
		if (element.className !== "") {
			var index = list.indexOf(element);
			if (index > -1) {
				list.splice(index, 1);
			}
		}
	}
	console.log(list.length)
	console.log(list)
}