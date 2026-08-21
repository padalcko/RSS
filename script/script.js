(() => {
  "use strict";

  const WEBHOOK_URL =
    "https://padalko.app.n8n.cloud/webhook/raccoon-seo-lead";


  /* =========================================
     HELPERS
  ========================================= */

  const qs = (selector, scope = document) =>
    scope.querySelector(selector);

  const qsa = (selector, scope = document) =>
    Array.from(scope.querySelectorAll(selector));

  const normalizePhone = (phone = "") => {
    return phone.replace(/[^\d+]/g, "");
  };

  const isValidPhone = (phone = "") => {
    return /^\+\d{7,15}$/.test(phone);
  };

  const getCurrentLanguage = () => {
    const htmlLang =
      document.documentElement.getAttribute("lang");

    return htmlLang === "pl" ? "pl" : "uk";
  };

  const getTexts = () => {
    const lang = getCurrentLanguage();

    if (lang === "pl") {
      return {
        required:
          "Wypełnij imię, telefon i adres e-mail.",
        phone:
          "Podaj numer telefonu w formacie międzynarodowym, np. +48123456789.",
        sending:
          "Wysyłam zgłoszenie...",
        success:
          "Dziękujemy! Zgłoszenie zostało wysłane. Wkrótce się skontaktujemy.",
        error:
          "Nie udało się wysłać formularza. Spróbuj ponownie później.",
        subscribeSuccess:
          "Dziękujemy! Zapisano adres e-mail do newslettera.",
        subscribeError:
          "Nie udało się zapisać do newslettera. Spróbuj ponownie później."
      };
    }

    return {
      required:
        "Заповніть імʼя, телефон та email.",
      phone:
        "Вкажіть телефон у міжнародному форматі, наприклад: +48123456789.",
      sending:
        "Відправляю заявку...",
      success:
        "Дякуємо! Заявку відправлено. Ми скоро звʼяжемося з вами.",
      error:
        "Не вдалося відправити форму. Спробуйте ще раз пізніше.",
      subscribeSuccess:
        "Дякуємо! Email додано до підписки.",
      subscribeError:
        "Не вдалося оформити підписку. Спробуйте ще раз пізніше."
    };
  };


  /* =========================================
     MODAL
  ========================================= */

  const backdrop = qs(".js-backdrop");
  const openModalButtons = qsa(".js-open-modal");
  const closeModalButton = qs(".js-close-modal");

  const openModal = () => {
    if (!backdrop) return;

    backdrop.classList.remove("is-hidden");
    document.body.classList.add("modal-open");
  };

  const closeModal = () => {
    if (!backdrop) return;

    backdrop.classList.add("is-hidden");
    document.body.classList.remove("modal-open");
  };

  if (openModalButtons.length) {
    openModalButtons.forEach((button) => {
      button.addEventListener("click", openModal);
    });
  }

  if (closeModalButton) {
    closeModalButton.addEventListener(
      "click",
      closeModal
    );
  }

  if (backdrop) {
    backdrop.addEventListener("click", (event) => {
      if (event.target === backdrop) {
        closeModal();
      }
    });
  }

  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      backdrop &&
      !backdrop.classList.contains("is-hidden")
    ) {
      closeModal();
    }
  });


  /* =========================================
     BURGER MENU
  ========================================= */

  const burger = qs(".burger");
  const navList = qs(".nav-list");

  const closeBurgerMenu = () => {
    if (!burger || !navList) return;

    navList.classList.remove("open");
    burger.classList.remove("active");
    burger.setAttribute(
      "aria-expanded",
      "false"
    );

    if (!backdrop ||
        backdrop.classList.contains("is-hidden")) {
      document.body.classList.remove(
        "modal-open"
      );
    }
  };

  const openBurgerMenu = () => {
    if (!burger || !navList) return;

    navList.classList.add("open");
    burger.classList.add("active");
    burger.setAttribute(
      "aria-expanded",
      "true"
    );
  };

  if (burger && navList) {
    burger.addEventListener("click", () => {
      const isOpen =
        navList.classList.contains("open");

      if (isOpen) {
        closeBurgerMenu();
      } else {
        openBurgerMenu();
      }
    });

    qsa(".nav-list .nav-link").forEach((link) => {
      link.addEventListener(
        "click",
        closeBurgerMenu
      );
    });
  }

  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) {
      closeBurgerMenu();
    }
  });


  /* =========================================
     SCROLL SPY
  ========================================= */

  const sections = qsa("section[id]");
  const navLinks = qsa(
    '.nav-link[href^="/#"], .nav-link[href^="#"]'
  );

  const updateActiveNavigation = () => {
    if (!sections.length || !navLinks.length) {
      return;
    }

    let currentSection = "";

    const offset =
      window.pageYOffset + 180;

    sections.forEach((section) => {
      if (
        offset >= section.offsetTop
      ) {
        currentSection =
          section.getAttribute("id");
      }
    });

    if (!currentSection) return;

    navLinks.forEach((link) => {
      const href =
        link.getAttribute("href") || "";

      const cleanHref =
        href.replace(/^\/?/, "");

      const isMatch =
        cleanHref === `#${currentSection}`;

      link.classList.toggle(
        "active",
        isMatch
      );
    });
  };

  if (sections.length && navLinks.length) {
    window.addEventListener(
      "scroll",
      updateActiveNavigation,
      { passive: true }
    );

    updateActiveNavigation();
  }


  /* =========================================
     FORM STATUS
  ========================================= */

  const setFormStatus = (
    form,
    message,
    type = ""
  ) => {
    const status =
      qs(".js-form-status", form);

    if (!status) return;

    status.textContent = message;

    status.className =
      "form-status js-form-status";

    if (type) {
      status.classList.add(type);
    }
  };


  /* =========================================
     COLLECT LEAD FORM DATA
  ========================================= */

  const collectFormData = (form) => {
    const formData =
      new FormData(form);

    const data =
      Object.fromEntries(
        formData.entries()
      );

    const pageTitle =
      document.title || "";

    return {
      createdAt:
        new Date().toISOString(),

      leadSource:
        "Raccoon SEO Studio Website",

      language:
        getCurrentLanguage(),

      pageUrl:
        window.location.href,

      pageTitle,

      name:
        (data.name || "").trim(),

      phone:
        normalizePhone(
          data.phone || ""
        ),

      email:
        (data.email || "").trim(),

      company:
        (data.company || "").trim(),

      service:
        data.service || "",

      budget:
        data.budget || "",

      comment:
        (data.comment || "").trim()
    };
  };


  /* =========================================
     SEND TO N8N
  ========================================= */

  const sendToN8n = async (payload) => {
    const response =
      await fetch(WEBHOOK_URL, {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body:
          JSON.stringify(payload)
      });

    if (!response.ok) {
      throw new Error(
        `Webhook error: ${response.status}`
      );
    }

    const contentType =
      response.headers.get(
        "content-type"
      );

    if (
      contentType &&
      contentType.includes(
        "application/json"
      )
    ) {
      try {
        return await response.json();
      } catch (error) {
        return {
          success: true
        };
      }
    }

    return {
      success: true
    };
  };


  /* =========================================
     LEAD FORMS
  ========================================= */

  const leadForms =
    qsa(".js-lead-form");

  if (leadForms.length) {
    leadForms.forEach((form) => {
      form.addEventListener(
        "submit",
        async (event) => {
          event.preventDefault();

          const texts =
            getTexts();

          const submitButton =
            qs(
              'button[type="submit"]',
              form
            );

          const payload =
            collectFormData(form);

          if (
            !payload.name ||
            !payload.phone ||
            !payload.email
          ) {
            setFormStatus(
              form,
              texts.required,
              "error"
            );

            return;
          }

          if (
            !isValidPhone(
              payload.phone
            )
          ) {
            setFormStatus(
              form,
              texts.phone,
              "error"
            );

            return;
          }

          try {
            setFormStatus(
              form,
              texts.sending
            );

            if (submitButton) {
              submitButton.disabled =
                true;
            }

            await sendToN8n(
              payload
            );

            setFormStatus(
              form,
              texts.success,
              "success"
            );

            form.reset();

            if (
              form.classList.contains(
                "modal-form"
              )
            ) {
              setTimeout(() => {
                closeModal();
              }, 1400);
            }
          } catch (error) {
            console.error(
              "Lead form error:",
              error
            );

            setFormStatus(
              form,
              texts.error,
              "error"
            );
          } finally {
            if (submitButton) {
              submitButton.disabled =
                false;
            }
          }
        }
      );
    });
  }


  /* =========================================
     FOOTER SUBSCRIBE
  ========================================= */

  const subscribeForms =
    qsa(".subscribe-form");

  if (subscribeForms.length) {
    subscribeForms.forEach((form) => {
      form.addEventListener(
        "submit",
        async (event) => {
          event.preventDefault();

          const texts =
            getTexts();

          const emailInput =
            qs(
              ".subscribe-input",
              form
            );

          const submitButton =
            qs(
              'button[type="submit"]',
              form
            );

          const email =
            emailInput
              ? emailInput.value.trim()
              : "";

          if (!email) return;

          const payload = {
            createdAt:
              new Date().toISOString(),

            leadSource:
              "Footer Subscribe Form",

            language:
              getCurrentLanguage(),

            pageUrl:
              window.location.href,

            pageTitle:
              document.title || "",

            name:
              "Newsletter subscriber",

            phone:
              "",

            email,

            company:
              "",

            service:
              "Newsletter",

            budget:
              "",

            comment:
              "Newsletter subscription"
          };

          try {
            if (submitButton) {
              submitButton.disabled =
                true;
            }

            await sendToN8n(
              payload
            );

            form.reset();

            window.alert(
              texts.subscribeSuccess
            );
          } catch (error) {
            console.error(
              "Subscribe error:",
              error
            );

            window.alert(
              texts.subscribeError
            );
          } finally {
            if (submitButton) {
              submitButton.disabled =
                false;
            }
          }
        }
      );
    });
  }


  /* =========================================
     EXTERNAL LINKS SAFETY
  ========================================= */

  qsa(
    'a[target="_blank"]'
  ).forEach((link) => {
    const rel =
      link.getAttribute("rel") || "";

    const relValues =
      new Set(
        rel
          .split(" ")
          .filter(Boolean)
      );

    relValues.add("noopener");
    relValues.add("noreferrer");

    link.setAttribute(
      "rel",
      Array.from(
        relValues
      ).join(" ")
    );
  });

})();