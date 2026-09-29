// The Rebuild tool of the menu items change list is a link, styled by the
// admin theme like the other tools: send its POST form instead of following it.
document.addEventListener("click", function (event) {
    var link = event.target.closest("a[data-lineup-rebuild-form]");
    if (!link) {
        return;
    }
    var form = document.getElementById(link.dataset.lineupRebuildForm);
    if (form) {
        event.preventDefault();
        form.submit();
    }
});
