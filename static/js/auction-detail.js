const countdown = document.getElementById("countdown");
const mainImage = document.getElementById("mainImage");

const thumbnails =
    document.querySelectorAll(".thumbnail");

thumbnails.forEach(thumbnail => {

    thumbnail.addEventListener("click", () => {

        mainImage.src = thumbnail.src;

        thumbnails.forEach(t =>
            t.classList.remove("active")
        );

        thumbnail.classList.add("active");

    });

});

if (countdown) {

    const end = new Date(
        countdown.dataset.end
    );

    function updateCountdown() {

        const now = new Date();

        const diff = end - now;

        if (diff <= 0) {

            countdown.textContent =
                "Auction Ended";

            return;
        }

        const days =
            Math.floor(diff / 86400000);

        const hours =
            Math.floor((diff % 86400000) / 3600000);

        const minutes =
            Math.floor((diff % 3600000) / 60000);

        const seconds =
            Math.floor((diff % 60000) / 1000);

        countdown.textContent =
            `${days}d ${hours}h ${minutes}m ${seconds}s`;

    }

    updateCountdown();

    setInterval(updateCountdown, 1000);

}