const API = "http://127.0.0.1:8000/tarefas";

// GET (Listar tudo)
async function carregarTarefas() {
    try {
        const res = await fetch(`${API}/`);
        const dados = await res.json();
        renderizar(dados);
    } catch (error) {
        console.error("Erro API:", error);
    }
}

// GET (Buscar)
async function buscarTarefas() {
    const termo = document.getElementById('busca').value;
    if(!termo) return carregarTarefas();
    
    try {
        const res = await fetch(`${API}/buscar?q=${termo}`);
        const dados = await res.json();
        renderizar(dados);
    } catch (error) {
        console.error("Erro busca:", error);
    }
}

// POST (Criar)
async function criarTarefa() {
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const dataLimite = document.getElementById('data_limite').value;

    if(!titulo) return alert("Título é obrigatório!");

    const payload = {
        titulo: titulo,
        descricao: descricao,
        concluida: false,
        data_limite: dataLimite ? dataLimite : null 
    };

    await fetch(`${API}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    // Limpa campos
    document.getElementById('titulo').value = "";
    document.getElementById('descricao').value = "";
    document.getElementById('data_limite').value = "";
    carregarTarefas();
}

// DELETE (Apagar)
async function deletar(id) {
    if(confirm("Tem certeza que deseja apagar?")) {
        await fetch(`${API}/${id}`, { method: "DELETE" });
        carregarTarefas();
    }
}

// PUT (Alternar Status Rápido - Botão Check)
async function toggleStatus(id, statusAtual, titulo, desc, data) {
    await fetch(`${API}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            titulo: titulo, 
            descricao: desc, 
            concluida: !statusAtual, // Inverte o status
            data_limite: data 
        })
    });
    carregarTarefas();
}

// ================= LÓGICA DO MODAL (EDIÇÃO) =================

// 1. Abre a janelinha e preenche os dados
function abrirModal(id, titulo, descricao, data, concluida) {
    document.getElementById('modalEditar').style.display = 'flex';
    
    // Preenche os inputs do modal com os dados atuais da tarefa
    document.getElementById('editId').value = id;
    document.getElementById('editTitulo').value = titulo;
    document.getElementById('editDescricao').value = descricao !== 'null' ? descricao : '';
    document.getElementById('editConcluida').value = concluida; // Guarda o status (true/false)
    
    // Formata a data para o input datetime-local (se existir)
    if(data && data !== 'null') {
        document.getElementById('editData').value = data.slice(0, 16); // Pega yyyy-MM-ddThh:mm
    } else {
        document.getElementById('editData').value = "";
    }
}

// 2. Fecha a janelinha
function fecharModal() {
    document.getElementById('modalEditar').style.display = 'none';
}

// 3. Salva a edição (PUT completo)
async function salvarEdicao() {
    const id = document.getElementById('editId').value;
    const titulo = document.getElementById('editTitulo').value;
    const descricao = document.getElementById('editDescricao').value;
    const data = document.getElementById('editData').value;
    // O valor no input hidden vem como string "true"/"false", precisamos converter
    const concluida = document.getElementById('editConcluida').value === 'true';

    if(!titulo) return alert("O título não pode ficar vazio!");

    const payload = {
        titulo: titulo,
        descricao: descricao,
        concluida: concluida, // Mantém o status que estava
        data_limite: data ? data : null
    };

    await fetch(`${API}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    fecharModal();
    carregarTarefas();
}

// ============================================================

function formatarData(dataISO) {
    if (!dataISO) return "";
    const data = new Date(dataISO);
    return data.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' });
}

function renderizar(tarefas) {
    const lista = document.getElementById('lista');
    lista.innerHTML = "";

    if (tarefas.length === 0) {
        lista.innerHTML = "<li style='justify-content:center; color:#777'>Nenhuma tarefa encontrada.</li>";
        return;
    }

    tarefas.forEach(t => {
        const li = document.createElement('li');
        if(t.concluida) li.classList.add('done');
        
        const dataHtml = t.data_limite 
            ? `<br><small style="color:#e67e22">📅 ${formatarData(t.data_limite)}</small>` 
            : '';

        // ATENÇÃO: Passamos os dados da tarefa para a função abrirModal()
        // O replace(/'/g, "\\'") serve para escapar aspas simples no texto e não quebrar o HTML
        const safeDesc = (t.descricao || '').replace(/'/g, "\\'");
        const safeTitle = t.titulo.replace(/'/g, "\\'");

        li.innerHTML = `
            <div class="task-content">
                <strong>${t.titulo}</strong>
                <small>${t.descricao || ''}</small>
                ${dataHtml}
            </div>
            <div class="actions">
                <button class="btn-check" onclick="toggleStatus(${t.id}, ${t.concluida}, '${safeTitle}', '${safeDesc}', '${t.data_limite || ''}')" title="Concluir/Reabrir">
                    ${t.concluida ? '↩️' : '✅'}
                </button>
                
                <!-- BOTÃO DE EDITAR -->
                <button class="btn-edit" onclick="abrirModal(${t.id}, '${safeTitle}', '${safeDesc}', '${t.data_limite || ''}', ${t.concluida})" title="Editar">
                    ✏️
                </button>

                <button class="btn-delete" onclick="deletar(${t.id})" title="Excluir">🗑️</button>
            </div>
        `;
        lista.appendChild(li);
    });
}

carregarTarefas();