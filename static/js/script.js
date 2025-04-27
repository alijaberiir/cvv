window.addEventListener("load", function () {
    var observer = window.lozad(".lozad", { rootMargin: window.innerHeight / 2 + "px 0px", threshold: 0.01 });
    observer.observe();
});
const scroll = new SmoothScroll('a[href*="#"]');
$("a.nav-link").on("click", () => {
    const navbar = $(".navbar-collapse");
    if (navbar && navbar.hasClass("show")) {
        $(".navbar-toggler").click();
    }
});

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}