const profileBtn = document.getElementById("profileBtn");

const dropdown = document.getElementById("dropdownMenu");

if(profileBtn){

    profileBtn.addEventListener("click",function(e){

        e.stopPropagation();

        dropdown.classList.toggle("show");

    });

    window.addEventListener("click",function(){

        dropdown.classList.remove("show");

    });

}