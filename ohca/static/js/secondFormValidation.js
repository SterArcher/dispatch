// ============================ handle date of birth and estimated age ==============================

function handleBirthdateField() {
    console.log("handledoublefield")
    var field1 = document.getElementById("id_dateOfBirth");
    var field2 = document.getElementById("id_estimatedAge");
    // var bool = true;
    console.log(field2.value)
    console.log(field1.value)

    if ((field1.value == "" || field1.value == null) && (field2.value == "" || field2.value == null)){
        field1.setAttribute("required", "");
    }
    else {
        field1.removeAttribute("required");
    }
}

document.getElementById("id_dateOfBirth").addEventListener("change", handleBirthdateField)
document.getElementById("id_estimatedAge").addEventListener("change", handleBirthdateField)


// ===========================================


// function handleTreatmentWithdrawn() {
//     var val = document.getElementById("id_treatmentWithdrawn_0").checked;
//     // var death2 = document.getElementById("id_survival30d_1");
//     if (val) {

//         document.getElementById("id_treatmentWithdrawnTimestamp_0").setAttribute("required", "");
//         document.getElementById("id_treatmentWithdrawnTimestamp_1").setAttribute("required", "");
//     }
//     else {
//         document.getElementById("id_treatmentWithdrawnTimestamp_0").removeAttribute("required");
//         document.getElementById("id_treatmentWithdrawnTimestamp_1").removeAttribute("required");
//     }}
// document.getElementById("id_treatmentWithdrawn_0").addEventListener("change", handleTreatmentWithdrawn)
// document.getElementById("id_treatmentWithdrawn_1").addEventListener("change", handleTreatmentWithdrawn)
// document.getElementById("id_treatmentWithdrawn_2").addEventListener("change", handleTreatmentWithdrawn)
// document.getElementById("id_treatmentWithdrawn_3").addEventListener("change", handleTreatmentWithdrawn)

function handleTreatmentWithdrawn1() {
    if (document.getElementById("id_treatmentWithdrawnTimestamp_1").value != null && document.getElementById("id_treatmentWithdrawnTimestamp_1").value != "") {
        document.getElementById("id_adWithdraw_0").checked = false;
        document.getElementById("id_adWithdraw_1").checked = false;
    }
}
function handleTreatmentWithdrawn2() {
    if (document.getElementById("id_adWithdraw_0").checked || document.getElementById("id_adWithdraw_0").checked) {
        document.getElementById("id_treatmentWithdrawnTimestamp_1").value = null;
        document.getElementById("id_treatmentWithdrawnTimestamp_0").value = null;
    }
}
document.getElementById("id_treatmentWithdrawnTimestamp_1").addEventListener("change", handleTreatmentWithdrawn1)
document.getElementById("id_treatmentWithdrawnTimestamp_0").addEventListener("change", handleTreatmentWithdrawn1)
document.getElementById("id_adWithdraw_0").addEventListener("change", handleTreatmentWithdrawn2)
document.getElementById("id_adWithdraw_1").addEventListener("change", handleTreatmentWithdrawn2)

function handleDiscDate() {
    var val = document.getElementById("id_survivalDischarge_0").checked;
    console.log(val)
    if (val) {
        document.getElementById("id_discDate").setAttribute("required", "");
    }
    else {
        document.getElementById("id_discDate").removeAttribute("required");
    }}
document.getElementById("id_survivalDischarge_0").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_1").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_2").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_3").addEventListener("change", handleDiscDate)

// other neuroprognostic tests
function tests() {
    if (document.getElementById("id_otherNeuroprognosticTests_0").checked) {
        document.getElementById("id_neuroprognosticTests").setAttribute("required", "");
    }
    else {
        document.getElementById("id_neuroprognosticTests").removeAttribute("required");
    }}
document.getElementById("id_otherNeuroprognosticTests_0").addEventListener("change", tests)
document.getElementById("id_otherNeuroprognosticTests_1").addEventListener("change", tests)
document.getElementById("id_otherNeuroprognosticTests_2").addEventListener("change", tests)
document.getElementById("id_otherNeuroprognosticTests_3").addEventListener("change", tests)
    

window.onload = function require() {
    checkFormReload();
    handleTreatmentWithdrawn1();
    handleTreatmentWithdrawn2();
    handleDiscDate();
    tests();
}