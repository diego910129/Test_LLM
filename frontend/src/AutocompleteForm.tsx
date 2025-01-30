import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const AutocompleteForm: React.FC = () => {
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [error, setError] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const fetchSuggestions = async () => {
    if (!input.trim()) {
      setSuggestions([]);
      return;
    }

    try {
      const response = await axios.get('http://localhost:8000/completions', {
        params: { text: input },
      });
      setSuggestions(response.data.suggestions);
      setError('');
    } catch (error: any) {
        if (error.response) {
            setError(error.response.data.detail || 'Failed to fetch suggestions');
        } else {
          setError('Network error, could not connect to server');
        }
      setSuggestions([]);
    }
  };

  useEffect(() => {
        const delay = 300; // add delay to prevent too many API calls
        let timeoutId: number | null = null;
        timeoutId = setTimeout(() => {
          fetchSuggestions();
        }, delay)
        return () => {
            if (timeoutId) clearTimeout(timeoutId);
        }
      }, [input]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setInput(e.target.value);
  };

  const handleSuggestionClick = async (suggestion: string) => {
      setInput(suggestion);
    setSuggestions([]);
    try {
      await axios.post('http://localhost:8000/completions', {
        text: input,
        completion: suggestion,
      });
    } catch (e: any) {
        setError('Failed to save completion.');
    }
    inputRef.current?.focus();
  };

  return (
    <div>
      <input
          type="text"
        ref={inputRef}
        value={input}
        onChange={handleInputChange}
        placeholder="Enter text..."
        aria-autocomplete="list"
        aria-owns="autocomplete-list"
        aria-expanded={suggestions.length > 0}
      />
      {suggestions.length > 0 && (
        <ul id="autocomplete-list" role="listbox">
          {suggestions.map((suggestion, index) => (
              <li
              key={index}
              role="option"
              onClick={() => handleSuggestionClick(suggestion)}
              aria-selected={false}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
        {error && <p className="error-message">{error}</p>}
    </div>
  );
};

export default AutocompleteForm;