// static/tabulator_engine.js

// Initialize Tabulator table
window.createTabulator = function (containerId, optionsJson) {
    const options = JSON.parse(optionsJson);

    // Destroy existing table if re-rendering
    const existing = Tabulator.findTable('#' + containerId);
    if (existing.length > 0) {
        existing[0].destroy();
    }

    // Add default column menu
    options.columnHeaderMenu = [
        {
            label: "Hide Column",
            action: function (e, column) {
                column.hide();
            }
        }
    ];

    const table = new Tabulator('#' + containerId, options);

    // Expose API globally
    window[containerId + '_table'] = table;
};


// Wait until Tabulator + DOM are ready
window.waitForElementAndInit = function (containerId, optionsJson) {
    const checkExist = setInterval(() => {
        const el = document.getElementById(containerId);
        if (el && window.createTabulator && window.Tabulator) {
            clearInterval(checkExist);
            window.createTabulator(containerId, optionsJson);
        }
    }, 50);
};


// Build the column chooser dropdown
window.buildColumnChooser = function (tableId, menuId) {
    const table = window[tableId + '_table'];
    if (!table) return;

    const menu = document.getElementById(menuId);
    menu.innerHTML = '';

    table.getColumns().forEach(col => {
        const field = col.getField();
        const title = col.getDefinition().title;

        const wrapper = document.createElement('div');
        wrapper.style.display = 'flex';
        wrapper.style.alignItems = 'center';
        wrapper.style.gap = '6px';
        wrapper.style.padding = '6px 8px';
        wrapper.style.backgroundColor = '#f9f9f9';
        wrapper.style.borderRadius = '3px';
        wrapper.style.whiteSpace = 'nowrap';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = col.isVisible();
        checkbox.style.cursor = 'pointer';
        checkbox.onchange = () => {
            if (checkbox.checked) col.show();
            else col.hide();
        };

        const label = document.createElement('label');
        label.textContent = title;
        label.style.cursor = 'pointer';
        label.style.margin = '0';
        label.style.fontSize = '13px';

        wrapper.appendChild(checkbox);
        wrapper.appendChild(label);
        menu.appendChild(wrapper);
    });
};
