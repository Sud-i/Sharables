# Shift Management Frontend Implementation Guide

## Overview
This guide provides comprehensive instructions for implementing the frontend for the new HR and Manager shift management system. The backend provides role-based shift management with audit trails and permission controls.

## Backend Endpoints Summary

### Base URL: `/api/v1/shift-management`

| Method | Endpoint | Description | Access Level |
|--------|----------|-------------|--------------|
| GET | `/employees` | Get employees for shift management | HR (all), Manager (direct reports) |
| GET | `/shifts` | Get available shifts | HR/Manager/Admin |
| GET | `/employee/{id}/schedule` | Get employee's shift schedule | HR/Manager (with permissions) |
| POST | `/assign-shift` | Assign shift to employee | HR/Manager (with permissions) |
| GET | `/employee/{id}/audit-trail` | Get shift change history | HR/Manager/Employee (own) |

## Authentication & Permissions

### Role-Based Access Control
```typescript
interface UserPermissions {
  isHR: boolean;      // Can manage all employees
  isManager: boolean; // Can manage direct reports only
  isAdmin: boolean;   // Can manage all employees
  canManageShifts: boolean; // Computed based on above
}

// Permission check example
const canManageEmployee = (currentUser: User, targetEmployeeId: string) => {
  if (currentUser.isHR || currentUser.isAdmin) return true;
  if (currentUser.isManager) {
    // Check if target employee is a direct report
    return currentUser.directReports.includes(targetEmployeeId);
  }
  return false;
};
```

### API Headers
```typescript
const apiHeaders = {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json'
};
```

## Core Components to Implement

### 1. Employee List Component
```typescript
interface Employee {
  id: string;
  employee_id: string;
  full_name: string;
  department: string | null;
  current_shift: ShiftInfo | null;
  manager_l1_name: string | null;
}

interface ShiftInfo {
  id: string;
  name: string;
  code: string | null;
  start_time: string; // "09:00"
  end_time: string | null; // "18:00"
  duration_hours: number;
  is_overnight: boolean;
  shift_type: string | null;
  color_code: string | null;
  description: string | null;
}

// API Call
const fetchEmployees = async (filters?: {
  search?: string;
  department_id?: string;
  limit?: number;
  offset?: number;
}) => {
  const params = new URLSearchParams();
  if (filters?.search) params.append('search', filters.search);
  if (filters?.department_id) params.append('department_id', filters.department_id);
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.offset) params.append('offset', filters.offset.toString());
  
  const response = await fetch(`/api/v1/shift-management/employees?${params}`, {
    headers: apiHeaders
  });
  return await response.json();
};
```

### 2. Shift Schedule Component
```typescript
interface EmployeeScheduleDay {
  date: string; // "2024-08-07"
  shift_id: string | null;
  shift_code: string | null;
  shift_name: string | null;
  shift_timings: string | null; // "09:00 AM – 06:00 PM"
  is_week_off: boolean;
  is_holiday: boolean;
  is_working_day: boolean;
  can_edit: boolean; // Only today and future dates
  assigned_by: string | null;
  assigned_at: string | null; // ISO datetime
  notes: string | null;
}

interface EmployeeSchedule {
  employee_id: string;
  employee_name: string;
  month: number;
  year: number;
  month_name: string;
  schedule: EmployeeScheduleDay[];
  total_working_days: number;
  total_week_offs: number;
  total_holidays: number;
}

// API Call
const fetchEmployeeSchedule = async (employeeId: string, month: number, year: number) => {
  const response = await fetch(
    `/api/v1/shift-management/employee/${employeeId}/schedule?month=${month}&year=${year}`,
    { headers: apiHeaders }
  );
  return await response.json();
};
```

### 3. Shift Assignment Component
```typescript
interface ShiftAssignmentRequest {
  employee_id: string;
  shift_id: string;
  start_date: string; // "2024-08-07"
  end_date?: string | null; // For date range, null for single day
  notes?: string | null;
  override_existing: boolean; // Whether to override existing assignments
}

interface ShiftAssignmentResponse {
  success: boolean;
  message: string;
  assigned_dates: string[];
  skipped_dates: string[];
  conflicts: Array<{
    date: string;
    existing_shift: string;
    message: string;
  }>;
}

// API Call
const assignShift = async (request: ShiftAssignmentRequest) => {
  const response = await fetch('/api/v1/shift-management/assign-shift', {
    method: 'POST',
    headers: apiHeaders,
    body: JSON.stringify(request)
  });
  return await response.json();
};
```

### 4. Audit Trail Component
```typescript
interface AuditTrailEntry {
  id: string;
  timestamp: string; // ISO datetime
  action: string; // "UPDATE", "ASSIGNED", etc.
  details: string; // Human readable description
  metadata: {
    action: string;
    affected_dates: string[];
    old_shift?: {
      id: string;
      code: string;
      name: string;
    };
    new_shift?: {
      id: string;
      code: string;
      name: string;
    };
    notes?: string;
  };
  changed_by: {
    id: string | null;
    name: string;
    employee_id: string | null;
  };
}

// API Call
const fetchAuditTrail = async (employeeId: string, filters?: {
  start_date?: string;
  end_date?: string;
  limit?: number;
  offset?: number;
}) => {
  const params = new URLSearchParams();
  if (filters?.start_date) params.append('start_date', filters.start_date);
  if (filters?.end_date) params.append('end_date', filters.end_date);
  if (filters?.limit) params.append('limit', filters.limit.toString());
  if (filters?.offset) params.append('offset', filters.offset.toString());
  
  const response = await fetch(
    `/api/v1/shift-management/employee/${employeeId}/audit-trail?${params}`,
    { headers: apiHeaders }
  );
  return await response.json();
};
```

## UI/UX Implementation Guidelines

### 1. Main Dashboard Layout
```tsx
const ShiftManagementDashboard = () => {
  return (
    <div className="shift-management-dashboard">
      {/* Header with role-based title */}
      <header>
        <h1>
          {user.isHR ? 'HR Shift Management' : 'Team Shift Management'}
        </h1>
        <div className="actions">
          <button onClick={handleBulkAssignment}>Bulk Assign</button>
          <button onClick={handleExport}>Export Schedule</button>
        </div>
      </header>
      
      {/* Employee search and filters */}
      <section className="employee-filters">
        <SearchInput onSearch={handleEmployeeSearch} />
        <DepartmentFilter onChange={handleDepartmentFilter} />
        <DateRangePicker onChange={handleDateRange} />
      </section>
      
      {/* Employee list with current shifts */}
      <section className="employee-list">
        <EmployeeGrid employees={employees} onSelectEmployee={handleEmployeeSelect} />
      </section>
      
      {/* Selected employee schedule */}
      {selectedEmployee && (
        <section className="schedule-view">
          <EmployeeScheduleCalendar 
            employee={selectedEmployee}
            schedule={schedule}
            onDateSelect={handleDateSelect}
            onShiftAssign={handleShiftAssign}
          />
        </section>
      )}
    </div>
  );
};
```

### 2. Calendar Grid Component
```tsx
const EmployeeScheduleCalendar = ({ employee, schedule, onDateSelect, onShiftAssign }) => {
  return (
    <div className="schedule-calendar">
      <div className="calendar-header">
        <h2>{employee.full_name}'s Schedule</h2>
        <div className="month-navigation">
          <button onClick={handlePreviousMonth}>←</button>
          <span>{schedule.month_name} {schedule.year}</span>
          <button onClick={handleNextMonth}>→</button>
        </div>
      </div>
      
      <div className="calendar-grid">
        {schedule.schedule.map((day) => (
          <div 
            key={day.date}
            className={`calendar-day ${getDayClassName(day)}`}
            onClick={() => day.can_edit && onDateSelect(day)}
          >
            <div className="date">{new Date(day.date).getDate()}</div>
            <div className="shift-info">
              {day.shift_name && (
                <div className="shift-badge" style={{backgroundColor: getShiftColor(day)}}>
                  {day.shift_code}
                </div>
              )}
              {day.shift_timings && (
                <div className="shift-timings">{day.shift_timings}</div>
              )}
            </div>
            {day.is_week_off && <div className="week-off-indicator">WO</div>}
            {day.is_holiday && <div className="holiday-indicator">H</div>}
            {!day.can_edit && <div className="past-date-overlay" />}
          </div>
        ))}
      </div>
      
      <div className="calendar-legend">
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#e74c3c'}} />
          <span>Night Shift</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#3498db'}} />
          <span>Day Shift</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#95a5a6'}} />
          <span>Week Off</span>
        </div>
      </div>
    </div>
  );
};
```

### 3. Shift Assignment Modal
```tsx
const ShiftAssignmentModal = ({ 
  isOpen, 
  onClose, 
  employee, 
  selectedDates, 
  availableShifts,
  onAssign 
}) => {
  const [selectedShift, setSelectedShift] = useState('');
  const [notes, setNotes] = useState('');
  const [overrideExisting, setOverrideExisting] = useState(false);
  
  const handleSubmit = async () => {
    const request = {
      employee_id: employee.id,
      shift_id: selectedShift,
      start_date: selectedDates[0],
      end_date: selectedDates.length > 1 ? selectedDates[selectedDates.length - 1] : null,
      notes,
      override_existing: overrideExisting
    };
    
    const result = await onAssign(request);
    
    if (result.success) {
      showSuccessToast(result.message);
      onClose();
    } else {
      showErrorToast('Failed to assign shift');
    }
  };
  
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="shift-assignment-modal">
        <h3>Assign Shift</h3>
        
        <div className="assignment-details">
          <p><strong>Employee:</strong> {employee.full_name}</p>
          <p><strong>Dates:</strong> {formatDateRange(selectedDates)}</p>
        </div>
        
        <div className="form-group">
          <label>Select Shift:</label>
          <select 
            value={selectedShift} 
            onChange={(e) => setSelectedShift(e.target.value)}
          >
            <option value="">Choose a shift...</option>
            {availableShifts.map((shift) => (
              <option key={shift.id} value={shift.id}>
                {shift.name} ({shift.start_time} - {shift.end_time})
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label>Notes (optional):</label>
          <textarea 
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add any notes about this assignment..."
          />
        </div>
        
        <div className="form-group">
          <label>
            <input 
              type="checkbox"
              checked={overrideExisting}
              onChange={(e) => setOverrideExisting(e.target.checked)}
            />
            Override existing assignments
          </label>
        </div>
        
        <div className="modal-actions">
          <button onClick={onClose}>Cancel</button>
          <button 
            onClick={handleSubmit}
            disabled={!selectedShift}
            className="primary"
          >
            Assign Shift
          </button>
        </div>
      </div>
    </Modal>
  );
};
```

### 4. Audit Trail Sidebar
```tsx
const AuditTrailSidebar = ({ employeeId, isOpen, onClose }) => {
  const [auditEntries, setAuditEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    if (isOpen && employeeId) {
      loadAuditTrail();
    }
  }, [isOpen, employeeId]);
  
  const loadAuditTrail = async () => {
    setLoading(true);
    try {
      const response = await fetchAuditTrail(employeeId);
      setAuditEntries(response.audit_trail);
    } catch (error) {
      showErrorToast('Failed to load audit trail');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className={`audit-sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <h3>Shift Change History</h3>
        <button onClick={onClose}>✕</button>
      </div>
      
      <div className="sidebar-content">
        {loading ? (
          <div className="loading-spinner">Loading...</div>
        ) : (
          <div className="audit-entries">
            {auditEntries.map((entry) => (
              <div key={entry.id} className="audit-entry">
                <div className="entry-header">
                  <span className="action-type">{entry.action}</span>
                  <span className="timestamp">
                    {formatDateTime(entry.timestamp)}
                  </span>
                </div>
                <div className="entry-details">
                  <p>{entry.details}</p>
                  {entry.metadata.old_shift && entry.metadata.new_shift && (
                    <div className="shift-change">
                      <span className="old-shift">
                        From: {entry.metadata.old_shift.name}
                      </span>
                      <span className="arrow">→</span>
                      <span className="new-shift">
                        To: {entry.metadata.new_shift.name}
                      </span>
                    </div>
                  )}
                  <div className="changed-by">
                    Changed by: {entry.changed_by.name}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
```

## Key Features to Implement

### 1. Permission-Based UI
- Show different interfaces for HR vs Managers
- Disable edit functions for employees outside user's scope
- Display appropriate messages for access denied scenarios

### 2. Date Restrictions
- Only allow edits for today and future dates
- Show visual indicators for past dates (grayed out)
- Display appropriate messages when trying to edit past dates

### 3. Conflict Handling
- Show warnings when overriding existing assignments
- Display conflict details clearly
- Allow users to choose whether to proceed with conflicts

### 4. Audit Visibility
- Show who assigned each shift and when
- Provide easy access to full audit trail
- Display change history in an understandable format

### 5. Bulk Operations
- Allow selection of multiple dates for single shift assignment
- Provide bulk assignment across multiple employees
- Show progress indicators for bulk operations

### 6. Responsive Design
- Ensure calendar works on mobile devices
- Provide appropriate touch interactions
- Consider alternative layouts for small screens

## Error Handling

### Common Error Scenarios
```typescript
const handleAPIError = (error: any) => {
  switch (error.status) {
    case 403:
      showErrorToast('You don\'t have permission to perform this action');
      break;
    case 404:
      showErrorToast('Employee or shift not found');
      break;
    case 400:
      showErrorToast(error.detail || 'Invalid request');
      break;
    default:
      showErrorToast('An unexpected error occurred');
  }
};
```

### Validation Rules
- Start date cannot be in the past
- End date cannot be before start date
- Shift must be selected for assignment
- Employee must be in user's management scope

## Testing Considerations

### Unit Tests
- Permission checking logic
- Date validation functions
- API request/response handling
- Component rendering with different user roles

### Integration Tests
- Full shift assignment workflow
- Audit trail functionality
- Permission-based access control
- Error handling scenarios

### User Acceptance Tests
- HR user can manage all employees
- Manager can only manage direct reports
- Audit trail shows complete change history
- Past dates cannot be edited

## Performance Considerations

### API Optimization
- Implement pagination for large employee lists
- Cache shift definitions
- Debounce search inputs
- Use appropriate loading states

### UI Optimization
- Virtual scrolling for large calendars
- Lazy loading of audit trail
- Efficient re-rendering of calendar days
- Proper memoization of computed values

This comprehensive guide provides all the necessary information to implement a robust shift management frontend that integrates seamlessly with the backend API while maintaining proper security and user experience standards.
