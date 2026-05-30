// Reveal on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el, i) => {
  el.style.transitionDelay = (Math.min(i, 6) * 60) + 'ms';
  io.observe(el);
});

// Mobile menu toggle
const mt = document.querySelector('.mob-toggle');
const mm = document.querySelector('.mob-menu');
if (mt && mm) mt.addEventListener('click', () => mm.classList.toggle('open'));

// Geography tabs
const cities = {
  msk: { city: 'Москва', addr: 'г. Москва, ул. Примерная, д. 1, офис 101', phone: '+7 (495) 123-45-67' },
  spb: { city: 'Санкт-Петербург', addr: 'г. Санкт-Петербург, пр. Примерный, д. 12', phone: '+7 (812) 123-45-67' },
  ekb: { city: 'Екатеринбург', addr: 'г. Екатеринбург, ул. Примерная, д. 5', phone: '+7 (343) 123-45-67' },
  krd: { city: 'Краснодар', addr: 'г. Краснодар, ул. Примерная, д. 8', phone: '+7 (861) 123-45-67' },
  nsk: { city: 'Новосибирск', addr: 'г. Новосибирск, ул. Примерная, д. 3', phone: '+7 (383) 123-45-67' },
};
document.querySelectorAll('.geo .tab').forEach((tab) => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.geo .tab').forEach((t) => t.classList.remove('active'));
    tab.classList.add('active');
    const c = cities[tab.dataset.city];
    if (!c) return;
    const p = document.querySelector('.geo .panel');
    p.querySelector('[data-f="city"]').textContent = c.city;
    p.querySelector('[data-f="addr"]').textContent = c.addr;
    p.querySelector('[data-f="phone"]').textContent = c.phone;
  });
});

// Demo forms / request buttons (no backend)
document.querySelectorAll('[data-demo-form]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Демо-версия сайта: форма не отправляется. На рабочем сайте заявка уйдёт менеджеру.');
  });
});
document.querySelectorAll('[data-req]').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    alert('Демо-версия сайта: здесь откроется форма запроса коммерческого предложения.');
  });
});
