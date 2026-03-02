/**
 * DAG Editor Utilities - Save/Load/Export/Import functionality
 */

// LocalStorage keys
const STORAGE_KEY_PREFIX = 'nice-dag-editor-';

export const DAGEditorUtils = {
  // Save DAG to localStorage
  saveToLocalStorage: (dagName, dagData) => {
    try {
      const key = `${STORAGE_KEY_PREFIX}${dagName}`;
      localStorage.setItem(key, JSON.stringify(dagData));
      return { success: true, message: `DAG "${dagName}" saved successfully` };
    } catch (error) {
      return { success: false, message: `Failed to save: ${error.message}` };
    }
  },

  // Load DAG from localStorage
  loadFromLocalStorage: (dagName) => {
    try {
      const key = `${STORAGE_KEY_PREFIX}${dagName}`;
      const data = localStorage.getItem(key);
      if (!data) {
        return { success: false, message: `No DAG found with name "${dagName}"` };
      }
      return { success: true, data: JSON.parse(data) };
    } catch (error) {
      return { success: false, message: `Failed to load: ${error.message}` };
    }
  },

  // Get all saved DAG names
  getAllSavedDAGs: () => {
    try {
      const keys = Object.keys(localStorage);
      const dagNames = keys
        .filter(key => key.startsWith(STORAGE_KEY_PREFIX))
        .map(key => key.replace(STORAGE_KEY_PREFIX, ''));
      return dagNames;
    } catch (error) {
      return [];
    }
  },

  // Delete DAG from localStorage
  deleteFromLocalStorage: (dagName) => {
    try {
      const key = `${STORAGE_KEY_PREFIX}${dagName}`;
      localStorage.removeItem(key);
      return { success: true, message: `DAG "${dagName}" deleted` };
    } catch (error) {
      return { success: false, message: `Failed to delete: ${error.message}` };
    }
  },

  // Export DAG to JSON file
  exportToFile: (dagName, dagData) => {
    try {
      const dataStr = JSON.stringify(dagData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${dagName || 'dag'}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      return { success: true, message: `DAG exported as "${link.download}"` };
    } catch (error) {
      return { success: false, message: `Failed to export: ${error.message}` };
    }
  },

  // Import DAG from JSON file
  importFromFile: (file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const data = JSON.parse(event.target.result);
          resolve({ success: true, data });
        } catch (error) {
          resolve({ success: false, message: `Invalid JSON: ${error.message}` });
        }
      };
      reader.onerror = () => {
        resolve({ success: false, message: 'Failed to read file' });
      };
      reader.readAsText(file);
    });
  },

  // Save to backend API (optional)
  saveToBackend: async (dagName, dagData, backendUrl = '/api/dags') => {
    try {
      if (!backendUrl) {
        return { success: false, message: 'Backend URL not configured' };
      }
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: dagName, data: dagData })
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return { success: true, message: `DAG saved to backend` };
    } catch (error) {
      return { success: false, message: `Backend save failed: ${error.message}` };
    }
  },

  // Load from backend API (optional)
  loadFromBackend: async (dagName, backendUrl = '/api/dags') => {
    try {
      if (!backendUrl) {
        return { success: false, message: 'Backend URL not configured' };
      }
      const response = await fetch(`${backendUrl}/${dagName}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return { success: false, message: `Backend load failed: ${error.message}` };
    }
  },

  // Extract DAG structure for analysis
  extractDAGInfo: (hierarchicalModel) => {
    try {
      if (!hierarchicalModel || !hierarchicalModel.nodes) {
        return { nodes: 0, edges: 0, nodeIds: [], edgeCount: 0 };
      }
      return {
        nodes: hierarchicalModel.nodes.length,
        edges: hierarchicalModel.edges ? hierarchicalModel.edges.length : 0,
        nodeIds: hierarchicalModel.nodes.map(n => n.id),
        edgeCount: hierarchicalModel.edges ? hierarchicalModel.edges.length : 0
      };
    } catch (error) {
      return { error: error.message };
    }
  }
};

export default DAGEditorUtils;
