// --- Mobile nav toggle -----------------------------------------------------
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");
if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
    navToggle.textContent = navLinks.classList.contains("open") ? "✕" : "☰";
  });
  navLinks.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      navLinks.classList.remove("open");
      navToggle.textContent = "☰";
    })
  );
}

// --- Scroll reveal -----------------------------------------------------
const revealEls = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && revealEls.length) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("in"));
}

// --- Contact form (AJAX submit, no page reload) -----------------------------------------------------
const form = document.querySelector(".contact-form");
if (form) {
  const msgBox = form.querySelector(".form-msg");
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Sending...";

    try {
      const res = await fetch("/submit-contact", {
        method: "POST",
        body: new FormData(form),
      });
      const data = await res.json();

      msgBox.textContent = data.message;
      msgBox.classList.remove("ok", "err");
      msgBox.classList.add("show", data.success ? "ok" : "err");

      clearTimeout(form._msgTimeout);
      form._msgTimeout = setTimeout(() => {
        msgBox.classList.remove("show");
      }, 5000);

      if (data.success) form.reset();
    } catch (err) {
      msgBox.textContent = "Something went wrong. Please try again or email us directly.";
      msgBox.classList.remove("ok");
      msgBox.classList.add("show", "err");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  });
}