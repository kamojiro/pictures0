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
  // const { data, error } = useSWR('/api/gcs/ocmai/random/signed-url', fetcher);
  const { data, error } = useSWR('http://localhost:8000/api/gcs/ocmai/random/signed-url', fetcher);
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <div>Loading...</div>;
  const signedUrl = data.signed_url;
  return (
    <>
      <h1>{data.title}</h1>
      <p>{data.tags}</p>
      <div>
      <img src={signedUrl} alt="kamomo image" />
      </div>
    </>
  )
}

export default App
