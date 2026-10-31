document.querySelectorAll(".listing-actions").forEach(action => {

    const button = action.querySelector(".action-btn");
    const menu = action.querySelector(".action-menu");

    button.addEventListener("click", function(e){

        e.stopPropagation();

        // Close every other menu
        document.querySelectorAll(".action-menu").forEach(m => {

            if (m !== menu) {

                m.classList.remove("show");

            }

        });

        menu.classList.toggle("show");

    });

});

// Click anywhere else closes all menus
document.addEventListener("click", function(){

    document.querySelectorAll(".action-menu").forEach(menu => {

        menu.classList.remove("show");

    });

});