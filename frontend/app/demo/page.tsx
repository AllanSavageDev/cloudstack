"use client";

import { useState, useEffect, useCallback } from "react";
import axios from "axios";

interface User {
  email: string;
  full_name?: string;
}

interface Item {
  id: number;
  name: string;
  description: string;
}

export default function DemoPage() {
  const [email, setEmail] = useState("demo@demo.com");
  const [password, setPassword] = useState("password");
  const [token, setToken] = useState<string | null>(null);
  const [me, setMe] = useState<User | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [newItem, setNewItem] = useState<Omit<Item, "id">>({ name: "", description: "" });
  const [editItem, setEditItem] = useState<Item>({ id: 0, name: "", description: "" });

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setMe(null);
    setItems([]);
  };

  const fetchUser = useCallback(async () => {
    try {
      const res = await axios.get("/api/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMe(res.data);
    } catch {
      logout();
    }
  }, [token]);

  const fetchItems = useCallback(async () => {
    try {
      const res = await axios.get("/api/items", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setItems(res.data);
    } catch {
      alert("Could not fetch items");
    }
  }, [token]);

  const login = async () => {
    try {
      const res = await axios.post(
        "/api/login",
        new URLSearchParams({ username: email, password }),
      );
      localStorage.setItem("token", res.data.access_token);
      setToken(res.data.access_token);
    } catch {
      alert("Login failed");
    }
  };

  const createItem = async () => {
    try {
      await axios.post("/api/items", newItem, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setNewItem({ name: "", description: "" });
      fetchItems();
    } catch {
      alert("Failed to create item");
    }
  };

  const updateItem = async () => {
    try {
      await axios.put(
        `/api/items/${editItem.id}`,
        {
          name: editItem.name,
          description: editItem.description,
        },
        { headers: { Authorization: `Bearer ${token}` } },
      );
      setEditItem({ id: 0, name: "", description: "" });
      fetchItems();
    } catch {
      alert("Failed to update item");
    }
  };

  const deleteItem = async (id: number) => {
    try {
      await axios.delete(`/api/items/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchItems();
    } catch {
      alert("Failed to delete item");
    }
  };

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) setToken(savedToken);
  }, []);

  useEffect(() => {
    if (token) {
      fetchUser();
      fetchItems();
    }
  }, [token, fetchUser, fetchItems]);

  if (!token) {
    return (
      <div className="p-4 flex justify-center items-center min-h-screen">
        <div className="w-full max-w-md">
          <h1 className="text-xl mb-4">Login</h1>
          <input
            className="border p-2 block mb-2 w-full"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
          />
          <input
            className="border p-2 block mb-2 w-full"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
          <button className="bg-blue-500 text-white px-4 py-2 w-full" onClick={login}>
            Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 max-w-xl mx-auto">
      <div className="mb-4">
        <h1 className="text-xl">Welcome, {me?.email}</h1>
        <button onClick={logout} className="text-sm text-gray-600 underline">
          Logout
        </button>
      </div>

      <div className="mb-6">
        <h2 className="text-lg font-semibold">Create Item</h2>
        <input
          className="border p-2 block w-full mb-2"
          value={newItem.name}
          onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
          placeholder="Name"
        />
        <input
          className="border p-2 block w-full mb-2"
          value={newItem.description}
          onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
          placeholder="Description"
        />
        <button className="bg-green-600 text-white px-4 py-2" onClick={createItem}>
          Create
        </button>
      </div>

      <div className="mb-6">
        <h2 className="text-lg font-semibold">Update Item</h2>
        <input
          className="border p-2 block w-full mb-2"
          value={editItem.id}
          onChange={(e) => setEditItem({ ...editItem, id: Number(e.target.value) })}
          placeholder="ID"
        />
        <input
          className="border p-2 block w-full mb-2"
          value={editItem.name}
          onChange={(e) => setEditItem({ ...editItem, name: e.target.value })}
          placeholder="Name"
        />
        <input
          className="border p-2 block w-full mb-2"
          value={editItem.description}
          onChange={(e) => setEditItem({ ...editItem, description: e.target.value })}
          placeholder="Description"
        />
        <button className="bg-blue-500 text-white px-4 py-2" onClick={updateItem}>
          Update
        </button>
      </div>

      <div className="mb-6">
        <h2 className="text-lg font-semibold">Items</h2>
        <button className="text-sm underline mb-2" onClick={fetchItems}>
          Reload Items
        </button>
        <ul>
          {items.map((item) => (
            <li key={item.id} className="border-b py-2">
              <div>
                <strong>{item.name}</strong> — {item.description}
              </div>
              <div className="text-sm mt-1">
                <button onClick={() => setEditItem(item)} className="text-blue-600 mr-4">
                  Edit
                </button>
                <button onClick={() => deleteItem(item.id)} className="text-red-600">
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
