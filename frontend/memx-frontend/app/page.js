export default function LandingPage() {
  return (
    <main className="min-h-screen px-6 py-12 max-w-3xl mx-auto text-gray-900 dark:text-gray-100 space-y-10">
      {/* Hero Section */}
      <section className="space-y-4 text-center">
        <h1 className="text-4xl font-bold">🧠 <span className="text-gray-900 dark:text-gray-100">memX</span></h1>
        <p className="text-lg text-gray-700 dark:text-gray-300">
          Real-time shared memory for multi-agent LLM systems: no chat, no controller.
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          No setup. Free to use. Just shared memory between agents.
        </p>

        <div className="space-x-4">
          <a
            href="/login"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Get Started
          </a>
          <a
            href="https://github.com/MehulG/memX"
            className="inline-block px-4 py-2 border border-blue-600 text-blue-600 dark:text-blue-400 rounded hover:bg-blue-50 dark:hover:bg-blue-900"
          >
            GitHub
          </a>
        </div>
      </section>

      {/* Features */}
      <section className="space-y-2">
        <h2 className="text-2xl font-semibold">⚡ Why memX?</h2>
        <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
          <li>Real-time shared key-value store</li>
          <li>Pub/Sub updates across agents</li>
          <li>JSON Schema enforcement</li>
          <li>API-key-based access control</li>
        </ul>
      </section>

      {/* Quickstart */}
      <section className="space-y-2">
        <h2 className="text-2xl font-semibold">🚀 Quickstart</h2>
        <ol className="list-decimal list-inside space-y-1 text-gray-700 dark:text-gray-300">
          <li>Install SDK: <code>pip install memx_sdk</code></li>
          <li><a className="text-blue-600 dark:text-blue-400 underline" href="/login">Get your API key</a></li>
          <li>Start coding:</li>
        </ol>
        <pre className="bg-gray-100 dark:bg-gray-800 p-3 rounded text-sm overflow-x-auto">
          {`from memx_sdk import memxContext

ctx = memxContext(api_key="your_api_key")

ctx.set_schema("agent:goal", {
  "type": "object",
  "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
  "required": ["x", "y"]
})

ctx.set("agent:goal", {"x": 1, "y": 7})
print(ctx.get("agent:goal"))
`}
        </pre>
      </section>

      {/* Agent Table */}
      <section className="space-y-2">
        <h2 className="text-2xl font-semibold">🧬 Example: Multi Agents, One Memory</h2>
        <img
          src="/example.gif"
          alt="memX demo"
        // className="w-full max-w-xl mx-auto rounded shadow"
        />

      </section>



      {/* Use Cases */}
      <section className="space-y-2">
        <h2 className="text-2xl font-semibold">🌐 Use Cases</h2>
        <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
          <li>Autonomous research agents</li>
          <li>LangGraph / CrewAI memory plugins</li>
          <li>LLM workflows with persistent state</li>
        </ul>
      </section>

      {/* Footer */}
      <footer className="pt-4 text-center text-sm text-gray-500 dark:text-gray-400">
        Open source under MIT License.{" "}
        <a href="https://github.com/MehulG/memX" className="text-blue-600 dark:text-blue-400 underline">GitHub</a>
      </footer>
    </main>
  );
}
