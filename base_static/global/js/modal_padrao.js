/**
 * Modal Padrão - JavaScript Unificado
 * Script reutilizável para modais AJAX com funcionalidades otimizadas
 * Baseado no padrão usado na tela de suporte
 */

class ModalPadrao {
  constructor(modalId, options = {}) {
    this.modalElement = document.getElementById(modalId);
    this.modal = new bootstrap.Modal(this.modalElement, {
      backdrop: 'static',
      keyboard: true,
      ...options.bootstrapOptions
    });
    this.modalContent = this.modalElement.querySelector('#modal-form-content, .modal-body');
    this.modalTitle = this.modalElement.querySelector('.modal-title');
    this.options = {
      titleCreate: 'Novo Item',
      titleEdit: 'Editar Item',
      loadingMessage: '<div class="text-center py-3"><div class="spinner-border spinner-border-sm text-primary" role="status"></div></div>',
      errorMessage: '<div class="alert alert-danger">Erro ao carregar formulário</div>',
      saveErrorMessage: 'Erro ao salvar',
      ...options
    };
    
    this.init();
  }

  init() {
    // Event listeners para botões de abertura do modal
    this.setupOpenModalButtons();
    this.setupEditButtons();
    this.setupCloseButtons();
  }

  setupCloseButtons() {
    // Garantir que todos os botões de fechar funcionem
    this.modalElement.addEventListener('click', (e) => {
      if (e.target.matches('.btn-close') || 
          e.target.matches('[data-bs-dismiss="modal"]') ||
          e.target.classList.contains('btn-cancelar')) {
        this.modal.hide();
      }
    });

    // Fechar ao clicar no backdrop
    this.modalElement.addEventListener('hidden.bs.modal', () => {
      this.modalContent.innerHTML = this.options.loadingMessage;
    });
  }

  setupOpenModalButtons() {
    // Botão principal de criar
    const createBtn = document.querySelector('.open-modal-btn');
    if (createBtn) {
      createBtn.onclick = (e) => {
        e.preventDefault();
        this.carregarFormulario(createBtn.getAttribute('data-url'), this.options.titleCreate);
      };
    }
  }

  setupEditButtons() {
    // Delegação de eventos para botões de editar
    document.onclick = (e) => {
      const editBtn = e.target.closest('.edit-client, .edit-suporte, .edit-servico, .edit-tarefa, .edit-btn');
      if (editBtn) {
        e.preventDefault();
        this.carregarFormulario(editBtn.getAttribute('data-url'), this.options.titleEdit);
      }
    };
  }

  carregarFormulario(url, titulo = 'Item') {
    if (this.modalTitle) {
      this.modalTitle.textContent = titulo;
    }
    
    this.modalContent.innerHTML = this.options.loadingMessage;
    this.modal.show();
    
    fetch(url)
      .then(response => response.text())
      .then(html => {
        this.modalContent.innerHTML = html;
        this.setupForm();
      })
      .catch(error => {
        console.error('Erro:', error);
        this.modalContent.innerHTML = this.options.errorMessage;
      });
  }

  setupForm() {
    const form = this.modalContent.querySelector('form');
    if (!form) return;
    
    // Adicionar botão cancelar se não existir
    this.addCancelButton(form);
    
    // Configurar envio do formulário
    form.onsubmit = (e) => {
      e.preventDefault();
      this.submitForm(form);
    };
  }

  addCancelButton(form) {
    // Procurar por área de botões existente
    let btnArea = form.querySelector('.btn, .modal-footer, .form-actions, .button-group');
    
    // Se não encontrar área de botões, criar uma
    if (!btnArea) {
      btnArea = document.createElement('div');
      btnArea.className = 'btn';
      form.appendChild(btnArea);
    }
    
    // Adicionar botão cancelar se não existir
    if (!btnArea.querySelector('.btn-cancelar')) {
      const btnCancelar = document.createElement('button');
      btnCancelar.type = 'button';
      btnCancelar.className = 'btn-cancelar';
      btnCancelar.textContent = 'CANCELAR';
      btnCancelar.onclick = () => this.modal.hide();
      btnArea.insertBefore(btnCancelar, btnArea.firstChild);
    }
  }

  submitForm(form) {
    const formData = new FormData(form);
    const submitBtn = form.querySelector('.btn-form, button[type="submit"], .btn-primary');
    
    if (submitBtn) {
      submitBtn.disabled = true;
      const originalText = submitBtn.textContent;
      submitBtn.textContent = 'SALVANDO...';
    }

    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
      }
    })
    .then(response => {
      // Verificar se a resposta é JSON ou texto
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return response.json();
      } else {
        return response.text().then(text => {
          // Se não é JSON, pode ser HTML com erros
          return { html: text, message: 'form_error' };
        });
      }
    })
    .then(data => {
      if (data.message === 'success') {
        this.modal.hide();
        window.location.reload();
      } else if (data.html) {
        // Recarregar o formulário com erros
        this.modalContent.innerHTML = data.html;
        this.setupForm();
      } else {
        alert('Erro: Resposta inválida do servidor');
      }
    })
    .catch(error => {
      console.error('Erro:', error);
      alert(this.options.saveErrorMessage);
    })
    .finally(() => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText || 'SALVAR';
      }
    });
  }

  // Métodos públicos para controle manual do modal
  show() {
    this.modal.show();
  }

  hide() {
    this.modal.hide();
  }

  // Método para carregar conteúdo customizado
  loadContent(content) {
    this.modalContent.innerHTML = content;
  }
}

// Função para inicializar modais automaticamente
function initModalPadrao(modalId, options = {}) {
  document.addEventListener('DOMContentLoaded', function() {
    new ModalPadrao(modalId, options);
  });
}

// Exportar para uso global
window.ModalPadrao = ModalPadrao;
window.initModalPadrao = initModalPadrao;
