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

  const addMessage = (text, type = 'bot') => {
    const bubble = document.createElement('div');
    bubble.className = `chat-widget__bubble${type === 'user' ? ' chat-widget__bubble--user' : ''}`;
    bubble.textContent = text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
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
        addMessage('Sorry, Lee is unavailable right now. Please try again later.');
      })
      .finally(() => {
        sendButton.disabled = false;
      });
  });
}
