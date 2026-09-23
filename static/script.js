const form = document.getElementById("candidateForm");

if (form) {
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const candidate = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            education: document.getElementById("education").value,
            experience: document.getElementById("experience").value,
            skills: document.getElementById("skills").value
        };

        try {
            const response = await fetch("/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(candidate)
            });

            const result = await response.json();

            document.getElementById("result").classList.remove("hidden");

            document.getElementById("candidateName").textContent = result.name;
            document.getElementById("candidateEmail").textContent = result.email;
            document.getElementById("candidateEducation").textContent = result.education;
            document.getElementById("candidateExperience").textContent =
                result.experience + " years";
            document.getElementById("candidateSkills").textContent = result.skills;
            document.getElementById("score").textContent = result.score;

            document.getElementById("result").scrollIntoView({
                behavior: "smooth"
            });

        } catch (error) {
            alert(
                "Unable to analyze application. " +
                "Please check that the Flask server is running."
            );

            console.error(error);
        }
    });
}
