// components/LogoutButton.js
"use client";
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";

export default function LogoutButton({ onLogout }) {
  const supabase = createClientComponentClient();

  async function handleLogout() {
    await supabase.auth.signOut();
    onLogout();
  }

  return (
    <button
      onClick={handleLogout}
      className="text-sm text-red-600 underline cursor-pointer ml-auto"
    >
      Logout
    </button>
  );
}