import { useState } from "react";
import { AuthAPI, UsersAPI } from "@/utils/api";   // adjust path if needed

export default function ApiTestPage() {
  const [email, setEmail] = useState("t@example.com");
  const [password, setPassword] = useState("secret123");
  const [me, setMe] = useState(null);
  const [users, setUsers] = useState([]);

  async function handleLogin() {
    await AuthAPI.login(email, password);
    const meData = await AuthAPI.me();
    setMe(meData);
  }

  async function loadUsers() {
    const data = await UsersAPI.list({ page: 1, pageSize: 10 });
    setUsers(data.items || data);
  }

  return (
    <div className="p-4 space-y-3">
      <div className="flex gap-2">
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email" />
        <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="password" type="password" />
        <button onClick={handleLogin}>Login</button>
        <button onClick={loadUsers}>Load Users</button>
      </div>
      <pre>{JSON.stringify(me, null, 2)}</pre>
      <pre>{JSON.stringify(users, null, 2)}</pre>
    </div>
  );
}
