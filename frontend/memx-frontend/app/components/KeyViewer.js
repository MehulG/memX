"use client";
import { useEffect, useState } from "react";
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";

export default function KeyViewer({ session }) {
  const supabase = createClientComponentClient();
  const [keys, setKeys] = useState([]);

  const fetchKeys = async () => {
    const { data } = await supabase.from("api_keys").select("*");
    setKeys(data || []);
  };

  useEffect(() => {
    fetchKeys();
  }, []);

  const deleteKey = async (key) => {
    await supabase.from("api_keys").delete().eq("key", key);
    fetchKeys();
  };

  const userPrefix = session.user.id.slice(0, 8);

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-2">🔑 Your API Keys</h2>
      <p className="text-sm text-gray-500 mb-4">Namespace: <code>{userPrefix}</code></p>
      {keys.length === 0 ? (
        <p>No keys found.</p>
      ) : (
        <table className="w-full text-left border">
          <thead>
            <tr className="border-b">
              <th className="p-2">Name</th>
              <th className="p-2">Key</th>
              <th className="p-2">Read Scope</th>
              <th className="p-2">Write Scope</th>
              <th className="p-2">Created At</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {keys.map((k) => (
              <tr key={k.key} className="border-b text-sm">
                <td className="p-2">{k.name}</td>
                <td className="p-2">{k.key}</td>
                <td className="p-2">{k.scopes.read?.join(", ")}</td>
                <td className="p-2">{k.scopes.write?.join(", ")}</td>
                <td className="p-2">{new Date(k.created_at).toLocaleString()}</td>
                <td className="p-2">
                  <button
                    className="text-red-500 underline cursor-pointer"
                    onClick={() => deleteKey(k.key)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}