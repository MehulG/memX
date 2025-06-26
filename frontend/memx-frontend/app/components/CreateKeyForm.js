"use client";
import { useState } from "react";
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";

export default function CreateKeyForm({ session, onCreated }) {
  const supabase = createClientComponentClient();
  const [name, setName] = useState("");
  const [readScope, setReadScope] = useState("agent:*");
  const [writeScope, setWriteScope] = useState("agent:goal");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const userPrefix = session.user.id.slice(0, 8);

  async function handleCreate(e) {
    e.preventDefault();
    setLoading(true);
    const apiKey = crypto.randomUUID().replace(/-/g, "").slice(0, 32);
    const scopes = {
      read: readScope.split(",").map((s) => `${userPrefix}:${s.trim()}`),
      write: writeScope.split(",").map((s) => `${userPrefix}:${s.trim()}`),
    };

    const { error } = await supabase.rpc("create_api_key", {
      key_name: name,
      key_value: apiKey,
      scopes,
      is_active: true,
    });

    if (error) {
      setStatus(`Error: ${error.message}`);
    } else {
      setStatus(`API Key Created: ${apiKey}`);
      setName("");
      setReadScope("agent:*");
      setWriteScope("agent:goal");
      if (onCreated) onCreated();
    }
    setLoading(false);
  }

  return (
    <form onSubmit={handleCreate} className="max-w-md mx-auto space-y-3 p-4">
      <h2 className="text-xl font-semibold">➕ Create New API Key</h2>
      Key name:
      <input
        className="w-full p-2 border"
        placeholder="Key name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      Read scope (comma separated):
      <input
        className="w-full p-2 border"
        placeholder="Read scope (comma separated)"
        value={readScope}
        onChange={(e) => setReadScope(e.target.value)}
        required
      />
      Write scope (comma separated):
      <input
        className="w-full p-2 border"
        placeholder="Write scope (comma separated)"
        value={writeScope}
        onChange={(e) => setWriteScope(e.target.value)}
        required
      />
      <button
        className="bg-green-600 text-white py-2 px-4 cursor-pointer disabled:opacity-50"
        type="submit"
        disabled={loading}
      >
        {loading ? "Creating..." : "Create"}
      </button>
      {status && <p className="text-sm text-blue-600 mt-2">{status}</p>}
    </form>
  );
}
