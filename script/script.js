(() => {
  "use strict";

  /* =========================================================
     CONFIG
  ========================================================= */

  const WEBHOOK_URL =
    "https://padalko.app.n8n.cloud/webhook/raccoon-seo-lead";


  /* =========================================================
     HELPERS
  ========================================================= */

  const qs = (selector, scope = document) => {
    return scope.querySelector(selector);
  };

  const qsa = (selector, scope = document) => {
    return Array.from(
      scope.querySelectorAll(selector)
    );
  };


  /* =========================================================
     CURRENT LANGUAGE
  ========================================================= */

  const getCurrentLanguage = () => {
    const lang =
      document.documentElement
        .getAttribute("lang")
        ?.toLowerCase();

    return lang === "pl"
      ? "pl"
      : "uk";
  };


  /* =========================================================
     TRANSLATIONS
  ========================================================= */

  const translations = {
    uk: {
      required:
        "Заповніть імʼя, телефон та email.",

      invalidPhone:
        "Вкажіть телефон у міжнародному форматі, наприклад +48123456789.",

      sending:
        "Відправляємо заявку...",

      success:
        "Дякуємо! Заявку відправлено. Ми скоро звʼяжемося з вами.",

      error:
        "Не вдалося відправити заявку. Спробуйте ще раз пізніше.",

      subscribeSuccess:
        "Дякуємо! Ваш email додано до підписки.",

      subscribeError:
        "Не вдалося оформити підписку. Спробуйте ще раз пізніше."
    },

    pl: {
      required:
        "Wypełnij imię, telefon i adres e-mail.",

      invalidPhone:
        "Podaj numer telefonu w formacie międzynarodowym, np. +48123456789.",

      sending:
        "Wysyłamy zgłoszenie...",

      success:
        "Dziękujemy! Zgłoszenie zostało wysłane. Wkrótce się skontaktujemy.",

      error:
        "Nie udało się wysłać zgłoszenia. Spróbuj ponownie później.",

      subscribeSuccess:
        "Dziękujemy! Twój adres e-mail został dodany do newslettera.",

      subscribeError:
        "Nie udało się zapisać do newslettera. Spróbuj ponownie później."
    }
  };


  const getTexts = () => {
    return translations[
      getCurrentLanguage()
    ];
  };


  /* =========================================================
     PHONE HELPERS
  ========================================================= */

  const normalizePhone = (
    phone = ""
  ) => {
    const trimmed =
      String(phone).trim();

    if (!trimmed) {
      return "";
    }

    const hasPlus =
      trimmed.startsWith("+");

    const digits =
      trimmed.replace(/\D/g, "");

    return hasPlus
      ? `+${digits}`
      : digits;
  };


  const isValidPhone = (
    phone = ""
  ) => {
    return /^\+\d{7,15}$/.test(
      phone
    );
  };


  /* =========================================================
     BODY LOCK
  ========================================================= */

  const lockBody = () => {
    document.body.classList.add(
      "modal-open"
    );
  };


  const unlockBody = () => {
    const backdrop =
      qs(".js-backdrop");

    const navList =
      qs(".nav-list");

    const modalOpen =
      backdrop &&
      !backdrop.classList.contains(
        "is-hidden"
      );

    const menuOpen =
      navList &&
      navList.classList.contains(
        "open"
      );

    if (
      !modalOpen &&
      !menuOpen
    ) {
      document.body.classList.remove(
        "modal-open"
      );
    }
  };


  /* =========================================================
     MODAL
  ========================================================= */

  const backdrop =
    qs(".js-backdrop");

  const modal =
    qs(".modal");

  const openModalButtons =
    qsa(".js-open-modal");

  const closeModalButton =
    qs(".js-close-modal");


  const openModal = () => {
    if (!backdrop) {
      return;
    }

    backdrop.classList.remove(
      "is-hidden"
    );

    lockBody();

    const firstInput =
      qs(
        "input, select, textarea",
        backdrop
      );

    if (firstInput) {
      window.setTimeout(() => {
        firstInput.focus();
      }, 100);
    }
  };


  const closeModal = () => {
    if (!backdrop) {
      return;
    }

    backdrop.classList.add(
      "is-hidden"
    );

    unlockBody();
  };


  openModalButtons.forEach(
    (button) => {
      button.addEventListener(
        "click",
        openModal
      );
    }
  );


  if (closeModalButton) {
    closeModalButton.addEventListener(
      "click",
      closeModal
    );
  }


  if (backdrop) {
    backdrop.addEventListener(
      "click",
      (event) => {
        if (
          event.target === backdrop
        ) {
          closeModal();
        }
      }
    );
  }


  if (modal) {
    modal.addEventListener(
      "click",
      (event) => {
        event.stopPropagation();
      }
    );
  }


  document.addEventListener(
    "keydown",
    (event) => {
      if (
        event.key === "Escape"
      ) {
        if (
          backdrop &&
          !backdrop.classList.contains(
            "is-hidden"
          )
        ) {
          closeModal();
        }

        closeMobileMenu();
      }
    }
  );


  /* =========================================================
     BURGER MENU
  ========================================================= */

  const burger =
    qs(".burger");

  const navList =
    qs(".nav-list");


  function openMobileMenu() {
    if (
      !burger ||
      !navList
    ) {
      return;
    }

    navList.classList.add(
      "open"
    );

    burger.classList.add(
      "active"
    );

    burger.setAttribute(
      "aria-expanded",
      "true"
    );

    lockBody();
  }


  function closeMobileMenu() {
    if (
      !burger ||
      !navList
    ) {
      return;
    }

    navList.classList.remove(
      "open"
    );

    burger.classList.remove(
      "active"
    );

    burger.setAttribute(
      "aria-expanded",
      "false"
    );

    unlockBody();
  }


  if (
    burger &&
    navList
  ) {
    burger.addEventListener(
      "click",
      () => {
        const isOpen =
          navList.classList.contains(
            "open"
          );

        if (isOpen) {
          closeMobileMenu();
        } else {
          openMobileMenu();
        }
      }
    );


    qsa(
      ".nav-list .nav-link"
    ).forEach((link) => {
      link.addEventListener(
        "click",
        closeMobileMenu
      );
    });
  }


  window.addEventListener(
    "resize",
    () => {
      if (
        window.innerWidth > 900
      ) {
        closeMobileMenu();
      }
    }
  );


  /* =========================================================
     SMOOTH INTERNAL ANCHORS
  ========================================================= */

  qsa('a[href^="#"]').forEach(
    (link) => {
      link.addEventListener(
        "click",
        (event) => {
          const href =
            link.getAttribute(
              "href"
            );

          if (
            !href ||
            href === "#"
          ) {
            return;
          }

          const target =
            qs(href);

          if (!target) {
            return;
          }

          event.preventDefault();

          const header =
            qs(".header");

          const headerHeight =
            header
              ? header.offsetHeight
              : 0;

          const top =
            target.getBoundingClientRect()
              .top +
            window.pageYOffset -
            headerHeight -
            20;

          window.scrollTo({
            top,
            behavior: "smooth"
          });

          closeMobileMenu();
        }
      );
    }
  );


  /* =========================================================
     SCROLL SPY
  ========================================================= */

  const sections =
    qsa("section[id]");

  const internalNavLinks =
    qsa(
      '.nav-link[href^="#"], .nav-link[href^="/#"], .nav-link[href^="/pl/#"]'
    );


  const getAnchorIdFromHref = (
    href
  ) => {
    if (!href) {
      return "";
    }

    const hashPosition =
      href.indexOf("#");

    if (hashPosition === -1) {
      return "";
    }

    return href.substring(
      hashPosition + 1
    );
  };


  const updateActiveNav = () => {
    if (
      !sections.length ||
      !internalNavLinks.length
    ) {
      return;
    }

    const header =
      qs(".header");

    const offset =
      window.scrollY +
      (
        header
          ? header.offsetHeight
          : 0
      ) +
      120;

    let currentSection = "";

    sections.forEach(
      (section) => {
        if (
          offset >=
          section.offsetTop
        ) {
          currentSection =
            section.id;
        }
      }
    );

    if (!currentSection) {
      return;
    }

    internalNavLinks.forEach(
      (link) => {
        const id =
          getAnchorIdFromHref(
            link.getAttribute(
              "href"
            )
          );

        link.classList.toggle(
          "active",
          id === currentSection
        );
      }
    );
  };


  if (
    sections.length &&
    internalNavLinks.length
  ) {
    window.addEventListener(
      "scroll",
      updateActiveNav,
      {
        passive: true
      }
    );

    updateActiveNav();
  }


  /* =========================================================
     FORM STATUS
  ========================================================= */

  const setFormStatus = (
    form,
    message,
    type = ""
  ) => {
    const status =
      qs(
        ".js-form-status",
        form
      );

    if (!status) {
      return;
    }

    status.textContent =
      message;

    status.classList.remove(
      "success",
      "error"
    );

    if (type) {
      status.classList.add(
        type
      );
    }
  };


  /* =========================================================
     BUTTON LOADING STATE
  ========================================================= */

  const setButtonLoading = (
    button,
    loading
  ) => {
    if (!button) {
      return;
    }

    if (loading) {
      button.dataset.originalText =
        button.textContent.trim();

      button.disabled = true;
    } else {
      button.disabled = false;

      if (
        button.dataset.originalText
      ) {
        button.textContent =
          button.dataset.originalText;

        delete button.dataset
          .originalText;
      }
    }
  };


  /* =========================================================
     COLLECT LEAD DATA
  ========================================================= */

  const collectLeadData = (
    form
  ) => {
    const formData =
      new FormData(form);

    const data =
      Object.fromEntries(
        formData.entries()
      );

    return {
      createdAt:
        new Date().toISOString(),

      leadSource:
        "Raccoon SEO Studio Website",

      language:
        getCurrentLanguage(),

      pageUrl:
        window.location.href,

      pagePath:
        window.location.pathname,

      pageTitle:
        document.title,

      name:
        String(
          data.name || ""
        ).trim(),

      phone:
        normalizePhone(
          data.phone || ""
        ),

      email:
        String(
          data.email || ""
        ).trim(),

      company:
        String(
          data.company || ""
        ).trim(),

      service:
        String(
          data.service || ""
        ).trim(),

      budget:
        String(
          data.budget || ""
        ).trim(),

      comment:
        String(
          data.comment || ""
        ).trim(),

      userAgent:
        navigator.userAgent
    };
  };


  /* =========================================================
     SEND WEBHOOK
  ========================================================= */

  const sendToWebhook =
    async (payload) => {

      const response =
        await fetch(
          WEBHOOK_URL,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body:
              JSON.stringify(
                payload
              )
          }
        );


      if (!response.ok) {
        throw new Error(
          `Webhook returned ${response.status}`
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


  /* =========================================================
     LEAD FORMS
  ========================================================= */

  const leadForms =
    qsa(".js-lead-form");


  leadForms.forEach(
    (form) => {

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
            collectLeadData(form);


          /* REQUIRED */

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


          /* PHONE */

          if (
            !isValidPhone(
              payload.phone
            )
          ) {
            setFormStatus(
              form,
              texts.invalidPhone,
              "error"
            );

            return;
          }


          /* EMAIL */

          const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

          if (
            !emailPattern.test(
              payload.email
            )
          ) {
            setFormStatus(
              form,
              texts.required,
              "error"
            );

            return;
          }


          try {

            if (
              submitButton
            ) {
              submitButton.dataset.originalText =
                submitButton
                  .textContent
                  .trim();

              submitButton.textContent =
                texts.sending;

              submitButton.disabled =
                true;
            }


            setFormStatus(
              form,
              texts.sending
            );


            await sendToWebhook(
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
              window.setTimeout(
                () => {
                  closeModal();
                },
                1600
              );
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

            if (
              submitButton
            ) {
              submitButton.disabled =
                false;

              if (
                submitButton.dataset
                  .originalText
              ) {
                submitButton.textContent =
                  submitButton.dataset
                    .originalText;

                delete submitButton
                  .dataset
                  .originalText;
              }
            }

          }

        }
      );

    }
  );


  /* =========================================================
     NEWSLETTER
  ========================================================= */

  const subscribeForms =
    qsa(".subscribe-form");


  subscribeForms.forEach(
    (form) => {

      form.addEventListener(
        "submit",
        async (event) => {

          event.preventDefault();

          const texts =
            getTexts();

          const input =
            qs(
              ".subscribe-input",
              form
            );

          const button =
            qs(
              'button[type="submit"]',
              form
            );


          if (!input) {
            return;
          }


          const email =
            input.value.trim();


          if (!email) {
            return;
          }


          const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


          if (
            !emailPattern.test(
              email
            )
          ) {
            input.focus();

            return;
          }


          const payload = {

            createdAt:
              new Date().toISOString(),

            leadSource:
              "Raccoon SEO Studio Newsletter",

            language:
              getCurrentLanguage(),

            pageUrl:
              window.location.href,

            pagePath:
              window.location.pathname,

            pageTitle:
              document.title,

            name:
              "",

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

            if (button) {
              setButtonLoading(
                button,
                true
              );
            }


            await sendToWebhook(
              payload
            );


            form.reset();


            window.alert(
              texts.subscribeSuccess
            );

          } catch (error) {

            console.error(
              "Newsletter error:",
              error
            );


            window.alert(
              texts.subscribeError
            );

          } finally {

            if (button) {
              setButtonLoading(
                button,
                false
              );
            }

          }

        }
      );

    }
  );


  /* =========================================================
     EXTERNAL LINKS
  ========================================================= */

  qsa(
    'a[target="_blank"]'
  ).forEach((link) => {

    const currentRel =
      link.getAttribute(
        "rel"
      ) || "";

    const values =
      new Set(
        currentRel
          .split(/\s+/)
          .filter(Boolean)
      );

    values.add(
      "noopener"
    );

    values.add(
      "noreferrer"
    );

    link.setAttribute(
      "rel",
      Array.from(values).join(" ")
    );

  });


  /* =========================================================
     HASH FROM ANOTHER PAGE
  ========================================================= */

  const scrollToCurrentHash =
    () => {

      if (
        !window.location.hash
      ) {
        return;
      }


      const target =
        qs(
          window.location.hash
        );


      if (!target) {
        return;
      }


      window.setTimeout(
        () => {

          const header =
            qs(".header");

          const headerHeight =
            header
              ? header.offsetHeight
              : 0;


          const top =
            target
              .getBoundingClientRect()
              .top +
            window.pageYOffset -
            headerHeight -
            20;


          window.scrollTo({
            top,
            behavior: "smooth"
          });

        },
        100
      );

    };


  window.addEventListener(
    "load",
    scrollToCurrentHash
  );


  /* =========================================================
     INITIAL STATE
  ========================================================= */

  if (burger) {
    burger.setAttribute(
      "aria-expanded",
      "false"
    );
  }

})();