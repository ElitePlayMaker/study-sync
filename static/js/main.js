/** Study Sync — UI micro-interactions */

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".ss-card, .ss-class-card, .ss-stat-card").forEach(function (el, i) {
        el.style.animationDelay = (i * 0.05) + "s";
    });
});
