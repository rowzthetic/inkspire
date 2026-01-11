import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react'; // Make sure you have lucide-react installed

const TattooLibrary = () => {
  const [meanings, setMeanings] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null); // For the popup modal

  // 1. Fetch data from your new Backend API
  useEffect(() => {
    const fetchLibrary = async () => {
      try {
        // If search is empty, fetch all. If not, append ?search=...
        const url = searchTerm 
          ? `http://127.0.0.1:8000/api/library/?search=${searchTerm}`
          : 'http://127.0.0.1:8000/api/library/';
        
        const res = await fetch(url);
        const data = await res.json();
        setMeanings(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching library:", error);
        setLoading(false);
      }
    };

    // specific delay so it doesn't search on every single keystroke immediately
    const delayDebounce = setTimeout(() => {
      fetchLibrary();
    }, 300);

    return () => clearTimeout(delayDebounce);
  }, [searchTerm]);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Header Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Tattoo Meaning Library</h1>
        <p className="text-gray-600 mb-8">Discover the symbolism behind the ink.</p>
        
        {/* Search Bar */}
        <div className="relative max-w-xl mx-auto">
          <input 
            type="text"
            placeholder="Search for 'Rose', 'Anchor', 'Strength'..."
            className="w-full p-4 pl-12 rounded-full border border-gray-300 shadow-sm focus:ring-2 focus:ring-purple-500 outline-none"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <Search className="absolute left-4 top-4 text-gray-400" />
        </div>
      </div>

      {/* Grid Display */}
      {loading ? (
        <p className="text-center">Loading Library...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
          {meanings.map((item) => (
            <div 
              key={item.id} 
              onClick={() => setSelectedItem(item)}
              className="bg-white rounded-xl shadow hover:shadow-lg transition cursor-pointer overflow-hidden border border-gray-100 group"
            >
              {/* Image Area */}
              <div className="h-48 bg-gray-200 overflow-hidden">
                {item.image ? (
                  <img src={item.image} alt={item.title} className="w-full h-full object-cover group-hover:scale-105 transition" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">No Image</div>
                )}
              </div>
              
              {/* Text Area */}
              <div className="p-4">
                <h3 className="text-xl font-bold text-gray-800">{item.title}</h3>
                <p className="text-gray-500 text-sm mt-1 truncate">{item.meaning}</p>
                
                {/* Tags */}
                <div className="mt-3 flex flex-wrap gap-2">
                  {item.tags.split(',').slice(0, 2).map((tag, idx) => (
                    <span key={idx} className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                      {tag.trim()}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal Popup for Details */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 relative">
            <button 
              onClick={() => setSelectedItem(null)}
              className="absolute top-4 right-4 text-gray-500 hover:text-black text-xl font-bold"
            >
              ✕
            </button>
            
            <h2 className="text-3xl font-bold mb-4">{selectedItem.title}</h2>
            
            <div className="flex gap-6 flex-col md:flex-row">
              {selectedItem.image && (
                <img src={selectedItem.image} alt={selectedItem.title} className="w-full md:w-1/2 rounded-lg object-cover" />
              )}
              <div className="flex-1">
                <h4 className="font-bold text-gray-700 mb-2">Meaning & Symbolism:</h4>
                <p className="text-gray-600 leading-relaxed whitespace-pre-line">
                  {selectedItem.meaning}
                </p>
                
                <div className="mt-6 pt-4 border-t">
                    <span className="text-sm font-semibold text-gray-500">Tags: </span>
                    <span className="text-sm text-purple-600">{selectedItem.tags}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TattooLibrary;