// components/Header.js
"use client";
import LogoutButton from "./LogoutButton";

export default function Header({ onLogout, showLogout = true }) {
  return (
    <header className="w-full bg-gray-900 text-white px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-lg font-bold">memX</h1>
        <p className="text-xs text-gray-300">A real-time shared memory layer for multi-agent LLM systems.</p>
      </div>
      {showLogout && <LogoutButton onLogout={onLogout} />}
    </header>
  );
}
