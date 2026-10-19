/* jshint esversion: 6, browser: true */
// Ask before giving up a seat. The server still validates identity, CSRF and eligibility.
// Without JavaScript the ordinary POST form remains available.
(() => {
    "use strict";
    document.addEventListener("submit", (event) => {
        const message = event.target.getAttribute("data-confirm");
        if (message && !event.defaultPrevented && !window.confirm(message)) {
            event.preventDefault();
        }
    });
})();
