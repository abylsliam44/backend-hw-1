import { useState } from 'react';
import { login } from '../../utils/api';

interface LoginFormProps {
  onSuccess: (token: string) => void;
}

export default function LoginForm({ onSuccess }: LoginFormProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const data = await login(username, password);
      localStorage.setItem('token', data.access_token);
      onSuccess(data.access_token);
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="username" className="form-label">
          Username
        </label>
        <input
          id="username"
          type="text"
          required
          className="input-field"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="password" className="form-label">
          Password
        </label>
        <input
          id="password"
          type="password"
          required
          className="input-field"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button type="submit" className="btn-primary w-full">
        Sign in
      </button>
    </form>
  );
} 