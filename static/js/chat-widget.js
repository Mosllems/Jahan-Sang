(function () {
  "use strict";

  function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
  }

  document.addEventListener("DOMContentLoaded", function () {
    const widget = document.getElementById("chat-widget");
    if (!widget) return;

    const toggleBtn = document.getElementById("chat-widget-toggle");
    const panel = document.getElementById("chat-widget-panel");
    const closeBtn = document.getElementById("chat-widget-close");
    const messagesEl = document.getElementById("chat-widget-messages");
    const typingEl = document.getElementById("chat-widget-typing");
    const form = document.getElementById("chat-widget-form");
    const input = document.getElementById("chat-widget-input");
    const sendBtn = form.querySelector(".chat-widget-send");
    const historyDataEl = document.getElementById("chat-history-data");

    function scrollToBottom() {
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function appendMessage(role, text) {
      const bubble = document.createElement("div");
      bubble.className = "chat-msg chat-msg--" + (role === "user" ? "user" : "bot");
      bubble.textContent = text;
      messagesEl.appendChild(bubble);
      scrollToBottom();
    }

    function renderHistory() {
      if (!historyDataEl) return;
      let history = [];
      try {
        history = JSON.parse(historyDataEl.textContent);
      } catch (e) {
        history = [];
      }
      history.forEach(function (item) {
        appendMessage(item.role, item.text);
      });
    }

    function showTyping() {
      typingEl.hidden = false;
    }
    function hideTyping() {
      typingEl.hidden = true;
    }

    function togglePanel(forceOpen) {
      const shouldOpen = typeof forceOpen === "boolean" ? forceOpen : panel.hidden;
      panel.hidden = !shouldOpen;
      if (shouldOpen) {
        input.focus();
        scrollToBottom();
      }
    }

    function sendMessage(event) {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;

      appendMessage("user", text);
      input.value = "";
      input.disabled = true;
      sendBtn.disabled = true;
      showTyping();

      fetch("/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: text }),
      })
        .then(function (response) {
          if (!response.ok) throw new Error("bad response");
          return response.json();
        })
        .then(function (data) {
          appendMessage("bot", data.reply);
        })
        .catch(function () {
          appendMessage("bot", "خطا در برقراری ارتباط. لطفاً دوباره تلاش کنید.");
        })
        .finally(function () {
          hideTyping();
          input.disabled = false;
          sendBtn.disabled = false;
          input.focus();
          scrollToBottom();
        });
    }

    toggleBtn.addEventListener("click", function () {
      togglePanel();
    });
    closeBtn.addEventListener("click", function () {
      togglePanel(false);
    });
    form.addEventListener("submit", sendMessage);

    renderHistory();
  });
})();
