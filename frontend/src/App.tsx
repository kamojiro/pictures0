import useSWR from 'swr';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const fetcher = (url: string) =>
  fetch(url).then((res) => {
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  });

function App() {
  const { data, error } = useSWR('/api/gcs/random/ocmai/signed-url', fetcher);
  // const { data, error } = useSWR('http://localhost:8000/api/gcs/random/ocmai/signed-url', fetcher);
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <div>Loading...</div>;
  const signedUrl = data.signed_url;
  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
          
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <div>
      <img src={signedUrl} alt="kamomo image" />
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
