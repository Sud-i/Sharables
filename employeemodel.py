from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Date, ForeignKey, Text, Enum, UniqueConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.db.database import Base
from src.core.enums import (
    EmployeeStatusEnum, EmploymentTypeEnum, GenderEnum, MaritalStatusEnum,
    ModuleEnum, PermissionLevelEnum, ContextTypeEnum
)


class Employee(Base):
    """Comprehensive employee model with industry-standard fields"""
    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Employee identification
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    employee_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True)  # HR system number
    
    # Personal information
    title: Mapped[Optional[str]] = mapped_column(String(10))  # Mr., Ms., Dr., etc.
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    suffix: Mapped[Optional[str]] = mapped_column(String(10))  # Jr., Sr., III, etc.
    preferred_name: Mapped[Optional[str]] = mapped_column(String(100))  # What they like to be called
    
    # Contact information
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    personal_email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    mobile: Mapped[Optional[str]] = mapped_column(String(20))
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    emergency_contact_relation: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Login credentials
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))  # Nullable for first-time setup
    is_password_set: Mapped[bool] = mapped_column(Boolean, default=False)
    password_reset_token: Mapped[Optional[str]] = mapped_column(String(255))
    password_reset_expires: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime)
    login_attempts: Mapped[int] = mapped_column(default=0)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Demographics
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(Enum(GenderEnum))
    marital_status: Mapped[Optional[MaritalStatusEnum]] = mapped_column(Enum(MaritalStatusEnum))
    nationality: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Employment details
    date_joined: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_confirmation: Mapped[Optional[date]] = mapped_column(Date)  # End of probation
    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(Enum(EmploymentTypeEnum), default=EmploymentTypeEnum.FULL_TIME)
    status: Mapped[EmployeeStatusEnum] = mapped_column(Enum(EmployeeStatusEnum), default=EmployeeStatusEnum.ACTIVE)
    termination_date: Mapped[Optional[date]] = mapped_column(Date)
    termination_reason: Mapped[Optional[str]] = mapped_column(Text)
    notice_period_days: Mapped[int] = mapped_column(default=30)
    
    # Organizational structure
    department_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"))
    grade_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("grades.id"))
    base_location_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("locations.id"))
    current_project_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"))
    
    # Reporting structure
    manager_l1_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"))  # Direct manager
    manager_l2_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"))  # Skip-level manager
    hr_partner_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"))  # Assigned HR partner
    
    # Job information
    job_title: Mapped[Optional[str]] = mapped_column(String(200))
    job_description: Mapped[Optional[str]] = mapped_column(Text)
    skills: Mapped[Optional[str]] = mapped_column(Text)  # JSON or comma-separated
    certifications: Mapped[Optional[str]] = mapped_column(Text)  # JSON or comma-separated
    
    # Work arrangements
    is_remote_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    work_from_home_days: Mapped[int] = mapped_column(default=0)  # Days per week
    work_location_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("locations.id"))  # Current work location
    
    # System flags & RBAC permissions
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)  # Super admin access
    is_hr: Mapped[bool] = mapped_column(Boolean, default=False)     # HR module access
    is_manager: Mapped[bool] = mapped_column(Boolean, default=False) # Management permissions
    is_finance: Mapped[bool] = mapped_column(Boolean, default=False) # Finance access
    is_system_user: Mapped[bool] = mapped_column(Boolean, default=True) # Can login to system
    
    # Profile information
    bio: Mapped[Optional[str]] = mapped_column(Text)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(500))
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"))
    
    # Relationships
    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    grade = relationship("Grade", foreign_keys=[grade_id], back_populates="employees")
    base_location = relationship("Location", foreign_keys=[base_location_id], back_populates="employees")
    work_location = relationship("Location", foreign_keys=[work_location_id])
    project = relationship("Project", foreign_keys=[current_project_id], back_populates="employees")
    
    # Reporting relationships
    manager_l1 = relationship("Employee", remote_side=[id], foreign_keys=[manager_l1_id], post_update=True)
    manager_l2 = relationship("Employee", remote_side=[id], foreign_keys=[manager_l2_id], post_update=True)
    hr_partner = relationship("Employee", remote_side=[id], foreign_keys=[hr_partner_id], post_update=True)
    
    # Shift relationships (for future use) - moved to string reference to avoid circular import
    # created_shifts = relationship("Shift", foreign_keys="Shift.created_by_id", back_populates="created_by")
    
    # Reverse relationships
    direct_reports = relationship("Employee", foreign_keys="Employee.manager_l1_id", back_populates="manager_l1")
    skip_reports = relationship("Employee", foreign_keys="Employee.manager_l2_id", back_populates="manager_l2")
    hr_managed_employees = relationship("Employee", foreign_keys="Employee.hr_partner_id", back_populates="hr_partner")
    
    # RBAC relationships (enhanced from unified model)
    employee_roles = relationship("EmployeeRole", foreign_keys="EmployeeRole.employee_id", back_populates="employee", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", foreign_keys="AuditLog.employee_id", back_populates="employee")
    
    # Created entities - fix overlapping relationships
    created_by_employee = relationship("Employee", remote_side=[id], foreign_keys=[created_by], overlaps="created_employees")
    
    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint('email', name='_employee_email_unique'),
        UniqueConstraint('employee_id', name='_employee_id_unique'),
        UniqueConstraint('username', name='_employee_username_unique'),
        Index('ix_employee_full_name', 'first_name', 'last_name'),
        Index('ix_employee_status', 'status'),
        Index('ix_employee_department', 'department_id'),
        Index('ix_employee_manager', 'manager_l1_id'),
        Index('ix_employee_date_joined', 'date_joined'),
    )
    
    @property
    def full_name(self) -> str:
        """Get the employee's full name"""
        parts = []
        if self.title:
            parts.append(self.title)
        parts.append(self.first_name)
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)
    
    @property
    def display_name(self) -> str:
        """Get the employee's preferred display name"""
        if self.preferred_name:
            return self.preferred_name
        return f"{self.first_name} {self.last_name}"
    
    @property
    def years_of_service(self) -> float:
        """Calculate years of service"""
        end_date = self.termination_date or datetime.now().date()
        delta = end_date - self.date_joined
        return round(delta.days / 365.25, 2)
    
    @property
    def is_new_hire(self) -> bool:
        """Check if employee is in probation period (< 90 days)"""
        if self.date_of_confirmation:
            return False
        days_since_joining = (datetime.now().date() - self.date_joined).days
        return days_since_joining < 90
    
    @property
    def needs_password_setup(self) -> bool:
        """Check if employee needs to set up their password"""
        return not self.is_password_set or self.password_hash is None
    
    @property
    def can_login(self) -> bool:
        """Check if employee can login to the system"""
        return (self.is_system_user and 
                self.is_active and 
                not self.is_locked and
                self.status == EmployeeStatusEnum.ACTIVE)
    
    @property
    def permission_level(self) -> str:
        """Get the highest permission level"""
        if self.is_admin:
            return "SUPER_ADMIN"
        elif self.is_hr:
            return "HR_ADMIN"
        elif self.is_manager:
            return "MANAGER"
        elif self.is_finance:
            return "FINANCE"
        else:
            return "EMPLOYEE"
    
    # === METHODS ===
    def has_permission(self, module: ModuleEnum, action: PermissionLevelEnum) -> bool:
        """Check if employee has specific permission"""
        # Super admin has all permissions
        if self.is_admin:
            return True
        
        # Quick checks for common permissions
        if module == ModuleEnum.HR and self.is_hr:
            return True
        
        if module == ModuleEnum.FINANCE and self.is_finance:
            return True
        
        # Check role-based permissions (would be implemented with EmployeeRole relationships)
        return self._check_role_permissions(module, action)
    
    def _check_role_permissions(self, module: ModuleEnum, action: PermissionLevelEnum) -> bool:
        """Check permissions via role assignments"""
        # Implementation would check employee_roles for specific permissions
        # This is where the detailed RBAC logic would go
        return False
    
    def __repr__(self):
        return f"<Employee {self.employee_id}: {self.full_name} ({self.permission_level})>"


class EmployeeRole(Base):
    """Many-to-many relationship between employees and roles"""
    __tablename__ = "employee_roles"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    role_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    
    # Context and validity
    context_type: Mapped[Optional[ContextTypeEnum]] = mapped_column(Enum(ContextTypeEnum), nullable=True)
    context_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Time-based permissions
    effective_from: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    effective_to: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Audit fields
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    assigned_by: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"))
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    revoked_by: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"))
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="employee_roles")
    role = relationship("Role", foreign_keys=[role_id], back_populates="employee_roles")
    assigned_by_employee = relationship("Employee", foreign_keys=[assigned_by])
    revoked_by_employee = relationship("Employee", foreign_keys=[revoked_by])
    
    __table_args__ = (
        UniqueConstraint('employee_id', 'role_id', 'context_type', 'context_id', name='_employee_role_context_unique'),
        Index('ix_employee_role_active', 'employee_id', 'is_active'),
        Index('ix_employee_role_context', 'context_type', 'context_id'),
    )
