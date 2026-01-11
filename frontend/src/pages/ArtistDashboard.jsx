// src/pages/ArtistDashboard.jsx

import React, { useState, useEffect } from 'react';
import { Camera, DollarSign, Clock, Calendar, Save, Trash2 } from 'lucide-react';

const ArtistDashboard = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [artistData, setArtistData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch Data on Load
  useEffect(() => {
    const fetchDashboard = async () => {
        // Replace with your actual token logic
        const token = localStorage.getItem('token'); 
        const res = await fetch('http://127.0.0.1:8000/api/auth/dashboard/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        setArtistData(data);
        setLoading(false);
    };
    fetchDashboard();
  }, []);

  if (loading) return <div className="p-10 text-center">Loading Dashboard...</div>;

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white p-6">
        <h2 className="text-2xl font-bold mb-8 text-purple-400">Inkspire Artist</h2>
        <nav className="space-y-4">
          <SidebarBtn icon={<Camera />} label="Profile & Portfolio" active={activeTab === 'profile'} onClick={() => setActiveTab('profile')} />
          <SidebarBtn icon={<Clock />} label="Schedule" active={activeTab === 'schedule'} onClick={() => setActiveTab('schedule')} />
          <SidebarBtn icon={<DollarSign />} label="Revenue" active={activeTab === 'revenue'} onClick={() => setActiveTab('revenue')} />
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 overflow-y-auto">
        {activeTab === 'profile' && <ProfileSection artist={artistData} />}
        {activeTab === 'schedule' && <ScheduleSection schedule={artistData.schedule} />}
        {activeTab === 'revenue' && <RevenueSection revenue={artistData.revenue} />}
      </div>
    </div>
  );
};

const SidebarBtn = ({ icon, label, active, onClick }) => (
  <button onClick={onClick} className={`flex items-center w-full p-3 rounded ${active ? 'bg-purple-600' : 'hover:bg-gray-800'}`}>
    {icon} <span className="ml-3">{label}</span>
  </button>
);

// --- 1. PROFILE & PORTFOLIO COMPONENT ---
const ProfileSection = ({ artist }) => {
    const [bio, setBio] = useState(artist.bio);
    
    const handleSaveBio = async () => {
        // Call your user update API here
        alert(`Saving bio: ${bio}`);
    };

    return (
        <div className="space-y-6">
            <div className="bg-white p-6 rounded shadow">
                <h3 className="text-xl font-bold mb-4">Edit Profile</h3>
                <textarea 
                    className="w-full p-2 border rounded" 
                    rows="4" 
                    value={bio} 
                    onChange={(e) => setBio(e.target.value)} 
                />
                <button onClick={handleSaveBio} className="mt-2 bg-purple-600 text-white px-4 py-2 rounded flex items-center">
                    <Save size={16} className="mr-2" /> Save Bio
                </button>
            </div>

            <div className="bg-white p-6 rounded shadow">
                <h3 className="text-xl font-bold mb-4">Portfolio</h3>
                <div className="grid grid-cols-4 gap-4">
                    {artist.portfolio.map(img => (
                        <div key={img.id} className="relative group">
                            <img src={`http://127.0.0.1:8000${img.image}`} alt="portfolio" className="h-32 w-full object-cover rounded" />
                            <button className="absolute top-1 right-1 bg-red-600 text-white p-1 rounded opacity-0 group-hover:opacity-100">
                                <Trash2 size={14} />
                            </button>
                        </div>
                    ))}
                    <div className="h-32 border-2 border-dashed border-gray-300 flex items-center justify-center rounded cursor-pointer hover:bg-gray-50">
                        <span className="text-gray-400">+ Upload</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

// --- 2. SCHEDULE COMPONENT ---
const ScheduleSection = ({ schedule: initialSchedule }) => {
    const [schedule, setSchedule] = useState(initialSchedule);

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
         const token = localStorage.getItem('token');
         await fetch('http://127.0.0.1:8000/api/auth/dashboard/schedule/', {
             method: 'POST',
             headers: { 
                 'Content-Type': 'application/json',
                 'Authorization': `Bearer ${token}`
             },
             body: JSON.stringify(schedule)
         });
         alert("Schedule Updated!");
    };

    return (
        <div className="bg-white p-6 rounded shadow">
            <div className="flex justify-between mb-6">
                <h3 className="text-xl font-bold">Weekly Schedule</h3>
                <button onClick={saveSchedule} className="bg-green-600 text-white px-4 py-2 rounded">Save Changes</button>
            </div>

            {schedule.map((day, index) => (
                <div key={day.id} className={`flex items-center space-x-4 mb-4 p-3 rounded border ${!day.is_active ? 'bg-gray-100 opacity-60' : ''}`}>
                    <div className="w-24 font-semibold">
                        <input type="checkbox" checked={day.is_active} onChange={() => toggleActive(index)} className="mr-2"/>
                        {day.day_name}
                    </div>
                    
                    {day.is_active && (
                        <>
                            <div>
                                <label className="text-xs text-gray-500 block">Start</label>
                                <input type="time" value={day.start_time.slice(0,5)} onChange={(e) => handleTimeChange(index, 'start_time', e.target.value)} className="border rounded p-1"/>
                            </div>
                            <div>
                                <label className="text-xs text-gray-500 block">End</label>
                                <input type="time" value={day.end_time.slice(0,5)} onChange={(e) => handleTimeChange(index, 'end_time', e.target.value)} className="border rounded p-1"/>
                            </div>
                            
                            <div className="pl-4 border-l">
                                <label className="text-xs text-red-400 block">Lunch Start</label>
                                <input type="time" value={day.break_start.slice(0,5)} onChange={(e) => handleTimeChange(index, 'break_start', e.target.value)} className="border rounded p-1"/>
                            </div>
                            <div>
                                <label className="text-xs text-red-400 block">Lunch End</label>
                                <input type="time" value={day.break_end.slice(0,5)} onChange={(e) => handleTimeChange(index, 'break_end', e.target.value)} className="border rounded p-1"/>
                            </div>
                        </>
                    )}
                    {!day.is_active && <span className="text-gray-500 italic">Day Off</span>}
                </div>
            ))}
        </div>
    );
};

// --- 3. REVENUE COMPONENT ---
const RevenueSection = ({ revenue }) => (
    <div className="grid grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded shadow border-l-4 border-green-500">
            <h3 className="text-gray-500 text-sm">Total Revenue</h3>
            <p className="text-3xl font-bold text-gray-800">${revenue}</p>
        </div>
        <div className="bg-white p-6 rounded shadow border-l-4 border-blue-500">
            <h3 className="text-gray-500 text-sm">Completed Appointments</h3>
            <p className="text-3xl font-bold text-gray-800">0</p>
        </div>
    </div>
);

export default ArtistDashboard;