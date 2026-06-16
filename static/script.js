if (localStorage.getItem('SignIn') === 'true')
    {
        document.getElementById("auth").textContent = "Logout";
    }
document.getElementById("auth").addEventListener('click', (e) => {
    e.preventDefault();
    if (localStorage.getItem('SignIn') === "false" || localStorage.getItem('SignIn') == null)
    {
        window.location.href = "../SignIn.html";
    }
    else
    {
        fetch("/logout", {
            method: "POST",
            credentials: "include"
        })
        .then(res => {
            if (res.redirected)
            {
                localStorage.setItem('SignIn', 'false');
                window.location.href = "../SignIn.html";
            }
        })
    }
})

document.querySelector(".nav-link a").style.fontWeight = "bold";
const links = document.querySelectorAll(".nav-link a");
const last_link = links[links.length - 1];
last_link.href = "https://forms.gle/XB1RpbsikaRg4JuE8";
last_link.target = "_blank";
last_link.style.textDecoration = "none";

links[1].href = "../help.html";