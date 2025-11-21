import { useEffect, useState } from 'react';
import axios from 'axios';
import type { NewsItem } from './types';
import { NewsCard } from './components/NewsCard';
import './index.css';

function App() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      const response = await axios.get<NewsItem[]>('http://localhost:8000/news');
      setNews(response.data);
      setError(null);
    } catch (error: any) {
      console.error("Error fetching news:", error);
      setError(error.message || "Failed to fetch news");
    } finally {
      setLoading(false);
    }
  };

  const handleCrawl = async () => {
    try {
      setUpdating(true);
      await axios.post('http://localhost:8000/crawl');
      await fetchNews();
    } catch (error: any) {
      console.error("Error updating news:", error);
      alert("Failed to update news");
    } finally {
      setUpdating(false);
    }
  };

  const handleLike = (id: number) => {
    setNews(prevNews => prevNews.map(item =>
      item.id === id ? { ...item, likes: item.likes + 1 } : item
    ));
  };

  if (loading && news.length === 0) return <div className="app-container">Loading...</div>;
  if (error) return <div className="app-container" style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI News Aggregator</h1>
        <button
          onClick={handleCrawl}
          disabled={updating}
          style={{
            padding: '8px 16px',
            backgroundColor: updating ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: updating ? 'not-allowed' : 'pointer'
          }}
        >
          {updating ? 'Updating...' : 'Update Articles'}
        </button>
      </header>
      <main className="news-grid">
        {news.length === 0 ? (
          <p>No news found.</p>
        ) : (
          news.map(item => (
            <NewsCard key={item.id} item={item} onLike={handleLike} />
          ))
        )}
      </main>
    </div>
  );
}

export default App;
