(() => {
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

    // Блокуємо скрол тільки якщо модалка відкрита
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

      const scrollPos = window.pageYOffset + 200; // враховуємо хедер

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

  if (burger && navList && contactsList) {
    burger.addEventListener("click", () => {
      const isOpen = navList.classList.toggle("open");
      contactsList.classList.toggle("open");
      burger.classList.toggle("active");

      // Блокуємо скрол тільки коли бургер відкритий
      document.body.style.overflow = isOpen ? "hidden" : "auto";

      burger.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    // Закриваємо бургер тільки при кліку по навігації хедера
    document.querySelectorAll(".nav-list .nav-link").forEach((link) => {
      link.addEventListener("click", () => {
        navList.classList.remove("open");
        contactsList.classList.remove("open");
        burger.classList.remove("active");
        document.body.style.overflow = "auto";
        burger.setAttribute("aria-expanded", "false");
      });
    });
  }
})();
