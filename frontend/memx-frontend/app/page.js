// app/page.js
"use client";
import { useState } from "react";
import AuthForm from "./components/AuthForm";
import KeyViewer from "./components/KeyViewer";
import CreateKeyForm from "./components/CreateKeyForm";
import LogoutButton from "./components/LogoutButton";
import Header from "./components/Header";

export default function Home() {
  const [session, setSession] = useState(null);

  if (!session) return (
    <>
    <AuthForm onAuth={setSession} />
    </>
  );
return (

  <>
    <Header showLogout={true} onLogout={() => setSession(null)} />
    <CreateKeyForm session={session} />
    <KeyViewer session={session} />
  </>
);
}
