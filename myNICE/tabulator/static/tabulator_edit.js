// static/tabulator_engine.js

// Initialize Tabulator table
window.createTabulator = function (containerId, optionsJson) {
    const options = JSON.parse(optionsJson);

    const existing = Tabulator.findTable('#' + containerId);
    if (existing.length > 0) {
        existing[0].destroy();
    }

    const table = new Tabulator('#' + containerId, options);
    window[containerId + '_table'] = table;
};

// Wait until DOM + Tabulator are ready
window.waitForElementAndInit = function (containerId, optionsJson) {
    const checkExist = setInterval(() => {
        const el = document.getElementById(containerId);
        if (el && window.createTabulator && window.Tabulator) {
            clearInterval(checkExist);
            window.createTabulator(containerId, optionsJson);
        }
    }, 50);
};

// Open Quill modal editor
window.openTinyEditor = function (tableId, row, field, modalId, textareaId) {
    const table = window[tableId + '_table'];
    if (!table || !row) return;

    const cell = row.getCell(field);
    if (!cell) return;

    const currentValue = cell.getValue() || '';

    const modal = document.getElementById(modalId);
    const editorContainer = document.getElementById(textareaId);

    if (!modal || !editorContainer) {
        console.error('Modal or editor container not found');
        return;
    }

    if (!window.Quill) {
        console.error('Quill not loaded');
        return;
    }

    console.log('Opening Quill editor for field:', field);
    modal.style.display = 'flex';
    editorContainer.innerHTML = ''; // Clear previous editor

    const saveBtn = modal.querySelector('.tiny-save');
    const cancelBtn = modal.querySelector('.tiny-cancel');

    // Create Quill instance
    const quill = new Quill(editorContainer, {
        theme: 'snow',
        modules: {
            toolbar: [
                ['bold', 'italic', 'underline', 'strike'],
                ['blockquote', 'code-block'],
                [{ 'header': 1 }, { 'header': 2 }],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'color': [] }, { 'background': [] }],
                ['link', 'image'],
                ['clean']
            ]
        }
    });

    // Set initial content
    quill.root.innerHTML = currentValue;

    if (saveBtn) {
        saveBtn.onclick = function() {
            const html = quill.root.innerHTML;
            cell.setValue(html);
            modal.style.display = 'none';
            console.log('Content saved');
        };
    }

    if (cancelBtn) {
        cancelBtn.onclick = function() {
            modal.style.display = 'none';
            console.log('Edit cancelled');
        };
    }
};

