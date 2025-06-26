"use client";
import { useState } from "react";
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";
import Header from "./Header";

export default function AuthForm({ onAuth }) {
  const supabase = createClientComponentClient();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("login");
  const [error, setError] = useState(null);
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    setLoading(true);
    try {
      if (mode === "login") {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        onAuth(data.session);
      } else {
        const { error: signupError } = await supabase.auth.signUp({ email, password });
        if (signupError) throw signupError;
        setInfo("Signed up successfully. Please check your email to confirm your account.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header showLogout={false} />
      <div className="flex flex-1 items-center justify-center">
        <div className="max-w-sm w-full p-4">
          <h2 className="text-xl font-bold mb-4">{mode === "login" ? "Login" : "Signup"}</h2>
          <form onSubmit={handleSubmit} className="space-y-3">
            <input
              className="w-full p-2 border"
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              className="w-full p-2 border"
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              className="bg-blue-500 text-white w-full py-2 cursor-pointer disabled:opacity-50"
              type="submit"
              disabled={loading}
            >
              {loading ? "Processing..." : mode === "login" ? "Login" : "Signup"}
            </button>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            {info && <p className="text-green-500 text-sm">{info}</p>}
          </form>
          <p className="text-sm mt-2">
            {mode === "login" ? "Don't have an account?" : "Already have an account?"} {" "}
            <button
              className="text-blue-600 cursor-pointer"
              onClick={() => setMode(mode === "login" ? "signup" : "login")}
              disabled={loading}
            >
              {mode === "login" ? "Signup" : "Login"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
