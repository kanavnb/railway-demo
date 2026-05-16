import { useEffect, useState } from "react";

function App() {
  const [items, setItems] = useState([]);
  const [text, setText] = useState("");

  const API = import.meta.env.VITE_API_URL;

  async function loadData() {
    const res = await fetch(`${API}/api/data`);
    const data = await res.json();

    setItems(data);
  }

  useEffect(() => {
    loadData();
  }, []);

  async function addItem() {
    await fetch(`${API}/api/data`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: text,
      }),
    });

    setText("");

    loadData();
  }

  async function deleteItem(id) {
    await fetch(`${API}/api/data/${id}`, {
      method: "DELETE",
    });

    loadData();
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>Student: YOUR_NAME | ID: YOUR_ID</h1>

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={addItem}>
        Add
      </button>

      {items.map((item) => (
        <div key={item.id}>
          {item.name}

          <button onClick={() => deleteItem(item.id)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}

export default App;
