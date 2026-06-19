(function () {
  function slider() {
    const track = document.getElementById("sliderTrack");
    if (!track) return;
    const slides = Array.from(track.children);
    const dots = document.getElementById("sliderDots");
    let current = 0;

    if (dots) dots.innerHTML = slides.map(() => "<span></span>").join("");
    const dotItems = dots ? Array.from(dots.children) : [];

    function render(index) {
      current = (index + slides.length) % slides.length;
      track.style.transform = `translateX(-${current * 100}%)`;
      dotItems.forEach((dot, i) => dot.classList.toggle("active", i === current));
    }

    document.getElementById("sliderPrev")?.addEventListener("click", () => render(current - 1));
    document.getElementById("sliderNext")?.addEventListener("click", () => render(current + 1));
    setInterval(() => render(current + 1), 4200);
    render(0);
  }

  function dateMask() {
    const field = document.querySelector('input[name="start_date"]');
    if (!field || field.type === "date") return;
    field.addEventListener("input", () => {
      let value = field.value.replace(/\D/g, "").slice(0, 8);
      if (value.length > 4) value = `${value.slice(0, 2)}.${value.slice(2, 4)}.${value.slice(4)}`;
      else if (value.length > 2) value = `${value.slice(0, 2)}.${value.slice(2)}`;
      field.value = value;
    });
  }

  function statusAutoSubmit() {
    document.querySelectorAll("[data-status-select]").forEach((select) => {
      select.dataset.old = select.value;
      select.addEventListener("change", () => {
        if (confirm("Сохранить новый статус заявки?")) select.form.submit();
        else select.value = select.dataset.old;
      });
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    slider();
    dateMask();
    statusAutoSubmit();
  });
})();
