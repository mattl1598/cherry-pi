function ReadForm() {
	var x = document.getElementById("cc-form");

	var dict1 = {
		"cc-email": {"type": "text", "regex": "^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,5})$"},
		"cc-conf-email": {"type": "text_match", "matches": "cc-email"},
		"cc-adults-name": {"type": "text", "regex": "^([A-Za-z\\-]+)(\\s[A-Za-z\\-]+)+$"},
		"cc-childs-name": {"type": "text", "regex": "^[A-z\\-]+$"},
		"cc-childs-age": {"type": "number", "min": 0, "max": 11},
		"cc-image": {"type": "image"},
		"cc-tcs": {"type": "checkbox", "required": true},
		"cc-mail-list": {"type": "checkbox", "required": false}
	};
	var error_dict = {
		"cc-email": {"id": "email_error", "border-id": "cc-email", "message": "Please enter a valid email."},
		"cc-conf-email": {"id": "email_conf_error", "border-id": "cc-conf-email", "message": "Email addresses must match."},
		"cc-adults-name": {"id": "fullname_error", "border-id": "cc-adults-name", "message": "Please enter the Parent/Guardians full name."},
		"cc-childs-name": {"id": "firstname_error", "border-id": "cc-childs-name", "message": "Only enter the childs first name."},
		"cc-childs-age": {"id": "age_error", "border-id": "cc-childs-age", "message": "Childs age must be between 0 and 11 to enter."},
		"cc-image": {"id": "file_error", "border-id": "cc-file", "message": "Please select a png or jpg/jpeg image file."},
		"cc-tcs": {"id": "tcs_error", "border-id": "cc-tcs", "message": "You must agree to the Terms and conditions to enter."}
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
					// console.log(id);
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
					// console.log(id);
					error_out.push(id);
				}
			}
		} else if (dict1[id]["type"] == "text_match") {
			val = element.value;
			if (val !== dict2[dict1[id]["matches"]]) {
				dict2["valid"] = false;
				// console.log(id);
				error_out.push(id);
			}
		} else if (dict1[id]["type"] == "number") {
			val = Number(element.value);
			if (val > dict1[id]["max"] || element.value == "" || val < dict1[id]["min"]) {
				dict2["valid"] = false;
				// console.log(id);
				error_out.push(id);
			}
		} else if (dict1[id]["type"] == "image"){
			val = element.value;
			var sub = val.substring(0, 12);
			// console.log(sub)
			if (sub == "data:image/p" || sub == "data:image/j") {
				// console.log("valid image")
			} else {
				dict2["valid"] = false;
				// console.log(id);
				error_out.push(id);
			}

		}
		dict2[id] = val;
	}
	if (dict2["valid"]) {
		// console.log(dict2);
		var myArr = uploadForm(dict2, x);
	} else {
		// console.log("Not Valid")
		for (var id in error_out) {
			// console.log(error_out[id]);
			document.getElementById(error_dict[error_out[id]]["border-id"]).classList.add('cc-error-border');
			document.getElementById(error_dict[error_out[id]]["id"]).innerHTML = error_dict[error_out[id]]["message"];
		}
	}
	// alert('test');
	// window.location.replace("/testing/submitted.html");
}

function uploadForm(dict, x) {
	x.style.display = "none";
	var y = document.getElementById("cc-uploading");
	y.style.display = "block";
	var xmlhttp = new XMLHttpRequest();
	var url = "http://larby.co.uk/sp-entry";

    xmlhttp.open("POST", url);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(dict));

	xmlhttp.onreadystatechange = function() {
		xmlhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			    var myArr = JSON.parse(this.responseText);
			    console.log(myArr);
				if (myArr["response_code"] == 200) {
					window.location.replace(document.getElementById("cc-success-url").value);
					console.log("Done")
				} else {
					y.style.display = "none";
					x.style.display = "flex";
					alert("Something went wrong. Please try again. \n" +
					"If this keeps happening, contact Silchester Players on Facebook or Twitter.")
				}
		    }
		};
	}
}

function encodeImageFileAsURL(element) {
    if(element.files[0].size > 9961472){
       alert("File is too big!");
       this.value = "";
    } else {
        var file = element.files[0];
		var reader = new FileReader();
		reader.onloadend = function() {
			document.getElementById("cc-image").value = reader.result
			// console.log('RESULT', reader.result)
		}
		reader.readAsDataURL(file);
    }
}

document.addEventListener("DOMContentLoaded", function() {removeBR()});

function removeBR() {
	// console.log("remove br")
	var formElement = document.getElementById("cc-form");
	var collection = formElement.getElementsByTagName("br");
	var list = Array.from(collection)
	// console.log(list.length)
	// console.log(list)
	for (var element of list) {
		if (element.className !== "") {
			var index = list.indexOf(element);
			if (index > -1) {
				list.splice(index, 1);
			}
		}
	}
	// console.log(list.length);
	for (var element of list) {
		// console.log(element);
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
	// console.log(list.length)
	// console.log(list)
}
