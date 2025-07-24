import React, { useState, useCallback } from 'react';
import SimpleExcelGrid from '../components/SimpleExcelGrid';
import { useTheme } from '../contexts/ThemeContext';

const ExcelGridDemo = () => {
  const { isDarkMode } = useTheme();
  
  // Sample data for demonstration
  const [gridData, setGridData] = useState([
    { id: 1, name: 'John Doe', department: 'Engineering', salary: 75000, startDate: '2023-01-15', status: 'Active', manager: 'Jane Smith' },
    { id: 2, name: 'Jane Smith', department: 'Engineering', salary: 95000, startDate: '2022-03-20', status: 'Active', manager: 'Bob Johnson' },
    { id: 3, name: 'Bob Johnson', department: 'Management', salary: 120000, startDate: '2021-06-10', status: 'Active', manager: 'Alice Brown' },
    { id: 4, name: 'Alice Brown', department: 'HR', salary: 85000, startDate: '2023-02-01', status: 'Active', manager: 'Charlie Davis' },
    { id: 5, name: 'Charlie Davis', department: 'Finance', salary: 90000, startDate: '2022-11-15', status: 'Active', manager: 'Diana Wilson' },
    { id: 6, name: 'Diana Wilson', department: 'Sales', salary: 70000, startDate: '2023-05-20', status: 'Active', manager: 'Eve Taylor' },
    { id: 7, name: 'Eve Taylor', department: 'Marketing', salary: 65000, startDate: '2023-08-10', status: 'Active', manager: 'Frank Miller' },
    { id: 8, name: 'Frank Miller', department: 'IT', salary: 80000, startDate: '2022-12-05', status: 'Active', manager: 'Grace Lee' },
    { id: 9, name: 'Grace Lee', department: 'Operations', salary: 72000, startDate: '2023-04-15', status: 'Active', manager: 'Henry Wang' },
    { id: 10, name: 'Henry Wang', department: 'Legal', salary: 110000, startDate: '2021-09-20', status: 'Active', manager: 'Ivy Chen' },
    { id: 11, name: 'Ivy Chen', department: 'Research', salary: 88000, startDate: '2022-07-30', status: 'Active', manager: 'Jack Wilson' },
    { id: 12, name: 'Jack Wilson', department: 'Quality', salary: 78000, startDate: '2023-03-25', status: 'Active', manager: 'Kelly Brown' },
    { id: 13, name: 'Kelly Brown', department: 'Engineering', salary: 82000, startDate: '2022-10-12', status: 'Active', manager: 'Jane Smith' },
    { id: 14, name: 'Liam Davis', department: 'Sales', salary: 68000, startDate: '2023-06-18', status: 'Active', manager: 'Diana Wilson' },
    { id: 15, name: 'Mia Johnson', department: 'Marketing', salary: 71000, startDate: '2023-07-22', status: 'Active', manager: 'Eve Taylor' },
    { id: 16, name: 'Noah Miller', department: 'IT', salary: 76000, startDate: '2022-08-14', status: 'Active', manager: 'Frank Miller' },
    { id: 17, name: 'Olivia Wilson', department: 'HR', salary: 73000, startDate: '2023-09-05', status: 'Active', manager: 'Alice Brown' },
    { id: 18, name: 'Paul Anderson', department: 'Finance', salary: 85000, startDate: '2022-05-28', status: 'Active', manager: 'Charlie Davis' },
    { id: 19, name: 'Quinn Taylor', department: 'Operations', salary: 74000, startDate: '2023-01-30', status: 'Active', manager: 'Grace Lee' },
    { id: 20, name: 'Ruby Lee', department: 'Legal', salary: 92000, startDate: '2021-11-16', status: 'Active', manager: 'Henry Wang' },
  ]);

  // Column definitions
  const columnDefs = [
    { 
      field: 'id', 
      headerName: 'ID', 
      width: 80, 
      editable: false,
      comparator: (a, b) => a - b
    },
    { 
      field: 'name', 
      headerName: 'Employee Name', 
      width: 150, 
      editable: true
    },
    { 
      field: 'department', 
      headerName: 'Department', 
      width: 120, 
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: {
        values: ['Engineering', 'Management', 'HR', 'Finance', 'Sales', 'Marketing', 'IT', 'Operations', 'Legal', 'Research', 'Quality']
      }
    },
    { 
      field: 'salary', 
      headerName: 'Salary', 
      width: 100, 
      editable: true,
      valueFormatter: (params) => {
        return params.value ? `$${params.value.toLocaleString()}` : '';
      }
    },
    { 
      field: 'startDate', 
      headerName: 'Start Date', 
      width: 120, 
      editable: true,
      cellEditor: 'agDateCellEditor',
      valueFormatter: (params) => {
        if (params.value) {
          return new Date(params.value).toLocaleDateString();
        }
        return '';
      }
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 100, 
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: {
        values: ['Active', 'Inactive', 'On Leave']
      },
      cellRenderer: (params) => {
        const status = params.value;
        const statusClass = status === 'Active' ? 'bg-green-100 text-green-800' : 
                           status === 'Inactive' ? 'bg-red-100 text-red-800' : 
                           'bg-yellow-100 text-yellow-800';
        return `<span class="px-2 py-1 rounded-full text-xs ${statusClass}">${status}</span>`;
      }
    },
    { 
      field: 'manager', 
      headerName: 'Manager', 
      width: 140, 
      editable: true 
    }
  ];

  // Event handlers
  const handleSelectionChanged = useCallback((event) => {
    console.log('Selection changed:', event.selectedRows);
  }, []);

  const handleCellValueChanged = useCallback((event) => {
    console.log('Cell value changed:', {
      field: event.colDef.field,
      oldValue: event.oldValue,
      newValue: event.newValue,
      data: event.data
    });
    
    // Update the data state
    setGridData(prevData => 
      prevData.map(row => 
        row.id === event.data.id ? { ...row, [event.colDef.field]: event.newValue } : row
      )
    );
  }, []);

  const addNewRow = () => {
    const newId = Math.max(...gridData.map(row => row.id)) + 1;
    const newRow = {
      id: newId,
      name: 'New Employee',
      department: 'Engineering',
      salary: 60000,
      startDate: new Date().toISOString().split('T')[0],
      status: 'Active',
      manager: 'Jane Smith'
    };
    setGridData([...gridData, newRow]);
  };

  const deleteSelectedRows = () => {
    // This would be implemented by getting selected rows from the grid
    // For now, we'll just remove the last row as an example
    setGridData(prevData => prevData.slice(0, -1));
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className={`text-3xl font-bold mb-2 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
            Excel Grid Demo
          </h1>
          <p className={`text-lg ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            A fully-featured Excel-like data grid with sorting, filtering, editing, and more.
          </p>
        </div>

        {/* Action buttons */}
        <div className="mb-6 flex flex-wrap gap-4">
          <button
            onClick={addNewRow}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add Row
          </button>
          
          <button
            onClick={deleteSelectedRows}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete Selected
          </button>
        </div>

        {/* Feature highlights */}
        <div className={`mb-6 p-4 rounded-lg ${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-blue-50 border-blue-200'} border`}>
          <h3 className={`text-lg font-semibold mb-2 ${isDarkMode ? 'text-white' : 'text-blue-900'}`}>
            🚀 Features Demo
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Selection:</strong> Click rows, use Ctrl+Click, Shift+Click
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Editing:</strong> Double-click cells to edit inline
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Copy/Paste:</strong> Ctrl+C/Ctrl+V between cells
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Sorting:</strong> Click column headers to sort
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Filtering:</strong> Use search boxes below headers
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Pinned:</strong> ID column is frozen on the left
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Undo/Redo:</strong> Ctrl+Z/Ctrl+Y for changes
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Export:</strong> Download as CSV or Excel
            </div>
            <div className={isDarkMode ? 'text-gray-300' : 'text-blue-800'}>
              <strong>Keyboard:</strong> Arrow keys, Enter, Tab navigation
            </div>
          </div>
        </div>

        {/* Excel Grid */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <SimpleExcelGrid
            data={gridData}
            columns={columnDefs}
            height={600}
            pinnedColumns={1}
            onSelectionChanged={handleSelectionChanged}
            onCellValueChanged={handleCellValueChanged}
            enableExport={true}
            enableGlobalSearch={true}
            enableColumnSearch={true}
            className="excel-demo-grid"
          />
        </div>

        {/* Usage instructions */}
        <div className={`mt-8 p-6 rounded-lg ${isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border`}>
          <h3 className={`text-xl font-semibold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
            📋 Usage Instructions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className={`font-medium mb-2 ${isDarkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Keyboard Shortcuts
              </h4>
              <ul className={`text-sm space-y-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Ctrl+C</kbd> Copy selected cells</li>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Ctrl+V</kbd> Paste clipboard content</li>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Ctrl+Z</kbd> Undo last change</li>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Ctrl+Y</kbd> Redo last undone change</li>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Ctrl+A</kbd> Select all cells</li>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Enter</kbd> Move down to next row</li>
                <li><kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Tab</kbd> Move right to next column</li>
              </ul>
            </div>
            <div>
              <h4 className={`font-medium mb-2 ${isDarkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                Mouse Actions
              </h4>
              <ul className={`text-sm space-y-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                <li>Click header to sort column</li>
                <li>Double-click cell to edit</li>
                <li>Drag column borders to resize</li>
                <li>Ctrl+Click for multi-select</li>
                <li>Shift+Click for range select</li>
                <li>Right-click for context menu</li>
                <li>Drag to select cell ranges</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExcelGridDemo;
