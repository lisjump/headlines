function SetDefaults(preferredsort, ascending) {
  sortby = preferredsort;
  booklabel = "";
  searchterms = "";
  if (ascending == "True") { reverse = false } else { reverse = true }
}

function CollapseMenu(menuid, toggleid) {
  var menu = document.getElementById(menuid);
  var toggle = document.getElementById(toggleid);
  var currentclass = menu.getAttribute("class")
  if (currentclass == "hiddenfeeditems") {
    menu.setAttribute("class","feeditems");
    toggle.innerHTML = "[-]";
  }
  else {
    menu.setAttribute("class","hiddenfeeditems");
    toggle.innerHTML = "[+]";
  }
}

function CollapseBox(boxid) {
  var box = document.getElementById(boxid);
  var currentclass = box.getAttribute("class")
  if (currentclass == "hiddenbox") {
    box.setAttribute("class","boxwithtitle");
  }
  else {
    box.setAttribute("class","hiddenbox");
  }
}