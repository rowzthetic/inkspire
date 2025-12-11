import { useState } from 'react';
import '../App.css';

export default function Contact() {
  // 1. Setup state to store the form data
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    date: '',
    placement: '',
    description: ''
  });

  const [status, setStatus] = useState(''); // To show success/error messages

  // 2. Update state when the user types
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // 3. Send data to Django when form is submitted
  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Sending...');

    try {
      // connecting to the Django API we just created
      const response = await fetch('http://127.0.0.1:8000/api/appointments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setStatus('Success! Appointment requested.');
        // Clear the form
        setFormData({ name: '', email: '', date: '', placement: '', description: '' });
      } else {
        setStatus('Error: Could not send request.');
        console.error('Server Error:', await response.text());
      }
    } catch (error) {
      setStatus('Error: Server is not running. Make sure the black terminal is open!');
      console.error('Network Error:', error);
    }
  };

  return (
    <section className="contact" style={{ paddingTop: '100px', minHeight: '80vh' }}>
        <h2>Book an Appointment</h2>
        <form className="contact-form" onSubmit={handleSubmit}>
            
            <input 
              type="text" 
              name="name" 
              placeholder="Your Name" 
              value={formData.name} 
              onChange={handleChange} 
              required 
            />
            
            <input 
              type="email" 
              name="email" 
              placeholder="Your Email" 
              value={formData.email} 
              onChange={handleChange} 
              required 
            />

            <div style={{display: 'flex', gap: '10px'}}>
              <input 
                type="date" 
                name="date" 
                value={formData.date} 
                onChange={handleChange} 
                required 
                style={{flex: 1}}
              />
              <input 
                type="text" 
                name="placement" 
                placeholder="Placement (e.g. Arm)" 
                value={formData.placement} 
                onChange={handleChange} 
                required 
                style={{flex: 1}}
              />
            </div>

            <textarea 
              name="description" 
              placeholder="Describe your tattoo idea..." 
              rows="5" 
              value={formData.description} 
              onChange={handleChange} 
              required
            ></textarea>

            <button type="submit" className="btn">Send Request</button>
            
            {/* Status Message */}
            {status && <p style={{marginTop: '15px', fontWeight: 'bold', color: '#e63946'}}>{status}</p>}
        </form>
    </section>
  );
}