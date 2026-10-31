function togglePassword(id, iconId){

    const input = document.getElementById(id);

    const icon = document.getElementById(iconId);

    icon.addEventListener("click", ()=>{

        if(input.type === "password"){

            input.type = "text";

            icon.classList.replace("fa-eye","fa-eye-slash");

        }else{

            input.type = "password";

            icon.classList.replace("fa-eye-slash","fa-eye");

        }

    });

}

togglePassword("password","togglePassword");

togglePassword("confirmPassword","toggleConfirm");