import React, { useState, useEffect } from 'react';
import { 
    Clock, Camera, DollarSign, Save, LogOut, 
    Settings, User 
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './ArtistDashboard.css'; // 👈 IMPORT THE CSS FILE HERE

const API_BASE_URL = 'http://localhost:8000';

const ArtistDashboard = () => {
  const [activeTab, setActiveTab] = useState('schedule');
  const [artistData, setArtistData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { logOut } = useAuth();

  const fetchDashboard = async () => {
    try {
      const token = localStorage.getItem('access') || localStorage.getItem('token');
      if (!token) { navigate('/login'); return; }

      const res = await fetch(`${API_BASE_URL}/api/auth/dashboard/`, {
          headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.status === 401) { logOut(); return; }

      const data = await res.json();
      setArtistData(data);
      setLoading(false);
    } catch (error) {
        console.error("Error fetching dashboard:", error);
        setLoading(false);
    }
  };

  useEffect(() => { fetchDashboard(); }, []);

  if (loading) return <div className="loading-screen">LOADING STUDIO...</div>;

  return (
    <div className="dashboard-container">
      
      {/* SIDEBAR */}
      <aside className="dashboard-sidebar">
        <div>
            {/* Logo */}
            <div className="logo-section">
                <div className="logo-icon"></div>
                <h2 className="brand-name">INKSPIRE</h2>
            </div>

            {/* Profile Snippet */}
            <div className="artist-snippet">
                <div className="snippet-avatar">
                    {artistData?.profile_picture ? (
                        <img src={`${API_BASE_URL}${artistData.profile_picture}`} alt="Profile" />
                    ) : (
                        <User color="#a1a1aa" size={20} />
                    )}
                </div>
                <div className="snippet-info">
                    <p className="role-label">Artist</p>
                    <p className="artist-name">{artistData?.username}</p>
                </div>
            </div>

            {/* Navigation */}
            <nav className="nav-menu">
                <NavButton icon={<Clock size={20}/>} label="Schedule" active={activeTab === 'schedule'} onClick={() => setActiveTab('schedule')} />
                <NavButton icon={<Camera size={20}/>} label="Portfolio" active={activeTab === 'profile'} onClick={() => setActiveTab('profile')} />
                <NavButton icon={<DollarSign size={20}/>} label="Revenue" active={activeTab === 'revenue'} onClick={() => setActiveTab('revenue')} />
                <NavButton icon={<Settings size={20}/>} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
            </nav>
        </div>
        
        {/* Logout */}
        <button onClick={logOut} className="logout-btn">
            <LogOut size={18} /> 
            <span>Sign Out</span>
        </button>
      </aside>

      {/* MAIN CONTENT */}
      <main className="dashboard-content">
        <div className="content-wrapper">
            {/* Header */}
            <header className="header-section">
                <div className="header-title">
                    <h1>{getHeaderTitle(activeTab)}</h1>
                    <p>Manage your studio presence and availability.</p>
                </div>
                <div className="date-display">
                    {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                </div>
            </header>

            {/* Tab Content */}
            <div className="tab-body">
                {activeTab === 'schedule' && <ScheduleSection schedule={artistData.schedule} />}
                {activeTab === 'profile' && <Placeholder title="Portfolio Gallery" icon={<Camera size={48}/>} />}
                {activeTab === 'revenue' && <Placeholder title="Financial Overview" icon={<DollarSign size={48}/>} />}
                {activeTab === 'settings' && <Placeholder title="Account Settings" icon={<Settings size={48}/>} />}
            </div>
        </div>
      </main>
    </div>
  );
};

/* --- SUB COMPONENTS --- */

const NavButton = ({ icon, label, active, onClick }) => (
  <button onClick={onClick} className={`nav-btn ${active ? 'active' : ''}`}>
    {icon}
    <span className="nav-label">{label}</span>
  </button>
);

const Placeholder = ({ title, icon }) => (
    <div style={{ padding: '60px', textAlign: 'center', border: '2px dashed #333', borderRadius: '16px', color: '#555' }}>
        <div style={{ marginBottom: '20px' }}>{icon}</div>
        <h2 style={{ fontSize: '24px', color: '#ddd' }}>{title}</h2>
        <p>This feature is currently under development.</p>
    </div>
);

const getHeaderTitle = (tab) => {
    switch(tab) {
        case 'schedule': return 'Weekly Schedule';
        case 'profile': return 'Portfolio Gallery';
        case 'revenue': return 'Financial Overview';
        case 'settings': return 'Studio Settings';
        default: return 'Dashboard';
    }
};

/* --- SCHEDULE COMPONENT --- */
const ScheduleSection = ({ schedule: initialSchedule }) => {
    const [schedule, setSchedule] = useState(initialSchedule || []);
    const [isSaving, setIsSaving] = useState(false);

    const handleTimeChange = (index, field, value) => {
        const newSchedule = [...schedule];
        newSchedule[index][field] = value;
        setSchedule(newSchedule);
    };

    const toggleActive = (index) => {
        const newSchedule = [...schedule];
        newSchedule[index].is_active = !newSchedule[index].is_active;
        setSchedule(newSchedule);
    };

    const saveSchedule = async () => {
         setIsSaving(true);
         const token = localStorage.getItem('access') || localStorage.getItem('token');
         try {
             const res = await fetch(`${API_BASE_URL}/api/auth/dashboard/schedule/`, {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                 body: JSON.stringify(schedule)
             });
             if(res.ok) alert("✅ Schedule Saved!");
             else alert("❌ Error saving schedule");
         } catch (e) { alert("Connection Error"); } 
         finally { setIsSaving(false); }
    };

    return (
        <div className="schedule-card">
            <div className="card-header">
                <div>
                    <h3 style={{ fontSize: '20px', margin: 0, fontWeight: 'bold' }}>Working Hours</h3>
                    <p style={{ color: '#a1a1aa', fontSize: '14px', margin: '4px 0 0' }}>Set your weekly availability.</p>
                </div>
                <button 
                    onClick={saveSchedule} 
                    disabled={isSaving}
                    className="save-btn-primary"
                >
                    <Save size={18} />
                    {isSaving ? "Saving..." : "Save Changes"}
                </button>
            </div>

            <div className="days-list">
                {schedule.map((day, index) => (
                    <div key={index} className={`day-row ${day.is_active ? 'active' : ''}`}>
                        
                        <div className="day-toggle">
                            <input 
                                type="checkbox" 
                                checked={day.is_active} 
                                onChange={() => toggleActive(index)} 
                                className="toggle-checkbox"
                            />
                            <span className="day-label">{day.day_name}</span>
                        </div>
                        
                        {day.is_active ? (
                            <div className="time-inputs">
                                <TimeInput label="Start" value={day.start_time} onChange={(v) => handleTimeChange(index, 'start_time', v)} />
                                <TimeInput label="End" value={day.end_time} onChange={(v) => handleTimeChange(index, 'end_time', v)} />
                                {/* Optional divider */}
                                <TimeInput label="Lunch In" value={day.break_start} onChange={(v) => handleTimeChange(index, 'break_start', v)} />
                                <TimeInput label="Lunch Out" value={day.break_end} onChange={(v) => handleTimeChange(index, 'break_end', v)} />
                            </div>
                        ) : (
                            <span className="unavailable-text">Currently Unavailable</span>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

const TimeInput = ({ label, value, onChange }) => (
    <div className="input-group">
        <label className="input-label">{label}</label>
        <input 
            type="time" 
            value={value ? value.slice(0,5) : ""} 
            onChange={(e) => onChange(e.target.value)} 
            className="time-field"
        />
    </div>
);

export default ArtistDashboard;