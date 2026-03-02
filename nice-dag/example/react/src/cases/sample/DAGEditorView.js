import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useNiceDag, useNiceDagNode, useNiceDagEdge } from '@ebay/nice-dag-react';
import { HierarchicalModel } from '../data/ReadOnlyViewData';
import {
  FullscreenExitOutlined,
  PlusCircleOutlined,
  DragOutlined,
  CloseCircleOutlined,
  CloseOutlined,
  SaveOutlined,
  DownloadOutlined,
  UploadOutlined,
  DeleteOutlined,
  CopyOutlined
} from '@ant-design/icons';
import { Button, Dropdown, Menu, Space, Input, Modal, message, Tabs, Select } from 'antd';
import ZoomInOutSlider from './ZoomInOutSlider';
import DAGEditorUtils from './DAGEditorUtils';
import './DAGEditorView.less';

const NODE_WIDTH = 150;
const NODE_HEIGHT = 60;
const CIRCLE_W_H = 30;

// ====== Node Components ======
function StartNode({ node, niceDag }) {
  const { startNodeDragging } = useNiceDagNode({ node, niceDag });
  return (
    <div className="editable-sample-start-node">
      <div className="editable-sample-start-node-move-hand" onMouseDown={startNodeDragging} />
      <SquareConnector type="out" node={node} niceDag={niceDag} />
    </div>
  );
}

function EndNode({ node, niceDag }) {
  const { startNodeDragging } = useNiceDagNode({ node, niceDag });
  return (
    <div className="editable-sample-end-node" onMouseDown={startNodeDragging}>
      <SquareConnector type="in" />
    </div>
  );
}

let nodeCtnRef = 0;

function Edge({ edge }) {
  const { onEdgeRemove, onNodeInsert } = useNiceDagEdge(edge);
  const runInsertBetween = useCallback(() => {
    onNodeInsert([
      { 'id': `insert-node-${nodeCtnRef}` },
      { 'id': `insert-node-${nodeCtnRef + 1}` },
      { 'id': `insert-node-${nodeCtnRef + 2}` }
    ]);
    nodeCtnRef += 3;
  }, [onNodeInsert]);

  return (
    <div className="dag-editor-edge-label">
      <CloseCircleOutlined 
        onClick={onEdgeRemove}
        style={{ cursor: 'pointer', fontSize: '12px' }}
      />
    </div>
  );
}

function SquareConnector({ type, node, niceDag }) {
  const { onConnectorMouseDown } = useNiceDagNode({ node, niceDag });
  return (
    <div
      className={`square-connector ${type}`}
      onMouseDown={e => {
        e.stopPropagation();
        onConnectorMouseDown(e, type === 'out' ? 'out' : 'in');
      }}
    />
  );
}

function NormalNode({ node, niceDag }) {
  const {
    onDeleteNode,
    startNodeDragging,
    onConnectorMouseDown
  } = useNiceDagNode({ node, niceDag });

  return (
    <div className="editable-sample-normal-node">
      <div className="editable-sample-normal-node-delete-btn">
        <CloseCircleOutlined onClick={onDeleteNode} />
      </div>
      <div className="editable-sample-normal-node-move-hand" onMouseDown={startNodeDragging} />
      <div className="editable-sample-normal-node-title">{node.id}</div>
      <SquareConnector type="in" node={node} niceDag={niceDag} />
      <SquareConnector type="out" node={node} niceDag={niceDag} />
    </div>
  );
}

// ====== Main Component ======
function DAGEditorView({ onDAGChange, backendUrl = null }) {
  const [currentDAGName, setCurrentDAGName] = useState('');
  const [savedDAGs, setSavedDAGs] = useState([]);
  const [dagInfo, setDagInfo] = useState(null);
  const [saveModalVisible, setSaveModalVisible] = useState(false);
  const [loadModalVisible, setLoadModalVisible] = useState(false);
  const [newDAGName, setNewDAGName] = useState('');
  const [dagModel, setDAGModel] = useState(HierarchicalModel);

  const renderNode = ({ node, niceDag }) => {
    if (node.id === 'start') {
      return <StartNode node={node} niceDag={niceDag} />;
    }
    if (node.id === 'end') {
      return <EndNode node={node} niceDag={niceDag} />;
    }
    return <NormalNode node={node} niceDag={niceDag} />;
  };

  const renderEdge = ({ edge }) => {
    return <Edge edge={edge} />;
  };

  const { niceDag, niceDagEl, minimapEl, render } = useNiceDag({
    initNodes: dagModel,
    minimapConfig: { width: 200, height: 150 },
    editable: true,
    getNodeSize: () => ({ width: NODE_WIDTH, height: NODE_HEIGHT }),
    renderNode,
    renderEdge,
  });

  // Start editing mode when niceDag is ready
  useEffect(() => {
    if (niceDag) {
      niceDag.startEditing();
    }
  }, [niceDag]);

  // Update saved DAGs list
  const refreshSavedDAGs = useCallback(() => {
    const dags = DAGEditorUtils.getAllSavedDAGs();
    setSavedDAGs(dags);
  }, []);

  // Update DAG info
  const updateDAGInfo = useCallback(() => {
    if (niceDag && niceDag.model) {
      const info = DAGEditorUtils.extractDAGInfo(niceDag.model);
      setDagInfo(info);
      if (onDAGChange) {
        onDAGChange(niceDag.model);
      }
    }
  }, [niceDag, onDAGChange]);

  useEffect(() => {
    updateDAGInfo();
    refreshSavedDAGs();
    const interval = setInterval(updateDAGInfo, 2000);
    return () => clearInterval(interval);
  }, [niceDag, updateDAGInfo, refreshSavedDAGs]);

  // Save DAG
  const handleSaveDAG = useCallback(async () => {
    if (!newDAGName.trim()) {
      message.error('Please enter a DAG name');
      return;
    }

    const dagData = {
      nodes: niceDag.model.nodes,
      edges: niceDag.model.edges
    };

    // Save to localStorage
    const result = DAGEditorUtils.saveToLocalStorage(newDAGName, dagData);
    if (!result.success) {
      message.error(result.message);
      return;
    }

    // Optionally save to backend
    if (backendUrl) {
      const backendResult = await DAGEditorUtils.saveToBackend(newDAGName, dagData, backendUrl);
      if (!backendResult.success) {
        message.warning(`Saved locally but: ${backendResult.message}`);
      }
    }

    message.success(result.message);
    setCurrentDAGName(newDAGName);
    setNewDAGName('');
    setSaveModalVisible(false);
    refreshSavedDAGs();
  }, [niceDag, newDAGName, backendUrl, refreshSavedDAGs]);

  // Load DAG
  const handleLoadDAG = useCallback((dagName) => {
    const result = DAGEditorUtils.loadFromLocalStorage(dagName);
    if (!result.success) {
      message.error(result.message);
      return;
    }

    // Update model with loaded data
    if (niceDag && niceDag.model && result.data) {
      niceDag.model.updateModel(result.data.nodes || [], result.data.edges || []);
      setCurrentDAGName(dagName);
      message.success(`Loaded DAG "${dagName}"`);
      setLoadModalVisible(false);
      updateDAGInfo();
    }
  }, [niceDag, updateDAGInfo]);

  // Export DAG
  const handleExportDAG = useCallback(() => {
    const dagData = {
      nodes: niceDag.model.nodes,
      edges: niceDag.model.edges
    };
    const result = DAGEditorUtils.exportToFile(currentDAGName || 'dag', dagData);
    if (result.success) {
      message.success(result.message);
    } else {
      message.error(result.message);
    }
  }, [niceDag, currentDAGName]);

  // Import DAG
  const handleImportDAG = useCallback(async (file) => {
    const result = await DAGEditorUtils.importFromFile(file);
    if (!result.success) {
      message.error(result.message);
      return;
    }

    if (niceDag && niceDag.model && result.data) {
      niceDag.model.updateModel(result.data.nodes || [], result.data.edges || []);
      message.success('DAG imported successfully');
      updateDAGInfo();
    }
  }, [niceDag, updateDAGInfo]);

  // Delete DAG
  const handleDeleteDAG = useCallback((dagName) => {
    Modal.confirm({
      title: 'Delete DAG',
      content: `Are you sure you want to delete "${dagName}"?`,
      okText: 'Yes',
      cancelText: 'No',
      onOk() {
        DAGEditorUtils.deleteFromLocalStorage(dagName);
        message.success(`Deleted "${dagName}"`);
        refreshSavedDAGs();
        if (currentDAGName === dagName) {
          setCurrentDAGName('');
        }
      }
    });
  }, [currentDAGName, refreshSavedDAGs]);

  return (
    <div className="dag-editor-container">
      <div className="dag-editor-toolbar">
        <Space>
          <span style={{ fontWeight: 'bold', minWidth: 120 }}>
            {currentDAGName ? `Editing: ${currentDAGName}` : 'New DAG'}
          </span>
          <Button
            icon={<SaveOutlined />}
            onClick={() => setSaveModalVisible(true)}
          >
            Save
          </Button>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => setLoadModalVisible(true)}
          >
            Load
          </Button>
          <Button
            icon={<CopyOutlined />}
            onClick={handleExportDAG}
            disabled={!niceDag?.model?.nodes?.length}
          >
            Export
          </Button>
          <Button
            icon={<UploadOutlined />}
            onClick={() => {
              const input = document.createElement('input');
              input.type = 'file';
              input.accept = '.json';
              input.onchange = (e) => handleImportDAG(e.target.files[0]);
              input.click();
            }}
          >
            Import
          </Button>
        </Space>
      </div>

      <div className="dag-editor-content">
        <div className="dag-canvas" ref={niceDagEl} />
        {render && render()}
        <div className="dag-info-panel">
          <div className="info-section">
            <h4>DAG Info</h4>
            <div className="info-item">
              <span>Nodes: {dagInfo?.nodes || 0}</span>
            </div>
            <div className="info-item">
              <span>Edges: {dagInfo?.edges || 0}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Node IDs:</span>
              <div className="info-value">
                {dagInfo?.nodeIds?.join(', ') || 'None'}
              </div>
            </div>
          </div>

          <div className="info-section">
            <h4>Saved DAGs</h4>
            {savedDAGs.length > 0 ? (
              <ul className="saved-dags-list">
                {savedDAGs.map(name => (
                  <li key={name}>
                    <span>{name}</span>
                    <Button
                      type="link"
                      size="small"
                      onClick={() => handleLoadDAG(name)}
                    >
                      Load
                    </Button>
                    <Button
                      type="link"
                      danger
                      size="small"
                      onClick={() => handleDeleteDAG(name)}
                    >
                      Delete
                    </Button>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No saved DAGs</p>
            )}
          </div>

          <div className="info-section">
            <ZoomInOutSlider niceDag={niceDag} />
          </div>

          <div className="minimap" ref={minimapEl} />
        </div>
      </div>

      {/* Save Modal */}
      <Modal
        title="Save DAG"
        visible={saveModalVisible}
        onOk={handleSaveDAG}
        onCancel={() => setSaveModalVisible(false)}
      >
        <Input
          placeholder="Enter DAG name"
          value={newDAGName}
          onChange={(e) => setNewDAGName(e.target.value)}
          onPressEnter={handleSaveDAG}
        />
      </Modal>

      {/* Load Modal */}
      <Modal
        title="Load DAG"
        visible={loadModalVisible}
        onCancel={() => setLoadModalVisible(false)}
        footer={null}
      >
        {savedDAGs.length > 0 ? (
          <Select
            placeholder="Select a saved DAG"
            style={{ width: '100%' }}
            onChange={handleLoadDAG}
            options={savedDAGs.map(name => ({ label: name, value: name }))}
          />
        ) : (
          <p>No saved DAGs available</p>
        )}
      </Modal>
    </div>
  );
}

export default DAGEditorView;
