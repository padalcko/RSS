(() => {
  const WEBHOOK_URL = "https://padalko.app.n8n.cloud/webhook/raccoon-seo-lead";

  /* ============================
     MODAL
  ============================ */
  const refs = {
    openModalBtn: document.querySelector(".js-open-modal"),
    closeModalBtn: document.querySelector(".js-close-modal"),
    modal: document.querySelector(".js-backdrop"),
  };

  const toggleModal = () => {
    if (!refs.modal) return;

    const isHidden = refs.modal.classList.toggle("is-hidden");
    document.body.style.overflow = isHidden ? "auto" : "hidden";
  };

  if (refs.openModalBtn && refs.closeModalBtn && refs.modal) {
    refs.openModalBtn.addEventListener("click", toggleModal);
    refs.closeModalBtn.addEventListener("click", toggleModal);

    refs.modal.addEventListener("click", (e) => {
      if (e.target === refs.modal) toggleModal();
    });
  }

  /* ============================
     SCROLL SPY
  ============================ */
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link");

  if (sections.length && navLinks.length) {
    window.addEventListener("scroll", () => {
      let current = "";
      const scrollPos = window.pageYOffset + 200;

      sections.forEach((section) => {
        if (scrollPos >= section.offsetTop) {
          current = section.getAttribute("id");
        }
      });

      navLinks.forEach((link) => {
        link.classList.toggle(
          "active",
          link.getAttribute("href") === `#${current}`
        );
      });
    });
  }

  /* ============================
     BURGER MENU
  ============================ */
  const burger = document.querySelector(".burger");
  const navList = document.querySelector(".nav-list");
  const contactsList = document.querySelector(".contacts-list");

  const closeBurgerMenu = () => {
    if (!burger || !navList || !contactsList) return;

    navList.classList.remove("open");
    contactsList.classList.remove("open");
    burger.classList.remove("active");
    document.body.style.overflow = "auto";
    burger.setAttribute("aria-expanded", "false");
  };

  if (burger && navList && contactsList) {
    burger.addEventListener("click", () => {
      const isOpen = navList.classList.toggle("open");

      contactsList.classList.toggle("open");
      burger.classList.toggle("active");

      document.body.style.overflow = isOpen ? "hidden" : "auto";
      burger.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    document.querySelectorAll(".nav-list .nav-link").forEach((link) => {
      link.addEventListener("click", closeBurgerMenu);
    });
  }

  /* ============================
     LEAD FORMS TO N8N
  ============================ */
  const leadForms = document.querySelectorAll(".js-lead-form");

  const normalizePhone = (phone) => {
    return phone.replace(/[^\d+]/g, "");
  };

  const isValidPhone = (phone) => {
    return /^\+\d{7,15}$/.test(phone);
  };

  const setFormStatus = (form, message, type = "") => {
    const status = form.querySelector(".js-form-status");

    if (!status) return;

    status.textContent = message;
    status.className = `form-status js-form-status ${type}`.trim();
  };

  const collectFormData = (form) => {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    return {
      createdAt: new Date().toISOString(),
      leadSource: "Raccoon SEO Studio Website",
      pageUrl: window.location.href,

      name: (data.name || "").trim(),
      phone: normalizePhone(data.phone || ""),
      email: (data.email || "").trim(),
      company: (data.company || "").trim(),
      service: data.service || "",
      comment: (data.comment || "").trim(),
    };
  };

  const sendLeadToN8n = async (payload) => {
    const response = await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Webhook error: ${response.status}`);
    }

    try {
      return await response.json();
    } catch (error) {
      return { success: true };
    }
  };

  if (leadForms.length) {
    leadForms.forEach((form) => {
      form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const submitButton = form.querySelector('button[type="submit"]');
        const payload = collectFormData(form);

        if (!payload.name || !payload.phone || !payload.email) {
          setFormStatus(
            form,
            "Заповніть імʼя, телефон та email.",
            "error"
          );
          return;
        }

        if (!isValidPhone(payload.phone)) {
          setFormStatus(
            form,
            "Вкажіть телефон у міжнародному форматі, наприклад: +12345678901.",
            "error"
          );
          return;
        }

        try {
          setFormStatus(form, "Відправляю заявку...");

          if (submitButton) {
            submitButton.disabled = true;
          }

          await sendLeadToN8n(payload);

          setFormStatus(
            form,
            "Дякую! Заявку відправлено. Ми скоро звʼяжемось з вами.",
            "success"
          );

          form.reset();
        } catch (error) {
          console.error(error);

          setFormStatus(
            form,
            "Заявку не вдалося відправити. Перевірте Webhook URL, CORS або Respond to Webhook у n8n.",
            "error"
          );
        } finally {
          if (submitButton) {
            submitButton.disabled = false;
          }
        }
      });
    });
  }

  /* ============================
     FOOTER SUBSCRIBE FORM
  ============================ */
  const subscribeForm = document.querySelector(".subscribe-form");

  if (subscribeForm) {
    subscribeForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const emailInput = subscribeForm.querySelector(".subscribe-input");
      const email = emailInput ? emailInput.value.trim() : "";

      if (!email) return;

      const payload = {
        createdAt: new Date().toISOString(),
        leadSource: "Footer Subscribe Form",
        pageUrl: window.location.href,
        name: "Підписник",
        phone: "",
        email,
        company: "",
        service: "Підписка на новини",
        comment: "Користувач підписався через форму у футері",
      };

      try {
        await sendLeadToN8n(payload);
        subscribeForm.reset();
        alert("Дякую! Ви підписались на новини.");
      } catch (error) {
        console.error(error);
        alert("Не вдалося відправити підписку. Перевірте n8n webhook.");
      }
    });
  }
})();