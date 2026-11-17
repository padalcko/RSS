(() => {
  "use strict";

  /* =========================================================
     CONFIG
  ========================================================= */

  const WEBHOOK_URL =
    "https://n8n.raccoon-studio.com.ua/webhook/raccoon-studio-leads";

  /* =========================================================
     HELPERS
  ========================================================= */

  const qs = (selector, scope = document) => {
    return scope.querySelector(selector);
  };

  const qsa = (selector, scope = document) => {
    return Array.from(scope.querySelectorAll(selector));
  };

  /* =========================================================
     CURRENT LANGUAGE
  ========================================================= */

  const getCurrentLanguage = () => {
    const lang = document.documentElement.getAttribute("lang")?.toLowerCase();

    return ["uk", "pl", "en"].includes(lang) ? lang : "uk";
  };

  /* =========================================================
     TRANSLATIONS
  ========================================================= */

  const translations = {
    en: {
      required: "Enter your name, phone number and email address.",
      invalidPhone: "Use an international phone number, such as +48123456789.",
      sending: "Sending your enquiry…",
      success: "Thank you! Your enquiry has been sent. We will be in touch soon.",
      error: "Your enquiry could not be sent. Please try again later.",
    },
    uk: {
      required: "Заповніть імʼя, телефон та email.",

      invalidPhone:
        "Вкажіть телефон у міжнародному форматі, наприклад +48123456789.",

      sending: "Відправляємо заявку...",

      success: "Дякуємо! Заявку відправлено. Ми скоро звʼяжемося з вами.",

      error: "Не вдалося відправити заявку. Спробуйте ще раз пізніше.",
    },

    pl: {
      required: "Wypełnij imię, telefon i adres e-mail.",

      invalidPhone:
        "Podaj numer telefonu w formacie międzynarodowym, np. +48123456789.",

      sending: "Wysyłamy zgłoszenie...",

      success:
        "Dziękujemy! Zgłoszenie zostało wysłane. Wkrótce się skontaktujemy.",

      error: "Nie udało się wysłać zgłoszenia. Spróbuj ponownie później.",
    },
  };

  const getTexts = () => {
    return translations[getCurrentLanguage()];
  };

  /* =========================================================
     PHONE HELPERS
  ========================================================= */

  const normalizePhone = (phone = "") => {
    const trimmed = String(phone).trim();

    if (!trimmed) {
      return "";
    }

    const hasPlus = trimmed.startsWith("+");
    const digits = trimmed.replace(/\D/g, "");

    return hasPlus ? `+${digits}` : digits;
  };

  const isValidPhone = (phone = "") => {
    return /^\+\d{7,15}$/.test(phone);
  };

  /* =========================================================
     BODY LOCK
  ========================================================= */

  const lockBody = () => {
    document.body.classList.add("modal-open");
  };

  const unlockBody = () => {
    const backdrop = qs(".js-backdrop");
    const navList = qs(".nav-list");

    const modalOpen = backdrop && !backdrop.classList.contains("is-hidden");

    const menuOpen = navList && navList.classList.contains("open");

    if (!modalOpen && !menuOpen) {
      document.body.classList.remove("modal-open");
    }
  };

  /* =========================================================
     MODAL
  ========================================================= */

  const backdrop = qs(".js-backdrop");
  const modal = qs(".modal");

  const openModalButtons = qsa(".js-open-modal");
  const closeModalButton = qs(".js-close-modal");

  let modalTrigger = null;

  const openModal = () => {
    if (!backdrop) {
      return;
    }

    closeLanguageMenu();
    modalTrigger = document.activeElement;
    closeMobileMenu();
    backdrop.classList.remove("is-hidden");
    qsa("body > header, body > main, body > footer").forEach(el => { el.inert = true; });
    lockBody();

    const firstInput = qs("input, select, textarea", backdrop);

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

    backdrop.classList.add("is-hidden");
    qsa("body > header, body > main, body > footer").forEach(el => { el.inert = false; });
    unlockBody();
    if (modalTrigger && modalTrigger.offsetParent !== null) modalTrigger.focus();
    else if (burger) burger.focus();
  };

  openModalButtons.forEach((button) => {
    button.addEventListener("click", openModal);
  });

  if (closeModalButton) {
    closeModalButton.addEventListener("click", closeModal);
  }

  if (backdrop) {
    backdrop.addEventListener("click", (event) => {
      if (event.target === backdrop) {
        closeModal();
      }
    });
  }

  if (modal) {
    modal.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      const modalActive = backdrop && !backdrop.classList.contains("is-hidden");
      const menuActive = navList && navList.classList.contains("open");
      const scope = modalActive ? modal : menuActive ? qs(".header") : null;
      if (scope) {
        const focusable = qsa('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex="0"]', scope)
          .filter(el => el.offsetParent !== null);
        const first = focusable[0], last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    }
    if (event.key === "Escape") {
      if (backdrop && !backdrop.classList.contains("is-hidden")) {
        closeModal();
      }

      closeMobileMenu();
    }
  });

  /* =========================================================
     BURGER MENU
  ========================================================= */

  const burger = qs(".burger");
  const navList = qs(".nav-list");

  function openMobileMenu() {
    if (!burger || !navList) {
      return;
    }

    closeLanguageMenu();
    navList.classList.add("open");
    qs("a, button", navList)?.focus();
    burger.classList.add("active");

    burger.setAttribute("aria-expanded", "true");

    lockBody();
  }

  function closeMobileMenu() {
    if (!burger || !navList) {
      return;
    }

    const hadFocus = navList.contains(document.activeElement);
    navList.classList.remove("open");
    if (hadFocus) burger.focus();
    burger.classList.remove("active");

    burger.setAttribute("aria-expanded", "false");

    unlockBody();
  }

  if (burger && navList) {
    burger.addEventListener("click", () => {
      const isOpen = navList.classList.contains("open");

      if (isOpen) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });

    qsa(".nav-list .nav-link").forEach((link) => {
      link.addEventListener("click", closeMobileMenu);
    });
  }

  window.addEventListener("resize", () => {
    if (window.innerWidth > (document.body.classList.contains("studio-v5") ? 1100 : 900)) {
      closeMobileMenu();
    }
  });

  /* Compact language disclosure: links retain their existing routes. */
  const languageSwitch = qs(".language-switch");
  const languageToggle = qs(".language-toggle");
  const languageOptions = qs(".language-options");

  function closeLanguageMenu(restoreFocus = false) {
    if (!languageToggle || !languageOptions) return;
    const wasOpen = !languageOptions.hidden;
    languageOptions.hidden = true;
    languageToggle.setAttribute("aria-expanded", "false");
    if (restoreFocus && wasOpen) languageToggle.focus();
  }

  function openLanguageMenu() {
    if (!languageOptions) return;
    closeMobileMenu();
    languageOptions.hidden = false;
    languageToggle.setAttribute("aria-expanded", "true");
  }

  if (languageSwitch && languageToggle && languageOptions) {
    languageToggle.addEventListener("click", () => {
      if (languageOptions.hidden) openLanguageMenu();
      else closeLanguageMenu();
    });
    languageSwitch.addEventListener("keydown", event => {
      if (event.key === "Escape") {
        event.preventDefault();
        closeLanguageMenu(true);
      } else if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        openLanguageMenu();
        const links = qsa("a", languageOptions);
        const current = links.indexOf(document.activeElement);
        const next = current < 0 ? (event.key === "ArrowDown" ? 0 : links.length - 1)
          : (current + (event.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
        links[next]?.focus();
      }
    });
    document.addEventListener("click", event => {
      if (!languageSwitch.contains(event.target)) closeLanguageMenu();
    });
    languageSwitch.addEventListener("focusout", event => {
      if (!languageSwitch.contains(event.relatedTarget)) closeLanguageMenu();
    });
  }

  // Native details/summary preserve keyboard interaction and independent answers.
  qsa(".faq-item").forEach(item => {
    const summary = qs("summary", item);
    item.addEventListener("toggle", () => summary.setAttribute("aria-expanded", String(item.open)));
  });

  /* =========================================================
     SMOOTH INTERNAL ANCHORS
  ========================================================= */

  const anchorTarget = (hash) => {
    if (!hash || hash === "#") {
      return null;
    }

    try {
      return document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch {
      return null;
    }
  };

  const scrollToAnchor = (target, focus = false) => {
    const headerHeight = qs(".header")?.offsetHeight || 0;

    if (focus) {
      const addedTabIndex = !target.hasAttribute("tabindex");

      if (addedTabIndex) {
        target.setAttribute("tabindex", "-1");
      }

      target.focus({
        preventScroll: true,
      });

      if (addedTabIndex) {
        target.addEventListener(
          "blur",
          () => target.removeAttribute("tabindex"),
          { once: true },
        );
      }
    }

    window.scrollTo({
      top: Math.max(
        0,
        target.getBoundingClientRect().top + window.scrollY - headerHeight - 20,
      ),

      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "auto"
        : "smooth",
    });
  };

  const normalizedPath = (path) => {
    return path.replace(/\/index\.html$/, "/");
  };

  qsa('a[href*="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      if (
        event.defaultPrevented ||
        event.button !== 0 ||
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey
      ) {
        return;
      }

      if (
        link.hasAttribute("download") ||
        (link.target && link.target !== "_self")
      ) {
        return;
      }

      const url = new URL(link.href, window.location.href);

      if (
        url.origin !== window.location.origin ||
        normalizedPath(url.pathname) !==
          normalizedPath(window.location.pathname) ||
        url.search !== window.location.search
      ) {
        return;
      }

      const target = anchorTarget(url.hash);

      if (!target) {
        return;
      }

      event.preventDefault();
      closeMobileMenu();

      if (window.location.hash !== url.hash) {
        window.history.pushState(null, "", url.hash);
      }

      scrollToAnchor(target, true);
    });
  });

  /* =========================================================
     SCROLL SPY
  ========================================================= */

  const sections = qsa("section[id]");

  const internalNavLinks = qsa(
    '.nav-link[href^="#"], ' +
      '.nav-link[href^="/#"], ' +
      '.nav-link[href^="/pl/#"], ' +
      '.nav-link[href^="/en/#"]',
  );

  const getAnchorIdFromHref = (href) => {
    if (!href) {
      return "";
    }

    const hashPosition = href.indexOf("#");

    if (hashPosition === -1) {
      return "";
    }

    return href.substring(hashPosition + 1);
  };

  const updateActiveNav = () => {
    if (!sections.length || !internalNavLinks.length) {
      return;
    }

    const header = qs(".header");

    const offset = window.scrollY + (header ? header.offsetHeight : 0) + 120;

    let currentSection = "";

    sections.forEach((section) => {
      if (offset >= section.offsetTop) {
        currentSection = section.id;
      }
    });

    if (!currentSection) {
      return;
    }

    internalNavLinks.forEach((link) => {
      const id = getAnchorIdFromHref(link.getAttribute("href"));

      link.classList.toggle("active", id === currentSection);
    });
  };

  if (sections.length && internalNavLinks.length) {
    window.addEventListener("scroll", updateActiveNav, { passive: true });

    updateActiveNav();
  }

  /* =========================================================
     FORM STATUS
  ========================================================= */

  const setFormStatus = (form, message, type = "") => {
    const status = qs(".js-form-status", form);

    if (!status) {
      return;
    }

    status.textContent = message;

    status.classList.remove("success", "error");

    if (type) {
      status.classList.add(type);
    }
  };

  /* =========================================================
     BUTTON LOADING STATE
  ========================================================= */

  const setButtonLoading = (button, loading) => {
    if (!button) {
      return;
    }

    if (loading) {
      button.dataset.originalText = button.textContent.trim();

      button.disabled = true;
    } else {
      button.disabled = false;

      if (button.dataset.originalText) {
        button.textContent = button.dataset.originalText;

        delete button.dataset.originalText;
      }
    }
  };

  /* =========================================================
     COLLECT LEAD DATA
  ========================================================= */

  const collectLeadData = (form) => {
    const formData = new FormData(form);

    const data = Object.fromEntries(formData.entries());

    const comment = String(data.message || data.comment || "").trim();

    return {
      createdAt: new Date().toISOString(),

      leadSource: "Raccoon SEO Studio Website",

      language: getCurrentLanguage(),

      pageUrl: window.location.href,

      // Field expected by n8n
      page: window.location.href,

      pagePath: window.location.pathname,

      pageTitle: document.title,

      name: String(data.name || "").trim(),

      phone: normalizePhone(data.phone || ""),

      email: String(data.email || "").trim(),

      company: String(data.company || "").trim(),

      service: String(data.service || "").trim(),

      budget: String(data.budget || "").trim(),

      // Original field retained
      comment,

      // Field expected by n8n
      message: comment,

      utm_source: new URLSearchParams(window.location.search).get("utm_source") || "",

      userAgent: navigator.userAgent,
    };
  };

  /* =========================================================
     SEND WEBHOOK
  ========================================================= */

  const sendToWebhook = async (payload) => {
    const response = await fetch(WEBHOOK_URL, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Webhook returned ${response.status}`);
    }

    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const result = await response.json();
      if (result?.success === false || result?.ok === false || result?.error) {
        throw new Error("Webhook rejected the enquiry");
      }
      return result;
    }
    // A successful HTTP response acknowledges receipt (including n8n's text response).
    return { success: true };
  };

  /* =========================================================
     LEAD FORMS
  ========================================================= */

  const leadForms = qsa(".js-lead-form");

  leadForms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (form.dataset.submitting === "true" || !form.reportValidity()) return;

      const texts = getTexts();

      const submitButton = qs('button[type="submit"]', form);

      const payload = collectLeadData(form);

      /* REQUIRED */

      if (!payload.name || !payload.phone || !payload.email) {
        setFormStatus(form, texts.required, "error");

        return;
      }

      /* PHONE */

      if (!isValidPhone(payload.phone)) {
        setFormStatus(form, texts.invalidPhone, "error");

        return;
      }

      /* EMAIL */

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailPattern.test(payload.email)) {
        setFormStatus(form, texts.required, "error");

        return;
      }

      form.dataset.submitting = "true";
      form.setAttribute("aria-busy", "true");
      try {
        if (submitButton) {
          submitButton.dataset.originalText = submitButton.textContent.trim();

          submitButton.textContent = texts.sending;

          submitButton.disabled = true;
        }

        setFormStatus(form, texts.sending);

        await sendToWebhook(payload);

        setFormStatus(form, texts.success, "success");

        form.reset();


      } catch (error) {
        console.error("Lead form error:", error);

        setFormStatus(form, texts.error, "error");
      } finally {
        delete form.dataset.submitting;
        form.removeAttribute("aria-busy");
        if (submitButton) {
          submitButton.disabled = false;

          if (submitButton.dataset.originalText) {
            submitButton.textContent = submitButton.dataset.originalText;

            delete submitButton.dataset.originalText;
          }
        }
      }
    });
  });

  /* =========================================================
     EXTERNAL LINKS
  ========================================================= */

  qsa('a[target="_blank"]').forEach((link) => {
    const currentRel = link.getAttribute("rel") || "";

    const values = new Set(currentRel.split(/\s+/).filter(Boolean));

    values.add("noopener");
    values.add("noreferrer");

    link.setAttribute("rel", Array.from(values).join(" "));
  });

  /* =========================================================
     HASH FROM ANOTHER PAGE
  ========================================================= */

  const scrollToCurrentHash = () => {
    const target = anchorTarget(window.location.hash);

    if (target) {
      scrollToAnchor(target);
    }
  };

  window.addEventListener("load", scrollToCurrentHash);

  window.addEventListener("hashchange", scrollToCurrentHash);

  /* =========================================================
     INITIAL STATE
  ========================================================= */

  if (burger) {
    burger.setAttribute("aria-expanded", "false");
  }
})();
