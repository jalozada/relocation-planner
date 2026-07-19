(function () {
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(";").shift();
        }
        return "";
    }

    document.addEventListener("htmx:configRequest", function (event) {
        event.detail.headers["X-CSRFToken"] = getCookie("csrftoken");
    });

    document.addEventListener("DOMContentLoaded", function () {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    });

    document.addEventListener("htmx:afterSwap", function () {
        if (window.lucide) {
            window.lucide.createIcons();
        }
    });
})();
