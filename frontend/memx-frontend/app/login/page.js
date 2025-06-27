"use client";
import { useState, useCallback } from "react";
import AuthForm from "../components/AuthForm";
import KeyViewer from "../components/KeyViewer";
import CreateKeyForm from "../components/CreateKeyForm";
import Header from "../components/Header";

export default function Login() {
  const [session, setSession] = useState(null);
  const [reload, setReload] = useState(0);

  const triggerReload = useCallback(() => {
    setReload((prev) => prev + 1);
  }, []);

  if (!session) {
    return <AuthForm onAuth={setSession} />;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header showLogout={true} onLogout={() => setSession(null)} />
      <CreateKeyForm session={session} onCreated={triggerReload} />
      <KeyViewer key={reload} session={session} />
    </div>
  );
}
