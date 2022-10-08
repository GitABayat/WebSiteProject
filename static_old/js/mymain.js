// When the user scrolls down 20px from the top of the document, slide down the navbar
// When the user scrolls to the top of the page, slide up the navbar (50px out of the top view)
// window.onscroll = function () { scrollFunction() };

// function scrollFunction() {
//   if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
//     document.getElementById("navbar").style.top = "0";
//   } else {
//     document.getElementById("navbar").style.top = "-200px";
//   }
// }

/**
 * Created by arman on 7/24/16.
 */
$(function () {
  $('.jalali_date-date').datepicker({
    dateFormat: 'yy-mm-dd',
    changeMonth: true,
    changeYear: true,
    // showOn: 'button',
    // buttonImage: '../jquery.ui.datepicker.jalali_date/themes/base/images/',
    // buttonImageOnly: true
  });
});


// group-delete


{/* //////////////////////////////////////////////////////// */ }
{/* request_status */ }
$("#checkAllproducts").click(function () {
  $('#productsTable input:checkbox').not(this).prop('checked', this.checked);
});


$("#productsBtnDelete").click({
  ModelName: "products",
  RedirectPath: "product", TableId: "productsTable"
}, DeleteRecords);


{/* request_type */ }
$("#productsgroupsBtnDelete").click({
  ModelName: "productsgroups",
  RedirectPath: "productsgroupsLV", TableId: "productsgroupsTable"
}, DeleteRecords);

{/* Group */ }
$("#checkAllGroup").click(function () {
  $('#GroupTable input:checkbox').not(this).prop('checked', this.checked);
});
$("#GroupBtnDelete").click({
  ModelName: "Group",
  RedirectPath: "GroupLv", TableId: "GroupTable"
}, DeleteRecords);

{/* Group_Detail */ }
$("#checkAllGroup_Detail").click(function () {
  $('#Group_DetailTable input:checkbox').not(this).prop('checked', this.checked);
});
$("#Group_DetailBtnDelete").click({
  ModelName: "Group_Detail",
  RedirectPath: "Group_DetailLisview", TableId: "Group_DetailTable"
}, DeleteRecords);

{/* Form */ }
$("#checkAllForm").click(function () {
  $('#FormTable input:checkbox').not(this).prop('checked', this.checked);
});
$("#FormBtnDelete").click({
  ModelName: "Form",
  RedirectPath: "formLv", TableId: "FormTable"
}, DeleteRecords);

{/* users */ }
$("#checkAllusers").click(function () {
  $('#usersTable input:checkbox').not(this).prop('checked', this.checked);
});
$("#usersBtnDelete").click({
  ModelName: "User",
  RedirectPath: "users", TableId: "usersTable"
}, DeleteRecords);
////////////////////////////////////////////////////

function DeleteRecords(event) {
  var message1 = "آیا از حذف سطر های انتخاب شده مطمئن هستید؟\n" +
    $('table .selected').length + ' ردیف انتخاب شد\n';
  var message = '';
  $("#example .selected td:first-child").each(function () {
    var row = $(this).closest("tr")[0];
    if (row.cells[1].innerHTML) {
      message += '' + row.cells[1].innerHTML + ',';
    }
    message += "";
  });
  message += '';

  var txt;
  if (message) {

    var r = confirm(message1 + message);

    if (r == true) {
      window.location.replace = "window-location.html";
      txt = window.location.replace("/DeleteRecords/" + message + "/" + event.data.ModelName + "/" + event.data.RedirectPath + "");

    }
  }
  return false;
}






