
document.addEventListener('DOMContentLoaded', function() {

 
  const typingElement = document.getElementById('typing-text');
  if (typingElement) {
    const phrases = [
      "I'm IT Specialist",
      "I'm Network Engineer",
      "I'm Web Developer",
      "I'm Systems Administrator",
      "I'm Tech Solutions Expert",
      "I'm IT Consultant",
      "I'm Problem Solver"
    ];
    
    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;
    
    function typeEffect() {
      const currentPhrase = phrases[phraseIndex];
      
      if (isDeleting) {
        typingElement.textContent = currentPhrase.substring(0, charIndex - 1);
        charIndex--;
        typingSpeed = 50;
      } else {
        typingElement.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;
        typingSpeed = 100;
      }
      
      if (!isDeleting && charIndex === currentPhrase.length) {
        isDeleting = true;
        typingSpeed = 2000;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
        typingSpeed = 500;
      }
      
      setTimeout(typeEffect, typingSpeed);
    }
    
    setTimeout(typeEffect, 1000);
  }

 
  const skillBars = document.querySelectorAll('.skill-bar-fill');
  
  const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
      }
    });
  }, { threshold: 0.5 });
  
  skillBars.forEach(bar => skillObserver.observe(bar));


  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        const offset = 80;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;
        
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });


  const revealElements = document.querySelectorAll('.card, .project-card, .timeline-item, .hero-row, .stat-item, .step, .testimonial-card, .cert-card, .quick-card, .cta-section, .core-skill-item, .reference-card, .language-item');
  
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        entry.target.style.transition = 'opacity 0.8s ease, transform 0.6s ease';
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  revealElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.8s ease, transform 0.6s ease';
    revealObserver.observe(el);
  });


  const counters = document.querySelectorAll('.stat-number');
  
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.count);
        let current = 0;
        const increment = Math.ceil(target / 40);
        
        const timer = setInterval(() => {
          current += increment;
          if (current >= target) {
            el.textContent = target;
            clearInterval(timer);
          } else {
            el.textContent = current;
          }
        }, 30);
        
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  
  counters.forEach(c => counterObserver.observe(c));


  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-side a:not(.hire-btn)');
  
  function highlightNav() {
    let current = '';
    const scrollPosition = window.scrollY + 120;
    
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });
    
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) {
        link.classList.add('active');
      }
    });
  }
  
  window.addEventListener('scroll', highlightNav);
  highlightNav();

  
  const heroSection = document.querySelector('.hero-section');
  if (heroSection) {
    window.addEventListener('scroll', function() {
      const scrolled = window.pageYOffset;
      const heroContent = heroSection.querySelector('.hero-row');
      if (heroContent && scrolled < heroSection.offsetHeight) {
        const translateY = scrolled * 0.3;
        heroContent.style.transform = `translateY(${translateY}px)`;
        heroContent.style.transition = 'transform 0.1s ease';
      }
    });
  }

 
  const scrollTopBtn = document.createElement('button');
  scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
  scrollTopBtn.className = 'scroll-top-btn';
  scrollTopBtn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: #4A9FD4;
    color: #0A1628;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 999;
    box-shadow: 0 4px 15px rgba(74, 159, 212, 0.3);
  `;
  
  document.body.appendChild(scrollTopBtn);


  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      scrollTopBtn.style.opacity = '1';
      scrollTopBtn.style.visibility = 'visible';
    } else {
      scrollTopBtn.style.opacity = '0';
      scrollTopBtn.style.visibility = 'hidden';
    }
  });

  scrollTopBtn.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  
  scrollTopBtn.addEventListener('mouseenter', function() {
    this.style.transform = 'translateY(-3px)';
    this.style.boxShadow = '0 6px 25px rgba(74, 159, 212, 0.5)';
  });

  scrollTopBtn.addEventListener('mouseleave', function() {
    this.style.transform = 'translateY(0)';
    this.style.boxShadow = '0 4px 15px rgba(74, 159, 212, 0.3)';
  });

 
  const projectCards = document.querySelectorAll('.project-card');
  projectCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      const img = this.querySelector('.project-img');
      if (img) {
        img.style.transition = 'transform 0.5s ease';
        img.style.transform = 'scale(1.05)';
      }
    });
    
    card.addEventListener('mouseleave', function() {
      const img = this.querySelector('.project-img');
      if (img) {
        img.style.transform = 'scale(1)';
      }
    });
  });

  
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const name = this.querySelector('input[placeholder="Full Name"]');
      const email = this.querySelector('input[placeholder="Email Address"]');
      const message = this.querySelector('textarea');
      
      if (name && email && message) {
        if (!name.value.trim() || !email.value.trim() || !message.value.trim()) {
          showFlashMessage('Please fill in all required fields.', 'error');
          return;
        }
        
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email.value.trim())) {
          showFlashMessage('Please enter a valid email address.', 'error');
          return;
        }
        
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        setTimeout(() => {
          showFlashMessage('Thank you for your message! I\'ll get back to you soon.', 'success');
          this.reset();
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }, 1500);
      }
    });
  }

  
  function showFlashMessage(message, type = 'success') {
    const flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) return;
    
    const flash = document.createElement('div');
    flash.className = `flash flash-${type}`;
    flash.textContent = message;
    
    flashContainer.appendChild(flash);
    
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s ease';
      flash.style.opacity = '0';
      setTimeout(() => {
        if (flash.parentNode) {
          flash.parentNode.removeChild(flash);
        }
      }, 500);
    }, 5000);
  }


  const statsSection = document.querySelector('.stats-section');
  if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const counters = document.querySelectorAll('.stat-number');
          counters.forEach(counter => {
            const target = parseInt(counter.dataset.count);
            let current = 0;
            const increment = Math.ceil(target / 40);
            
            const timer = setInterval(() => {
              current += increment;
              if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
              } else {
                counter.textContent = current;
              }
            }, 30);
          });
          statsObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    
    statsObserver.observe(statsSection);
  }

  
  const whatsappBtns = document.querySelectorAll('.btn-whatsapp, .whatsapp-float, .whatsapp-btn');
  whatsappBtns.forEach(btn => {
    btn.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-3px) scale(1.02)';
    });
    btn.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  console.log('Portfolio ready - Kipkosgei Brandon');
});