// Smooth scrolling for internal links
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Animated scroll triggers for sections
  const revealSections = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, { threshold: 0.15 });
  revealSections.forEach(section => observer.observe(section));
});

// Loading indicator for bots/interactives (placeholder)
function showLoadingIndicator() {
  let loader = document.getElementById('loading-indicator');
  if (!loader) {
    loader = document.createElement('div');
    loader.id = 'loading-indicator';
    loader.style.position = 'fixed';
    loader.style.top = '0';
    loader.style.left = '0';
    loader.style.width = '100vw';
    loader.style.height = '100vh';
    loader.style.background = 'rgba(255,255,255,0.7)';
    loader.style.display = 'flex';
    loader.style.alignItems = 'center';
    loader.style.justifyContent = 'center';
    loader.style.zIndex = '9999';
    loader.innerHTML = '<div style="border:4px solid #eee;border-top:4px solid #22c7ff;border-radius:50%;width:48px;height:48px;animation:spin 1s linear infinite;"></div>';
    document.body.appendChild(loader);
  }
  loader.style.display = 'flex';
}
function hideLoadingIndicator() {
  const loader = document.getElementById('loading-indicator');
  if (loader) loader.style.display = 'none';
}
// Example usage: showLoadingIndicator(); hideLoadingIndicator();
// Exit-intent popup
let exitIntentShown = false;
function showExitIntentPopup() {
  if (exitIntentShown) return;
  exitIntentShown = true;
  const popup = document.createElement('div');
  popup.style.position = 'fixed';
  popup.style.top = '0';
  popup.style.left = '0';
  popup.style.width = '100vw';
  popup.style.height = '100vh';
  popup.style.background = 'rgba(10,18,32,0.92)';
  popup.style.display = 'flex';
  popup.style.alignItems = 'center';
  popup.style.justifyContent = 'center';
  popup.style.zIndex = '9999';
  popup.innerHTML = `
    <div style="background:#fff;max-width:340px;padding:32px 24px;border-radius:18px;text-align:center;box-shadow:0 8px 32px rgba(34,199,255,0.13);">
      <h2 style="color:#222;margin-bottom:10px;">Wait! Don’t leave yet</h2>
      <p style="color:#222;margin-bottom:18px;">Get a free website launch checklist or book a free consult before you go.</p>
      <a href="/contact/" class="button button--primary" style="margin-bottom:10px;">Book a free consult</a><br>
      <button id="close-exit-popup" class="button button--ghost" style="margin-top:10px;">No thanks</button>
    </div>
  `;
  document.body.appendChild(popup);
  document.getElementById('close-exit-popup').onclick = () => popup.remove();
}
setTimeout(() => {
  document.addEventListener('mouseout', function(e) {
    if (e.clientY < 40) {
      showExitIntentPopup();
    }
  });
}, 2000);
const revealTargets = document.querySelectorAll('.reveal');
const navToggle = document.querySelector('[data-nav-toggle]');
const navPanel = document.querySelector('[data-nav-panel]');
const chatWidget = document.querySelector('[data-chat-widget]');

const currentYear = new Date().getFullYear();
const footerYear = document.querySelector('[data-year]');

if (footerYear) {
  footerYear.textContent = currentYear;
}

if (navToggle && navPanel) {
  navToggle.addEventListener('click', () => {
    const isOpen = navPanel.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navPanel.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navPanel.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.18 });

  revealTargets.forEach((element, index) => {
    element.style.transitionDelay = `${index * 90}ms`;
    observer.observe(element);
  });
} else {
  revealTargets.forEach((element) => element.classList.add('is-visible'));
}

if (chatWidget) {
  const toggleButton = chatWidget.querySelector('.chat-widget__toggle');
  const panel = chatWidget.querySelector('.chat-widget__panel');
  const closeButton = chatWidget.querySelector('.chat-widget__close');
  const form = chatWidget.querySelector('.chat-widget__form');
  const input = chatWidget.querySelector('#chat-widget-input');
  const messages = chatWidget.querySelector('.chat-widget__messages');
  const sendButton = chatWidget.querySelector('.chat-widget__send');
  const chatHistory = [];
  let typingIndicator = null;

  const addMessage = (text, type = 'bot') => {
    const bubble = document.createElement('div');
    bubble.className = `chat-widget__bubble${type === 'user' ? ' chat-widget__bubble--user' : ''}`;
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
  };

  const showTypingIndicator = () => {
    if (typingIndicator) return;
    typingIndicator = document.createElement('div');
    typingIndicator.className = 'chat-widget__typing';
    typingIndicator.innerHTML = '<span class="chat-widget__typing-dot"></span><span class="chat-widget__typing-dot"></span><span class="chat-widget__typing-dot"></span>';
    messages.appendChild(typingIndicator);
    messages.scrollTop = messages.scrollHeight;
  };

  const hideTypingIndicator = () => {
    if (typingIndicator) {
      typingIndicator.remove();
      typingIndicator = null;
    }
  };

  const getCsrfToken = () => {
    const tokenInput = document.querySelector('.csrf-token-form input[name="csrfmiddlewaretoken"]');
    return tokenInput ? tokenInput.value : '';
  };

  const openPanel = () => {
    panel.classList.add('is-open');
    panel.setAttribute('aria-hidden', 'false');
    toggleButton.setAttribute('aria-expanded', 'true');
    input.focus();
  };

  const closePanel = () => {
    panel.classList.remove('is-open');
    panel.setAttribute('aria-hidden', 'true');
    toggleButton.setAttribute('aria-expanded', 'false');
  };

  toggleButton.addEventListener('click', () => {
    const isOpen = panel.classList.contains('is-open');
    if (isOpen) {
      closePanel();
    } else {
      openPanel();
      if (!messages.childElementCount) {
        addMessage('Hi, I am Lee. Ask me anything about Bwire Global Tech.');
      }
    }
  });

  closeButton.addEventListener('click', closePanel);

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const value = input.value.trim();
    if (!value) {
      return;
    }
    addMessage(value, 'user');
    chatHistory.push({ role: 'user', content: value });
    input.value = '';
    sendButton.disabled = true;
    showTypingIndicator();
    fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ message: value, history: chatHistory })
    })
      .then((response) => response.json())
      .then((data) => {
        hideTypingIndicator();
        if (data.answer) {
          addMessage(data.answer);
          chatHistory.push({ role: 'assistant', content: data.answer });
          return;
        }

        if (data.error) {
          addMessage('Sorry, Lee is unavailable right now. Please try again later.');
          return;
        }

        addMessage('Sorry, Lee is unavailable right now. Please try again later.');
      })
      .catch(() => {
        hideTypingIndicator();
        addMessage('Sorry, Lee is unavailable right now. Please try again later.');
      })
      .finally(() => {
        sendButton.disabled = false;
      });
  });
}
